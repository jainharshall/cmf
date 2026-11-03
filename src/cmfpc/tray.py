import sys
import threading

import pystray
from PIL import Image, ImageDraw

from .device import Device

MODES = [("Noise cancellation", "anc"), ("Transparency", "transparency"), ("Off", "off")]


class Tray:
    def __init__(self, mac: str, model: str):
        self.mac, self.model = mac, model
        self.dev = None
        self.lock = threading.Lock()
        self.stop = threading.Event()
        self.battery = {}
        self.mode = None
        self.icon = pystray.Icon("cmfpc", self._image(), "cmfpc: connecting...", menu=pystray.Menu(self._items))

    @staticmethod
    def _image():
        img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        ImageDraw.Draw(img).ellipse((8, 8, 56, 56), fill=(230, 230, 230, 255), outline=(30, 30, 30, 255), width=4)
        return img

    def _battery_text(self):
        if self.dev is None or not self.battery:
            return "Not connected"
        return "  ".join(f"{k[0].upper()} {v['level']}%{'+' if v['charging'] else ''}" for k, v in self.battery.items())

    def _items(self):
        yield pystray.MenuItem(self._battery_text(), None, enabled=False)
        for label, mode in MODES:
            yield pystray.MenuItem(
                label, self._setter(mode), checked=lambda item, m=mode: self.mode == m, radio=True
            )
        yield pystray.MenuItem("Quit", self._quit)

    def _setter(self, mode):
        def action(icon, item):
            with self.lock:
                if self.dev is None:
                    return
                try:
                    self.dev.set_anc(mode)
                    self.mode = mode
                except Exception as e:
                    print("set_anc failed:", e)
            icon.update_menu()
        return action

    def _drop(self):
        if self.dev is not None:
            try:
                self.dev.t.close()
            except Exception:
                pass
        self.dev = None
        self.battery = {}

    def _poll(self):
        while not self.stop.is_set():
            try:
                with self.lock:
                    if self.dev is None:
                        self.dev = Device(self.mac, self.model)
                        self.dev.__enter__()
                    b = self.dev.get_battery()
                    if b is None:
                        raise OSError("no battery reply")
                    self.battery = b
                    self.mode = self.dev.get_anc()
            except Exception as e:
                print("reconnecting:", e)
                with self.lock:
                    self._drop()
            self.icon.title = "cmfpc: " + self._battery_text()
            self.icon.update_menu()
            self.stop.wait(30 if self.battery else 5)

    def _quit(self, icon, item):
        self.stop.set()
        with self.lock:
            self._drop()
        icon.stop()

    def run(self):
        threading.Thread(target=self._poll, daemon=True).start()
        self.icon.run()


import asyncio

from . import profiles


async def _find():
    from winrt.windows.devices.bluetooth import BluetoothDevice
    from winrt.windows.devices.enumeration import DeviceInformation

    sel = BluetoothDevice.get_device_selector_from_pairing_state(True)
    infos = await DeviceInformation.find_all_async_aqs_filter(sel)
    out = []
    for i in infos:
        model = i.name.lower().replace(" ", "_")
        if model in profiles.available():
            dev = await BluetoothDevice.from_id_async(i.id)
            a = f"{dev.bluetooth_address:012X}"
            out.append((":".join(a[j:j + 2] for j in range(0, 12, 2)), model))
    return out


def main():
    if len(sys.argv) >= 3:
        mac, model = sys.argv[1], sys.argv[2]
    else:
        found = asyncio.run(_find())
        if not found:
            sys.exit("No paired CMF buds found. Pair them in Windows, or run: cmfpc-tray MAC MODEL")
        mac, model = found[0]
    Tray(mac, model).run()


if __name__ == "__main__":
    main()