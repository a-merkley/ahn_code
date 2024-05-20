# Preprocess sleep data, look for sleep stages
import csv
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import scipy.signal as signal
import seeg_library as slib
import seeg_constants as CONST
import mne
import scaleogram as scg
import mpl_toolkits


# Get data
patient = "p1"
p_num = patient[1:]
root = "C:\\Users\\amand\\Documents\\Research\\Project_AHN\\Data_processing\\data\\meditation_sleep\\"
path = root + patient + "\\M" + p_num + "_Sleep.edf"

data = mne.io.read_raw_edf(path, preload=True)
channels = slib.create_channel_dict(data.ch_names)
print(channels)
print(data.info)

raw_data = data.get_data()

fs = 1024
abs_start = 600000
abs_finish = 700000
end_time = 20000
relative_start = abs_start / (60*fs)
relative_finish = abs_finish / (60*fs)
t = np.linspace(relative_start, relative_finish, abs_finish - abs_start)

# ACC
# ch1 = raw_data[channels["G'1"], :]
# ch2 = raw_data[channels["G'2"], :]
# ch3 = raw_data[channels["G'3"], :]

# # FIXME: TEST FILTERING
# ch_list = ["G1", "G2", "G3", "G4", "G5"]#, "I1", "A1", "B1", "C1", "U1", "F1"]
# for i, chname in enumerate(ch_list):
#     ch = slib.band_noise_filter(raw_data[channels[chname], :], lower=0.1, upper=80)
#     plt.psd(ch[abs_start:abs_finish], NFFT=2 * fs, Fs=fs, noverlap=fs, label=chname)
# plt.legend()
# plt.show()

cho = slib.band_noise_filter(raw_data[channels["G1"], :], lower=0.1, upper=200)
cho = mne.filter.filter_data(cho, fs, 0.5, 100)
plt.plot(t, cho[abs_start:abs_finish])
plt.title("Patient M1, electrode G1")
plt.xlabel("Time (s)")
plt.show()

ch1 = slib.band_noise_filter(ch1, lower=0.1, upper=80)
ch2 = slib.band_noise_filter(ch2, lower=0.1, upper=80)
f, Pxx_den = signal.welch(ch1, fs, nperseg=1024, noverlap=0)  # FIXME: ???
plt.semilogy(f, Pxx_den)
plt.show()
plt.psd(ch1[abs_start:abs_finish], NFFT=2*fs, Fs=fs, color='firebrick', noverlap=fs)
plt.psd(ch1[abs_start:abs_finish], NFFT=2*fs, Fs=fs, color='teal', noverlap=0)
# plt.psd(ch1[550000:600000], NFFT=2*fs, Fs=fs, color='orange')
# plt.psd(ch1[600000:650000], NFFT=2*fs, Fs=fs, color='teal')
# plt.psd(ch1[650000:700000], NFFT=2*fs, Fs=fs, color='purple')
plt.show()

# FIXME: TESTING
ch1 = slib.band_noise_filter(ch1, lower=0.1, upper=450)
scales = scg.periods2scales(np.arange(300, 600))
# fig, ax = plt.subplots(1, 1)
ax = scg.cws(ch1[abs_start:abs_finish], scales=scales)
plt.show()

plt.specgram(ch1, Fs=fs)
plt.show()

ch1 = mne.filter.filter_data(ch1, fs, 4, 20)
ch2 = mne.filter.filter_data(ch2, fs, 4, 20)
ch3 = mne.filter.filter_data(ch3, fs, 4, 20)
plt.plot(t, ch1[abs_start:abs_finish], label="Amygdala")
plt.plot(t, ch2[abs_start:abs_finish]+0.0004, label="ACC")
plt.plot(t, ch3[abs_start:abs_finish]-0.0004, label="Insula")
plt.title("Channel 1, 2, 3 in ACC")
plt.legend()
plt.xlabel("Time (minutes)")
plt.ylabel("Voltage (uV)")
plt.show()


# data.compute_psd(fmax=50).plot()
# plt.show()

print("Hi")

