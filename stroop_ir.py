# Application of IR to stroop dataset
import csv
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import scipy.signal as signal
import seeg_library as slib
import seeg_constants as CONST
from sklearn.model_selection import train_test_split
from datetime import datetime


# Constants for this (July 17) experiment
patient = 'p7'
event = "stim"  # On what even to align stroop tasks. Choose "start" (trial start), "stim" (stimulus onset), or "key" (keypress)
alignment = "left"  # Choose "center" or "left"
width = 1000  # Trials will be this long
start_time = 0  # Start measuring width from this time

# Collect patient metadata
subject = CONST.Subject(patient)
region = subject.fusiform
probes = len(region)
dim = int(np.ceil(np.sqrt(probes)))  # for nice subplotting

# Create file paths
csv_path = patient + "_behavior_" + alignment + str(width) + "_" + event + ".csv"
npy_path = patient + "_trials_" + alignment + str(width) + "_" + event + ".npy"
ch_path = patient + "_ch.csv"

# Read in data
behavior_df = pd.read_csv(csv_path)
with open(npy_path, 'rb') as f:
    trials = np.load(f)
channels_raw = next(csv.DictReader(open(ch_path)))
channels = {i: int(j) for i, j in channels_raw.items()}

f1 = "p7_trials_left1000_stim.npy"
f2 = "p7_trials_left1000_key.npy"
trials, behavior_df = slib.sham_augment(f1, f2, csv_path)


# # Time between stim and keypress
# delta = slib.time_btw_events(behavior_df['stim_time'], behavior_df['key_time'])
# for i in np.arange(0, 200, 40):
#     plt.plot([i, i], [0, 2.7], 'k')  # Mark the start of a new experiment
# plt.plot(delta)
# plt.show()

# Collect channel indices
ch_name = ["G-G'1", "G-G'2", "G-G'3", "G-G'4", "G-G'5"]
ch_name = ["F'1", "F'2", "F'3", "G-G'1", "G-G'2", "G-G'3"]
dims = len(ch_name)
ch_idx = [channels[ch_name[i]] for i in range(dims)]

# Get message and data matrix
M = slib.stroop_color2numeric(behavior_df['color'])  # behavior_df['congruent'].to_numpy()
A_total = trials[:, ch_idx, :]
num_trial = trials.shape[0]

# Split data into train and test
A_train, A_test, M_train, M_test = train_test_split(A_total, M, test_size=0.2)

# Iterative regression on each time point
bin_size = 1
corr_arr = np.zeros((dims, 1000))
for i, t in enumerate(np.arange(0, width, bin_size)):
    # Train the regression
    A = np.mean(A_train[:, :, t:t+bin_size], axis=2)
    # ir_vec = slib.elastic_ir(A.T, M_train, dims=dims, alpha=0.0, beta=0)
    ir_vec = slib.iterative_regression(A.T, M_train)

    # Test correlations
    for j in range(dims):
        A_test0 = np.mean(A_test[:, :, t:t+bin_size], axis=2)
        proj = A_test0 @ ir_vec[:, j]
        corr_arr[j, i] = np.corrcoef(M_test.T, proj)[0, 1]
    print(t)

for i in range(dims-1):
    plt.plot(corr_arr[i, :])
plt.plot([0, 1000/bin_size], [0, 0], 'k--')
plt.xlabel("Time since stimulus (ms)")
plt.show()

print("Pause")
