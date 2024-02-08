#Simple script to read out tracked target from RFbeam K-LD7
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

# plot speed/distance
sub1 = fig.add_subplot(121)
point_sub1, = sub1.plot(0,0,'o',markersize=15,markerFaceColor='b',markerEdgeColor='k')
plt.grid(True)
plt.axis([-25, 25, 0, 1000])
plt.title('Distance / Speed')
plt.xlabel('Speed [km/h]')
plt.ylabel('Distance [cm]')

# plot distance/distance
sub2 = fig.add_subplot(122)
point_sub2, = sub2.plot(0,0,'o',markersize=15,markerFaceColor='b',markerEdgeColor='k')
plt.grid(True)
plt.axis([-500, 500, 0, 1000])
plt.title('Distance / Distance \n (Green: Receding, Red: Approaching)')
plt.xlabel('Distance [cm]')
plt.ylabel('Distance [cm]')

# readout and plot TDAT data continuously
for ctr in range(100):

    # request next frame data
    TDAT = (8).to_bytes(4, byteorder='little')
    header = bytes("GNFD", 'utf-8')
    cmd_frame = header+payloadlength+TDAT
    com_obj.write(cmd_frame)
    
    # get acknowledge
    resp_frame = com_obj.read(9)
    if resp_frame[8] != 0:
        print('Error: Command not acknowledged')
    
    # get data 
    resp_frame = com_obj.read(8)

    # check if target detected by checking payloadlength and then get data
    target_detected = 0
    if resp_frame[4] > 1:
        target_detected = 1
        TDAT_Distance = np.frombuffer(com_obj.read(2), dtype=np.uint16)
        TDAT_Speed = np.frombuffer(com_obj.read(2), dtype=np.int16)/100
        TDAT_Angle =  math.radians(np.frombuffer(com_obj.read(2), dtype=np.int16)/100)
        TDAT_Magnitude = np.frombuffer(com_obj.read(2), dtype=np.uint16)
        
        distance_x = -(TDAT_Distance * math.sin(TDAT_Angle))
        distance_y = TDAT_Distance * math.cos(TDAT_Angle)
    
    if target_detected:
        # set new coordinates
        point_sub1.set_xdata(TDAT_Speed)
        point_sub1.set_ydata(TDAT_Distance)
        
        point_sub2.set_xdata(distance_x)
        point_sub2.set_ydata(distance_y)
        
        if TDAT_Speed > 0 :
            point_sub2.set_markerfacecolor('g')
        else:
            point_sub2.set_markerfacecolor('r')  
        
        # draw figures
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
