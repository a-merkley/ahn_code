import numpy as np
from matplotlib import pyplot as plt
import seeg_library as slib
import seeg_constants as CONST
from datetime import datetime
import pandas as pd
from scipy.stats import ttest_ind, f_oneway, zscore, tukey_hsd, ttest_rel


# Parameters
patient_lst = ['p7', 'p8', 'p9', 'p10', 'p11', 'p12']
root = "C:\\Users\\amand\\Documents\\Research\\Project_AHN\\Data_processing\\data\\"

num_patients = len(patient_lst)
c_clr = "blue"
ic_clr = "red"

rxn = []
congruent = []
control = []
gratton_type = []
gratton_rt = []

for patient in patient_lst:
    csv_path = root + patient + "\\behavior\\" + patient + "_"

    subject = CONST.Subject(patient)
    num_stroop_exp = subject.NUM_STROOP

    for i in range(num_stroop_exp):
        # Read in behavior csv
        experiment = "stroop" + str(i + 1)
        path_csv = csv_path + experiment + ".csv"
        df = slib.read_csv_file(path_csv)
        num_trials = len(df)

        # Compute reaction times
        stim_arr = df['stim_time'].to_numpy()
        choice_arr = df['key_time'].to_numpy()
        stim_time = [datetime.strptime(stim_arr[j], '%H:%M:%S.%f') for j in range(num_trials)]
        choice_time = [datetime.strptime(choice_arr[j], '%H:%M:%S.%f') for j in range(num_trials)]
        rxn_time = np.array([(choice_time[j] - stim_time[j]).total_seconds() for j in range(num_trials)])
        rxn.append(rxn_time)

        # Get congruent and control
        congruent_flag = df['congruent'].to_numpy()
        control_flag = df['control'].to_numpy()
        congruent.append(congruent_flag)
        control.append(control_flag)

        # Get Gratton data
        for j in range(num_trials):
            if j == 0:
                gratton_type.append("nan")
                gratton_rt.append(-1)
            else:
                if congruent_flag[j-1] == 0 and congruent_flag[j] == 0:
                    gratton_type.append("ic->ic")
                elif congruent_flag[j-1] == 0 and congruent_flag[j] == 1:
                    gratton_type.append("ic->c")
                elif congruent_flag[j - 1] == 1 and congruent_flag[j] == 0:
                    gratton_type.append("c->ic")
                elif congruent_flag[j - 1] == 1 and congruent_flag[j] == 1:
                    gratton_type.append("c->c")
                gratton_rt.append(rxn_time[j])


# Concatenate data from all experiments
rxn = np.concatenate(rxn)
congruent = np.concatenate(congruent)
control = np.concatenate(control)
gratton_df = pd.DataFrame({"Type": gratton_type, "RT": gratton_rt})
gratton_rt = np.array(gratton_rt)

# Dealing with outliers
outliers = np.where(abs(zscore(rxn)) > 3)[0]
rxn = np.delete(rxn, outliers)
congruent = np.delete(congruent, outliers)
control = np.delete(control, outliers)

# Gratton outliers
idx = outliers[gratton_rt[outliers] > 0]  # Don't remove the previous element if the outlier element is the first trial
previous_idx = idx  # FIXME: CHECK THIS!!!
gratton_df = gratton_df.drop(index=previous_idx)

# Get zscore metrics
rxn_mean = np.mean(rxn)
rxn_std = np.std(rxn)

# Recover incongruent and congruent trials (without controls)
rxn_c = rxn[np.where((congruent == 1) & (control == 0))[0]]
rxn_ic = rxn[np.where((congruent == 0) & (control == 0))[0]]
rxn_c = (rxn_c - rxn_mean) / rxn_std
rxn_ic = (rxn_ic - rxn_mean) / rxn_std

# Group metrics
rxn_c_mean = np.mean(rxn_c)
rxn_ic_mean = np.mean(rxn_ic)

# Stats: RT
t_stat, t_pval = ttest_ind(rxn_c, rxn_ic)
a_stat, a_pval = f_oneway(rxn_c, rxn_ic)
print("T-test c vs ic p-value = " + str(t_pval))
print("ANOVA c vs ic p-value = " + str(a_pval))

# # Plotting reaction times
# plt.plot([rxn_c_mean, rxn_c_mean], [0, 1], color=c_clr, linestyle='--', label="Congruent mean")
# plt.plot([rxn_ic_mean, rxn_ic_mean], [0, 1], color=ic_clr, linestyle='--', label="Incongruent mean")
# plt.hist(rxn_c, bins=25, histtype="step", density=True, color=c_clr)
# plt.hist(rxn_ic, bins=25, histtype="step", density=True, color=ic_clr)
# plt.legend()
# plt.xlabel("Reaction Time (Z-score)")
# # plt.ylabel("Counts")
# plt.title("Overall reaction time: " + str(num_patients) + " patients")
# plt.show()

# Gratton effect computation
# FIXME: check outlier removal!!! check zscoring!
gratton = []
for effect in ["ic->ic", "c->ic", "ic->c", "c->c"]:
    idx = gratton_df.index[gratton_df['Type'] == effect]
    rt = gratton_df['RT'].loc[idx].to_numpy()
    gratton.append(rt)
    print(effect + ": " + str(np.mean(rt)))
    plt.hist(rt, bins=25, histtype="step", density=False, label=effect)

# Get some stats
g_stat, g_pval = f_oneway(*gratton)
posthoc = tukey_hsd(*gratton)
posthoc_pval = posthoc.pvalue
print(posthoc_pval)

# Finish plotting
plt.title("Gratton effect")
plt.ylabel("Count")
plt.xlabel("Reaction time (s)")
plt.legend()
plt.show()
