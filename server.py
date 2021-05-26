import socket as sock
import numpy as np
import io
from csi_camera import *


server = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
server.bind(('127.0.0.1', 1234))
server.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 10)
server.listen(5)


client, client_address = server.accept()

csi = start_capturing()

while True:
    res, img = next(csi)
    if not res:
        continue
    buffer = io.BytesIO() 
    np.save(buffer, img)
    img_bytes = buffer.getvalue()
    client.send(len(img_bytes).to_bytes(4, byteorder='big', signed=True) + img_bytes)

