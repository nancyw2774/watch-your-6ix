'''
Architecture:

constant loop that monitors incoming data and determines whether a threat is detected
    - distance, speed, speed of cyclist

when a hazard condition is satisfied, call external function to call CV + send info to phone
'''
import time
import time
import requests
from kld7_wrapper import kld7_wrapper
from kld7 import Target

def main():
    '''
    setup input sources
    '''
    url = "http://172.20.10.2:5001"
    radar = kld7_wrapper().radar
    camera_on = False

    while True:
        target_data = radar.read_TDAT()
        if target_data is None:
            if camera_on:
                try_request(url, "trigger_event", "5")
                try_request(url, "trigger_event", "0")
                camera_on = False
            time.sleep(0.1)
            continue

        if hazard_check_required(target_data, url):
            try:
                hazard = requests.get(url+"/has_hazard")
            except requests.RequestException as e:
                print(e)
                continue
            
            if hazard.status_code == 200 and hazard.text == "True":
                danger_level = get_danger_level(target_data.distance, target_data.speed)
                try_request(url, "trigger_event", str(danger_level))

                if danger_level > 1:
                    if not camera_on:
                        turned_on_camera = try_request(url, "trigger_event", "4")
                        if turned_on_camera:
                            camera_on = True
                    continue

        # no hazard condition, turn off lights and camera
        if camera_on:
            try_request(url, "trigger_event", "5")
            try_request(url, "trigger_event", "0")
            camera_on = False
        time.sleep(2)

def hazard_check_required(target_data: Target, url, close_range = False):   
    # mock_speed = server.get_mock()
    speed = get_speed(url)
    if speed is None: # TODO: potentially add error handling? for now skip on timeout
        return False
    
    if close_range:
        return hazard_check_close(target_data, url, speed)
    return hazard_check_far(target_data, url, speed)

def hazard_check_close(target_data: Target, speed): 
    if speed == 0:
        if target_data.distance < 1:
            return True
    else:
        if target_data.speed < 0 or target_data.distance < 2:
            return True
        
    return False

def hazard_check_far(target_data: Target, speed):
    # outlining cases to take action
    if target_data.speed > 0:
        return False
    
    # case 1: bike is moving
    if speed > 2:
        # max 25m distance to trigger alerts
        if target_data.speed < 0:
            if target_data.distance < 25: 
                return True
        elif target_data.distance < 10: # TODO: This case is never reached?
            return True
    # case 2: if bike is not moving, hazard when speed < -20
    elif target_data.speed < -20:
        return True
    
    return False

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
        requests.get(url+'/'+endpoint+'/'+parameter)
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