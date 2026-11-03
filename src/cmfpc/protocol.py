BATTERY_REQ = 0xC007
BATTERY_RESP = 0x4007
IDS = {2: "left", 3: "right", 4: "case"}  # unverified mapping


def parse_battery(payload: bytes) -> dict:
    out = {}
    for i in range(payload[0]):
        dev, val = payload[1 + 2 * i], payload[2 + 2 * i]
        out[IDS.get(dev, f"id{dev}")] = {"level": val & 0x7F, "charging": bool(val & 0x80)}
    return out