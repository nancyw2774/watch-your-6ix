# Simple script to read out raw target data from RFbeam K-LD7
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
import math

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

# readout and plot PDAT data continuously
for ctr in range(100):
    
    # request next frame data
    PDAT = (4).to_bytes(4, byteorder='little')
    header = bytes("GNFD", 'utf-8')
    cmd_frame = header+payloadlength+PDAT
    com_obj.write(cmd_frame)

    # get acknowledge
    resp_frame = com_obj.read(9)
    if resp_frame[8] != 0:
        print('Error: Command not acknowledged')
    
    # get header 
    resp_frame = com_obj.read(4)
    
    # get payload len
    resp_len = com_obj.read(4)
    
    # initialize arrays
    distances_x = np.zeros(100)
    distances_y = np.zeros(100)
    speeds = np.zeros(100)
    distances = np.zeros(100)
    i = 0
    
    length = resp_len[0]
    
    # get data, until payloadlen is zero
    while length > 0:
        PDAT_Distance = np.frombuffer(com_obj.read(2), dtype=np.uint16)
        PDAT_Speed = np.frombuffer(com_obj.read(2), dtype=np.int16)/100
        PDAT_Angle = math.radians(np.frombuffer(com_obj.read(2), dtype=np.int16)/100)
        PDAT_Magnitude = np.frombuffer(com_obj.read(2), dtype=np.uint16)
        
        distances_x[i] = -(PDAT_Distance * math.sin(PDAT_Angle))
        distances_y[i] = PDAT_Distance * math.cos(PDAT_Angle)
        distances[i] = PDAT_Distance
        speeds[i] = PDAT_Speed
        
        i = i + 1
        
        # subtract stored datalen from payloadlen
        length = length - 8

   # clear figure
    plt.clf()
    
    # plot speed/distance
    sub1 = plt.subplot(121)
    for j in range(np.count_nonzero(distances)):
        point_Sub1, = sub1.plot(speeds[j],distances[j],marker='o',markersize=15,markerFaceColor='b',markerEdgeColor='k')
    
    plt.grid(True)
    plt.axis([-25, 25, 0, 1000])
    plt.title('Distance / Speed')
    plt.xlabel('Speed [km/h]')
    plt.ylabel('Distance [cm]')


    # plot distance/distance
    sub2 = plt.subplot(122)
    for y in range(np.count_nonzero(distances_x)):
        if speeds[y] > 0 :
            point_Sub2, = sub2.plot(distances_x[y], distances_y[y],marker='o',markersize=15,markerFaceColor='g',markerEdgeColor='k')
        else:
            point_Sub2, = sub2.plot(distances_x[y], distances_y[y],marker='o',markersize=15,markerFaceColor='r',markerEdgeColor='k')
       
    plt.grid(True)
    plt.axis([-500, 500, 0, 1000])
    plt.title('Distance / Distance \n (Green: Receding, Red: Approaching)')
    plt.xlabel('Distance [cm]')
    plt.ylabel('Distance [cm]')
    
    # draw no. of targets
    plt.text(0.8, 0.95,'No. of targets: ' + str(np.count_nonzero(distances)), horizontalalignment='center', verticalalignment='center', transform = sub2.transAxes)
    
    # draw figure
    fig.canvas.draw()
    fig.canvas.flush_events()

    # reset arrays
    distances_x = np.zeros(100)
    distances_y = np.zeros(100)
    speeds = np.zeros(100)
    distances = np.zeros(100)
    i = 1   


# disconnect from sensor 
payloadlength = (0).to_bytes(4, byteorder='little')
header = bytes("GBYE", 'utf-8')
cmd_frame = header+payloadlength
com_obj.write(cmd_frame)

# get response
response_gbye = com_obj.read(9)
if response_gbye[8] != 0:
    print("Error during disconnecting with K-LD7")


# close connection to COM port 
com_obj.close()
