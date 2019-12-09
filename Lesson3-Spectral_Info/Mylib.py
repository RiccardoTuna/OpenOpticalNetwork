import json as js
import gnpy.core.info as gn
import matplotlib.pyplot as plt
import numpy as np

# Exercise 2
# Plot the spectral information

def plot_spectrum(si):

    freq = np.zeros(len(si.carriers))
    power = np.zeros(len(si.carriers))

    for i, ch_i in enumerate(si.carriers):
        freq[i] = ch_i.frequency/1e12
        power[i] = 10*(np.log10(ch_i.power.signal/0.001))

    plt.plot(freq, power, '.b', label='line 1', linewidth=2)
    plt.ylabel('Power [dBm]')
    plt.xlabel('frequency [THz]')
    plt.grid()
    plt.show()