from cmfpc import features as f
from cmfpc.codec import Frame


class Fake:
    def __init__(self, replies=None):
        self.sent, self.replies = [], replies or {}

    def send(self, cmd, payload=b""):
        self.sent.append((cmd, bytes(payload)))

    def request(self, cmd, resp, payload=b"", timeout=2.0):
        p = self.replies.get(cmd)
        return None if p is None else Frame(resp, bytes.fromhex(p))


def test_reply_command_is_request_xor_8000():
    assert 0xC050 ^ 0x8000 == 0x4050 and 0xC007 ^ 0x8000 == 0x4007


def test_writes():
    d = Fake()
    f.set_eq_preset(d, "pop"); f.set_bass(d, True, 3); f.set_spatial(d, "fixed")
    f.set_low_latency(d, True); f.set_low_latency(d, False); f.set_dual(d, True)
    f.ring(d, "left", True); f.ring(d, "right", False)
    assert d.sent == [
        (0xF01D, b"\x03\x00"), (0xF051, b"\x01\x06"), (0xF052, b"\x01\x00"),
        (0xF040, b"\x01\x00"), (0xF040, b"\x02\x00"), (0xF01A, b"\x01"),
        (0xF002, b"\x02\x01"), (0xF002, b"\x03\x00"),
    ]


def test_reads():
    d = Fake({0xC050: "00 00", 0xC04E: "01 06", 0xC04F: "01 00", 0xC027: "00", 0xC041: "02"})
    assert f.get_eq_preset(d) == "dirac"
    assert f.get_bass(d) == {"enabled": True, "level": 3, "wire": 6}
    assert f.get_spatial(d) == "fixed"
    assert f.get_dual(d) is False
    assert f.get_low_latency(d) is False
    assert f.get_low_latency(Fake()) is None