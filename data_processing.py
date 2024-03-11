'''
Architecture:

constant loop that monitors incoming data and determines whether a threat is detected
    - distance, speed, speed of cyclist

when a hazard condition is satisfied, call external function to call CV + send info to phone
'''
import time
import time
import traceback
import os.path
import requests
from kld7_wrapper import kld7_wrapper

def main():
    '''
    setup input sources
    '''
    url = "http://172.20.10.2:5001"
    radar = kld7_wrapper().radar
    camera_on = False

    while True:
        # speed = test_server.get_speed()
        detection_data = radar.read_TDAT()
        if detection_data == None:
            if camera_on:
                try_request(url, "trigger_event", "5")
                try_request(url, "trigger_event", "0")
                camera_on = False
            time.sleep(0.1)
            continue
        # # outlining cases to take action
        # if detection_data.speed > 0 and camera_on:
        #     server.trigger_event(5)
        #     server.trigger_event(0)
        #     camera_on = False
        #     continue
        danger_level = get_danger_level(detection_data.distance, detection_data.speed)
        #case 1: bike is moving, object detected
        # add bike speed if statement here
        # if speed > 2:
        #     if detection_data.speed < 0:
        #         if detection_data.distance < 25: #max 25m distance to trigger alerts
        #             try:
        #                 hazard = requests.get(url+"/has_hazard")
        #                 if hazard.code == 200 and hazard.text == "True":
        #                     try:
        #                         event = requests.get(url+"/trigger_event/"+str(danger_level))
        #                     except requests.RequestException as e:
        #                         print(e)
        #                     if not camera_on:
        #                         try:
        #                             event = requests.get(url+"/trigger_event/4")
        #                             camera_on = True
        #                         except requests.RequestException as e:
        #                             print(e)
        #                     continue
        #             except requests.RequestException as e:
        #                 print(e)
        #     elif detection_data.distance < 10:
        #         try:
        #             hazard = requests.get(url+"/has_hazard")
        #             if hazard.code == 200 and hazard.text == "True":
        #                 try:
        #                     event = requests.get(url+"/trigger_event/"+str(danger_level))
        #                 except requests.RequestException as e:
        #                     print(e)
        #                 if not camera_on:
        #                     try:
        #                         event = requests.get(url+"/trigger_event/4")
        #                         camera_on = True
        #                     except requests.RequestException as e:
        #                         print(e)
        #                 continue
        #         except requests.RequestException as e:
        #             print(e)
        # elif detection_data.speed < -20:
        #     try:
        #         hazard = requests.get(url+"/has_hazard")
        #         if hazard.code == 200 and hazard.text == "True":
        #             try:
        #                 event = requests.get(url+"/trigger_event/"+str(danger_level))
        #             except requests.RequestException as e:
        #                 print(e)
        #             if not camera_on:
        #                 try:
        #                     event = requests.get(url+"/trigger_event/4")
        #                     camera_on = True
        #                 except requests.RequestException as e:
        #                     print(e)
        #             continue
        #     except requests.RequestException as e:
        #         print(e)
        #else: if bike is not moving, hazard when speed < -20
        # no hazard condition, turn off lights and camera

        # TEST
        # mock_speed = server.get_mock()
        mock_speed = get_speed(url)
        if mock_speed != 0:
            if detection_data.speed >= 0 or detection_data.distance > 2:
                pass

            try:
                hazard = requests.get(url+"/has_hazard")
                if hazard.status_code != 200:
                    pass # error handling?
                if hazard.text == "False":
                    pass
                
                try_request(url, "trigger_event", str(danger_level))

                if danger_level > 1:
                    if not camera_on:
                        if try_request(url, "trigger_event", "4"):
                            camera_on = True
                    continue
            except requests.RequestException as e:
                print(e)
        else:
            if detection_data.distance >= 1:
                pass

            try:
                hazard = requests.get(url+"/has_hazard")
                if hazard.status_code != 200:
                    pass # error handling?
                if hazard.text == "False":
                    pass
                
                try_request(url, "trigger_event", str(danger_level))

                if danger_level > 1:
                    if not camera_on:
                        if try_request(url, "trigger_event", "4"):
                            camera_on = True
                    continue
            except requests.RequestException as e:
                print(e)

        if camera_on:
            try_request(url, "trigger_event", "5")
            try_request(url, "trigger_event", "0")
            camera_on = False
        time.sleep(2)

def get_speed(url):
    requests.get(url+"/request_speed")

    timeout = 5
    start_time = time.perf_counter()
    while (time.perf_counter()-start_time) < timeout:
        response = requests.get(url+"/get_speed")
        if response.text != "Speed Not Updated":
            return float(response.text)
        time.sleep(0.5)

    return None

# returns success
def try_request(url, endpoint, parameter = ""):
    try:
        event = requests.get(url+'/'+endpoint+'/'+parameter)
    except requests.RequestException as e:
        print(e)
        return False
    return True

def get_danger_level(distance, speed):
    hazard = distance**2 - speed**2
    
    if hazard < 300:
        return 2
    if hazard < 100:
        return 3
    return 1

if __name__ == "__main__":
    main()