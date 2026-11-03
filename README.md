# cmfpc

Unofficial PC companion for Nothing / CMF earbuds (CMF Buds 2, Buds Pro 2). Not affiliated with Nothing.

Status: **early scaffold.** Codec and tests work; the device commands in `profiles/` are placeholders until verified via HCI capture (`docs/PROTOCOL.md`).

## Architecture
transport (RFCOMM) -> codec (frames, CRC) -> device (high-level API) -> CLI / future tray UI.
Per-model behaviour lives in `src/cmfpc/profiles/*.json`, so adding a device means adding a file.

## Use
```
pip install -e .
python -m pytest
cmfpc models
cmfpc probe AA:BB:CC:DD:EE:FF            # find RFCOMM channel
cmfpc dump AA:BB:CC:DD:EE:FF --model cmf_buds_2 --channel N
```

## Roadmap
- [ ] Verify framing + battery from capture
- [ ] ANC modes
- [ ] In-ear detection, find device
- [ ] Tray UI
- [ ] EQ, gestures
