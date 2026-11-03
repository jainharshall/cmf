"""Frame encode/decode.

Layout (ASSUMED, verify against your own HCI capture, see docs/PROTOCOL.md):
  header(3) | command(2, LE) | length(2, LE) | op_id(1) | payload | crc16(2, LE)
CRC covers everything before the CRC. Header and CRC variant live in the
device profile, so a model with different framing needs only a new profile.
"""
from dataclasses import dataclass

DEFAULT_HEADER = bytes([0x55, 0x60, 0x01])


def crc16_modbus(data: bytes) -> int:
    crc = 0xFFFF
    for b in data:
        crc ^= b
        for _ in range(8):
            crc = (crc >> 1) ^ 0xA001 if crc & 1 else crc >> 1
    return crc


@dataclass
class Frame:
    command: int
    payload: bytes = b""
    op_id: int = 0


def encode(frame: Frame, header: bytes = DEFAULT_HEADER, use_crc: bool = True) -> bytes:
    body = (
        header
        + frame.command.to_bytes(2, "little")
        + len(frame.payload).to_bytes(2, "little")
        + bytes([frame.op_id])
        + frame.payload
    )
    if use_crc:
        body += crc16_modbus(body).to_bytes(2, "little")
    return body


class FrameParser:
    """Feed raw bytes from the socket, get complete Frames out."""

    def __init__(self, header: bytes = DEFAULT_HEADER, use_crc: bool = True):
        self.header, self.use_crc = header, use_crc
        self.buf = bytearray()

    def feed(self, data: bytes):
        self.buf += data
        out = []
        h = len(self.header)
        while True:
            i = self.buf.find(self.header)
            if i < 0:
                # keep a tail that could be the start of a header
                del self.buf[: max(0, len(self.buf) - (h - 1))]
                break
            del self.buf[:i]
            fixed = h + 5
            if len(self.buf) < fixed:
                break
            plen = int.from_bytes(self.buf[h + 2 : h + 4], "little")
            total = fixed + plen + (2 if self.use_crc else 0)
            if len(self.buf) < total:
                break
            raw = bytes(self.buf[:total])
            del self.buf[:total]
            if self.use_crc:
                if crc16_modbus(raw[:-2]) != int.from_bytes(raw[-2:], "little"):
                    continue  # corrupt frame, resync
                raw = raw[:-2]
            out.append(
                Frame(
                    command=int.from_bytes(raw[h : h + 2], "little"),
                    op_id=raw[h + 4],
                    payload=raw[h + 5 :],
                )
            )
        return out
