
from kld7_interface import Radar
from icm20948_interface import IMU

# TODO: add connection object
# TODO: add cv stuff?
class BlindSpotDetection:
    def __init__(self):
        self.radar = Radar()
        self.imu = IMU()

def main():
    pass

if __name__ == "__main__":
    main()