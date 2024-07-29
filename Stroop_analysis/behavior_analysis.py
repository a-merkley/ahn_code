'''
Stroop behavioral analysis
- Reaction time calculation (comparing congruent/incongruent)
- Gratton effect
'''

import numpy as np
from matplotlib import pyplot as plt
import seeg_library as slib
import seeg_constants as CONST
from datetime import datetime
from scipy.stats import ttest_ind


# Parameters
patient = 'p10'

root = "C:\\Users\\amand\\Documents\\Research\\Project_AHN\\Data_processing\\data\\"
csv_path = root + patient + "\\behavior\\" + patient + "_"

subject = CONST.Subject(patient)
num_stroop_exp = subject.NUM_STROOP

rxn_times = []
congruent_arr = []

ic_gratton = []
c_gratton = []

for i in range(num_stroop_exp):
    print("\n" + patient + ", experiment " + str(i))

    # Read in behavior csv
    experiment = "stroop" + str(i+1)
    path_csv = csv_path + experiment + ".csv"
    df = slib.read_csv_file(path_csv)
    num_trials = len(df)

    # Compute reaction times
    stim_arr = df['stim_time'].to_numpy()
    choice_arr = df['key_time'].to_numpy()
    stim_time = [datetime.strptime(stim_arr[j], '%H:%M:%S.%f') for j in range(num_trials)]
    choice_time = [datetime.strptime(choice_arr[j], '%H:%M:%S.%f') for j in range(num_trials)]
    rxn = np.array([(choice_time[j] - stim_time[j]).total_seconds() for j in range(num_trials)])
    rxn_times.append(rxn)

    # Filter out congruent/incongruent trials
    congruent_flag = df['congruent'].to_numpy()
    congruent_arr.append(congruent_flag)

    # Compute average & median reaction times
    for c_flag in [0, 1]:
        rxn_filt = rxn[np.where(congruent_flag == c_flag)[0]]
        rxn_av = np.mean(rxn_filt)
        rxn_med = np.median(rxn_filt)
        print("c_flag = " + str(c_flag) + ". Average = " + str(round(rxn_av, 3)) + ". Median = " + str(rxn_med))

    # Construct gratton lists
    ic_idx = []; c_idx = []
    for j in range(1, num_trials):
        if congruent_flag[j-1] == 0:
            ic_idx.append(j)
        else:
            c_idx.append(j)

    # Mean Gratton effect
    ic_gratton_av = np.mean(rxn[ic_idx])
    c_gratton_av = np.mean(rxn[c_idx])

    # Median Gratton effect
    ic_gratton_med = np.median(rxn[ic_idx])
    c_gratton_med = np.median(rxn[c_idx])

    # Save Gratton lists (add an index shift to each experiment)
    ic_gratton.append(ic_idx + np.array(len(ic_idx)*[i*num_trials]))
    c_gratton.append(c_idx + np.array(len(c_idx)*[i*num_trials]))


# Concatenate data from all experiments
congruent_arr = np.concatenate(congruent_arr)
rxn_times = np.concatenate(rxn_times)
ic_gratton = np.concatenate(ic_gratton)
c_gratton = np.concatenate(c_gratton)

# Separate congruent and incongruent
rxn_c_all = rxn_times[np.where(congruent_arr == 1)[0]]
rxn_ic_all = rxn_times[np.where(congruent_arr == 0)[0]]
stats_rxn = ttest_ind(rxn_c_all, rxn_ic_all)

# Gratton overall
gratton_ic_av = np.mean(rxn_times[ic_gratton])
gratton_c_av = np.mean(rxn_times[c_gratton])
print("IC Gratton: " + str(gratton_ic_av))
print("C Gratton: " + str(gratton_c_av))
stats_gratton = ttest_ind(rxn_times[c_gratton], rxn_times[ic_gratton])

# Plotting
rxn_c_all[rxn_c_all > 4] = 0  # FIXME: do outlier detection better
plt.hist(rxn_c_all, bins=20)
plt.hist(rxn_ic_all, bins=20)
plt.show()

print("Hi")

