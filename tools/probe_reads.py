"""Read-only check: asks the buds for each setting and prints raw + parsed values.
Compare with what the Nothing X app shows. Nothing is written to the buds.
Usage: python probe_reads.py AA:BB:CC:DD:EE:FF
"""
import sys
import time

sys.path.insert(0, "src")
from cmfpc.device import Device
from cmfpc import features as f

mac = sys.argv[1]
with Device(mac, "cmf_buds_2") as d:
    time.sleep(1)
    reads = [
        ("battery", 0xC007), ("anc", 0xC01E), ("eq preset", 0xC050), ("ultra bass", 0xC04E),
        ("spatial audio", 0xC04F), ("low latency", 0xC041), ("in-ear detection", 0xC00E),
        ("dual connection", 0xC027),
    ]
    for name, cmd in reads:
        fr = d.request(cmd, cmd ^ 0x8000, timeout=2.0)
        print(f"{name:18s}", "no reply" if fr is None else f"cmd=0x{fr.command:04X} payload={fr.payload.hex(' ')}")
    print("\nparsed:")
    print(" eq preset   :", f.get_eq_preset(d))
    print(" ultra bass  :", f.get_bass(d))
    print(" spatial     :", f.get_spatial(d))
    print(" low latency :", f.get_low_latency(d))
    print(" in-ear      :", f.get_in_ear(d))
    print(" dual conn.  :", f.get_dual(d))