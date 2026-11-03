# CMF Buds 2 control protocol (reverse-engineered)

Status: observed on one pair of CMF Buds 2 from Windows. Anything not marked **verified** is a guess.

## Transport
- Bluetooth Classic RFCOMM, custom serial service UUID `aeac4a03-dff5-498f-843a-34487cf133eb`.
- Windows does not expose a fixed channel number for it: raw RFCOMM sockets to channels 1-30 time out.
  Connect by service UUID through WinRT (`BluetoothDevice.GetRfcommServicesAsync`, then `StreamSocket`).
- The buds stay silent until they receive a valid request.

## Frame format (verified)
```
55 60 01 | cmd (2 bytes, LE) | length (2 bytes, LE) | op (1 byte) | payload | CRC16 (2 bytes, LE)
```
- CRC is CRC-16/MODBUS (poly 0xA001, init 0xFFFF) over everything before the CRC.
- Replies use the request command with the top bit cleared: `0xC007` -> `0x4007`.

## Commands
| Purpose | Request | Reply | Payload | Status |
|---|---|---|---|---|
| Battery | `0xC007` | `0x4007` | `count, (id, value)...`; value low 7 bits = %, top bit = charging | verified |
| Get ANC mode | `0xC01E` | `0x401E` | `01 <mode> 00 02 01 00` | verified |
| Set ANC mode | `0xF00F` | `0x700F` (payload `00`, treated as ack) | `01 <mode> 00` | verified |
| Firmware/info | `0xC001`, `0xC006` | `0x4001`, `0x4006` | version-like strings, per-bud firmware and serial text | decoded, unused |

### ANC mode byte (verified)
| Byte | Mode |
|---|---|
| `0x05` | Off |
| `0x07` | Transparency |
| `0x01` | Noise cancellation |

`0x03` was sent during testing; its effect was not recorded, so it is not listed.

### Battery ids (unverified)
Ids `2` and `3` appear in battery replies; they are assumed to be left and right.
An id `4` (case) is assumed but was never observed.

## Method
1. Enumerate services with WinRT, find the one that is not a standard profile.
2. Send guessed frames and log raw replies.
3. Check replies with the CRC to confirm the framing.
4. Test each command on hardware and compare against what is heard.

## Not done
- In-ear detection events, EQ, gestures.
- Other models (CMF Buds Pro 2 is untested).
