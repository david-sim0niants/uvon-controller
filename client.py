import socket as sock
import numpy as np
import io
import sys
import cv2
import time


def get_local_address():
    s = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    address = s.getsockname()
    s.close()
    return address


if __name__ == '__main__':

    local_address = get_local_address()
    # local_address = ('127.0.0.1', 1234)
    server_address = (sys.argv[1], int(sys.argv[2]))

    client = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
    client.bind(local_address)

    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

        client.sendto(bytes([0x01]), server_address)

        header = client.recv(6)

        width = int.from_bytes(header[:2], 'big')
        height = int.from_bytes(header[2:4], 'big')
        channels = int.from_bytes(header[4:5], 'big')
        dtype = np.dtype(header[5:6].decode())

        print(width, height, channels, dtype)

        bytes_len = width * height * channels * dtype.itemsize
        print(bytes_len / dtype.itemsize)

        img_bytes = bytearray(bytes_len)
        num_bytes_filled = 0
        num_packs_recieved = 0
        packet_size = 32768

        bytes_len_floor = bytes_len + packet_size
        while num_bytes_filled < bytes_len_floor:
            packet = client.recv(packet_size)
            img_bytes[num_bytes_filled:num_bytes_filled + packet_size] = packet
            num_bytes_filled += packet_size
            num_packs_recieved += 1
            print(num_packs_recieved)
        img_bytes = img_bytes[:bytes_len]
        

        img = np.frombuffer(img_bytes, dtype=dtype).reshape(height, width, channels)

        cv2.imshow('camera', img)
        cv2.waitKey(0)

