<div align="center">

# cmfpc

**Control your CMF Buds from Windows. No phone needed.**

[![Release](https://img.shields.io/github/v/release/jainharshall/cmf?style=flat-square)](https://github.com/jainharshall/cmf/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)
![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11-blue?style=flat-square)

<img src="docs/screenshot.png" width="360" alt="cmfpc window">

</div>

Unofficial desktop app for Nothing / CMF earbuds. Not affiliated with Nothing Technology Limited.

## Features (verified on CMF Buds 2)
- Left and right battery
- Noise cancellation / Transparency / Off
- Ultra Bass (on/off and level)
- Spatial Audio (Fixed / Off)
- Low Lag Mode
- In-ear detection
- Equaliser presets
- Finds your paired buds automatically and reconnects

## Install
1. Pair your buds in Windows Settings, then Bluetooth & devices.
2. Download `cmfpc.exe` from the [latest release](https://github.com/jainharshall/cmf/releases) and run it.

Windows SmartScreen may warn because the file is unsigned: click More info, then Run anyway.
Turn Bluetooth off on your phone first, so the buds connect to this PC.

## Roadmap
- [ ] Custom EQ (Bass / Mid / Treble)
- [ ] Gestures, Dual Connection, Find my buds
- [ ] Other models (CMF Buds Pro 2 is untested)

## How it works
The buds expose a custom Bluetooth serial service. Windows has no fixed channel for it, so cmfpc connects by service UUID through WinRT. Notes: [docs/PROTOCOL.md](docs/PROTOCOL.md)

Protocol details were worked out by observing the buds and cross-checking behaviour against the open-source ear-web project (GPL-3.0). cmfpc contains no code from it.

## Run from source
```
pip install -e .
pip install pywebview pystray pillow winrt-runtime winrt-Windows.Devices.Bluetooth winrt-Windows.Devices.Bluetooth.Rfcomm winrt-Windows.Devices.Enumeration winrt-Windows.Networking winrt-Windows.Networking.Sockets winrt-Windows.Foundation winrt-Windows.Foundation.Collections winrt-Windows.Storage.Streams
python -m cmfpc.app
```

## License
[MIT](LICENSE)