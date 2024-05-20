# For p5 and p6, which had malfunctioning Natus triggers, reconstruct triggers from Matlab timestamps
# NOTE: currently only valid to run for patient p5 and beyond (previous system latency too high)
import numpy as np
import pandas as pd
import mne
from matplotlib import pyplot as plt
import scipy.signal as signal
import seeg_library as slib
import seeg_constants as CONST
from datetime import datetime


# Get neurophys data
patient = "p6"
subject = CONST.Subject(patient)
p_num = patient[1:]
root = "C:\\Users\\amand\\Documents\\Research\\Project_AHN\\Data_processing\\data\\"
path_edf = root + patient + "\\p" + p_num + ".edf"

data = mne.io.read_raw_edf(path_edf, preload=True)
channels = slib.create_channel_dict(data.ch_names)
raw_data = data.get_data()

# Get behavior data with timestamps, FIXME: START WITH STROOP 1
path_csv = root + patient + "\\behavior\\p" + p_num + "_stroop3.csv"
behavior = pd.read_csv(path_csv)
time_format = "%H:%M:%S.%f"
stim_time = behavior['stim_time'].to_numpy()
key_time = behavior['key_time'].to_numpy()

########################################### Iterate thru a bunch of ms
rec_start = '10:29:54'
window = 1000
for j in np.arange(0, 1000, 20):
    ms = str(round(j))
    if j < 100:
        start_ms = rec_start + ".0" + ms
    else:
        start_ms = rec_start + "." + ms
    start_time = datetime.strptime(start_ms, time_format)
    print(start_time)

    n_trials = len(stim_time)
    rec1 = np.zeros((n_trials, window))  # Get 1s worth of data
    rec2 = np.zeros((n_trials, window))  # Get 1s worth of data
    rec3 = np.zeros((n_trials, window))  # Get 1s worth of data
    for i in range(n_trials):
        diff_seconds = (datetime.strptime(stim_time[i], time_format) - start_time).total_seconds()
        timebin = round(CONST.fs * diff_seconds)
        rec1[i, :] = slib.band_noise_filter(raw_data[channels["F'1"], timebin:timebin+window])
        rec2[i, :] = slib.band_noise_filter(raw_data[channels["F'2"], timebin:timebin+window])
        rec3[i, :] = slib.band_noise_filter(raw_data[channels["F'3"], timebin:timebin+window])

    plt.plot(np.mean(rec1, axis=0))
    plt.plot(np.mean(rec2, axis=0))
    plt.plot(np.mean(rec3, axis=0))
    plt.plot([200, 200], [-2*10**(-5), 2*10**(-5)], 'k--')
    plt.plot([450, 450], [-2*10**(-5), 2*10**(-5)], 'k--')
    plt.title(start_ms)
    plt.show()

########################################### For a single time point
start_time = datetime.strptime(subject.recording_start, time_format)

# Align time stamps to recording start
raw_arr = []
window = 1500
n_trials = len(stim_time)
amcc1 = np.zeros((n_trials, window))  # Get 1s worth of data
amcc2 = np.zeros((n_trials, window))  # Get 1s worth of data
amcc3 = np.zeros((n_trials, window))  # Get 1s worth of data
for i in range(n_trials):
    diff_seconds = (datetime.strptime(stim_time[i], time_format) - start_time).total_seconds()
    timebin = round(CONST.fs * diff_seconds)
    amcc1[i, :] = slib.band_noise_filter(raw_data[channels["G-G'1"], timebin:timebin+window])
    amcc2[i, :] = slib.band_noise_filter(raw_data[channels["G-G'2"], timebin:timebin+window])
    amcc3[i, :] = slib.band_noise_filter(raw_data[channels["G-G'3"], timebin:timebin+window])
    # amcc1[i, :] = slib.band_noise_filter(raw_data[channels["F'1"], timebin:timebin+window])
    # amcc2[i, :] = slib.band_noise_filter(raw_data[channels["F'2"], timebin:timebin+window])
    # amcc3[i, :] = slib.band_noise_filter(raw_data[channels["F'3"], timebin:timebin+window])
    raw_arr.append(timebin)

plt.plot(np.mean(amcc1, axis=0))
plt.plot(np.mean(amcc2, axis=0))
plt.plot(np.mean(amcc3, axis=0))
plt.show()

print(raw_arr)
amcc = slib.band_noise_filter(raw_data[channels["G-G'1"], :480000])
plt.plot(amcc)
plt.stem(raw_arr, 10**(-4)*np.ones(len(raw_arr)), 'r')
plt.show()
