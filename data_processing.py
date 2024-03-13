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
import subprocess

def main():
    '''
    setup input sources
    '''
    result = subprocess.run(['hostname', '-I'], capture_output=True, text=True)
    url = "http://" + result.stdout.split()[0] + ":5001"
    print(url)
    radar = kld7_wrapper().radar
    camera_on = False
    test_mode = True

    while True:
        try:
            target_data = radar.read_TDAT()
        except Exception as e:
            print(e)
            continue
        if target_data is None:
            print("no detection")
            if camera_on:
                try_request(url, "trigger_event", "5")
                try_request(url, "trigger_event", "0")
                camera_on = False
            time.sleep(0.1)
            continue

        print("detection")
        if hazard_check_required(target_data, url, test_mode):
            try:
                hazard = requests.get(url+"/has_hazard")
            except requests.RequestException as e:
                print(e)
                continue
            print(f"hazard text: {hazard.text}")
            
            if hazard.status_code == 200 and hazard.text == "True":
                try:
                    danger_level = get_danger_level(target_data.distance, target_data.speed, test_mode)
                except Exception as e:
                    print(e)
                    continue
                try_request(url, "trigger_event", str(danger_level))

                if danger_level > 0:
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
        time.sleep(0.1)

def hazard_check_required(target_data: Target, url, test = False):   
    # mock_speed = server.get_mock()
    bike_speed = get_speed(url)
    if bike_speed is None: # TODO: potentially add error handling? for now skip on timeout
        return False
    
    if test:
        return hazard_check_close(target_data, bike_speed)
    return hazard_check_far(target_data, bike_speed)

def hazard_check_close(target_data: Target, bike_speed): 
    if bike_speed == 0:
        if target_data.distance < 5:
            return True
    else:
        if target_data.speed < 0 or target_data.distance < 10:
            return True
        
    return False

def hazard_check_far(target_data: Target, bike_speed):
    return True # TODO: tune
    # outlining cases to take action
    if target_data.speed > 0:
        return False
    
    # case 1: bike is moving
    if bike_speed > 2:
        # max 25m distance to trigger alerts
        if target_data.distance < 30: 
            return True
    # case 2: if bike is not moving, hazard when speed < -20
    elif target_data.speed < -20:
        return True
    
    return False

    # # outlining cases to take action
    # if target_data.speed > 0:
    #     return False
    
    # # case 1: bike is moving
    # if bike_speed > 2:
    #     # max 25m distance to trigger alerts
    #     if target_data.speed < 0:
    #         if target_data.distance < 25: 
    #             return True
    #     elif target_data.distance < 10: # TODO: This case is never reached?
    #         return True
    # # case 2: if bike is not moving, hazard when speed < -20
    # elif target_d1ata.speed < -20:
    #     return True
    
    # return False

def get_speed(url):
    requests.get(url+"/request_speed")

    timeout = 2
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

def get_danger_level(target_distance, target_speed, test = False):
    if test:
        if target_distance < 2:
            return 3
        if target_distance < 3:
            return 2
        if target_distance < 4:
            return 1
        return 0
    else:
        return 2 # TODO: tune
        hazard = target_distance**2 - target_speed**2
        
        if hazard < 300:
            return 2
        if hazard < 100:
            return 3
        return 1

if __name__ == "__main__":
    main()