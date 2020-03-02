# Exercise 1
# Instantiate and use an EDFA.

import json as js
import gnpy.core.info as gn
import matplotlib.pyplot as plt
import numpy as np
import Mylib as ml
import gnpy.core.elements as gnel
import utilities as ut

# 2. create a json file with the parameters of your EDFA. This json file has the
# following parameters:


params = {"gain_target": 12, "tilt_target": 0, "out_voa": 0}

data = {"uid" : "amp_id", "type": "Edfa", "type_variety": "simple edfa", "operational": params}

# write json data into a file
with open("Amp_Parameters2.json", "w") as write_file:
    js.dump(data, write_file, indent=4)


# 4. instantiate an EDFA using the json file you just created.

Edfa_par = ut.get_edfa_parameters("Amp_Parameters2.json",
                                  "/Users/Tuna/PycharmProjects/OpenOptical/Lesson_4-Amplifiers/eqp2.json")

EDFA = gnel.Edfa(**Edfa_par)

#print(Edfa)

# 5. instantiate a noiseless WDM comb according to the parameters described
# in eqpt.json file

# read json data from a file
with open("eqp2.json", "r") as read_file:
    data = js.load(read_file)

# From the json data, extract only the values needed for the spectral info (SI)
si_data = data['SI'][0]


#Exercise 3
#Power sweep
# 1. instantiate the EDFA and the WDM comb described in exercise # 2.
# 2. propagate the WDM comb through the EDFA by varying the channel
# power before the EDFA by ± 2 dB with steps of 0.5 dB.

sweep_step = 0.5

central_channel_signal = np.zeros(9)
central_channel_ASE = np.zeros(9)
central_channel_OSNR = np.zeros(9)
sweep_dB = np.arange(-2, 2.5, 0.5)
print('The power levels (in dB) are:', sweep_dB)

# Transponder (for point 4)
# 1 Import transceiver from gnpy.core.elements
Receiver = gnel
# 2 instantiate it calling the constructor with the argument (uid=’receiver’).
Rx_signal = Receiver.Transceiver('receiver')

for j in range(0,9):

    # Compute the WDM for the interested Spectral info
    si = gn.create_input_spectral_information(si_data['f_min'], si_data['f_max'], si_data['roll_off'],
                                              si_data['baud_rate'], 10 ** ((si_data['power_dbm'] + sweep_dB[j]) / 10) / 1000,
                                              si_data['spacing'])

    new_si = EDFA(si)

    tmp = new_si.carriers[45]
    central_channel_signal[j] = 10*np.log10(tmp.power.signal/0.001)
    central_channel_ASE[j] = 10*np.log10(tmp.power.ase/0.001)

    # 3 receive the signals using the transceiver as a function which argument is
    # the spectral information
    Rx_signal._calc_snr(new_si)

    central_channel_OSNR[j] = Rx_signal.osnr_ase[45]

# 3. plot the signal power, ASE noise power of the central channel for each
# point of the sweep.

plt.figure()
plt.plot(sweep_dB,central_channel_signal, 'ob', sweep_dB, central_channel_ASE, 'or', label='line 1', linewidth=2)
plt.ylabel('Power [dBm]')
plt.xlabel('Sweep dB')
plt.legend(['Signal power', 'ASE noise'])
plt.title('Output of EDFA - power sweep at the input')
plt.grid()

# 4. plot the OSNR of the central channel for each point of the sweep.
# Hint: use a transponder.

plt.figure()
plt.plot(sweep_dB, central_channel_OSNR, 'ob', label='line 1', linewidth=2)
plt.ylabel('OSNR')
plt.xlabel('Sweep dB')
#plt.legend(['OSNR', 'ASE noise'])
plt.title('OSNR - power sweep at the input')
plt.grid()

plt.show()
