<div align="center">

# cmfpc

**Control your CMF Buds from Windows. No phone needed.**

[![Release](https://img.shields.io/github/v/release/jainharshall/cmf?style=flat-square)](https://github.com/jainharshall/cmf/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)
![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11-blue?style=flat-square)
![Python](https://img.shields.io/badge/python-3.9%2B-yellow?style=flat-square)
[![Stars](https://img.shields.io/github/stars/jainharshall/cmf?style=flat-square)](https://github.com/jainharshall/cmf/stargazers)

<img src="docs/screenshot.png" width="320" alt="cmfpc tray menu">

</div>

A small system-tray app that talks to Nothing / CMF earbuds directly over Bluetooth. It was built by reverse-engineering the buds' control protocol, because there is no official Windows app.

> Unofficial. Not affiliated with or endorsed by Nothing Technology Limited. "Nothing" and "CMF" are their trademarks.

## Features

- Left and right bud battery, with a charging indicator
- Switch between **Noise cancellation**, **Transparency** and **Off** from the tray
- Shows the mode your buds are currently in
- Finds your paired buds automatically
- Single `.exe`, no Python needed

## Supported devices

| Device | Battery | ANC modes | Current mode |
|---|:---:|:---:|:---:|
| CMF Buds 2 | ✅ | ✅ | ✅ |
| CMF Buds Pro 2 | untested | untested | untested |

Got a different model? See [Adding a device](#adding-a-device).

## Install

1. Pair your buds in **Windows Settings → Bluetooth & devices**.
2. Download `cmfpc-tray.exe` from the [latest release](https://github.com/jainharshall/cmf/releases).
3. Run it. A grey dot appears in the system tray (it may be under the `^` arrow).
4. Right-click the dot.

Windows SmartScreen may warn because the file is unsigned: click **More info → Run anyway**.

## How it works

The buds expose a custom Bluetooth serial service. Windows has no fixed channel number for it, so cmfpc connects by service UUID through WinRT and speaks a small framed protocol (command, length, payload, CRC16).

Full notes: [docs/PROTOCOL.md](docs/PROTOCOL.md)

## Run from source

```powershell
pip install -e .
pip install pystray pillow winrt-runtime winrt-Windows.Devices.Bluetooth winrt-Windows.Devices.Bluetooth.Rfcomm winrt-Windows.Devices.Enumeration winrt-Windows.Networking winrt-Windows.Networking.Sockets winrt-Windows.Foundation winrt-Windows.Foundation.Collections winrt-Windows.Storage.Streams
python -m cmfpc.tray
python -m pytest
```

## Adding a device

Per-model behaviour lives in `src/cmfpc/profiles/*.json`. Copy one, put in the bytes you verified on your hardware, and open a pull request. Capture steps are in [docs/PROTOCOL.md](docs/PROTOCOL.md).

## Troubleshooting

- **Menu says "Not connected":** make sure the buds are out of the case, connected to this PC in Windows, and not holding a connection to your phone.
- **No tray icon:** check the `^` overflow arrow next to the clock.
- **Two copies running:** quit one; only one app can hold the connection.

## Roadmap

- [ ] Confirm CMF Buds Pro 2
- [ ] In-ear detection
- [ ] Equaliser
- [ ] Run at startup

## License

[MIT](LICENSE)
