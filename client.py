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

        client.sendto(bytes([0x01]), server_address)

        width = int.from_bytes(client.recv(2), 'big')
        height = int.from_bytes(client.recv(2), 'big')
        channels = int.from_bytes(client.recv(1), 'big')
        dtype = np.dtype(client.recv(1).decode())

        bytes_len = width * height * channels * dtype.itemsize
        print(bytes_len)

        img_bytes = bytearray(bytes_len)
        num_bytes_filled = 0
        while num_bytes_filled < bytes_len:
            img_bytes[num_bytes_filled:num_bytes_filled + 4096] = client.recv(4096)
            num_bytes_filled += 4096

        img = np.frombuffer(img_bytes, dtype=dtype).reshape(height, width, channels)

        cv2.imshow('camera', img)

