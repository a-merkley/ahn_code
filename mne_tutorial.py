# Testbench for random codes and development
import numpy as np
import pandas as pd
import mne
from matplotlib import pyplot as plt
import scipy.signal as signal
import seeg_library as slib
import seeg_constants as CONST
from datetime import datetime


# Read in raw data
# path_edf = "C:\\Users\\amand\\Documents\\Research\\Project_AHN\\Data_processing\\data\\p9\\p9.edf"
path_edf = "C:\\Users\\amand\\Documents\\Research\\Project_AHN\\Data_processing\\data\\p10\\p10.edf"
data = mne.io.read_raw_edf(path_edf, preload=True)
channels = slib.create_channel_dict(data.ch_names)

raw_data = data.get_data()
trig_chan = raw_data[channels["TRIG"]]
# plt.plot([297818, 297818], [0, 205], 'k'); plt.plot([361180, 361180], [0, 205], 'k')
# plt.plot([373346, 373346], [0, 205], 'r'); plt.plot([567804, 567804], [0, 205], 'r')
# plt.plot([627466, 627466], [0, 205], 'g'); plt.plot([861936, 861936], [0, 205], 'g')
# plt.plot([927029, 927029], [0, 205], 'b'); plt.plot([1121641, 1121641], [0, 205], 'b')
# plt.plot([1178725, 1178725], [0, 205]); plt.plot([1384603, 1384603], [0, 205])
# plt.plot([1456986, 1456986], [0, 205]); plt.plot([1655915, 1655915], [0, 205])
# plt.plot([1704343, 1704343], [0, 205]); plt.plot([1740542, 1740542], [0, 205])
# plt.plot([1944372, 1944372], [0, 205]); plt.plot([2144180, 2144180], [0, 205])
plt.plot(trig_chan)
plt.show()

### COMPARING MATLAB TIMESTAMPS TO NATUS TRIGGERS IN P7 AND BEYOND
# Rough approximation of first stroop task in  p7
debut = 542000
fin = 647000
trigger = trig_chan[debut:fin]

# Align trigger channel at first pulse
diffr = np.diff(trigger)
first_pulse = np.where(diffr == 1)[0][0]  # stimulus onset
second_pulse = np.where(diffr == 1)[0][1]  # the actual keypress

# Read behavior file
behavior = pd.read_csv("C:\\Users\\amand\\Documents\\Research\\Project_AHN\\Data_processing\\data\\p7\\behavior\\p7_stroop3.csv")
keytime = behavior['key_time'].to_numpy()
time_format = "%H:%M:%S.%f"

second_pulse_t = 0.777  # FIXME: AUTOMATE
abs_time_arr = [second_pulse_t]
baseline = datetime.strptime(keytime[0], time_format)
for i in range(1, len(keytime)):
    abs_t = datetime.strptime(keytime[i], time_format)
    t_diff = (abs_t - baseline).total_seconds() + second_pulse_t
    abs_time_arr.append(t_diff)

trig_len = len(trigger[first_pulse:])
t = np.linspace(0, trig_len / 1024, trig_len)
print(abs_time_arr)

plt.plot(t, trigger[first_pulse:]-254)
plt.stem(abs_time_arr, np.ones(len(abs_time_arr)))
plt.show()


