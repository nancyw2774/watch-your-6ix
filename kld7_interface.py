from kld7 import KLD7

class kld7_class:

    def __init__(self):
        try:
            self.radar = KLD7("/dev/ttyS0", baudrate=115200)
        except Exception as e:
            print(f"An error occurred while initializing the KLD7 radar: {e}")


    def read(self):
        try:
            detection_data = self.radar.read_DDAT()
            print(detection_data)
            possible_targets = self.radar.read_PDAT()
            print(possible_targets)
            raw_adc_frame = self.radar.read_RADC()
            print(raw_adc_frame)
        except KLD7.KLD7Exception as e:
            print(f"KLD7 Exception: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def close_connection(self):
        self.radar.close()


def main():
    kld7_instance = kld7_class()
    # kld7_instance.read()
    kld7_instance.close_connection()

if __name__ == "__main__":
    main()