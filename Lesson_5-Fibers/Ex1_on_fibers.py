# Exercise 1
# Instantiate and use a Fiber span.

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
          "con_in": 0.5, "att_in" : 0, "con_out": 0.5,
          "type_variety": "SSMF", "dispersion": 1.67e-5,
          "gamma": 0.00127}

data = {"uid": "fiber_id", "params": params}

# write json data into a file
with open("Fiber_Parameters.json", "w") as write_file:
    js.dump(data, write_file, indent=4)


# 3. Instantiate the fiber from the JSON file.
# Hint: use the kwargs to pass the dictionary to the constructor function.
# To pass a dictionary as kwargs to a function do as follows:

# read json data from a file
with open("Fiber_Parameters.json", "r") as read_file:
    data = js.load(read_file)

fiber = gnel.Fiber(**data)

# 4. instantiate a noiseless WDM comb according to the parameters described
# in eqpt.json file

# read json data from a file
with open("eqp.json", "r") as read_file:  # Exercise 2: ../eqp2.json"
    data = js.load(read_file)

# From the json data, extract only the values needed for the spectral info (SI)
si_data = data['SI'][0]

# Compute the WDM for the interested Spectral info
si = gn.create_input_spectral_information(si_data['f_min'], si_data['f_max'], si_data['roll_off'], si_data['baud_rate'],
                                          10**(si_data['power_dbm']/10)/1000, si_data['spacing'])

# 5. propagate the WDM comb through the Fiber.
# Hint: As Fiber has the method call (self, spectral info), an object Fiber
# can be used as function. So, the command fiber(spectral information) will
# return the spectral information propagated through the fiber.

ml.plot_signal(si)

new_si = fiber(si)

# 6. plot the signal before and after the propagation and the NLI noise power
# after the propagation

ml.plot_signal_NLI(new_si)

# 7. plot the signal-to-NLI noise ratio (the SNRNL) after the Fiber.

ml.plot_SNR_NLI(new_si)

plt.show()