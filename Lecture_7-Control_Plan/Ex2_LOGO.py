# Exercise 2 - LOGO

import json as js
import gnpy.core.info as gn
import matplotlib.pyplot as plt
import numpy as np
#import Mylib as ml
import gnpy.core.elements as gnel
import utilities as ut

# 1. Compute the optimum transmitted power according to the LOGO algorithm.

f_min = 191.30e12
baud_rate = 34e9
f_max = 196.0e12

f_0 = (f_max+f_min)/2  # central frequency
B_opt = f_max-f_min

n_f_amp = 5.5

R_s = baud_rate

Beta_2 = 1.67e-05  # fiber dispersion

h = 6.626e-34  # Planck constant

spacing = 50e9  # delta f
K_s = spacing / R_s

loss_coef = 0.2

alpha = loss_coef / (20 * np.log10(np.e))
L = 80
L_eff = (1 - np.exp(-2 * alpha * L))/(2 * alpha)

gamma = 0.00127

n_NLI = (16/(27*np.pi)) * \
        np.log((np.power(np.pi, 2)/2) * (np.abs(Beta_2)*np.power(R_s, 2)/alpha) * np.power(B_opt/(K_s*R_s), 2/K_s)) * \
        (alpha/np.abs(Beta_2)) * np.power(gamma, 2) * (np.power(L_eff, 2)/np.power(R_s, 2))

B_ch = R_s
P_base = h*f_0*B_ch
F = n_f_amp*2

P_opt = np.power((F*L*P_base)/(2*n_NLI), 1/3)

P_opt_dBm = 10*np.log10(P_opt/1e-3)

print(P_opt_dBm)


# 2. Propagate the spectral information through the line of the previous exercise using the optimum transmitted power.

# 3. Plot the obtained GSNR at the end of the line for the middle channel in
# the spame plot of exercise 1 (plot a single point using a marker).