import serial
import sys
import threading as th
import time



def reading_thread(dev : serial.Serial):
    while True:
        print(dev.readall().decode())
        time.sleep(0.001)

def writing_thread(dev : serial.Serial):
    while True:
        cmd = input('Enter Cmd: ').encode()
        uvon_dev.write(cmd)
        time.sleep(0.001)


if __name__ == '__main__':

    port = sys.argv[1]
    baudrate = int(sys.argv[2]) if len(sys.argv) > 1 else 115200
    
    uvon_dev = serial.Serial(port, baudrate)

    reading = th.Thread(target=reading_thread, args=(uvon_dev,))
    writing = th.Thread(target=writing_thread, args=(uvon_dev,))

    reading.start()
    reading.join()

    writing.start()
    writing.join()

