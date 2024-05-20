# To open edfs and check out raw channels, triggers, etc
import numpy as np
from matplotlib import pyplot as plt
import mne
import seeg_library as slib
import seeg_constants as CONST
import pandas as pd
import scipy.signal as signal


# Constants for each patient and file save specification. FIXME: THE FOLLOWING ARE PARAMETERS YOU CAN CHANGE
patient = 'p7'
root = "C:\\Users\\amand\\Documents\\Research\\Project_AHN\\Data_processing\\data\\"

# Collect patient metadata
subject = CONST.Subject(patient)
e_map = subject.E_MAP

# Build file paths
edf_path = root + patient + "\\" + patient + ".edf"
csv_root = root + patient + "\\behavior\\" + patient + "_"

# Read in raw data
data = mne.io.read_raw_edf(edf_path, preload=True)
channels = slib.create_channel_dict(data.ch_names)
raw_data = data.get_data()

# Plot trigger channel
stim_chan = raw_data[channels["TRIG"]]
plt.plot(stim_chan)
plt.show()
