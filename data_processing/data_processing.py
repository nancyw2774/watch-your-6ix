'''
Architecture:

constant loop that monitors incoming data and determines whether a threat is detected
    - distance, speed, speed of cyclist

when a hazard condition is satisfied, call external function to call CV + send info to phone
'''
import time

def main():
    '''
    setup input sources
    '''
 

    while True:
        bike_speed = "BIKE SPEED"
        bike_dir = "BIKE DIR"
        radar = "PLACEHOLDER"
        imu = "PLACEHOLDER"
        # outlining cases to take action
        #case 1: bike is moving, object detected
        if bike_speed > 5:
            if radar < 25: #max 25m distance to trigger alerts
                time.sleep(0.1)
                temp = # sample new radar distance
                if abs(temp-radar) > 10:
                    continue #sample again, big change in reading implies an erroneous reading
                if temp - radar <= 0: #object distance non-increasing
                    if temp-radar < 15:
                        continue # object closing very fast, warn immediate while processing cv
                    continue
                    #call CV to verify object identity
        else:
            if radar < 25:
                time.sleep(0.1)
                temp = # sample new radar distance
                if abs(temp-radar) > 10:
                    continue #sample again, big change in reading implies an erroneous reading
                if temp - radar < 15: #object object is closing at fast, speed, call cv but warn immediately
                    continue
                    #call CV to verify object identity