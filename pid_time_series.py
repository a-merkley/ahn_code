import seeg_constants as CONST
import numpy as np
import pandas as pd
import csv
import sys
from matplotlib import pyplot as plt

print(sys.path)
sys.path.append("C:\\Users\\amand\\Documents\\Research\\Software\\IDTxl")


from idtxl.bivariate_pid import BivariatePID
from idtxl.data import Data


# Constants for this (July 17) experiment
patient = 'p3'
event = "stim"  # On what even to align stroop tasks. Choose "start" (trial start), "stim" (stimulus onset), or "key" (keypress)
alignment = "center"  # Choose "center" or "left"
width = 2000  # Trials will be this long
start_time = 0  # Start measuring width from this time

# Collect patient metadata
subject = CONST.Subject(patient)
region = subject.amcc
region2 = subject.insula_l
probes = len(region)
dim = int(np.ceil(np.sqrt(probes)))

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

###### ANALYSIS 1 ###### Trial averaging in time
# Average trials by congruency
congruency = behavior_df['congruent'].to_numpy()
c_idx = np.where(congruency == 1)[0]
nc_idx = np.where(congruency == 0)[0]
c_trials = np.mean(trials[c_idx, :, start_time:width], axis=0)
nc_trials = np.mean(trials[nc_idx, :, start_time:width], axis=0)


num_pts = 500
unq_s1_arr = np.zeros(num_pts)
red_arr = np.zeros(num_pts)
syn_arr = np.zeros(num_pts)
for t in range(num_pts):
    data_x = 1000*trials[:, channels[region[0]], t]
    data_x = data_x.astype(int)
    data_y = 1000*trials[:, channels[region2[0]], t]
    data_y = data_y.astype(int)
    data = Data(np.vstack((congruency, data_x, data_y)), 'ps', normalise=False)


    # Initialize PID estimator
    pid = BivariatePID()
    alph = 2
    settings_tartu = {'pid_estimator': 'TartuPID', 'lags_pid': [0, 0]}
    settings_sydney = {
        'alph_s1': alph,
        'alph_s2': alph,
        'alph_t': alph,
        'max_unsuc_swaps_row_parm': 60,
        'num_reps': 63,
        'max_iters': 1000,
        'pid_estimator': 'SydneyPID',
        'lags_pid': [0, 0]}

    results_tartu = pid.analyse_single_target(
        settings=settings_tartu, data=data, target=2, sources=[0, 1])

    unq_s1_arr[t] = results_tartu.get_single_target(2)['unq_s1']
    red_arr[t] = results_tartu.get_single_target(2)['shd_s1_s2']
    syn_arr[t] = results_tartu.get_single_target(2)['syn_s1_s2']
    # print(results_tartu.get_single_target(2)['unq_s2'])
    # print(results_tartu.get_single_target(2)['shd_s1_s2'])
    # print(results_tartu.get_single_target(2)['syn_s1_s2'])

plt.plot(unq_s1_arr, label="Unique in aMCC (vs insula)")
plt.plot(red_arr, label="Redundancy")
plt.plot(syn_arr, label="Synergy")
plt.legend()
plt.show()
