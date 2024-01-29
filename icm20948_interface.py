#!/usr/bin/env python

import time
from icm20948 import ICM20948


class IMU:

    def __init__(self):
        try:
            self._conn = ICM20948()
        except Exception as e:
            print(f"An error occurred while initializing the ICM20948 IMU: {e}")


    def read(self):
        x, y, z = self._conn.read_magnetometer_data()
        ax, ay, az, gx, gy, gz = self._conn.read_accelerometer_gyro_data()

        print("""
Accel: {:05.2f} {:05.2f} {:05.2f}
Gyro:  {:05.2f} {:05.2f} {:05.2f}
Mag:   {:05.2f} {:05.2f} {:05.2f}""".format(
            ax, ay, az, gx, gy, gz, x, y, z
            ))

        time.sleep(0.25)


def main():
    print("""read-all.py

Reads all ranges of movement: accelerometer, gyroscope and

compass heading.

Press Ctrl+C to exit!

""")
    imu = IMU()

    while True:
        imu.read()


if __name__ == "__main__":
    main()