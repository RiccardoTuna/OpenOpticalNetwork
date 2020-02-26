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

data = {"uid": "amp_id", "type": "Edfa", "type_variety" : "simple edfa", "operational" : params}

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

# Compute the WDM for the interested Spectral info
si = gn.create_input_spectral_information(si_data['f_min'], si_data['f_max'], si_data['roll_off'], si_data['baud_rate'], 10**(si_data['power_dbm']/10)/1000, si_data['spacing'])

# 6. propagate the WDM comb through the EDFA.
# Hint: As Edfa has the method call (self, spectral info), it can be used
# as function. So, the command edfa(spectral information) will return the
# spectral information propagated through the EDFA.

ml.plot_signal(si)

new_si = EDFA(si)

# 7. plot the signal and ASE noise power before and after the propagation.

ml.plot_signal_ASE(new_si)
#print(new_si)

# 8. plot the signal-to-ASE noise ration (the OSNR) after the EDFA.

ml.plot_OSNR(new_si)
plt.show()
