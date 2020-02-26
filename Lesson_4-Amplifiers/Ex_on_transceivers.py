# Exercise 1
# Update the spectral information and update it.

import json as js
import gnpy.core.info as gn
import matplotlib.pyplot as plt
import numpy as np
import Mylib as ml
import gnpy.core.elements as gnel

# 1. Instantiate a spectral information with the parameters indicated in eqpt.json file

# read json data from a file
with open("eqp.json", "r") as read_file:
    data = js.load(read_file)

# From the json data, extract only the values needed for the spectral info (SI)
si_data = data['SI'][0]

# Compute the WDM for the interested Spectral info
si = gn.create_input_spectral_information(si_data['f_min'], si_data['f_max'], si_data['roll_off'], si_data['baud_rate'],
                                          10**(si_data['power_dbm']/10)/1000, si_data['spacing'])

# plot the channels
# ml.plot_spectrum(si)

# 2. Update the spectral information increasing the power of the signals by 3
# dB and adding an ASE noise power per channel equal to -40 dBm and a nli
# power equal to -43 dBm. To do it use the ‘._replace()‘ method of spectral
# information. You can find the documentation here: https://docs.python.org/3/library/collections.html

ASE_noise_dBm = -40  # dBm
nli_noise_dBm = -43  # dBm

# We have to convert from dB to linear scale (the class uses this representation)
ASE_noise_W = 10**(ASE_noise_dBm/10)/1000  # W
nli_noise_W = 10**(nli_noise_dBm/10)/1000  # W

# Update the powers level in the object (for the power we can just double it = add 3dB)
for i, ch_i in enumerate(si.carriers):
    updated_sign_pwr = ch_i.power.signal * 2
    temp = ch_i.power._replace(signal=updated_sign_pwr, nli=nli_noise_W, ase=ASE_noise_W)
    si.carriers[i] = ch_i._replace(power=temp)

# 3. Plot signal power, ASE noise power and NLI power in the same plot. [x
# axis: frequency (THz) and y axis: power (dBm)]

ml.plot_spectrum(si)

# Exercise 2
# Receive signals

# 1 Import transceiver from gnpy.core.elements
Receiver = gnel

# 2 instantiate it calling the constructor with the argument (uid=’receiver’)
Rx_signal = Receiver.Transceiver('receiver')

# 3 receive the signals using the transceiver as a function which argument is
# the spectral information
Rx_signal._calc_snr(si)

# 4 Now the transceiver has snr, osnr ase and osnr nli of the received signal. Plot
# them in the same graph.[x axis: frequency (THz) and y axis: (dB)]
ml.plot_receiver(Rx_signal, si)

plt.show()
