import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

data = np.loadtxt('blamb_20150506_2241.txt')

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
plt.title('Brian Lamb House, Pullman, WA on ' + t[0].strftime('%d %b %Y'))
plt.subplot(312)
plt.plot(t,p)
plt.ylabel('Pressure (mb)')
plt.subplot(313)
plt.plot(t,co2)
plt.xlabel('Time (UTC)')
plt.ylabel('CO2 (ppmv)')


