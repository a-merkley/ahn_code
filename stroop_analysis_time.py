# Analyses of stroop task in time domain
import csv
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seeg_library as slib
import seeg_constants as CONST


# Constants
patient = 'p9'
event = "key"  # On what even to align stroop tasks. Choose "start" (trial start), "stim" (stimulus onset), or "key" (keypress)
alignment = "center"  # Choose "center" or "left"
width = 1000  # Trials will be this long (in ms)
start_time = 0  # Start measuring width from this time

# Collect patient metadata
subject = CONST.Subject(patient)
region = subject.entorhinal
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


# Average trials by congruency
congruency = behavior_df['congruent'].to_numpy()
color = behavior_df['color']

# Choose stimuli by congruency binary label
c_idx = np.where(congruency == 1)[0]
nc_idx = np.where(congruency == 0)[0]
# # Choose stimuli by word color
# c_idx = np.where(color.str.find('blue').to_numpy() == 0)[0]
# nc_idx = np.where(color.str.find('green').to_numpy() == 0)[0]

c_trials = np.mean(trials[c_idx[:-1], :, start_time:width], axis=0)
nc_trials = np.mean(trials[nc_idx[:-1], :, start_time:width], axis=0)

# Plot trials
c_stderr = np.std(trials[c_idx, :, start_time:width], axis=0) / np.sqrt(len(c_idx))
nc_stderr = np.std(trials[nc_idx, :, start_time:width], axis=0) / np.sqrt(len(nc_idx))
t = np.arange(start_time, width)/1000 if alignment == "left" else np.arange(-int(width/2), int(width/2))/1000
for i, c in enumerate(region):
    plt.subplot(dim, dim, i+1)
    plt.errorbar(t, c_trials[channels[c]], yerr=c_stderr[channels[c]], label="congruent", ecolor='blue', fmt='k')
    plt.errorbar(t, nc_trials[channels[c]], yerr=nc_stderr[channels[c]], label="incongruent", ecolor='orange', fmt='k')
    y_max = max(max(c_trials[channels[c]]), max(nc_trials[channels[c]]))
    y_min = min(min(c_trials[channels[c]]), min(nc_trials[channels[c]]))
    plt.plot([0, 0], [y_min, y_max], 'k--')

    # Plot labeling
    if i == 4:
        plt.ylabel("Voltage (uV)")
    plt.title('Channel ' + str(i + 1))
    plt.xticks(fontsize=10, rotation=0)
    plt.yticks(fontsize=10, rotation=0)
    plt.xlabel("Time (s)")
    plt.legend(loc='upper right', fontsize='small')

plt.suptitle("Posterior cingulate cortex, centered on keypress, congruency")  # FIXME: NEEDS TO BE MANUALLY CHANGED
plt.show()

