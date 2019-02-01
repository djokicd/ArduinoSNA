#!/usr/bin/python3

__author__ = "Danilo Dokic"
__email__ = "djokicd@outlook.com"
__license__ = "GPLv3+"

# Automatic measurement of static characteristics of RF detector

pow_syntax = "SOUR1:POW"    # Setting power [dBm]
att_syntax = "SOUR1:POW:ATT" # Attenuator range [10]

from pylab import *
import time # for delay

import vxi11    # GPIB   comm port lib
import serial  # Serial comm port lib
import visa

#NA = None
NA = vxi11.Instrument('192.168.1.3')

print( "Network analyzer: ", NA.ask('*IDN?') )

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = 2.00)

#   Power range per attenuator: ( From doc.)
#       --------------------------------
#       | Attenuator  |  Power Range    |
#       | -------------------------------
#       | 0 dB        |  -5 to 10 dBm   |
#       | 10 dB       |  -15 to 0 dBm   |
#       | 20 dB       |  -25 to -10 dBm |
#       | 30 dB       |  -35 to -20 dBm |
#       | 40 dB       |  -45 to -30 dBm |
#       ---------------------------------

def calculate_attenuation( P ): # P - power [dBm]
    if ( P > 5 or P < -45):
        raise ValueError('Power out of range!')
    if  ( -45 <= P and P < -30):
        return 40
    elif( -35 <= P and P < -20):
        return 30
    elif( -25 <= P and P < -10):
        return 20
    elif( -15 <= P and P < 0):
        return 10
    elif ( -5 <= P and P < 10):
        return 0

def command_Arduino( command ): # giving out command to Arduino
    print ("ARD_OUT: " + command)
    ser.write(b'SAMPLE\n')
    ser.flush()
    time.sleep(0.2)
    return

def read_Arduino():
    print("Reading...")
    V = 0
    while( ser.inWaiting() ): 
        V = ser.readline()

    V = float(V)
    print("V[ard] = " + str(V) )
    return V

def command_NA( command = "*idn?" ): # giving out command to Network analyzer
    print (" NA_OUT: " + command)
    NA.write(command)
    time.sleep(0.1)
    return 


def set_power_attenuator( P ):
    
    global current_power_attenuator

    Px = calculate_attenuation( P )
    
    # Check if setting power range is required
    if (Px != current_power_attenuator):
        current_power_attenuator = Px
        command_NA( att_syntax + " " + str(Px)  )

def set_power(P):
    if ( P > 5 or P < -45):
        raise ValueError('Power out of range!')
   
    command_NA( pow_syntax + " " + str(P) )



# Init with no initial power attenuation
current_power_attenuator = None
power_vector = np.arange(-10, 5, 0.5)
power_vector = flip(power_vector)
print(power_vector)

### MAIN CODE

V_vector = zeros(size(power_vector))
j = 0


time.sleep(2.00)

while( ser.inWaiting() ): 
    ser.readline()

command_Arduino("SAMPLE\n")
read_Arduino()

for P in power_vector:
    
    set_power_attenuator(P)
    set_power(P)

    time.sleep(0.100)

    command_Arduino("SAMPLE\n")
    Value = read_Arduino()
    
    V_vector[j] = Value
    j+=1

plt.plot(power_vector, V_vector, 'ro')
plt.title("Static characteristics of RF detector sensor")
plt.xlabel("Power [dBm]")
plt.ylabel("Measured voltage [V]")
plt.grid()
plt.show()

timestr = time.strftime("_at_%H:%M:%S")

savetxt("measure" + timestr + ".csv", column_stack((power_vector, V_vector)), header = "P [dBm], V [V]")
