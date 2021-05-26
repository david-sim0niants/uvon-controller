import socket as sock
import numpy as np
import io
import sys
import cv2


client = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
client.connect((sys.args[1], int(sys.args[2])))

while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

    header = client.recv(4)
    bytes_len = int.from_bytes(header)

    img_bytes = client.recv(bytes_len)
    img = np.load(io.BytesIO(img_bytes))

    cv2.imshow('camera', img)

