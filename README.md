\# cmfpc



Unofficial Windows tray app for Nothing / CMF earbuds. Not affiliated with Nothing.



\## Supported

| Device | Battery | ANC modes | Current mode readout |

|---|---|---|---|

| CMF Buds 2 | verified | verified | verified |

| CMF Buds Pro 2 | untested | untested | untested |



\## Use

1\. Pair the buds in Windows Bluetooth settings.

2\. Download `cmfpc-tray.exe` from the Releases page and run it.

3\. Right-click the grey dot in the system tray (it may be under the `^` arrow).



The menu shows left/right battery and lets you switch Noise cancellation / Transparency / Off.



Windows SmartScreen may warn about the file because it is not signed. Click "More info", then "Run anyway".



\## How it works

The buds expose a custom Bluetooth serial service (UUID `aeac4a03-dff5-498f-843a-34487cf133eb`).

Windows has no fixed channel number for it, so the app connects by UUID through WinRT.

Details are in \[docs/PROTOCOL.md](docs/PROTOCOL.md).



\## Run from source

```

pip install -e .

pip install pystray pillow winrt-runtime winrt-Windows.Devices.Bluetooth winrt-Windows.Devices.Bluetooth.Rfcomm winrt-Windows.Devices.Enumeration winrt-Windows.Networking winrt-Windows.Networking.Sockets winrt-Windows.Foundation winrt-Windows.Foundation.Collections winrt-Windows.Storage.Streams

python -m cmfpc.tray

python -m pytest

```



\## Adding another device

Copy a JSON file in `src/cmfpc/profiles/`, fill in the verified bytes, and open a pull request.

