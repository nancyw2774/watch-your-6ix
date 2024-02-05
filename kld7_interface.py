import time
import serial
import matplotlib.pyplot as plt
import numpy as np
import math

# TODO raise error on failed ack
class Radar:

    def __init__(self):
        COM_Port = "/dev/ttyAMA0"

        # create serial object with corresponding COM Port and open it 
        self.com_obj=serial.Serial(COM_Port)
        self.com_obj.baudrate=115200
        self.com_obj.parity=serial.PARITY_EVEN
        self.com_obj.stopbits=serial.STOPBITS_ONE
        self.com_obj.bytesize=serial.EIGHTBITS

        # connect to sensor and set baudrate 
        self.payloadlength = (4).to_bytes(4, byteorder='little')
        value = (3).to_bytes(4, byteorder='little')
        header = bytes("INIT", 'utf-8')
        cmd_init = header+self.payloadlength+value
        self.com_obj.write(cmd_init)

        # get response
        response_init = self.com_obj.read(9)
        if response_init[8] != 0:
            print('Error during initialisation for K-LD7')

        # delay 75ms
        time.sleep(0.075)

        # change to higher baudrate
        self.com_obj.baudrate = 2E6

    def set_max_speed(self):

        # change max speed to 25km/h
        value = (1).to_bytes(4, byteorder='little')
        header = bytes("RSPI", 'utf-8')
        cmd_frame = header+self.payloadlength+value
        self.com_obj.write(cmd_frame)

        # get response
        response_init = self.com_obj.read(9)
        if response_init[8] != 0:
            print('Error: Command not acknowledged')

    def set_max_range(self):

        # change max range to 10m
        value = (1).to_bytes(4, byteorder='little')
        header = bytes("RRAI", 'utf-8')
        cmd_frame = header+self.payloadlength+value
        self.com_obj.write(cmd_frame)

        # get response
        response_init = self.com_obj.read(9)
        if response_init[8] != 0:
            print('Error: Command not acknowledged')

    def read(self):
        # readout PDAT data continuously
            
        # request next frame data
        PDAT = (4).to_bytes(4, byteorder='little')
        header = bytes("GNFD", 'utf-8')
        cmd_frame = header+self.payloadlength+PDAT
        self.com_obj.write(cmd_frame)

        # get acknowledge
        resp_frame = self.com_obj.read(9)
        if resp_frame[8] != 0:
            print('Error: Command not acknowledged')
        
        # get header 
        resp_frame = self.com_obj.read(4)
        
        # get payload len
        resp_len = self.com_obj.read(4)
        
        # initialize arrays
        distances_x = np.zeros(100)
        distances_y = np.zeros(100)
        speeds = np.zeros(100)
        distances = np.zeros(100)
        i = 0
        
        length = resp_len[0]
        
        # get data, until payloadlen is zero
        while length > 0:
            PDAT_Distance = np.frombuffer(self.com_obj.read(2), dtype=np.uint16)
            PDAT_Speed = np.frombuffer(self.com_obj.read(2), dtype=np.int16)/100
            PDAT_Angle = math.radians(np.frombuffer(self.com_obj.read(2), dtype=np.int16)/100)
            PDAT_Magnitude = np.frombuffer(self.com_obj.read(2), dtype=np.uint16)
            
            distances_x[i] = -(PDAT_Distance * math.sin(PDAT_Angle))
            distances_y[i] = PDAT_Distance * math.cos(PDAT_Angle)
            distances[i] = PDAT_Distance
            speeds[i] = PDAT_Speed
            
            i = i + 1
            
            # subtract stored datalen from payloadlen
            length = length - 8
            
        # reset arrays
        distances_x = np.zeros(100)
        distances_y = np.zeros(100)
        speeds = np.zeros(100)
        distances = np.zeros(100)
        i = 1   

    def close_connection(self):

        # disconnect from sensor 
        payloadlength = (0).to_bytes(4, byteorder='little')
        header = bytes("GBYE", 'utf-8')
        cmd_frame = header+payloadlength
        self.com_obj.write(cmd_frame)

        # get response
        response_gbye = self.com_obj.read(9)
        if response_gbye[8] != 0:
            print("Error during disconnecting with K-LD7")


        # close connection to COM port 
        self.com_obj.close()


def main():
    radar = Radar()
    # kld7_instance.read()
    radar.close_connection()

if __name__ == "__main__":
    main()