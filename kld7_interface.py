from kld7 import KLD7

class Radar:

    def __init__(self):
        try:
            self._conn = KLD7("/dev/ttyS0")
        except Exception as e:
            print(f"An error occurred while initializing the KLD7 radar: {e}")
            raise


    def read(self):
        try:
            detection_data = self._conn.read_DDAT()
            print(detection_data)
            possible_targets = self._conn.read_PDAT()
            print(possible_targets)
            raw_adc_frame = self._conn.read_RADC()
            print(raw_adc_frame)
        except KLD7.KLD7Exception as e:
            print(f"KLD7 Exception: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def close_connection(self):
        self._conn.close()


def main():
    radar = Radar()
    # kld7_instance.read()
    radar.close_connection()

if __name__ == "__main__":
    main()