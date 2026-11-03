import sys, time
sys.path.insert(0, "src")
from cmfpc.device import Device

MAC = "2c:be:ee:57:26:6c"
with Device(MAC, "cmf_buds_2") as d:
    print("connected")
    time.sleep(1)
    print("battery:", d.get_battery())