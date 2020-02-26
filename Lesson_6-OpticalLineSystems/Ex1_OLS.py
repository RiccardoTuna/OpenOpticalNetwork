# Exercise 1 - Find Gain for Transparent Mode

import json as js
import gnpy.core.info as gn
import matplotlib.pyplot as plt
import numpy as np
import Mylib as ml
import gnpy.core.elements as gnel
import utilities as ut

# 2. create a json file with the parameters of your Fiber. This json file has the
# following parameters:

params = {"length": 80, "loss_coef": 0.2, "length_units": "km",
           "att_in" : 0, "con_in": 0.5, "con_out": 0.5,
          "type_variety" : "SSMF", "dispersion": 1.67e-5,
          "gamma": 0.0}

data = {"uid": "fiber_id", "params" : params}

# write json data into a file
with open("Fiber_Parameters.json", "w") as write_file:
    js.dump(data, write_file, indent=4)


# 3. Instantiate the fiber from the JSON file.

# read json data from a file
with open("Fiber_Parameters.json", "r") as read_file:
    data = js.load(read_file)

fiber = gnel.Fiber(**data)

# 4. Instantiate the spectral information.

# read json data from a file
with open("eqp.json", "r") as read_file:
    data = js.load(read_file)
# From the json data, extract only the values needed for the spectral info (SI)
si_data = data['SI'][0]
# Compute the WDM for the interested Spectral info
si = gn.create_input_spectral_information(si_data['f_min'], si_data['f_max'], si_data['roll_off'], si_data['baud_rate'], 10**(si_data['power_dbm']/10)/1000, si_data['spacing'])

# 5. Propagate the WDM comb through the Fiber.
propagated_si = fiber(si)

# 6. Calculate the loss for the channel 45

channels = propagated_si.carriers

initial_power_dBm = -1

output_fiber_power_W = channels[45].power.signal

output_fiber_power_dBm = 10*np.log10(output_fiber_power_W/1e-3)

print('The output power after the fiber for the channel 45 (in dBm) is:', output_fiber_power_dBm)

# output power should be Ptx - L*att - con_in - con_out = -1 -80*0.2 -0.5 -0.5

loss = initial_power_dBm - output_fiber_power_dBm

print("The loss is: ", loss)


# 7. Instantiate the amplifier, as in Exercise 1.4 Lesson 4, in such a way it
# recovers the loss.

params = {"gain_target": loss, "tilt_target": 0, "out_voa": 0}

data = {"uid" : "amp_id", "type": "Edfa", "type_variety" : "simple edfa", "operational": params}

# write json data into a file
with open("Amp_Parameters.json", "w") as write_file:
    js.dump(data, write_file, indent=4)

Edfa_par = ut.get_edfa_parameters("Amp_Parameters.json",
                                  "/Users/Tuna/PycharmProjects/OpenOptical/Lesson_6-OpticalLineSystems/eqp.json")

EDFA = gnel.Edfa(**Edfa_par)

# propagate the WDM comb through the EDFA.

amplified_si = EDFA(propagated_si)

# 8. Plot the input and output signal power for each channel and verified the
# are the same.

ml.plot_signal(si)

ml.plot_signal(propagated_si)

ml.plot_signal(amplified_si)

plt.show()
