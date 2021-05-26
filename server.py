import socket as sock
import numpy as np
import io
from csi_camera import *


if __name__ == '__main__':

    local_address = ('10.42.0.1', 1235)

    server = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
    server.bind(local_address)
    server.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 10)

    csi = start_capturing()

    while True:
        client_data, client_address = server.recvfrom(1)
        if not client_data[0]:
            continue

        res, img = next(csi)
        if not res:
            continue

        width_b = img.shape[1].to_bytes(2, 'big')
        height_b = img.shape[0].to_bytes(2, 'big')
        if len(img.shape) > 2:
            channels_b = img.shape[2].to_bytes(1, 'big')
        else:
            channels_b = bytes([1])
        dtype_b = img.dtype.char.encode()[:1]

        server.sendto(width_b + height_b + channels_b + dtype_b, client_address)

        img_bytes = img.data.to_bytes()
        packet_size = 4096
        for packet in range(0, len(img_bytes) + packet_size, packet_size):
            server.sendto(img_bytes[packet:packet + packet_size], client_address)

