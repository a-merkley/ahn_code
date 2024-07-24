# Analyses of stroop task in time domain
import csv
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import scipy.signal as signal
import seeg_library as slib
import seeg_constants as CONST
from sklearn import model_selection, svm


# Constants
patient = 'p9'
event = "key"  # On what even to align stroop tasks. Choose "start" (trial start), "stim" (stimulus onset), or "key" (keypress)
alignment = "center"  # Choose "center" or "left"
width = 1000  # Trials will be this long
start_time = 0  # Start measuring width from this time

# Collect patient metadata
subject = CONST.Subject(patient)
region = subject.pcc
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

# from datetime import datetime, date
# stim_time = behavior_df['stim_time'].to_list()
# key_time = behavior_df['key_time'].to_list()
# diff_arr = []
# for i in range(len(stim_time)):
#     print(i)
#     try:
#         t1 = datetime.strptime(stim_time[i], "%H:%M:%S.%f")
#     except:
#         t1 = datetime.strptime(stim_time[i], "%H:%M:%S")
#     try:
#         t2 = datetime.strptime(key_time[i], "%H:%M:%S.%f")
#     except:
#         t2 = datetime.strptime(key_time[i], "%H:%M:%S")
#     tdiff = t2 - t1
#     diff_arr.append(tdiff.total_seconds())
# print(np.mean(diff_arr))
# plt.plot(diff_arr)
# plt.show()

###### ANALYSIS 1 ###### Trial averaging in time
# Average trials by congruency
congruency = behavior_df['congruent'].to_numpy()
color = behavior_df['color']
# c_idx = np.where(color.str.find('blue').to_numpy() == 0)[0]
# nc_idx = np.where(color.str.find('green').to_numpy() == 0)[0][:-1]
# ez_idx = np.where(color.str.find('red').to_numpy() == 0)[0]
c_idx = np.where(congruency == 1)[0][:-1]
nc_idx = np.where(congruency == 0)[0][:-1]  # FIXME, REMOVE THE :-1
c_trials = np.mean(trials[c_idx, :, start_time:width], axis=0)
nc_trials = np.mean(trials[nc_idx, :, start_time:width], axis=0)
# ez_trials = np.mean(trials[ez_idx, :, start_time:width], axis=0)

# Plot trials
c_stderr = np.std(trials[c_idx, :, start_time:width], axis=0) / np.sqrt(len(c_idx))
nc_stderr = np.std(trials[nc_idx, :, start_time:width], axis=0) / np.sqrt(len(nc_idx))
# ez_stderr = np.std(trials[ez_idx, :, start_time:width], axis=0) / np.sqrt(len(ez_idx))
t = np.arange(start_time, width)/1000 if alignment == "left" else np.arange(-int(width/2), int(width/2))/1000
for i, c in enumerate(region):
    plt.subplot(dim, dim, i+1)
    plt.errorbar(t, c_trials[channels[c]], yerr=c_stderr[channels[c]], label="congruent", ecolor='blue', fmt='k')
    plt.errorbar(t, nc_trials[channels[c]], yerr=nc_stderr[channels[c]], label="incongruent", ecolor='orange', fmt='k')
    # plt.errorbar(t, ez_trials[channels[c]], yerr=ez_stderr[channels[c]], label="red", ecolor='#8c1812', fmt='k')
    y_max = max(max(c_trials[channels[c]]), max(nc_trials[channels[c]]))
    y_min = min(min(c_trials[channels[c]]), min(nc_trials[channels[c]]))
    plt.plot([0, 0], [y_min, y_max], 'k--')
    # plt.plot(t, c_trials[channels[c]], label="congruent", color='k')
    # plt.plot(t, nc_trials[channels[c]], label="incongruent", color='b')
    if i == 4:
        plt.ylabel("Voltage (uV)")
    plt.title('Channel ' + str(i + 1))
    plt.xticks(fontsize=10, rotation=0)
    plt.yticks(fontsize=10, rotation=0)
    plt.xlabel("Time (s)")
    plt.legend(loc='upper right', fontsize='small')
plt.suptitle("Posterior cingulate cortex, centered around keypress")
plt.show()



###### ANALYSIS 2 ###### Classification into congruent or incongruent for each channel on probe
scores = []
trials_truncated = trials[:, channels[region[0]], 1200:1210]
# plt.plot(np.mean(trials_truncated[c_idx], axis=0))
# plt.plot(np.mean(trials_truncated[nc_idx], axis=0))
# plt.show()
x_train, x_test, y_train, y_test = model_selection.train_test_split(trials_truncated, congruency, test_size=0.2)

# Zscore
trial_mean = np.repeat(np.mean(x_train, axis=0), x_train.shape[0], axis=1)
trial_std = np.std(x_train, axis=0)

# Create classifier and cross validation
svm_clf = svm.SVC(kernel='rbf', C=1e-6)
cv = model_selection.RepeatedStratifiedKFold(n_splits=5, n_repeats=1)

# # Hyperparameter tuning
# param = dict()
# param['C'] = (1e-15, 100.0, 'log-uniform')
# search = sk.model_selection.GridSearchCV(svm_clf, param, cv=cv)
# search.fit(x_train, y_train)

# Cross validation
train_score = model_selection.cross_val_score(svm_clf, x_train, y_train, cv=cv)

# Test accuracy
svm_clf.fit(x_train, y_train)
test_score = svm_clf.score(x_test, y_test)
scores.append(test_score)
print(test_score)

plt.plot(scores)
plt.show()

print("Hi")
