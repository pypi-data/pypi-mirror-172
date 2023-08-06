from typing import List, Optional, Union

from selenium.common.exceptions import (  # type: ignore
    JavascriptException,
    TimeoutException,
)
from selenium.webdriver.support.ui import WebDriverWait  # type: ignore
from typing_extensions import Literal, TypedDict

from inspector_commons.bridge.bridge_browser import BrowserBridge  # type: ignore
from inspector_commons.bridge.mixin import traceback  # type: ignore


class SelectorType(TypedDict):
    strategy: str
    value: str


class MatchType(TypedDict):
    name: str
    value: str


class Meta(TypedDict):
    source: str
    screenshot: str
    matches: List[MatchType]


class RecordedOperation(TypedDict):
    type: str
    value: Union[None, str, bool]
    path: Optional[str]
    time: Optional[int]
    trigger: Literal["click", "change", "unknown"]
    selectors: List[SelectorType]
    meta: Optional[List[Meta]]


class RecordEvent(TypedDict):
    list: List[RecordedOperation]
    actionType: Literal["exception", "stop", "append"]
    url: Optional[str]


class RecorderBridge(BrowserBridge):
    """Javascript API bridge for the web recorder functionality."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._current_url: Optional[str] = None
        self._recorded_operations: List[RecordedOperation] = []

    @traceback
    def start_recording(self) -> List[RecordedOperation]:
        # TODO: Handle as async in future instead of blocking
        self.logger.debug("Starting recording...")
        self._record()
        self.logger.debug("Recorded events: %s", self._recorded_operations)
        return self._recorded_operations

    @traceback
    def stop_recording(self) -> List[RecordedOperation]:
        # TODO: Handle as async in future instead of blocking
        self.logger.debug("Stopping recording...")
        self.driver.stop_recording()
        return self._recorded_operations

    @traceback
    def show_guide(self):
        self.driver.show_guide("recording-guide")

    def _record(self):
        self._recorded_operations = []
        while True:
            # TODO: Could we try catch the page change?
            try:
                self._wait_for_page_to_load()
                event: RecordEvent = self.driver.record_event()
                self.logger.debug("Raw event: %s", event)
            except JavascriptException as exc:
                self.logger.debug("Ignoring Javascript exception: %s", exc)
                event: RecordEvent = {
                    "actionType": "exception",
                    "list": [],
                    "url": self._current_url,
                }
            except TimeoutException:
                self.logger.debug("Retrying after script timeout")
                event: RecordEvent = {
                    "actionType": "exception",
                    "list": [],
                    "url": self._current_url,
                }

            if not event:
                self.logger.error("Received empty event: %s", event)
                continue

            if not self._handle_event(event):
                return

    def _handle_event(self, event: RecordEvent) -> bool:
        event_type = event["actionType"]
        event_url = event["url"]

        if not self._current_url:
            self._current_url = event_url
        elif event_url != self._current_url:
            message: RecordedOperation = {
                "path": None,
                "time": None,
                "meta": None,
                "selectors": [],
                "type": "comment",
                "value": f"Recorder detected that URL changed to {event_url}",
                "trigger": "unknown",
            }
            self._current_url = event_url
            self._recorded_operations += [message]
        if event_type == "exception":
            self.logger.debug("Event(s) is an exception: %s", event)
            return True  # Ignore errors for now
        elif event_type == "event":
            self.logger.debug("Received event(s) from page: %s", event["list"])
            self._recorded_operations += self._get_valid_ops(event=event)
            return True
        elif event_type == "stop":
            self.logger.debug("Received stop from page")
            self.driver.stop_recording()
            self._recorded_operations += event["list"]
            return False
        else:
            raise ValueError(f"Unknown event type: {event_type}")

    def _get_valid_ops(self, event: RecordEvent):
        valid_ops = []
        for operation in event["list"]:
            if "selectors" not in operation or len(operation["selectors"]) == 0:
                continue
            valid_selectors = []
            valid_metas = []
            for selector in operation["selectors"]:
                meta = self.validate(
                    strategy=selector["strategy"],
                    value=selector["value"],
                    hide_highlights=True,
                )
                if "matches" not in meta or len(meta["matches"]) == 0:
                    self.logger.error("Selector %s was NOT valid: %s", selector, meta)
                    continue
                valid_selectors.append(selector)
                valid_metas.append(meta)
                self.logger.debug("Raw event metadata for %s: %s", selector, meta)
            operation["selectors"] = valid_selectors
            operation["meta"] = valid_metas
            if len(valid_selectors) > 0:
                valid_ops.append(operation)
        return valid_ops

    def _wait_for_page_to_load(self):
        waiter = WebDriverWait(self.driver, 10)
        waiter.until(
            lambda x: x.selenium.execute_script("return document.readyState")
            == "complete"
        )
