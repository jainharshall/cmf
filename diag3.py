import sys, time
sys.path.insert(0, "src")
from cmfpc.transport import WinRtTransport
from cmfpc.codec import Frame, encode

ADDR = "2c:be:ee:57:26:6c"
t = WinRtTransport(ADDR, "aeac4a03-dff5-498f-843a-34487cf133eb")
t.open()
print("connected, listening 5s (silence is normal)...")
end = time.time() + 5
while time.time() < end:
    d = t.recv()
    if d:
        print("RX raw:", d.hex(" "))

for cmd in (0xC007, 0xC001, 0xC006):   # guessed battery / info / status requests
    pkt = encode(Frame(cmd))
    print("TX", hex(cmd), pkt.hex(" "))
    t.send(pkt)
    end = time.time() + 3
    while time.time() < end:
        d = t.recv()
        if d:
            print("  RX raw:", d.hex(" "))
t.close()