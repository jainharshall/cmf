import time
from . import codec, profiles
from .transport import RfcommTransport


def _hex(v: str) -> int:
    return int(v, 16)


class Device:
    def __init__(self, address: str, model: str, channel=None):
        self.p = profiles.load(model)
        ch = channel or self.p["rfcomm_channel"]
        if not ch:
            raise ValueError("RFCOMM channel unknown: pass --channel or run `cmfpc probe`")
        self.header = bytes.fromhex(self.p["header"])
        self.parser = codec.FrameParser(self.header, self.p["crc"])
        self.t = RfcommTransport(address, ch)

    def __enter__(self):
        self.t.open()
        return self

    def __exit__(self, *a):
        self.t.close()

    def send(self, command: int, payload: bytes = b""):
        self.t.send(codec.encode(codec.Frame(command, payload), self.header, self.p["crc"]))

    def read_frames(self, seconds: float = 2.0):
        end, out = time.time() + seconds, []
        while time.time() < end:
            out += self.parser.feed(self.t.recv())
        return out

    def raw_dump(self, seconds: float = 10.0):
        """Print every frame received. Run this first to learn what your buds send."""
        for f in self.read_frames(seconds):
            print(f"cmd=0x{f.command:04X} op={f.op_id} payload={f.payload.hex()}")

    def get_battery(self):
        c = self.p["commands"]["get_battery"]
        self.send(_hex(c["id"]), bytes.fromhex(c["payload"]))
        return self.read_frames()

    def set_anc(self, mode: str):
        byte = _hex(self.p["anc_modes"][mode])
        self.send(_hex(self.p["commands"]["set_anc"]["id"]), bytes([0x01, byte, 0x00]))
