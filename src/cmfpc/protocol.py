BATTERY_REQ = 0xC007
BATTERY_RESP = 0x4007
IDS = {2: "left", 3: "right", 4: "case"}  # unverified mapping

ANC_GET_REQ = 0xC01E
ANC_GET_RESP = 0x401E
ANC_SET_ACK = 0x700F


def parse_anc_byte(payload: bytes) -> int:
    return payload[1]


def parse_battery(payload: bytes) -> dict:
    out = {}
    for i in range(payload[0]):
        dev, val = payload[1 + 2 * i], payload[2 + 2 * i]
        out[IDS.get(dev, f"id{dev}")] = {"level": val & 0x7F, "charging": bool(val & 0x80)}
    return out