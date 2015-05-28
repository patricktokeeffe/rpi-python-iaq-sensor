import Adafruit_BMP.BMP085 as BMP085
from time import sleep
from datetime import datetime

# Initialize the BMP180 pressure/temperature sensor.
#    ....Note that the Adafruit module works for both BMP085 and BMP180 sensors.
Psensor = BMP085.BMP085()

# Open a file with a name that contains the current date and time.
dt = datetime.now().strftime('%Y%m%d_%H%M')
f = open('/home/pi/work/projects/iaq/python/BMP180_' + dt + '.txt','w')

# Take sensor data until user interrupts using Ctrl-c.
try:
    while True:
#        print 'Sample taken at: ' + datetime.now().strftime('%H:%M:%S')
        t = datetime.now().strftime('%s')
        f.write(t + '  ' + '{0:0.1f}'.format(Psensor.read_temperature()) + '  ' + '{0:0.1f}'.format(Psensor.read_pressure()) + '\n')
#	print 'Temperature from BMP: ' + '{0:0.1f}*C'.format(Psensor.read_temperature()) + '  ' + 'Pressure from BMP: {0:0.1f} Pa'.format(Psensor.read_pressure())
        sleep(5)
except KeyboardInterrupt:
    f.close()


