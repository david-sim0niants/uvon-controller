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


if __name__ == '__main__':

    local_address = get_local_address()
    server_address = (sys.argv[1], int(sys.argv[2]))

    client = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
    client.bind(local_address)

    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

        client.sendto([0x01], server_address)

        header = client.recv(4)
        bytes_len = int.from_bytes(header)

        img_bytes = client.recv(bytes_len)
        img = np.load(io.BytesIO(img_bytes))

        cv2.imshow('camera', img)

