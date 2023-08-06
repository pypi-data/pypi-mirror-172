from inspector_commons.bridge.bridge_browser import BrowserBridge  # type: ignore
from inspector.windows.base import Window


class BrowserWindow(Window):
    BRIDGE = BrowserBridge
    DEFAULTS = {
        "title": "Robocorp Web Element Locator",
        "url": "browser.html",
        "width": 480,
        "height": 100,
        "on_top": True,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._force_closing = False

    def on_closing(self):
        should_close = super().on_closing()
        if not should_close:
            return False

        driver = self._context.webdriver
        if driver is not None and driver.is_running:
            try:
                driver.clear()
            except Exception as exc:  # pylint: disable=broad-except
                self.logger.debug("Failed to clear webdriver: %s", exc)

        return True
