import rplidar
from breezyslam.algorithms import RMHC_SLAM
from breezyslam.sensors import RPLidarA1
import sys
import numpy as np
import atexit
import serial
import time



if __name__ == '__main__':
    
    lidar = rplidar.RPLidar(sys.argv[1])


    print('RPLidar health:', lidar.get_health()[0])
    print('RPLidar info: ', lidar.get_info())

    lidar.start_motor()
    scans_iterator = lidar.iter_scans()

    slam = RMHC_SLAM(RPLidarA1(), 800, 5)
    
    
    uvon_dev = serial.Serial(sys.argv[2], 115200)
    time.sleep(2)
    uvon_dev.write(b'2\n')
    uvon_dev.write(b'I1\n')

    atexit.register(lambda: uvon_dev.write(b'2\n'))
    atexit.register(lambda: uvon_dev.write(b'I0\n'))
    atexit.register(lidar.stop)
    atexit.register(lidar.disconnect)

    forward_cmd = b'm1,15,0,15\n'
    backward_cmd = b'm0,15,1,15\n'
    left_cmd = b'm1,1,0,15\n'
    right_cmd = b'm1,15,0,1\n'


    while True:
        scans = np.array(next(scans_iterator))
        slam.update(scans[..., 1].tolist(), scan_angles_degrees=scans[..., 2].tolist())

        x, y, theta = slam.getpos()

        theta = np.arcsin(np.sin(theta * np.pi / 180)) * 180 / np.pi

        print(x, y, theta)

        if -10 <= theta <= 10:
            uvon_dev.write(forward_cmd)
        elif -170 < theta < -10:
            uvon_dev.write(left_cmd)
        elif 10 < theta < 170:
            uvon_dev.write(right_cmd)
        else:
            uvon_dev.write(backward_cmd)
        time.sleep(0.1)


