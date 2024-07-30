import numpy as np
from matplotlib import pyplot as plt
import seeg_library as slib
import seeg_constants as CONST
from datetime import datetime
from scipy.stats import ttest_ind, f_oneway


# Parameters
patient_lst = ['p7', 'p8', 'p9', 'p10', 'p11', 'p12']
root = "C:\\Users\\amand\\Documents\\Research\\Project_AHN\\Data_processing\\data\\"

num_patients = len(patient_lst)
thresh = 4  # threshold for # seconds for a bad reaction time

rxn_c = []
rxn_ic = []
control_flag = []

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
        rxn = np.array([(choice_time[j] - stim_time[j]).total_seconds() for j in range(num_trials)])
        outlier_idx = np.where(rxn > thresh)[0]
        rxn = np.delete(rxn, outlier_idx)

        # Filter out congruent and control
        congruent_flag = np.delete(df['congruent'].to_numpy(), outlier_idx)
        control_flag = np.delete(df['control'].to_numpy(), outlier_idx)
        idx_c = np.where((congruent_flag == 1) & (control_flag == 0))[0]
        idx_ic = np.where((congruent_flag == 0) & (control_flag == 0))[0]
        rxn_c.append(rxn[idx_c])
        rxn_ic.append(rxn[idx_ic])





