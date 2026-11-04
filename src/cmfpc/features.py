"""Feature commands for CMF Buds 2 (model base B179).

Command IDs and payload layouts come from observing how the open-source
ear-web client talks to this model. Only battery and ANC are verified on real
hardware so far; everything here is marked UNVERIFIED until tested.
Reply command = request command ^ 0x8000 (e.g. 0xC050 -> 0x4050).
"""

# (UI name -> wire level) for the equaliser presets; order assumed from ear-web's button layout
EQ_PRESETS = {"dirac": 0, "rock": 1, "electronic": 2, "pop": 3, "vocals": 4, "classical": 5, "custom": 6}
EQ_NAMES = {v: k for k, v in EQ_PRESETS.items()}
SPATIAL = {"off": (0, 0), "fixed": (1, 0)}


def _get(dev, req):
    return dev.request(req, req ^ 0x8000)


# --- equaliser preset (UNVERIFIED) ---
def get_eq_preset(dev):
    f = _get(dev, 0xC050)
    return EQ_NAMES.get(f.payload[0], f"unknown({f.payload[0]})") if f else None


def set_eq_preset(dev, name):
    dev.send(0xF01D, bytes([EQ_PRESETS[name], 0x00]))


# --- ultra bass: level 1..5, wire value = level * 2 (UNVERIFIED) ---
def get_bass(dev):
    f = _get(dev, 0xC04E)
    return None if not f else {"enabled": f.payload[0] == 1, "level": f.payload[1] // 2, "wire": f.payload[1]}


def set_bass(dev, enabled, level):
    dev.send(0xF051, bytes([1 if enabled else 0, level * 2]))


# --- spatial audio: off / fixed (UNVERIFIED) ---
def get_spatial(dev):
    f = _get(dev, 0xC04F)
    if not f:
        return None
    mode, head = f.payload[0], f.payload[1] if len(f.payload) > 1 else 0
    for name, (m, h) in SPATIAL.items():
        if (m, h) == (mode, head):
            return name
    return f"unknown({mode},{head})"


def set_spatial(dev, name):
    m, h = SPATIAL[name]
    dev.send(0xF052, bytes([m, h]))


# --- low latency mode (UNVERIFIED; on=1, off=2 when writing) ---
def get_low_latency(dev):
    f = _get(dev, 0xC041)
    return None if not f else f.payload[0] == 1  # 2 = off (matches app), 1 = on


def set_low_latency(dev, on):
    dev.send(0xF040, bytes([1 if on else 2, 0x00]))


# --- in-ear detection (UNVERIFIED) ---
def get_in_ear(dev):
    f = _get(dev, 0xC00E)
    return None if not f or len(f.payload) < 3 else f.payload[2]


def set_in_ear(dev, on):
    dev.send(0xF004, bytes([1, 1, 1 if on else 0]))


# --- dual connection on/off (UNVERIFIED) ---
def get_dual(dev):
    f = _get(dev, 0xC027)
    return None if not f else f.payload[0] == 1


def set_dual(dev, on):
    dev.send(0xF01A, bytes([1 if on else 0]))


# --- find my buds: REMOVE THE BUDS FROM YOUR EARS FIRST, this is loud (UNVERIFIED) ---
def ring(dev, side, on):
    dev.send(0xF002, bytes([2 if side == "left" else 3, 1 if on else 0]))