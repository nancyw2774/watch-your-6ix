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
import requests

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
    url = "http://10.0.0.108:5001"
    sensor = kld7_class().radar
    camera_on = False

    while True:
        speed = server.get_speed()
        detection_data = sensor.read_TDAT()
        # # outlining cases to take action
        # if detection_data.speed > 0 and camera_on:
        #     server.trigger_event(5)
        #     server.trigger_event(0)
        #     camera_on = False
        #     continue
        
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
                    try:
                        hazard = requests.get(url+"/has_hazard")
                        if hazard.code == 200 and hazard.text == "True":
                            try:
                                event = requests.get(url+"/trigger_event/"+str(danger_level))
                            except requests.RequestException as e:
                                print(e)
                            if not camera_on:
                                try:
                                    event = requests.get(url+"/trigger_event/4")
                                    camera_on = True
                                except requests.RequestException as e:
                                    print(e)
                            continue
                    except requests.RequestException as e:
                        print(e)
            elif detection_data.distance < 10:
                try:
                    hazard = requests.get(url+"/has_hazard")
                    if hazard.code == 200 and hazard.text == "True":
                        try:
                            event = requests.get(url+"/trigger_event/"+str(danger_level))
                        except requests.RequestException as e:
                            print(e)
                        if not camera_on:
                            try:
                                event = requests.get(url+"/trigger_event/4")
                                camera_on = True
                            except requests.RequestException as e:
                                print(e)
                        continue
                except requests.RequestException as e:
                    print(e)
        elif detection_data.speed < -20:
            try:
                hazard = requests.get(url+"/has_hazard")
                if hazard.code == 200 and hazard.text == "True":
                    try:
                        event = requests.get(url+"/trigger_event/"+str(danger_level))
                    except requests.RequestException as e:
                        print(e)
                    if not camera_on:
                        try:
                            event = requests.get(url+"/trigger_event/4")
                            camera_on = True
                        except requests.RequestException as e:
                            print(e)
                    continue
            except requests.RequestException as e:
                print(e)
        #else: if bike is not moving, hazard when speed < -20
        # no hazard condition, turn off lights and camera
        if camera_on:
            try:
                event = requests.get(url+"/trigger_event/5")
            except requests.RequestException as e:
                print(e)
            try:
                event = requests.get(url+"/trigger_event/0")
            except requests.RequestException as e:
                print(e)
            camera_on = False

if __name__ == "__main__":
    main()