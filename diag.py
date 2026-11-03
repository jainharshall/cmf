import socket
ADDR = "2c:be:ee:57:26:6c"
for ch in range(1, 11):
    s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    s.settimeout(3)
    try:
        s.connect((ADDR, ch))
        print(ch, "OPEN")
    except OSError as e:
        print(ch, e.errno, e)
    finally:
        s.close()