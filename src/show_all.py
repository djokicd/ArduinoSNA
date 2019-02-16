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
import sys, os

ARD = IArduino(dev = '/dev/ttyUSB0', baudRate = 9600, timeout = 2.00)
ARD.setSafetyDelay(0.1)
ARD.connect()

while(1==1):
        ARD.command("SAMPLE0"); V1 = ARD.read();
        ARD.command("SAMPLE1"); V2 = ARD.read();
        ARD.command("SAMPLE2"); V3 = ARD.read();

        sys.stdout = sys.__stdout__
        print("Measurements: ", V1, "\t", V2, "\t", V3, "\t")
        sys.stdout = open(os.devnull, 'w')
