#!/usr/bin/python3

__author__ = "Danilo Dokic"
__email__ = "djokicd@outlook.com"
__license__ = "GPLv3+"

# Automatic measurement of static characteristics of RF detector

from pylab import np, plt
from arduinosna import *

NA = INetworkAnalyzerE5062('192.168.1.3')
NA.setSafetyParams(delay = 0.2, Pmax = 5, Pmin = -45)
NA.connect()

ARD = IArduino(dev = '/dev/ttyUSB0', baudRate = 9600, timeout = 2.00)
ARD.setSafetyDelay(0.2)
ARD.connect()

# Input - power
power_vector = np.arange(-10, 5, 0.5)
power_vector = np.flip(power_vector)
print("Powers testing ", power_vector)

# Output - measurements
V_vector = np.zeros(np.size(power_vector))
j = 0

for P in power_vector:
    NA.setPower(P)
    ARD.command("SAMPLE0")
    V_vector[j] = ARD.read()
    j += 1

plt.plot(power_vector, V_vector, 'ro')
plt.title("Static characteristics of RF detector sensor")
plt.xlabel("Power [dBm]")
plt.ylabel("Measured voltage [V]")
plt.grid()
plt.show()

timestr = time.strftime("_at_%H:%M:%S")

np.savetxt("V_vs_P" + timestr + ".csv", np.column_stack((power_vector,
           V_vector)), header="P [dBm], V [V]")
