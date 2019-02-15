#!/usr/bin/python3

from pylab import *
import sys
fn = sys.argv[1]

npzfile = np.load(fn)

F = npzfile['F']
P = npzfile['P']
V_mtx = npzfile['V']
S11_mtx = npzfile['S11']

fig, ax = plt.subplots()
c = ax.pcolormesh(F/1e9, P, V_mtx, cmap='RdBu' )
ax.set_title('Sensor voltage [V]')
plt.xlabel("Frequency [GHz]")
plt.ylabel("Power [dBm]")
fig.colorbar(c, ax=ax)

fig, ax = plt.subplots()
c = ax.pcolormesh(F/1e9, P, S11_mtx, cmap='RdBu' )
ax.set_title('S11 [dB]')
plt.xlabel("Frequency [GHz]")
plt.ylabel("Power [dBm]")
fig.colorbar(c, ax=ax)

plt.show()
