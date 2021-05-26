import socket as sock
import numpy as np
import io
from csi_camera import *
from client import get_local_address


if __name__ == '__main__':

    local_address = get_local_address()

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
        buffer = io.BytesIO() 
        np.save(buffer, img)
        img_bytes = buffer.getvalue()
        server.sendto(len(img_bytes).to_bytes(4, byteorder='big', signed=True) + img_bytes, client_address)

