"""Windows transport: connect to an RFCOMM service by UUID via WinRT."""
import asyncio
import queue
import threading

from winrt.windows.devices.bluetooth import BluetoothDevice, BluetoothCacheMode
from winrt.windows.networking.sockets import StreamSocket, SocketProtectionLevel
from winrt.windows.storage.streams import DataReader, DataWriter, InputStreamOptions


class WinRtTransport:
    def __init__(self, address: str, service_uuid: str):
        self.address = int(address.replace(":", ""), 16)
        self.uuid = service_uuid.lower()
        self.q = queue.Queue()
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self.loop.run_forever, daemon=True)
        self.sock = self.writer = self.reader = None

    def open(self, timeout: float = 10.0):
        self.thread.start()
        asyncio.run_coroutine_threadsafe(self._open(), self.loop).result(timeout)
        asyncio.run_coroutine_threadsafe(self._read_loop(), self.loop)

    async def _open(self):
        dev = await BluetoothDevice.from_bluetooth_address_async(self.address)
        if dev is None:
            raise OSError("device not found: pair/connect it in Windows first")
        res = await dev.get_rfcomm_services_async(BluetoothCacheMode.UNCACHED)
        svc = next((s for s in res.services if str(s.service_id.uuid).lower() == self.uuid), None)
        if svc is None:
            raise OSError(f"service {self.uuid} not found")
        self.sock = StreamSocket()
        await self.sock.connect_async(
            svc.connection_host_name,
            svc.connection_service_name,
            SocketProtectionLevel.BLUETOOTH_ENCRYPTION_ALLOW_NULL_AUTHENTICATION,
        )
        self.reader = DataReader(self.sock.input_stream)
        self.reader.input_stream_options = InputStreamOptions.PARTIAL
        self.writer = DataWriter(self.sock.output_stream)

    async def _read_loop(self):
        try:
            while True:
                n = await self.reader.load_async(1024)
                if n == 0:
                    break
                buf = bytearray(n)
                self.reader.read_bytes(buf)
                self.q.put(bytes(buf))
        except Exception as e:
            self.q.put(b"")
            print("read loop ended:", e)

    def send(self, data: bytes):
        async def _w():
            self.writer.write_bytes(data)
            await self.writer.store_async()
        asyncio.run_coroutine_threadsafe(_w(), self.loop).result(5)

    def recv(self, n: int = 1024) -> bytes:
        try:
            return self.q.get(timeout=0.5)
        except queue.Empty:
            return b""

    def close(self):
        if self.sock:
            self.sock.close()
            self.sock = None
        self.loop.call_soon_threadsafe(self.loop.stop)