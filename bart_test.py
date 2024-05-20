# Analyze first and last keypresses in balloon inflation to look for error-related negativity
import numpy as np
from matplotlib import pyplot as plt
import mne
import seeg_library as slib
import seeg_constants as CONST
import pandas as pd
import scipy.signal as signal


# Constants for each patient and file save specification. FIXME: THE FOLLOWING ARE PARAMETERS YOU CAN CHANGE
patient = 'p9'
root = "C:\\Users\\amand\\Documents\\Research\\Project_AHN\\Data_processing\\data\\"

# Collect patient metadata
subject = CONST.Subject(patient)
e_map = subject.E_MAP
region = subject.amygdala_r

# Build file paths
edf_path = root + patient + "\\" + patient + ".edf"
csv_root = root + patient + "\\behavior\\" + patient + "_"

# Read in raw data
data = mne.io.read_raw_edf(edf_path, preload=True)
channels = slib.create_channel_dict(data.ch_names)
n_chan = len(channels)

# # FIXME: MAJOR DEBUGGING HAPPENING HERE
# abs_start = 500000
# abs_finish = 1000000
# raw_data = data.get_data()
# # ch = raw_data[channels["G-G'3"], :]
# # ch = mne.filter.filter_data(ch, 1024, 0.5, 30)
# # plt.plot(ch[abs_start:abs_finish], label="ACC")
#
# trig = raw_data[channels["TRIG"]]
# plt.plot(trig)
# plt.show()
# # FIXME: MAJOR DEBUGGING HAPPENING HERE

exp_times = slib.get_exp_endpoints(data, subject.NUM_EXP, patient)

alignment = 'left'  # Align events either 'left' or 'center'
press_num = 0  # Which keypress to surround? 0 = 1st keypress, -1 = last keypress, and everything in between

# Collect balloons from all experiments
for exp_idx in range(subject.NUM_BART):

    # Extract BART experiment raw data
    experiment = "bart" + str(exp_idx+1)
    experiment_id = e_map[experiment]
    raw_data = data.get_data(start=exp_times[experiment_id][0], stop=exp_times[experiment_id][1])

    # Collect trial start times
    trigger = raw_data[channels["TRIG"]]

    # FIXME: REMOVE, FOR DORIAN MAY 9
    second_end = len(trigger) / 1000
    ts = np.linspace(0, second_end, len(trigger))
    plt.plot(ts, trigger)
    plt.xlabel("Time (s)")
    plt.title("BART example trigger")
    plt.show()

    t_rising = np.where(np.diff(trigger) == 1)[0]
    t_rising_diff = np.diff(t_rising)
    t_start = t_rising[np.where(t_rising_diff < 150)[0]]  # Look for double pulses with small time difference FIXME: MAY NEED TO CHANGE 150
    glitch_idx = np.where(np.diff(t_start) < 200)[0] + 1  # Filter out glitches
    t_start = np.delete(t_start, glitch_idx)

    # Filter raw data
    raw_data = slib.band_noise_filter(raw_data, lower=0.1)

    # Collect behavioral and trial data
    csv_path = csv_root + experiment + ".csv"
    # FIXME: UPDATE THE HACKY STUFF HERE
    behavior = pd.read_csv(csv_path, names=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14'], header=None)

    # Collect ephys 200ms after last keypress
    time_after = 200  # number ms after keypress
    last_trial = np.zeros((len(t_start), raw_data.shape[0], time_after))
    for i, t in enumerate(t_start):
        start = t_start[i]
        if i < len(t_start) - 1:
            end = t_start[i + 1]
        else:
            end = raw_data.shape[1]
        t_pulse = np.where(np.diff(trigger[start:end]) == 1)[0]
        t_keypress = t_pulse[2:]
        t_last = t_keypress[press_num] + start
        last_trial[i, :, :] = raw_data[:, t_last:t_last + time_after] * 10 ** 6  # convert to uV

    # Collect cashin or explosion result after each balloon
    # FIXME: THIS CAN CHANGE WITH PATIENT CHOICE - EXPERIMENT UPDATED IN BETWEEN
    b_result = np.zeros(len(t_start))  # cashin = 0, explosion = 1
    for idx, row in behavior.iterrows():
        if idx >= len(t_start):
            break
        if 'cashin' in row.to_string():
            b_result[idx] = 0
        else:
            b_result[idx] = 1

    # Average last keypress over all trials
    explode_idx = np.where(b_result == 1)[0]
    cashin_idx = np.where(b_result == 0)[0]
    av_cashin = np.mean(last_trial[cashin_idx, :, :], axis=0)
    av_explode = np.mean(last_trial[explode_idx, :, :], axis=0)
    ex_stderr = np.std(last_trial[explode_idx, :, :], axis=0) / np.sqrt(len(explode_idx))
    ca_stderr = np.std(last_trial[cashin_idx, :, :], axis=0) / np.sqrt(len(cashin_idx))
    t = np.arange(time_after)
    for i, c in enumerate(region):  # FIXME: CHANGE THE REGION HERE!!!
        if i < 4:
            plt.subplot(2, 2, i + 1)  # plt.subplot(3, 4, i + 1)
            # plt.errorbar(t, av_explode[channels[c], :], yerr=ex_stderr[channels[c]], label="Explode", ecolor='#f17386',
            #              fmt='k')
            # plt.errorbar(t, av_cashin[channels[c], :], yerr=ca_stderr[channels[c]], label="Cashin", ecolor='#73a1f1',
            #              fmt='b')

            plt.plot(av_explode[channels[c], :], label="Explosion")
            plt.plot(av_cashin[channels[c], :], label="Cashin")
            plt.legend(loc='upper right', fontsize='small')
            plt.title('Channel ' + str(i + 1))
            plt.xticks(fontsize=10, rotation=0)
            plt.yticks(fontsize=10, rotation=0)
            # plt.gca().invert_yaxis()
            if i == 4:
                plt.ylabel('Voltage (uV)')
    plt.suptitle("BART, aMCC: 200ms after first keypress")
    plt.show()

