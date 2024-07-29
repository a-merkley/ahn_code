'''
Stroop behavioral analysis
- Reaction time calculation (comparing congruent/incongruent)
- Gratton effect (2-way and 4-way)
    - 2-way is any trial preceded by either congruent or incongruent
    - 4-way is all combos of (in)congruent preceded by (in)congruent
'''

import numpy as np
from matplotlib import pyplot as plt
import seeg_library as slib
import seeg_constants as CONST
from datetime import datetime
from scipy.stats import ttest_ind, f_oneway


# Parameters
patient = 'p8'

root = "C:\\Users\\amand\\Documents\\Research\\Project_AHN\\Data_processing\\data\\"
csv_path = root + patient + "\\behavior\\" + patient + "_"

subject = CONST.Subject(patient)
num_stroop_exp = subject.NUM_STROOP

thresh = 4  # threshold for # seconds for a bad reaction time

# Lists to save across all experiments
rxn_times = []
congruent_arr = []
ii_gratton4 = []
ic_gratton4 = []
ci_gratton4 = []
cc_gratton4 = []

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

    # Filter out congruent/incongruent trials & controls
    congruent_flag = df['congruent'].to_numpy()
    congruent_arr.append(congruent_flag)
    control_flag = df['control'].to_numpy()

    # Compute average & median reaction times
    for c_flag in [0, 1]:
        rxn_filt = rxn[np.where((congruent_flag == c_flag) & (control_flag == 0) & (rxn < thresh))[0]]
        rxn_av = np.mean(rxn_filt)
        rxn_med = np.median(rxn_filt)
        print("c_flag = " + str(c_flag) + ". Average = " + str(round(rxn_av, 3)) + ". Median = " + str(rxn_med))


    # Construct 2-way and 4-way gratton lists
    ii4_idx = []; ic4_idx = []; ci4_idx = []; cc4_idx = []  # 4-way lists
    for j in range(1, num_trials):
        if congruent_flag[j-1] == 0:
            if congruent_flag[j] == 0:
                ii4_idx.append(j)
            else:
                ci4_idx.append(j)
        else:
            if congruent_flag[j] == 0:
                ic4_idx.append(j)
            else:
                cc4_idx.append(j)

    # Mean 2-way Gratton effect
    ic_idx = ii4_idx + ci4_idx
    c_idx = ic4_idx + cc4_idx
    ic_gratton_av = np.mean(rxn[ic_idx])
    c_gratton_av = np.mean(rxn[c_idx])

    # Mean 4-way Gratton effect
    ii4_av = np.mean(rxn[ii4_idx])
    ci4_av = np.mean(rxn[ci4_idx])
    ic4_av = np.mean(rxn[ic4_idx])
    cc4_av = np.mean(rxn[cc4_idx])

    # Median 2-way Gratton effect
    ii4_med = np.median(rxn[ii4_idx])
    ci4_med = np.median(rxn[ci4_idx])
    ic4_med = np.median(rxn[ic4_idx])
    cc4_med = np.median(rxn[cc4_idx])

    # Save 4-way Gratton index lists (add an index shift to each experiment)
    ii_gratton4.append(ii4_idx + np.array(len(ii4_idx)*[i*num_trials]))
    ci_gratton4.append(ci4_idx + np.array(len(ci4_idx)*[i*num_trials]))
    ic_gratton4.append(ic4_idx + np.array(len(ic4_idx)*[i*num_trials]))
    cc_gratton4.append(cc4_idx + np.array(len(cc4_idx)*[i*num_trials]))


# Concatenate data from all experiments
congruent_arr = np.concatenate(congruent_arr)
rxn_times = np.concatenate(rxn_times)
ii_gratton4 = np.concatenate(ii_gratton4)
ci_gratton4 = np.concatenate(ci_gratton4)
ic_gratton4 = np.concatenate(ic_gratton4)
cc_gratton4 = np.concatenate(cc_gratton4)

# Separate congruent and incongruent
rxn_c_all = rxn_times[np.where(congruent_arr == 1)[0]]
rxn_ic_all = rxn_times[np.where(congruent_arr == 0)[0]]
rxn_c_av = np.mean(rxn_c_all)
rxn_ic_av = np.mean(rxn_ic_all)
stats_rxn = ttest_ind(rxn_c_all, rxn_ic_all)

# 2-way Gratton overall
ic_gratton2 = np.concatenate((ii_gratton4, ci_gratton4))
c_gratton2 = np.concatenate((ic_gratton4, cc_gratton4))
gratton_ic_av = np.mean(rxn_times[ic_gratton2])
gratton_c_av = np.mean(rxn_times[c_gratton2])
print("2-way IC Gratton: " + str(gratton_ic_av))
print("2-way C Gratton: " + str(gratton_c_av))
stats_gratton2 = ttest_ind(rxn_times[c_gratton2], rxn_times[ic_gratton2])

# 4-way Gratton overall
ii4_av_tot = np.mean(rxn_times[ii_gratton4])
ic4_av_tot = np.mean(rxn_times[ic_gratton4])
ci4_av_tot = np.mean(rxn_times[ci_gratton4])
cc4_av_tot = np.mean(rxn_times[cc_gratton4])
stats_gratton4 = f_oneway(rxn_times[ii_gratton4], rxn_times[ci_gratton4], rxn_times[ic_gratton4], rxn_times[cc_gratton4])

# Plotting
rxn_c_all[rxn_c_all > 4] = 0  # FIXME: do outlier detection better
plt.hist(rxn_c_all, bins=20)
plt.hist(rxn_ic_all, bins=20)
plt.show()
