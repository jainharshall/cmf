"""RFCOMM transport using Python's built-in Bluetooth socket (Windows/Linux)."""
import socket


class RfcommTransport:
    def __init__(self, address: str, channel: int):
        self.address, self.channel = address, channel
        self.sock = None

    def open(self, timeout: float = 5.0):
        s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        s.settimeout(timeout)
        s.connect((self.address, self.channel))
        self.sock = s

    def send(self, data: bytes):
        self.sock.sendall(data)

    def recv(self, n: int = 1024) -> bytes:
        try:
            return self.sock.recv(n)
        except socket.timeout:
            return b""

    def close(self):
        if self.sock:
            self.sock.close()
            self.sock = None


def probe_channels(address: str, channels=range(1, 31), timeout: float = 2.0):
    """No easy SDP lookup via stdlib on Windows: try channels, report which accept."""
    found = []
    for ch in channels:
        t = RfcommTransport(address, ch)
        try:
            t.open(timeout)
            found.append(ch)
        except OSError:
            pass
        finally:
            t.close()
    return found
