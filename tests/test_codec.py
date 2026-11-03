from cmfpc.codec import Frame, FrameParser, crc16_modbus, encode


def test_crc_check_value():
    assert crc16_modbus(b"123456789") == 0x4B37  # standard CRC-16/MODBUS check


def test_roundtrip():
    f = Frame(0xC007, b"\x01\x02", op_id=3)
    assert FrameParser().feed(encode(f)) == [f]


def test_split_stream_and_garbage():
    raw = b"\x00\xff" + encode(Frame(1, b"ab")) + encode(Frame(2))
    p = FrameParser()
    got = p.feed(raw[:7]) + p.feed(raw[7:])
    assert [x.command for x in got] == [1, 2]


def test_bad_crc_dropped():
    raw = bytearray(encode(Frame(1, b"ab")))
    raw[-1] ^= 0xFF
    assert FrameParser().feed(bytes(raw)) == []
