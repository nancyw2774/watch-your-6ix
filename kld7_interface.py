from kld7 import KLD7, KLD7Exception
import time
import traceback

class kld7_class:

    def __init__(self):
        try:
            self.radar = KLD7("/dev/ttyAMA0", baudrate=115200)
        except Exception as e:
            print(f"An error occurred while initializing the KLD7 radar: {e}")


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

    # TODO: fix crashing on response from close command
    def close_connection(self):
        # disconnect from sensor 
        payloadlength = (0).to_bytes(4, byteorder='little')
        header = bytes("GBYE", 'utf-8')
        cmd_frame = header+payloadlength
        self.radar._port.write(cmd_frame)

        # get response
        try:
            response_gbye = self.radar._port.read(9)
        except Exception as e:
            print(f"got exception {e}")
        if response_gbye[8] != 0:
            print('Error during disconnecting with K-LD7')

        # close connection to COM port 
        self.radar._port.close()


def main():
    kld7_instance = kld7_class()
    start_time = time.perf_counter()
    try:
        while time.perf_counter() - start_time < 5:
            kld7_instance.read()
    except Exception as e:
        print(f"Got exception {e}")
    kld7_instance.close_connection()

if __name__ == "__main__":
    main()