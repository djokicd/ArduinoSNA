#!/usr/bin/python3

__author__ = "Danilo Dokic"
__email__ = "djokicd@outlook.com"
__license__ = "GPLv3+"

from pylab import plt, np
import vxi11
import serial
import time

class INetworkAnalyzerE5062:
    """
        Network Analyzer E5062 interface class
    """
    powSyntax = "SOUR1:POW"
    attSyntax = "SOUR1:POW:ATT"
    freqSyntax = "SENS1:FREQ:CENT"
    currentAttenuation = None

    def __init__(self, address):
        self.ip = address
        print("Defined NA at ", self.ip)

    def setSafetyParams(self, delay = 0.1, Pmax = 5, Pmin = -45):
        self.commandDelay = delay
        self.Pmin = Pmin
        self.Pmax = Pmax

    def powerInBounds(self, P):
        if ( P >= self.Pmin and P <= self.Pmax):
            return True
        else:
            return False

    def connect(self):
        #self.NA = vxi11.Instrument( self.ip )
        print("Testing connection to NA...")
        #print( self.NA.ask("*IDN?") )

    def calculateAttenuation(self, P):  # P - power [dBm]
        if (P > 5 or P < -45):
            raise ValueError('Power out of range!')
        if (-45 <= P and P < -30):
            return 40
        elif(-35 <= P and P < -20):
            return 30
        elif(-25 <= P and P < -10):
            return 20
        elif(-15 <= P and P < 0):
            return 10
        elif (-5 <= P and P < 10):
            return 0

    def setAttenuator(self, P):
        Px = self.calculateAttenuation(P)

        if (Px != self.currentAttenuation):
            self.currentAttenuation = Px
            self.command(self.attSyntax + " " + str(Px))

    def setPower(self, P):
        self.setAttenuator(P)
        if (self.powerInBounds(P)):
            self.command(self.powSyntax + " " + str(P))
        else:
            print('Power out of range!')
        return

    def setFrequency(self, F):
        if ( F >= 3e5 and F <= 3e9  ):
            self.command(self.freqSyntax + " " + str(F))
        else:
            print("Frequency out of range!")
        return

    def command(self, command="*IDN?"):
        print ("To NA: " + command)
        #self.NA.write(command)
        time.sleep(self.commandDelay)
        return

class IArduino:

    def __init__ (self, dev, baudRate, timeout):
        self.dev = dev
        self.baud = baudRate
        self.timeout = timeout
        print("Defined Arduino at ", self.dev,
              ", using baud rate ", self.baud,
              ", with timeout ", self.timeout)

    def connect(self):
        #self.ser = serial.Serial(dev, baudRate, timeout)

        print("Waiting for bootloader and clearing buffer")
        time.sleep(2.00)

        #while(self.ser.inWaiting()):
        #   self.ser.readline()
        self.command("SAMPLE")
        self.read()


    def setSafetyDelay(self, delay = 0.1):
        self.commandDelay = delay

    def command(self, command):  # giving out command to Arduino
        print ("To Arduino: " + command)
        #self.ser.write( command + "\n")
        #self.ser.flush()
        time.sleep(self.commandDelay)
        return

    def read(self):
        print("Reading arduino...")
        V = 0
        #while(self.ser.inWaiting()):
        #    V = self.ser.readline()

        V = float(V)
        print("From Arduino: " + str(V))
        return V
