#!/usr/bin/python3

from pylab import *
from scipy import interpolate
from arduinosna import *

d = np.load("Filtar_Characteristics_2.npz")
f = d["f"]
V0 = d["V0"]
V1 = d["V1"]
V2 = d["V2"]

R_sens = Sensor("data/sens1_char.npz")
E_sens = Sensor("data/sens2_char.npz")
T_sens = Sensor("data/sens3_char.npz")

_, PR = R_sens.measure(f, V0)
_, PE = E_sens.measure(f, V2)
_, PT = T_sens.measure(f, V1)

plt,figure(1)
plt.plot(f/1e9, PR)
plt.plot(f/1e9, PE)
plt.plot(f/1e9, PT)
legend(["R", "E", "T"])
plt.xlabel("Frequency [GHz]")
plt.ylabel("Power [dBm]")
plt.grid()

S21 = PE-PT-20

## Extract refference value
ref_data = np.genfromtxt('../S21.CSV', delimiter=',', skip_header=3)
print(ref_data[:][0]/1e9)

plt.figure(2)
plt.plot(f/1e9, S21)
plt.plot(ref_data[:,0]/1e9, ref_data[:,1])
plt.xlabel("Frequency [GHz]")
plt.ylabel("S21 [dB]")
plt.title("Comparison of measurements")
plt.grid()
legend(["ArduinoSNA", "Agilent E5062"])

plt.show()
