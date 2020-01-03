# Exercise 3 - Non-Linear propagation

import json as js
import gnpy.core.info as gn
import matplotlib.pyplot as plt
import numpy as np
import Mylib as ml
import gnpy.core.elements as gnel
import utilities as ut

# 1. Modify the fiber json such as the gamma parameter is 0.00127.

# A. Instantiate the fiber from the JSON file.

# read json data from a file
with open("Fiber_Parameters.json", "r") as read_file:
    data = js.load(read_file)

data["params"]["gamma"] = 0.00127

# 2. Build a line system composed of 10 span (fiber - amplifier). The line has
# to be a vector of tuples, each containing a fiber and an amplifier with the
# new configurations.

# B. Instantiate the EDFA from the JSON file.
Edfa_par = ut.get_edfa_parameters("Amp_Parameters.json","/Users/Tuna/PycharmProjects/OpenOptical/Lesson_6/eqp.json") # Exercise 2: ../eqp2.json"

num_span = 10
line_system = [{}]*10
tupla_i = dict()

for i in range(0, num_span):
    tupla_i = {"fiber": gnel.Fiber(**data), "edfa": gnel.Edfa(**Edfa_par)}
    line_system[i] = tupla_i

# 3. Use the transiever object to evaluate the GSNR, the OSNR and the
# SNRNL of the sectral information after each span.

# Instantiate the spectral information.
# read json data from a file
with open("eqp.json", "r") as read_file:  # Exercise 2: ../eqp2.json"
    data = js.load(read_file)
# From the json data, extract only the values needed for the spectral info (SI)
si_data = data['SI'][0]
# Compute the WDM for the interested Spectral info
si = gn.create_input_spectral_information(si_data['f_min'], si_data['f_max'], si_data['roll_off'], si_data['baud_rate'], 10**(si_data['power_dbm']/10)/1000, si_data['spacing'])

# Propagate the spectral information through the all line elements, saving
# the output signal information to each span.

spectral_info_spans = [{}]*10

for i in range(0, len(line_system)):
    tupla_i = line_system[i]
    fiber_i = tupla_i["fiber"]
    edfa_i = tupla_i["edfa"]

    propagated_si = fiber_i(si)
    amplified_si = edfa_i(propagated_si)
    si = amplified_si
    spectral_info_spans[i] = si

# 3. Use the transiever object to evaluate the GSNR and the OSNR of the
# sectral information after each span.

# Transiever
# a. Import transceiver from gnpy.core.elements
Receiver = gnel
# b. instantiate it calling the constructor with the argument (uid=’receiver’).
Rx_signal = Receiver.Transceiver('receiver')

gsnr = np.zeros(10)
osnr_ASE = np.zeros(10)
osnr_NLI = np.zeros(10)

for j in range(0, len(line_system)):
    # c. receive the signals using the transceiver as a function which argument is
    # the spectral information
    Rx_signal._calc_snr(spectral_info_spans[j])

    gsnr[j] = Rx_signal.snr[45]
    osnr_ASE[j] = Rx_signal.osnr_ase[45]
    osnr_NLI[j] = Rx_signal.osnr_nli[45]

# 4. Plot the SNR, the OSNR and the SNRNL evolution through the line, span
# by span, for the channel 45.

plt.figure(1)
plt.plot(range(10), gsnr, '.r', range(10), osnr_ASE, '.g', range(10), osnr_NLI, '.b', label='line 1', linewidth=2)
plt.ylabel('OSNR')
plt.xlabel('Span number')
plt.legend(['GSNR', 'OSNR ASE', 'OSNR NLI'])
plt.title('GSNR, OSNR, SNR_NLI - each span')
plt.ylim((15, 40))
plt.grid()
plt.show()

# 5. Plot the GSNR and the OSNR for each channel at the end of the line

ml.plot_receiver(Rx_signal, si)
