#!/usr/bin/python
#
# Python script to sample indoor air quality in Brian Lamb's home.
#
# Written by Von P. Walden (Using info from Adafruit and CO2meter.com)
#            5 May 2015
#
######################################################################
# Setup for BMP180 pressure/temperature sensor
import Adafruit_BMP.BMP085 as BMP085
from time import sleep
from datetime import datetime
Psensor = BMP085.BMP085()
print "P/T sensor ready.\n"

#####################################################################
# Setup for K-30 CO2 Sensor
import serial
import time
ser = serial.Serial("/dev/ttyAMA0")
ser.baudrate=9600
print "Serial Connected! CO2 sensor ready."
ser.flushInput()
time.sleep(1)

####################################################################
# Open a file with a name that contains the current date and time.
dt = datetime.now().strftime('%Y%m%d_%H%M')
fn = 'jobson_' + dt + '.txt'
f = open(fn,'w')
f.close()

# Take sensor data until user interrupts using Ctrl-c.
try:
    while True:
        f = open(fn,'a')
        print 'Sample taken at: ' + datetime.now().strftime('%H:%M:%S')
        t = datetime.now().strftime('%s')
        # Sample P/T sensor.
        T = Psensor.read_temperature()
        P = Psensor.read_pressure() 
        # Sample co2 sensor.
        ser.write("\xFE\x44\x00\x08\x02\x9F\x25")
        time.sleep(.01)
        resp = ser.read(7)
        high = ord(resp[3])
        low = ord(resp[4])
        co2 = (high*256) + low

        f.write(t + '  ' + '{0:0.1f}'.format(T) + '  ' + '{0:0.1f}'.format(P) + '  ' + '{0:0.1f}'.format(co2) + '\n')
        print 'Temperature from BMP: ' + '{0:0.1f}*C'.format(T) + '  ' + 'Pressure from BMP: {0:0.1f} Pa'.format(P)+ '  ' + 'CO2: {0:0.1f} ppmv'.format(co2)
        f.close()
        sleep(30)
except KeyboardInterrupt:
    f.close()


