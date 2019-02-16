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
ARD.setSafetyDelay(0.1)
ARD.connect()

# Input - power
freq_v = np.arange( 900e6, 3e9, 10e6 )
print (freq_v)

# Output - measurements
V0_vector = np.zeros(np.size(freq_v))
V1_vector = np.zeros(np.size(freq_v))
V2_vector = np.zeros(np.size(freq_v))
S11_vector = np.zeros(np.size(freq_v))

j = 0

for f in freq_v:
    NA.setFrequency(f)
    ARD.command("SAMPLE0")
    V0_vector[j] = ARD.read()

    ARD.command("SAMPLE1")
    V1_vector[j] = ARD.read()

    ARD.command("SAMPLE2")
    V2_vector[j] = ARD.read()

    j+=1

plt.figure(1)
plt.plot(freq_v, V0_vector)
plt.plot(freq_v, V1_vector)
plt.plot(freq_v, V2_vector)
plt.title("Static characteristics of RF detector sensor")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Measured voltage [V]")
plt.grid()
plt.legend(['E', 'R', 'T'])

np.savez("Filtar_Characteristics_2.npz", f = freq_v, V0 = V0_vector, V1 = V1_vector, V2 = V2_vector)

plt.show()

#timestr = time.strftime("_at_%H:%M:%S")

#np.savetxt("V_s11_vs_P" + timestr + ".csv", np.column_stack((freq_v,
#           V_vector, S11_vector)), header="P [dBm], V [V]")
