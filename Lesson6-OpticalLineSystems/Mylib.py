import json as js
import gnpy.core.info as gn
import matplotlib.pyplot as plt
import numpy as np

# Exercise 2
# Plot the spectral information

def plot_spectrum(si):

    freq = np.zeros(len(si.carriers))
    signal_power = np.zeros(len(si.carriers))
    ase_power = np.zeros(len(si.carriers))
    nli_power = np.zeros(len(si.carriers))

    for i, ch_i in enumerate(si.carriers):
        freq[i] = ch_i.frequency/1e12
        signal_power[i] = 10*(np.log10(ch_i.power.signal/0.001))
        if (ch_i.power.ase != 0):
            ase_power[i] = 10 * (np.log10(ch_i.power.ase / 0.001))
        if (ch_i.power.nli != 0):
            nli_power[i] = 10 * (np.log10(ch_i.power.nli / 0.001))

    plt.figure()
    plt.plot(freq, signal_power, '.b', freq, ase_power, '.r', freq, nli_power, '.g', label='line 1', linewidth=2)
    plt.ylabel('Power [dBm]')
    plt.xlabel('frequency [THz]')
    plt.legend(['Signal power', 'ASE power', 'NLI power'])
    plt.title('Spectral info')
    plt.grid()
    plt.show()


def plot_receiver(receiver, si):

    freq = np.zeros(len(si.carriers))
    snr = receiver.snr
    osnr_ASE = receiver.osnr_ase
    osnr_NLI = receiver.osnr_nli

    for i, ch_i in enumerate(si.carriers):
        freq[i] = ch_i.frequency/1e12

    plt.figure()
    plt.plot(freq, snr, '*b', freq, osnr_ASE, '.r', freq, osnr_NLI, '.g', label='line 1', linewidth=2)
    plt.ylabel('OSNR [dB]')
    plt.xlabel('frequency [THz]')
    plt.legend(['SNR', 'OSNR ASE', 'OSNR NLI'])
    plt.title('Receiver')
    plt.grid()
    plt.show()


def plot_signal_ASE(si):
    freq = np.zeros(len(si.carriers))
    signal_power = np.zeros(len(si.carriers))
    ase_power = np.zeros(len(si.carriers))

    for i, ch_i in enumerate(si.carriers):
        freq[i] = ch_i.frequency/1e12
        signal_power[i] = 10*(np.log10(ch_i.power.signal/0.001))
        if (ch_i.power.ase != 0):
            ase_power[i] = 10 * (np.log10(ch_i.power.ase / 0.001))

    plt.figure()
    plt.plot(freq, signal_power, '.b', freq, ase_power, '.r', label='line 1', linewidth=2)
    plt.ylabel('Power [dBm]')
    plt.xlabel('frequency [THz]')
    plt.legend(['Signal power', 'ASE power'])
    plt.title('Spectral info')
    plt.grid()
    plt.show()

def plot_signal_NLI(si):
    freq = np.zeros(len(si.carriers))
    signal_power = np.zeros(len(si.carriers))
    nli_power = np.zeros(len(si.carriers))

    for i, ch_i in enumerate(si.carriers):
        freq[i] = ch_i.frequency/1e12
        signal_power[i] = 10*(np.log10(ch_i.power.signal/0.001))
        if (ch_i.power.nli != 0):
            nli_power[i] = 10 * (np.log10(ch_i.power.nli / 0.001))

    plt.figure()
    plt.plot(freq, signal_power, '.b', freq, nli_power, '.r', label='line 1', linewidth=2)
    plt.ylabel('Power [dBm]')
    plt.xlabel('frequency [THz]')
    plt.legend(['Signal power', 'ASE power'])
    plt.title('Spectral info')
    plt.grid()
    plt.show()

def plot_signal(si):

    freq = np.zeros(len(si.carriers))
    signal_power = np.zeros(len(si.carriers))

    for i, ch_i in enumerate(si.carriers):
        freq[i] = ch_i.frequency/1e12
        signal_power[i] = 10*(np.log10(ch_i.power.signal/0.001))

    plt.figure()
    plt.plot(freq, signal_power, '.b', label='line 1', linewidth=2)
    plt.ylabel('Power [dBm]')
    plt.xlabel('frequency [THz]')
    plt.legend(['Signal power'])
    plt.title('Spectral info')
    plt.grid()
    plt.show()

def plot_OSNR(si):

    freq = np.zeros(len(si.carriers))
    signal_power = np.zeros(len(si.carriers))
    ase_power = np.zeros(len(si.carriers))
    OSNR = np.zeros(len(si.carriers))

    for i, ch_i in enumerate(si.carriers):
        freq[i] = ch_i.frequency/1e12
        signal_power[i] = 10*(np.log10(ch_i.power.signal/0.001))
        if (ch_i.power.ase != 0):
            ase_power[i] = 10 * (np.log10(ch_i.power.ase / 0.001))
        OSNR[i] = signal_power[i] - ase_power[i]

    plt.figure()
    plt.plot(freq, OSNR, '.b', label='line 1', linewidth=2)
    plt.ylabel('Power [dBm]')
    plt.xlabel('frequency [THz]')
    plt.legend(['OSNR'])
    plt.title('Spectral info')
    plt.grid()
    plt.show()

def plot_SNR_NLI(si):

    freq = np.zeros(len(si.carriers))
    signal_power = np.zeros(len(si.carriers))
    nli_power = np.zeros(len(si.carriers))
    SNR_nli = np.zeros(len(si.carriers))

    for i, ch_i in enumerate(si.carriers):
        freq[i] = ch_i.frequency/1e12
        signal_power[i] = 10*(np.log10(ch_i.power.signal/0.001))
        if (ch_i.power.nli != 0):
            nli_power[i] = 10 * (np.log10(ch_i.power.nli / 0.001))
        SNR_nli[i] = signal_power[i] - nli_power[i]

    plt.figure()
    plt.plot(freq, SNR_nli, '.b', label='line 1', linewidth=2)
    plt.ylabel('Power [dBm]')
    plt.xlabel('frequency [THz]')
    plt.legend(['SNR_nli'])
    plt.title('Spectral info')
    plt.grid()
    plt.show()

