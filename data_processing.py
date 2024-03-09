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
import server

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
    camera_on = False

    while True:
        speed = server.get_speed()
        detection_data = sensor.read_TDAT()
        # outlining cases to take action
        if detection_data.speed > 0 and camera_on:
            server.trigger_event(5)
            server.trigger_event(0)
            camera_on = False
            continue
        
        hazard = detection_data.distance**2 - detection_data.speed**2
        danger_level = 1
        if hazard < 300:
            danger_level = 2
        if hazard < 100:
            danger_level = 3
        #case 1: bike is moving, object detected
        # add bike speed if statement here
        if speed > 2:
            if detection_data.speed < 0:
                if detection_data.distance < 25: #max 25m distance to trigger alerts
                    if server.has_hazard() == "True":
                        server.trigger_event(danger_level)
                        if not camera_on:
                            server.trigger_event(4)
                            camera_on = True
                        continue
            elif detection_data.distance < 10:
                if server.has_hazard() == "True":
                    server.trigger_event(danger_level)
                    if not camera_on:
                        server.trigger_event(4)
                        camera_on = True
                    continue
        elif detection_data.speed < -20:
            if server.has_hazard() == "True":
                server.trigger_event(danger_level)
                if not camera_on:
                    server.trigger_event(4)
                    camera_on = True
                continue
        #else: if bike is not moving, hazard when speed < -20
        # no hazard condition, turn off lights and camera
        server.trigger_event(5)
        server.trigger_event(0)
        camera_on = False

if __name__ == "__main__":
    main()