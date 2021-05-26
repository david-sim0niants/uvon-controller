import socket as sock
import numpy as np
import io
import sys
import cv2


def get_local_address():
    s = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    address = s.getsockname()
    s.close()
    return address


local_address = get_local_address()

client = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
client.bind(('127.0.0.1', local_address[1]))

while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

    client_ip_bytes = bytes(int(x) for x in local_address[0].split('.'))
    client_port_bytes = local_address[1].to_bytes(2, 'big')
    client.sendto(client_ip_bytes + client_port_bytes, (sys.argv[1], int(sys.argv[2])))

    header = client.recv(4)
    bytes_len = int.from_bytes(header)

    img_bytes = client.recv(bytes_len)
    img = np.load(io.BytesIO(img_bytes))

    cv2.imshow('camera', img)

