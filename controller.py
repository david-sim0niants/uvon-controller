import rplidar
from breezyslam.algorithms import RMHC_SLAM
from breezyslam.sensors import RPLidarA1
import sys
import numpy as np
import atexit



if __name__ == '__main__':
    
    lidar = rplidar.RPLidar(sys.argv[1])

    atexit.register(lidar.stop)
    atexit.register(lidar.disconnect)

    print('RPLidar health:', lidar.get_health()[0])
    print('RPLidar info: ', lidar.get_info())

    lidar.start_motor()
    scans_iterator = lidar.iter_scans()

    slam = RMHC_SLAM(RPLidarA1(), 800, 5)

    while True:
        scans = np.array(next(scans_iterator))
        slam.update(scans[..., 1].tolist(), scan_angles_degrees=scans[..., 2].tolist())

        x, y, theta = slam.getpos()

        print(x, y, theta)

