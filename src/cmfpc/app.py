"""cmfpc desktop window (pywebview). Run: python -m cmfpc.app [MAC MODEL]"""
import asyncio
import sys
import threading
from pathlib import Path

import webview

from .device import Device
from .tray import _find


class Api:
    def __init__(self, mac, model):
        self._mac, self._model = mac, model
        self._dev = None
        self._lock = threading.Lock()

    def _drop(self):
        if self._dev is not None:
            try:
                self._dev.t.close()
            except Exception:
                pass
        self._dev = None

    def state(self):
        if not self._mac:
            try:
                found = asyncio.run(_find())
            except Exception:
                found = []
            if not found:
                return {"connected": False,
                        "error": "No paired CMF buds found. Connect them to this PC in Windows Bluetooth settings."}
            self._mac, self._model = found[0]
        with self._lock:
            try:
                if self._dev is None:
                    self._dev = Device(self._mac, self._model)
                    self._dev.__enter__()
                b = self._dev.get_battery()
                if b is None:
                    raise OSError("no reply from buds")
                return {"connected": True, "battery": b, "mode": self._dev.get_anc()}
            except Exception as e:
                self._drop()
                return {"connected": False, "error": f"Not connected ({e})"}

    def set_anc(self, mode):
        with self._lock:
            if self._dev is None:
                return False
            try:
                self._dev.set_anc(mode)
                return True
            except Exception:
                self._drop()
                return False


def main():
    mac = model = None
    if len(sys.argv) >= 3:
        mac, model = sys.argv[1], sys.argv[2]
    page = Path(__file__).parent / "ui" / "index.html"
    webview.create_window("cmfpc", str(page), js_api=Api(mac, model),
                          width=430, height=820, background_color="#000000")
    webview.start()


if __name__ == "__main__":
    main()