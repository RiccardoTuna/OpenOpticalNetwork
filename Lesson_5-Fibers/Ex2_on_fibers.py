# Exercise 2
# Fiber and Amplifier cascade
# 1. instantiate a fiber as described in the previous exercise and an EDFA with
# the parameters described in the exercise # 1 of the previous set but with
# an amplifier gain=17 dB.
# 4. plot the Signal power, NLI power and ASE power before and after each
# network element.
# 5. plot the GSNR, SNRNL and OSNR after the EDFA and after the Fiber.

import json as js
import gnpy.core.info as gn
import matplotlib.pyplot as plt
import numpy as np
import Mylib as ml
import gnpy.core.elements as gnel
import utilities as ut

# instantiate a fiber
params = { "length": 80, "loss_coef": 0.2, "length_units": "km", "att_in": 0,
          "con_in":0.5, "att_in" : 0, "con_in": 0.5, "con_out":0.5,
          "con_out":0.5, "type_variety" : "SSMF", "dispersion": 1.67e-5,
          "gamma": 0.00127 }
data = {"uid" : "fiber_id", "params" : params}
with open("Fiber_Parameters.json", "w") as write_file:
    js.dump(data, write_file, indent=4)
with open("Fiber_Parameters.json", "r") as read_file:
    data = js.load(read_file)
fiber = gnel.Fiber(**data)

# instantiate an EDFA
params = {"gain_target": 17, "tilt_target": 0, "out_voa": 0}  # Exercise 2: "gain_target": 17
data = {"uid" : "amp_id", "type" : "Edfa", "type_variety" : "simple edfa", "operational" : params}
with open("Amp_Parameters.json", "w") as write_file:
    js.dump(data, write_file, indent=4)
Edfa_par = ut.get_edfa_parameters("Amp_Parameters.json","/Users/Tuna/PycharmProjects/OpenOptical/Lesson4/eqp.json")
EDFA = gnel.Edfa(**Edfa_par)

# 2. instantiate the spectral information as well.

with open("eqp.json", "r") as read_file:
    data = js.load(read_file)
si_data = data['SI'][0]
si = gn.create_input_spectral_information(si_data['f_min'], si_data['f_max'], si_data['roll_off'], si_data['baud_rate'], 10**(si_data['power_dbm']/10)/1000, si_data['spacing'])

# 3. propagate the spectral information through the fiber and then through
# the EDFA.

# 4. plot the Signal power, NLI power and ASE power before and after each
# network element.

#ml.plot_signal(si) # signal power at the beginning

# Fiber propagation

si = fiber(si)
# 5. plot the GSNR, SNRNL and OSNR after the EDFA and after the Fiber.
# ml.plot_signal_NLI(si) # signal power after fiber propagation
# ml.plot_SNR_NLI(si)

#EDFA amplification

si = EDFA(si)
ml.plot_spectrum(si) # signal power after the amp

# Transponder (for point 5)
# a. Import transceiver from gnpy.core.elements
Receiver = gnel
# b. instantiate it calling the constructor with the argument (uid=’receiver’).
Rx_signal = Receiver.Transceiver('receiver')
Rx_signal._calc_snr(si)
ml.plot_receiver(Rx_signal, si)
# We see an snr almost equal to osnr_ase, due to the very small amount of nli noise power wrt ase