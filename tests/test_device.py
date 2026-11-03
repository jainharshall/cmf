from cmfpc.device import Device


def test_device_api_surface():
    for name in ("send", "request", "get_battery", "get_anc", "set_anc"):
        assert callable(getattr(Device, name))