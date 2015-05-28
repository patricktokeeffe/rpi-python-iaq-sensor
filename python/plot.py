#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

fn = 'jobson_20150512_1805'

data = np.loadtxt(fn+'.txt')

# Extract time
t = np.array([])
for d in data[:,0]:
    t = np.append(t, datetime.fromtimestamp(d))

T   = data[:,1]
p   = data[:,2]/100.
co2 = data[:,3]

plt.figure()
plt.subplot(311)
plt.plot(t,T)
plt.ylabel('Temp (C)')
plt.title('LAR room 302, Pullman, WA on ' + t[0].strftime('%d %b %Y'))
plt.subplot(312)
plt.plot(t,p)
plt.ylabel('Pressure (mb)')
plt.subplot(313)
plt.plot(t,co2)
plt.xlabel('Time (UTC)')
plt.ylabel('CO2 (ppmv)')

plt.savefig(fn+'.png')


