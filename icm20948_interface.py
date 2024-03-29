#!/usr/bin/env python

import time
from icm20948 import ICM20948
from collections import deque

# TODO: figure out calibration sequence
class IMU:

    def __init__(self):
        try:
            self._conn = ICM20948()
        except Exception as e:
            print(f"An error occurred while initializing the ICM20948 IMU: {e}")

        self._accel_q = deque([], maxlen=5)
        self._gyro_q = deque([], maxlen=5)
        self._mag_q = deque([], maxlen=5)
        self._time_q = deque([], maxlen=5)

    # using moving window avg for basic filtering
    def get_accel(self):
        return sum(self._accel_q) / len(self._accel_q)

    def get_gyro(self):
        return sum(self._gyro_q) / len(self._gyro_q)

    def get_mag(self):
        return sum(self._mag_q) / len(self._mag_q)

    # TODO: run as thread to update values
    def update_qs(self):
        x, y, z = self._conn.read_magnetometer_data()
        ax, ay, az, gx, gy, gz = self._conn.read_accelerometer_gyro_data()
        self._accel_q.append((ax, ay, az))
        self._gyro_q.append((gx, gy, gz))
        self._mag_q.append((x, y, z))
        self._time_q.append(time.perf_counter())
        time.sleep(0.25)

    def print_params(self):
        x, y, z = self._mag_q[-1]
        ax, ay, az = self._accel_q[-1]
        gx, gy, gz = self._gyro_q[-1]

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
        imu.print_params()


if __name__ == "__main__":
    main()