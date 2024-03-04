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

    def setup(self):
        self.radar.set_param("RSPI", 3) # Maximum speed. 0=12.5km/h, 1=25km/h, 2=50km/h, 3=100km/h
        self.radar.set_param("RRAI", 3) # Maximum range. 0=5m, 1=10m, 2=30m, 3=100m
        self.radar.set_param("TRFT", 0) # Tracking filter type. 0 = Standard, 1 = Fast detection, 2 = Long visibility
        # self.radar.set_param("VISU", ) # Vibration suppression. 0-16, 0=no suppression, 16=high suppression
    '''
        MIRA = _RadarParamDescriptor(
            7, "Min detection distance. 0–100% of range setting")
        MARA = _RadarParamDescriptor(
            8, "Max detection distance. 0–100% of range setting")
        MIAN = _RadarParamDescriptor(
            9, "Min detection angle. -90° to +90°")
        MAAN = _RadarParamDescriptor(
            10, "Max detection angle. -90° to +90°")
        MISP = _RadarParamDescriptor(
            11, "Min detection speed. 0–100% of speed setting")
        MASP = _RadarParamDescriptor(
            12, "Max detection speed. 0–100% of speed setting")
        DEDI = _RadarParamDescriptor(
            13, "Detection direction. 0 = Approaching, 1 = Receding, 2 = Both")
            
        RATH = _RadarParamDescriptor(
            14, "Range threshold. 0–100% of range setting")
        ANTH = _RadarParamDescriptor(
            15, "Angle threshold. -90° to +90°")
        SPTH = _RadarParamDescriptor(
            16, "Speed threshold. 0–100% of speed setting")

        HOLD = _RadarParamDescriptor(
            20, "Hold time. 1-7200 seconds")

        MIDE = _RadarParamDescriptor(
            21, "Micro detection re-trigger. 0 = Off, 1 = Re-trigger")
        MIDS = _RadarParamDescriptor(
            22, "Micro detection sensitivity. 0-9. 0=Min. sensitivity, 9=Max. sensitivity.")
    '''
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

if __name__ == "__main__":
    main()