import socket as sock
import sys
import time


video_cmd = b'p\n'

enable_move_cmd = b'1\n'
disable_move_cmd = b'2\n'

enable_uv_cmd = b'I1\n'
disable_uv_cmd = b'I0\n'

forward_cmd = b'm1,23,0,23\n'
backward_cmd = b'm0,23,1,23\n'
left_cmd = b'm0,17,0,17\n'
right_cmd = b'm1,17,1,17\n'
stop_cmd = b'm1,1,1,1\n'


def server_side(address, dev_port, record_name=None):

    s = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
    s.bind(address)
    s.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 10)

    PACKET_SIZE = 16

    import serial
    import atexit
    import csi_camera as csi

    dev = serial.Serial(dev_port, 112000) 

    uv_enabled = False
    move_enabled = False
    last_move_cmd = None

    atexit.register(lambda: dev.write(disable_uv_cmd)) 
    atexit.register(lambda: dev.write(disable_move_cmd) if move_enabled else None)

    video_writer = None

    while True:
        cmd, _ = s.recvfrom(PACKET_SIZE) 
        print(cmd)

        if cmd == video_cmd and record_name is not None:
            if video_writer is not None:
                video_writer.release()
            else:
                cap = csi.start_capturing(record_name, flip_method=2)
                video_writer = next(cap)

        elif cmd == enable_uv_cmd or cmd == disable_uv_cmd:
            dev.write(cmd)
            uv_enabled = not uv_enabled

        elif cmd == enable_move_cmd or cmd == disable_move_cmd:
            dev.write(cmd)
            move_enabled = not move_enabled

        elif cmd != last_move_cmd:
            dev.write(cmd)
            last_move_cmd = cmd

        if record_name is not None and video_writer is not None:
            next(cap)

        

def client_side(address, server_address):
    
    s = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
    s.bind(address)
    s.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 10)

    key2cmd = {
        'Up': forward_cmd,
        'w': forward_cmd,

        'Down': backward_cmd,
        's': backward_cmd,

        'Left': left_cmd,
        'a': left_cmd,

        'Right': right_cmd,
        'd': right_cmd,

        'space': stop_cmd,

        '1': enable_move_cmd,
        '2': disable_move_cmd,

        'i': enable_uv_cmd,
        'o': disable_uv_cmd,

        'p': video_cmd,
    }


    def on_key_press(event):
        root.title("{}: {}".format(str(event.type), event.keysym)) 
        if event.keysym in key2cmd:
            s.sendto(key2cmd[event.keysym], server_address)
            print(event.keysym)


    import tkinter as tk
    
    root = tk.Tk()
    root.geometry('640x480')

    root.bind('<KeyPress>', on_key_press)

    tk.mainloop()


def get_local_address():
    s = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    address = s.getsockname()
    s.close()
    return address



if __name__ == '__main__':

    if len(sys.argv) <= 1:
        print('gomik es?')
        exit()

    if sys.argv[1] == 'server':

        ip = sys.argv[2]
        port = int(sys.argv[3])
        dev_port = sys.argv[4]
        record_name = None if len(sys.argv) < 6 else sys.argv[5]

        server_side((ip, port), dev_port, record_name)


    elif sys.argv[1] == 'client':

        server_ip = sys.argv[2]
        server_port = int(sys.argv[3])

        address = get_local_address()

        client_side(address, (server_ip, server_port))


    else:
        print('gomik es?')

