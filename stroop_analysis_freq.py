# Analyses of stroop task in frequency domain
import csv
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import scipy.signal as signal
import seeg_library as slib
import seeg_constants as CONST


# Constants for this (July 17) experiment
event = 2  # On what even to align stroop tasks. 1: trial start, 2: stim appear, 3: button press
width = 1000  # Trials will be this long
band = CONST.delta
samp_freq = CONST.fs
patient = "p2"

# Collect patient metadata
subject = CONST.Subject(patient)
region = subject.amcc
probes = len(region)
dim = int(np.ceil(np.sqrt(probes)))

# Read in data
behavior_df = pd.read_csv('p3_behavior_left1000_key.csv')
with open('p3_trials_left1000_key.npy', 'rb') as f:
    trials = np.load(f)
channels_raw = next(csv.DictReader(open("p3_ch.csv")))
channels = {i: int(j) for i, j in channels_raw.items()}

# Collect trials by congruency
congruency = behavior_df['congruent'].to_numpy()
c_idx = np.where(congruency == 1)[0]
nc_idx = np.where(congruency == 0)[0]
c_trials = trials[c_idx, :, :width]
nc_trials = trials[nc_idx, :, :width]

# Pick a signal
amcc_chan = channels[region[0]]
x_raw = np.mean(c_trials[:, amcc_chan, :], axis=0)

# Bandpass filter
b_low, a_low = signal.butter(N=4, Wn=(band[0], band[1]), btype='bandpass', fs=samp_freq)
x = signal.filtfilt(b_low, a_low, x_raw)

# Get PSD (periodogram)
psd_tuple = signal.periodogram(x, fs=samp_freq, window='boxcar')
x_axis = psd_tuple[0]
psd = psd_tuple[1]
plt.plot(psd)
plt.show()

# Convolve with Morlet wavelet
morlet = signal.morlet(50)
x_wavelet = abs(signal.convolve(morlet, x))
plt.plot(x_wavelet)
plt.show()

print("brkpt")
