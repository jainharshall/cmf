# Protocol notes (fill this in from your own capture)

Everything in `profiles/*.json` is UNVERIFIED until confirmed here.

## Capture
1. Android: Developer options -> enable "Bluetooth HCI snoop log".
2. Toggle Bluetooth off/on, open Nothing X, do ONE action at a time (ANC mode, EQ...), note the order.
3. Pull the log (`adb bugreport`), open in Wireshark, filter `btrfcomm`.
4. Record each action -> bytes below.

## Findings
| Action | Command ID | Payload | Response |
|--------|-----------|---------|----------|
| battery | ? | ? | ? |
| ANC off | ? | ? | ? |
| ANC on | ? | ? | ? |
| transparency | ? | ? | ? |

Cross-check against Gadgetbridge's Nothing device code (read, then reimplement; it is AGPL).
