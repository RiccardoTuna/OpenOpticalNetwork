# Exercise 2 - Linear propagation

import json as js
import gnpy.core.info as gn
import matplotlib.pyplot as plt
import numpy as np
import Mylib as ml
import gnpy.core.elements as gnel
import utilities as ut

# 2. 2. create a json file with the parameters of your Fiber. This json file has the
# following parameters:

# 1. Build a line system composed of 10 span (fiber - amplifier). The line has
# to be a vector of tuples, each containing a fiber and an amplifier with the
# configuration of Exercise 1.

# A. Instantiate the fiber from the JSON file.

# read json data from a file
with open("Fiber_Parameters.json", "r") as read_file:
    data = js.load(read_file)
#fiber = gnel.Fiber(**data)

# B. Instantiate the EDFA from the JSON file.
Edfa_par = ut.get_edfa_parameters("Amp_Parameters.json","/Users/Tuna/PycharmProjects/OpenOptical/Lesson_6/eqp.json") # Exercise 2: ../eqp2.json"
#EDFA = gnel.Edfa(**Edfa_par)

num_span = 10
line_system = [{}]*10
tupla_i = dict()

for i in range(0, num_span):
    tupla_i = {"fiber":gnel.Fiber(**data), "edfa": gnel.Edfa(**Edfa_par)}
    line_system[i] = tupla_i
    #line_system[i]

# Instantiate the spectral information.
# read json data from a file
with open("eqp.json", "r") as read_file:  # Exercise 2: ../eqp2.json"
    data = js.load(read_file)
# From the json data, extract only the values needed for the spectral info (SI)
si_data = data['SI'][0]
# Compute the WDM for the interested Spectral info
si = gn.create_input_spectral_information(si_data['f_min'], si_data['f_max'], si_data['roll_off'], si_data['baud_rate'], 10**(si_data['power_dbm']/10)/1000, si_data['spacing'])

# 2. Propagate the spectral information through the all line elements, saving
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

ml.plot_signal(spectral_info_spans[len(line_system)-1])

# 3. Use the transiever object to evaluate the GSNR and the OSNR of the
# sectral information after each span.

# Transiever
# a. Import transceiver from gnpy.core.elements
Receiver = gnel
# b. instantiate it calling the constructor with the argument (uid=’receiver’).
Rx_signal = Receiver.Transceiver('receiver')

central_channel_signal = np.zeros(9)
central_channel_ASE = np.zeros(9)
central_channel_OSNR = np.zeros(9)

for j in range(0, len(line_system)-1):
    # c. receive the signals using the transceiver as a function which argument is
    # the spectral information
    Rx_signal._calc_snr(spectral_info_spans[j])
    print(Rx_signal.osnr_ase[45])
    central_channel_OSNR[j] = Rx_signal.osnr_ase[45]

plt.figure()
plt.plot(range(9), central_channel_OSNR, '.b', label='line 1', linewidth=2)
plt.ylabel('OSNR')
plt.xlabel('Span number')
# plt.legend(['OSNR', 'ASE noise'])
plt.title('OSNR - each span')
plt.grid()
plt.show()