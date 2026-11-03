import asyncio
from winrt.windows.devices.bluetooth import BluetoothDevice, BluetoothCacheMode
from winrt.windows.networking.sockets import StreamSocket, SocketProtectionLevel

ADDR = "2c:be:ee:57:26:6c"  # your correct MAC

async def main():
    dev = await BluetoothDevice.from_bluetooth_address_async(int(ADDR.replace(":", ""), 16))
    if dev is None:
        print("Device not found: pair it in Windows first")
        return
    print("name:", dev.name, "| status:", dev.connection_status)
    res = await dev.get_rfcomm_services_async(BluetoothCacheMode.UNCACHED)
    print("error:", res.error, "| services:", res.services.size)
    for s in res.services:
        print("\nservice uuid:", s.service_id.uuid)
        sock = StreamSocket()
        try:
            await sock.connect_async(
                s.connection_host_name,
                s.connection_service_name,
                SocketProtectionLevel.BLUETOOTH_ENCRYPTION_ALLOW_NULL_AUTHENTICATION,
            )
            print("  CONNECTED")
        except Exception as e:
            print("  failed:", e)
        finally:
            sock.close()

asyncio.run(main())