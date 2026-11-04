"""Write test: changes each setting, reads it back, then restores your original value.
Play some music first so you can hear the bass/EQ changes. Do not touch the Nothing X app meanwhile.
Usage: python try_writes.py AA:BB:CC:DD:EE:FF
"""
import sys
import time

sys.path.insert(0, "src")
from cmfpc.device import Device
from cmfpc import features as f

mac = sys.argv[1]


def run(label, change, read, expected, restore):
    try:
        change()
        time.sleep(1.5)
        got = read()
        print(f"{'OK  ' if got == expected else 'DIFF'} {label}: expected {expected!r}, got {got!r}")
    finally:
        restore()
        time.sleep(1.5)


with Device(mac, "cmf_buds_2") as d:
    time.sleep(1)
    bass = f.get_bass(d)
    eq = f.get_eq_preset(d)
    spatial = f.get_spatial(d)
    lat = f.get_low_latency(d)
    ear = f.get_in_ear(d)
    print("original:", bass, eq, spatial, lat, ear, "\n")

    run("ultra bass level 3 -> 4", lambda: f.set_bass(d, True, 4),
        lambda: (f.get_bass(d) or {}).get("level"), 4, lambda: f.set_bass(d, bass["enabled"], bass["level"]))
    run("ultra bass off", lambda: f.set_bass(d, False, bass["level"]),
        lambda: (f.get_bass(d) or {}).get("enabled"), False, lambda: f.set_bass(d, bass["enabled"], bass["level"]))
    if eq in f.EQ_PRESETS:
        run("eq preset -> pop", lambda: f.set_eq_preset(d, "pop"),
            lambda: f.get_eq_preset(d), "pop", lambda: f.set_eq_preset(d, eq))
    if spatial in f.SPATIAL:
        other = "off" if spatial == "fixed" else "fixed"
        run(f"spatial audio -> {other}", lambda: f.set_spatial(d, other),
            lambda: f.get_spatial(d), other, lambda: f.set_spatial(d, spatial))
    run("low latency -> on", lambda: f.set_low_latency(d, True),
        lambda: f.get_low_latency(d), True, lambda: f.set_low_latency(d, bool(lat)))
    if ear is not None:
        run("in-ear detection -> off", lambda: f.set_in_ear(d, False),
            lambda: f.get_in_ear(d), 0, lambda: f.set_in_ear(d, bool(ear)))
    print("\nafter restore:", f.get_bass(d), f.get_eq_preset(d), f.get_spatial(d), f.get_low_latency(d), f.get_in_ear(d))