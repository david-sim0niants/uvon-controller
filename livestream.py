import socket as sock
from csi_camera import *



def server_side(address, **cam_params):
    
    s = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
    s.bind(address)

    
