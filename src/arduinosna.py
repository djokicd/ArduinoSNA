#!/usr/bin/python3

__author__ = "Danilo Dokic"
__email__ = "djokicd@outlook.com"
__license__ = "GPLv3+"

from pylab import plt, np
from scipy import interpolate
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
    spanSyntax = "SENS1:FREQ:SPAN"
    currentAttenuation = None
    currentSpan = None

    S11 = None

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

    def ask(self, command):
        return( self.NA.ask(command) )

    def connect(self):
        self.NA = vxi11.Instrument( self.ip )
        print("Testing connection to NA...")
        print(self.ask("*IDN?"))
        self.command("CALC1:PAR1:DEF S11")
        self.command("CALC1:FORM MLOG")

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
        if (self.currentSpan is None):
            self.currentSpan = 0
            self.command(self.spanSyntax + " 0")

        if ( F >= 3e5 and F <= 3e9  ):
            self.command(self.freqSyntax + " " + str(F))
        else:
            print("Frequency out of range!")
        return

    def getS11(self):
         self.S11 = str( self.ask("CALC1:DATA:FDAT?") )
         self.S11 = float(self.S11.split(",")[0])
         return self.S11

    def command(self, command="*IDN?"):
        print ("To NA: " + command)
        self.NA.write(command)
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

    def __del__(self):
        self.ser.close()
        print("Closed Arduino connection.")

    def connect(self):
        self.ser = serial.Serial(self.dev, self.baud, timeout = self.timeout)

        print("Waiting for bootloader and clearing buffer")

        time.sleep(2.00)
        self.command("INIT")
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

        self.command("SAMPLE0")
        self.read()

        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()


    def setSafetyDelay(self, delay = 0.1):
        self.commandDelay = delay

    def command(self, command):  # giving out command to Arduino
        print ("To Arduino: " + command)
        self.ser.write( str.encode(command + "\n") )
        self.ser.flush()
        time.sleep(self.commandDelay)
        return

    def read(self):
        print("Reading arduino...")
        V = 0

        while(self.ser.inWaiting()):
            V = self.ser.readline()

        self.ser.reset_input_buffer();

        V = float(V)
        print("From Arduino: " + str(V))
        return V

class Sensor:
    """
    Sensor behaviour is defined using
    .npz file
    """
    def __init__(self, filename):
        print(filename)
        d = np.load(filename)
        self.data = d
        self.Fmin = d["F"].min()
        self.Fmax = d["F"].max()
        self.Pmin = d["P"].min()
        self.Pmax = d["P"].max()
        print("Sensor params defined for:",
              self.Fmin/1e9, " < f[GHz] < ", self.Fmax/1e9, "; ",
              self.Pmin, " < P[dBm] < ", self.Pmax, ".")

    def estimatePower(self, f0, plot = False):
        """
        Estimate sensor characterisic using
        linear interpolation for given frequency
        - returns: FUNCTION V = V(P)
        """
        freq_values = self.data["F"][0]
        pow_values = np.transpose(self.data["P"])[0]
        print(pow_values)

        n = 0
        fractj = 0.00

        if (f0 < self.Fmin):
            n = 0
        elif(f0 > self.Fmax):
            n = -1
        else:
            freq_idxs = np.arange(0, len(freq_values))
            value_to_index = interpolate.interp1d(freq_values, freq_idxs, kind='linear')
            j = value_to_index(f0)
            fractj = j-int(j)
            n = int(j)
        print(n)
        if (fractj == 0.00):
            V = np.transpose(self.data["V"])[n]
        else:
            V = np.transpose(self.data["V"])[n] * (1-fractj) + np.transpose(self.data["V"])[n+1] * (fractj)

        if (plot == True):
            plt.figure()
            plt.plot(V, pow_values)
            plt.xlabel("Voltage [V]")
            plt.ylabel("Power [dBm]")
            plt.show()

        estimator = interpolate.interp1d(V, pow_values, fill_value="extrapolate")
        return estimator

    def measure(self, freqs, V):
        """
        Return power-freqs vector from voltage-freqs
        vector
        """
        P = np.zeros(np.shape(V))
        j = 0
        for f in freqs:
            print(f)
            estP = self.estimatePower(f)
            P[j] = estP(V[j])
            j += 1

        return freqs, P
