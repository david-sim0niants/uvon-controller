import socket as sock
import numpy as np
import io
from csi_camera import *
import time
import struct


if __name__ == '__main__':

    PACKET_SIZE = 2 ** 15

    local_address = ('10.42.0.1', 1235)
    # local_address = ('127.0.0.1', 1235)

    server = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
    server.bind(local_address)
    server.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 10)

    csi = start_capturing(flip_method=2)

    while True:
        client_data, client_address = server.recvfrom(1)
        if not client_data[0]:
            continue

        res, img = next(csi)
        if not res:
            continue

        img_encoded = cv2.imencode('.jpg', img)[1].tobytes()

        size = len(img_encoded)
        num_packs = int(np.ceil(size / (PACKET_SIZE - 1)))
        packet_begin = 0
        
        while num_packs:
            packet_end = packet_begin + PACKET_SIZE
            server.sendto(struct.pack('B', num_packs) + img_encoded[packet_begin:packet_end], client_address)
            packet_begin = packet_end
            num_packs -= 1

        
        
