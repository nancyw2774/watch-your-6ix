import serial
import time

SERIAL_PORT = '/dev/ttyAMA0'
BAUD_RATE = 115200
TIMEOUT = 1

REQUEST_COMMAND = b'GET_DATA\r\n'

def main():
    try:
        ser = serial.Serial(SERIAL_PORT, baudrate=BAUD_RATE, timeout=TIMEOUT)
        print(f"Serial port {SERIAL_PORT} set up succesfully")

        ser.write(REQUEST_COMMAND)
        response = ser.readline()
        print("Response received from KLD7 radar:", response)

        ser.close()
        print("Serial port closed successfully")
    except serial.SerialException as e:
        print(f"Serial exception: {e}")
    except Exception as e:
        print(f"Exception as {e}")

if __name__ == "__main__":
    main()