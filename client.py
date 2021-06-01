import socket as sock
import numpy as np
import io
import sys
import cv2
import struct
import time
import atexit


def get_local_address():
    s = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    address = s.getsockname()
    s.close()
    return address


if __name__ == '__main__':

    PACKET_SIZE = 2 ** 15

    local_address = get_local_address()
    # local_address = ('127.0.0.1', 1234)
    server_address = (sys.argv[1], int(sys.argv[2]))

    client = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
    client.bind(local_address)

    video_writer = cv2.VideoWriter(sys.argv[3], cv2.VideoWriter_fourcc(*'MJPG'), 20, (600, 400))
    atexit.register(lambda: video_writer.release())

    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

        client.sendto(bytes([0x01]), server_address)
        img_data = b''
        while True:
            packet, _ = client.recvfrom(PACKET_SIZE)
            packs_left = struct.unpack('B', packet[:1])[0]
            img_data += packet[1:]
            if packs_left <= 1:
                break

        img = cv2.imdecode(np.frombuffer(img_data, 'uint8'), cv2.IMREAD_COLOR)
        video_writer.write(img)

        cv2.imshow('camera', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

    client.close()


