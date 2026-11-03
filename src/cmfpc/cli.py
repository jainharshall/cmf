import argparse
from . import profiles
from .device import Device
from .transport import probe_channels


def main():
    ap = argparse.ArgumentParser(prog="cmfpc")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("models")
    p = sub.add_parser("probe")
    p.add_argument("address")
    for name in ("dump", "battery", "anc"):
        s = sub.add_parser(name)
        s.add_argument("address")
        s.add_argument("--model", required=True)
        s.add_argument("--channel", type=int)
        if name == "anc":
            s.add_argument("mode")
    a = ap.parse_args()

    if a.cmd == "models":
        print("\n".join(profiles.available()))
    elif a.cmd == "probe":
        print("open RFCOMM channels:", probe_channels(a.address))
    else:
        with Device(a.address, a.model, a.channel) as d:
            if a.cmd == "dump":
                d.raw_dump()
            elif a.cmd == "battery":
                for f in d.get_battery():
                    print(f"cmd=0x{f.command:04X} payload={f.payload.hex()}")
            elif a.cmd == "anc":
                d.set_anc(a.mode)


if __name__ == "__main__":
    main()
