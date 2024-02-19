from kld7 import KLD7, KLD7Exception
import time
import traceback

'''
datasheet: https://rfbeam.ch/wp-content/uploads/dlm_uploads/2022/10/K-LD7_Datasheet.pdf
library api: https://kld7.readthedocs.io/en/latest/API.html#data-types 
'''

class kld7_class:

    def __init__(self):
        try:
            self.radar = KLD7("/dev/ttyAMA0", baudrate=115200)
        except Exception as e:
            print(f"An error occurred while initializing the KLD7 radar: {e}")
            # TODO: gracefully close


    def readout(self):
        try:
            detection_data = self.radar.read_DDAT()
            print("detection data")
            print(detection_data)
            possible_targets = self.radar.read_PDAT()
            print("possible target data")
            print(possible_targets)
        except KLD7Exception as e:
            print(f"KLD7 Exception: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print(traceback.format_exc())

#TODO: prevent crashing on connection close
def main():
    kld7_instance = kld7_class()
    start_time = time.perf_counter()
    try:
        while time.perf_counter() - start_time < 5:
            kld7_instance.readout()
    except Exception as e:
        print(f"Got exception reading from radar: {e}")

    try:
        kld7_instance.radar.close()
    except Exception as e:
        print(f"Got exception closing connection: {e}")

if __name__ == "__main__":
    main()