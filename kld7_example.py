from kld7 import KLD7, KLD7Exception
import time
import traceback
import subprocess

'''
datasheet: https://rfbeam.ch/wp-content/uploads/dlm_uploads/2022/10/K-LD7_Datasheet.pdf
library api: https://kld7.readthedocs.io/en/latest/API.html#data-types 
'''

class kld7_class:

    # radar set to None on failure to init
    def __init__(self):
        self.radar = None
        port = "/dev/ttyAMA0"
        # self.radar = KLD7(port, baudrate=115200)
        
        try:
            self.radar = KLD7(port, baudrate=115200)
        except Exception as e:
            print(f"An unexpected error occurred while initializing the KLD7 radar: {e}")
            
            # see if granting permissions fixes issue (catching permission error directly is not working)
            try:
                print(f"Granting permissions for {port}")
                subprocess.run(["sudo", "chmod", "g+r", "/dev/ttyAMA0"], check=True)
                self.radar = KLD7(port, baudrate=115200)
            except Exception as pe:
                print(f"Error setting permissions for {port}: {pe}")


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
    if kld7_instance.radar is not None:
        start_time = time.perf_counter()
        while time.perf_counter() - start_time < 5:
            kld7_instance.readout()
        # kld7_instance.radar.close()

if __name__ == "__main__":
    main()