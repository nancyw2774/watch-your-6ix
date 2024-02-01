from kld7 import KLD7
import time
import serial
import matplotlib.pyplot as plt
import numpy as np

#TODO: cite RFBEAM

class Radar:

    def __init__(self):
        COM_Port = '/dev/ttyAMA0'

        # create serial object with corresponding COM Port and open it 
        self.com_obj=serial.Serial(COM_Port)
        self.com_obj.baudrate=115200
        self.com_obj.parity=serial.PARITY_EVEN
        self.com_obj.stopbits=serial.STOPBITS_ONE
        self.com_obj.bytesize=serial.EIGHTBITS

        # connect to sensor and set baudrate 
        payloadlength = (4).to_bytes(4, byteorder='little')
        value = (3).to_bytes(4, byteorder='little')
        header = bytes("INIT", 'utf-8')
        cmd_init = header+payloadlength+value
        self.com_obj.write(cmd_init)

        # get response
        response_init = self.com_obj.read(9)
        if response_init[8] != 0:
            print('Error during initialisation for K-LD7')
        else:
            print('K-LD7 initialized')


    def read(self):
        pass

    def close(self):# disconnect from sensor 
        payloadlength = (0).to_bytes(4, byteorder='little')
        header = bytes("GBYE", 'utf-8')
        cmd_frame = header+payloadlength
        self.com_obj.write(cmd_frame)

        # get response
        response_gbye = self.com_obj.read(9)
        if response_gbye[8] != 0:
            print('Error during disconnecting with K-LD7')

        # close connection to COM port 
        self.com_obj.close()


def main():
    radar = Radar()
    radar.read()
    # radar.close_connection()
    # radar._conn._port.close()

if __name__ == "__main__":
    main()