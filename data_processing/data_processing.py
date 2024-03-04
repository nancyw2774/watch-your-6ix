'''
Architecture:

constant loop that monitors incoming data and determines whether a threat is detected
    - distance, speed, speed of cyclist

when a hazard condition is satisfied, call external function to call CV + send info to phone
'''
import time
from kld7 import KLD7, KLD7Exception
import time
import traceback
import subprocess

class kld7_class:

    # radar set to None on failure to init
    def __init__(self):
        self.radar = None
        port = "/dev/ttyAMA0"
        
        try:
            self.radar = KLD7(port, baudrate=115200)
        except Exception as e:
            print(f"An unexpected error occurred while initializing the KLD7 radar: {e}")

            # see if granting permissions fixes issue (catching permission error directly is not working)
            try:
                print(f"Granting permissions for {port}")
                subprocess.run(["sudo", "chmod", "g+r", port], check=True)
                self.radar = KLD7(port, baudrate=115200)
            except Exception as pe:
                print(f"Error setting permissions for {port}: {pe}")

def main():
    '''
    setup input sources
    '''
    sensor = kld7_class().radar

    while True:
        detection_data = sensor.read_TDAT()
        # outlining cases to take action
        #case 1: bike is moving, object detected

        # add bike speed if statement here
        if detection_data.speed < 0:
            if detection_data.distance < 25: #max 25m distance to trigger alerts
                #call CV to verify object identity
                print("hazard moving closer")
                continue
        else:
            if detection_data.distance < 10:
                #call CV to verify object identity
                print("hazard is really close")
                continue
        #else: if bike is not moving, hazard when speed < -20

if __name__ == "__main__":
    main()