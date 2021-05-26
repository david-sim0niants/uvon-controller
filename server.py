import socket as sock
import numpy as np
import io
from csi_camera import *


server = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
server.bind(('127.0.0.1', 1234))
server.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 10)

csi = start_capturing()

while True:
    client_data = server.recvfrom(6)
    client_ip = '%d.%d.%d.%d' % (client_data[0], client_data[1], client_data[2], client_data[3])
    client_port = '%d' % int.from_bytes(client_data[4:])

    res, img = next(csi)
    if not res:
        continue
    buffer = io.BytesIO() 
    np.save(buffer, img)
    img_bytes = buffer.getvalue()
    server.sendto(len(img_bytes).to_bytes(4, byteorder='big', signed=True) + img_bytes, (client_ip, client_port))

