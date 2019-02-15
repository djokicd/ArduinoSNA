#!/usr/bin/python3

__author__ = "Danilo Dokic"
__email__ = "djokicd@outlook.com"
__license__ = "GPLv3+"

# Automatic measurement of static characteristics of RF detector

from pylab import np, plt
from arduinosna import *
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

NA = INetworkAnalyzerE5062('192.168.1.3')
NA.setSafetyParams(delay = 0.2, Pmax = 5, Pmin = -45)
NA.connect()

ARD = IArduino(dev = '/dev/ttyUSB0', baudRate = 9600, timeout = 2.00)
ARD.setSafetyDelay(0.1)
ARD.connect()

# Input - power
freq_v = np.arange( 1e9, 3e9, 0.025e9 )
power_v = np.arange( -45, -5, 2.5)

F, P = np.meshgrid(freq_v, power_v)
V_mtx = np.zeros(np.shape(F))
S11_mtx = np.zeros(np.shape(F))

for i in range(0, np.shape(F)[0]):
    for j in range(0, np.shape(F)[1]):

        print("### Progress : ", i, "/", np.shape(F)[0]-1, " : ", j, "/",
              np.shape(F)[1]-1 )

        NA.setPower( P[i][j] )
        NA.setFrequency( F[i][j] )
        ARD.command("SAMPLE0")
        V = ARD.read()
        S11 = NA.getS11();
        V_mtx[i][j] = V
        S11_mtx[i][j] = S11


timestr = time.strftime("_at_%H:%M:%S")

np.savez('Measurement_of_sensor' + timestr + '.npz', F=F, P=P, V=V_mtx, S11=S11_mtx)

print("Completed.")
