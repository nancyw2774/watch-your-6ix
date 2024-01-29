#Simple script to read out raw FFT and ADC data from RFbeam K-LD7
#
#**************************************************************************
# RFbeam Microwave GmbH
#**************************************************************************
#
# Author:   RFbeam Microwave GmbH
# Date:     20.09.2019
# Python Version: 3.7.4
#
# Notes:    Enter the corresponding COM Port and make sure all modules
#           are installed before executing
#
#--------------------------------------------------------------------------
# Rev 1.0   | 15.10.2019    | - Initial version                     |  FN
#**************************************************************************

import time
import serial
import matplotlib.pyplot as plt
import numpy as np

COM_Port = 'COM5'

# create serial object with corresponding COM Port and open it 
com_obj=serial.Serial(COM_Port)
com_obj.baudrate=115200
com_obj.parity=serial.PARITY_EVEN
com_obj.stopbits=serial.STOPBITS_ONE
com_obj.bytesize=serial.EIGHTBITS

# connect to sensor and set baudrate 
payloadlength = (4).to_bytes(4, byteorder='little')
value = (3).to_bytes(4, byteorder='little')
header = bytes("INIT", 'utf-8')
cmd_init = header+payloadlength+value
com_obj.write(cmd_init)

# get response
response_init = com_obj.read(9)
if response_init[8] != 0:
    print('Error during initialisation for K-LD7')

# delay 75ms
time.sleep(0.075)

# change to higher baudrate
com_obj.baudrate = 2E6

# change max speed to 25km/h
value = (1).to_bytes(4, byteorder='little')
header = bytes("RSPI", 'utf-8')
cmd_frame = header+payloadlength+value
com_obj.write(cmd_frame)

# get response
response_init = com_obj.read(9)
if response_init[8] != 0:
    print('Error: Command not acknowledged')

# change max range to 10m
value = (1).to_bytes(4, byteorder='little')
header = bytes("RRAI", 'utf-8')
cmd_frame = header+payloadlength+value
com_obj.write(cmd_frame)

# get response
response_init = com_obj.read(9)
if response_init[8] != 0:
    print('Error: Command not acknowledged')

# create figure
fig = plt.figure(figsize=(10,5))
plt.ion()
plt.show()

x = list(range(256))

# readout and plot time and frequency data continuously
for ctr in range(100):

    # request next frame data
    payload = (3).to_bytes(4, byteorder='little')
    header = bytes("GNFD", 'utf-8')
    cmd_frame = header+payloadlength+payload
    com_obj.write(cmd_frame)
    
    # get acknowledge
    resp_frame = com_obj.read(9)
    if resp_frame[8] != 0:
        print('Error: Command not acknowledged')

    # get data
    for i in range(2):
        # get message header
        resp_frame = com_obj.read(8)
        
        # get ADC or FFT data
        if (resp_frame[0:4]) == b'RADC':
                # read ADC data 
                ADC_A1_I = np.frombuffer(com_obj.read(512), dtype=np.uint16)
                ADC_A1_Q = np.frombuffer(com_obj.read(512), dtype=np.uint16)
                ADC_A2_I = np.frombuffer(com_obj.read(512), dtype=np.uint16)
                ADC_A2_Q = np.frombuffer(com_obj.read(512), dtype=np.uint16)
                ADC_B1_I = np.frombuffer(com_obj.read(512), dtype=np.uint16)
                ADC_B1_Q = np.frombuffer(com_obj.read(512), dtype=np.uint16)
        if (resp_frame[0:4]) == b'RFFT':
                # read FFT data
                fft_data = np.frombuffer(com_obj.read(512), dtype=np.uint16)
                threshold = np.frombuffer(com_obj.read(512), dtype=np.uint16)
        
    # clear figure
    plt.clf()
    
    # create ADC plot
    sub1 = fig.add_subplot(121)
    sub1.plot(x,ADC_A1_I,x,ADC_A1_Q,x,ADC_A2_I,x,ADC_A2_Q,x,ADC_B1_I,x,ADC_B1_Q)
    sub1.legend({'I1 A','Q1 A','I2 A','Q2 A','I1 B','Q1 B'},loc='upper right')
    sub1.grid(True)
    sub1.axis([0, 255, 0, 65536])
    plt.title('ADC Data')
    plt.xlabel('ADC sample number') 
    plt.ylabel('ADC bit value') 
   
    # create FFT plot 
    sub2 = fig.add_subplot(122)
    speed = np.linspace(-25,25,len(fft_data))
    sub2.plot(speed,np.fft.fftshift(fft_data)/100,speed,np.fft.fftshift(threshold)/100,'-')
    sub2.grid(True)
    sub2.axis([-25, 25, 0,100])
    plt.title('FFT Data')
    plt.xlabel('Speed [km/h]') 
    plt.ylabel('Signal amplitude [dB]') 
    sub2.legend({'FFT','Threshold'})
    
    fig.canvas.draw()
    fig.canvas.flush_events()
    
# disconnect from sensor 
payloadlength = (0).to_bytes(4, byteorder='little')
header = bytes("GBYE", 'utf-8')
cmd_frame = header+payloadlength
com_obj.write(cmd_frame)

# get response
response_gbye = com_obj.read(9)
if response_gbye[8] != 0:
    print('Error during disconnecting with K-LD7')

# close connection to COM port 
com_obj.close()
