# Exercise 1 - Power Sweep

import json as js
import gnpy.core.info as gn
import matplotlib.pyplot as plt
import numpy as np
#import Mylib as ml
import gnpy.core.elements as gnel
import utilities as ut

# 2. create a json file with the parameters of your Fiber

params = {"length": 80, "loss_coef": 0.3, "length_units": "km",
          "con_in": 0, "att_in": 0, "con_out": 0,
          "type_variety": "SSMF", "dispersion": 1.67e-5,
          "gamma": 0.00127}

data = {"uid": "fiber_id", "params": params}

# write json data into a file
with open("Fiber_Parameters.json", "w") as write_file:
    js.dump(data, write_file, indent=4)

# 3. Instantiate the amplifier, as in Exercise 1.4 Lesson 4, in such a way it
# recovers the loss

loss = params["length"]*params["loss_coef"]

params = {"gain_target": loss, "tilt_target": 0, "out_voa": 0}  # Exercise 2: "gain_target": 17

data = {"uid": "amp_id", "type": "Edfa", "type_variety": "simple edfa", "operational": params}

# write json data into a file
with open("Amp_Parameters.json", "w") as write_file:
    js.dump(data, write_file, indent=4)

Edfa_par = ut.get_edfa_parameters("Amp_Parameters.json",
                                  "/Users/Tuna/PycharmProjects/OpenOptical/Lesson_7-Control_Plan/eqp.json")

EDFA = gnel.Edfa(**Edfa_par)

# 4. Instantiate the fiber from the JSON file.
with open("Fiber_Parameters.json", "r") as read_file:
    data = js.load(read_file)
fiber = gnel.Fiber(**data)

# 5. Build a line composed of 10 span (fiber - amplifier). The line has to
# be a vector of tuples, each containing a fiber and an amplifier with the
# configuration of Exercise 1.
num_span = 10
line_system = [{}]*10
tupla_i = dict()

for i in range(0, num_span):
    tupla_i = {"fiber":gnel.Fiber(**data), "edfa": gnel.Edfa(**Edfa_par)}
    line_system[i] = tupla_i

# 6. Instantiate the spectral information according to eqpt.json file
# read json data from a file
with open("eqp.json", "r") as read_file:  # Exercise 2: ../eqp2.json"
    data = js.load(read_file)
# From the json data, extract only the values needed for the spectral info (SI)
si_data = data['SI'][0]
# Compute the WDM for the interested Spectral info
si = gn.create_input_spectral_information(si_data['f_min'], si_data['f_max'], si_data['roll_off'], si_data['baud_rate'], 10**(si_data['power_dbm']/10)/1000, si_data['spacing'])

# 7. Perform a power sweep varying the power per channel of the spectral
#    information between -5 and +2 dBm with steps of 0.25 dBm.

sweep_dB = np.arange(-4, 4.25, 0.5)

# Transceiver
# a. Import transceiver from gnpy.core.elements
Receiver = gnel
# b. instantiate it calling the constructor with the argument (uid=’receiver’).
Rx_signal = Receiver.Transceiver('receiver')

gsnr = np.zeros(len(sweep_dB))
osnr_ASE = np.zeros(len(sweep_dB))
osnr_NLI = np.zeros(len(sweep_dB))

for j in range(0, len(sweep_dB)):
    # Compute the WDM for the interested Spectral info
    si = gn.create_input_spectral_information(si_data['f_min'], si_data['f_max'], si_data['roll_off'],
                                              si_data['baud_rate'], 10 ** ((si_data['power_dbm'] + sweep_dB[j]) / 10) / 1000,
                                              si_data['spacing'])

    for tupla_i in line_system:
        fiber_i = tupla_i["fiber"] # i-th span
        edfa_i = tupla_i["edfa"] # i-th amplifier
        propagated_si = fiber_i(si)
        amplified_si = edfa_i(propagated_si)
        si = amplified_si

    Rx_signal._calc_snr(si)

    gsnr[j] = Rx_signal.snr[45]
    osnr_ASE[j] = Rx_signal.osnr_ase[45]
    osnr_NLI[j] = Rx_signal.osnr_nli[45]



# 1. Compute the optimum transmitted power according to the LOGO algorithm.

f_min = 191.30e12
baud_rate = 34e9
f_max = 196.0e12

f_0 = (f_max+f_min)/2  # central frequency
B_opt = (f_max-f_min)/1e12  # optimum band [THz]

R_s = baud_rate/1e12  # Symbol rate [Tsymbol/sec]

Beta_2 = 1.67e-05  # fiber dispersion
Beta_2 = -20.875

h = 6.62607e-34  # Planck constant

spacing = 50e9/1e12  # delta f [THz]
K_s = spacing / R_s

loss_coef = 0.3
alpha = loss_coef / (20 * np.log10(np.e))  # alpha: [1/km]

L = 80  # length [Km]
L_eff = (1 - np.exp(-2 * alpha * L))/(2 * alpha)  # [Km]

gamma = 0.00127*1e3  # dispersion coeff [W/km]

N_ch = B_opt/spacing

n_NLI = (4/(27*np.pi)) * \
        np.log((np.power(np.pi, 2)/4) * (np.abs(Beta_2)*np.power(R_s, 2)/alpha) * np.power(N_ch, 2/K_s)) * \
        (1/(alpha*np.power(np.abs(Beta_2), 1))) * np.power(gamma, 2) * (1/np.power(R_s, 2))

B_ch = R_s*1e12
n_f_amp = 5.5  # noise figure
F_dB = n_f_amp
# F_dB = 10*np.log10(F_lin)
F_lin = 10**(F_dB/10)
A = (np.power(10, loss_coef*L/10)-1)

P_ase = h * f_0 * B_ch * F_lin * A

P_opt = np.power(P_ase/(2 * n_NLI), 1/3)
print('Optimum power (in W): ', P_opt)

P_opt_dBm = 10*np.log10(P_opt/1e-3)
print('Optimum power (in dBm): ', P_opt_dBm)

# Compute the WDM for the interested Spectral info
si = gn.create_input_spectral_information(si_data['f_min'], si_data['f_max'], si_data['roll_off'], si_data['baud_rate'],
                                          10**(P_opt_dBm/10)/1000, si_data['spacing'])

# Propagate along the line system system the SI with optimum power
for i in range(0, len(line_system)):
    tupla_i = line_system[i]
    fiber_i = tupla_i["fiber"]
    edfa_i = tupla_i["edfa"]

    propagated_si = fiber_i(si)
    amplified_si = edfa_i(propagated_si)
    si = amplified_si


Rx_signal._calc_snr(si)
gsnr_optimum = Rx_signal.snr[45]

# We have to pass from power sweep to actual power in dBm (starting power is -1dBm)
sweep_dB = sweep_dB-1

plt.figure(1)
plt.plot(sweep_dB, gsnr, '.r', sweep_dB, osnr_ASE, '.g', sweep_dB, osnr_NLI, '.b', P_opt_dBm, gsnr_optimum, '.k',
         label='line 1', linewidth=2)
plt.ylabel('SNR [dB]')
plt.xlabel('Power sweep')
plt.legend(['GSNR', 'OSNR ASE', 'OSNR NLI'])
plt.title('GSNR, OSNR, SNR_NLI - each span')
plt.ylim((min(gsnr.all(), osnr_ASE.all(), osnr_NLI.all()), 40))
plt.grid()
plt.show()
