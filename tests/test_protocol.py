from cmfpc.codec import FrameParser
from cmfpc.protocol import parse_battery

CAPTURE = bytes.fromhex("55 60 01 07 40 05 00 00 02 02 5a 03 55 93 40")


def test_real_battery_frame():
    (f,) = FrameParser().feed(CAPTURE)
    assert f.command == 0x4007
    assert parse_battery(f.payload) == {
        "left": {"level": 90, "charging": False},
        "right": {"level": 85, "charging": False},
    }
