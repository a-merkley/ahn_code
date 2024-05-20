# Create a mega stroop dataset from all raw trials. Saves raw data, behavior data, channel names
import csv
import numpy as np
import pandas as pd
import mne
import seeg_library as slib
import seeg_constants as CONST
from matplotlib import pyplot as plt


# Constants for each patient and file save specification. FIXME: THE FOLLOWING ARE PARAMETERS YOU CAN CHANGE
patient = 'p9'
width = 1000  # Trials will be this long
event = 2  # On what even to align stroop tasks. 1: stimulus onset, 2: keypress, 3: trial start (only exists for p1, p2)
alignment = 'center'  # Align events either 'left' or 'center'
root = "C:\\Users\\amand\\Documents\\Research\\Project_AHN\\Data_processing\\data\\"

# Collect patient metadata
subject = CONST.Subject(patient)
e_map = subject.E_MAP
num_stroop_exp = subject.NUM_STROOP
if event == 1:
    event_name = "stim"
elif event == 2:
    event_name = "key"
else:
    event_name = "start"

# Build file paths
edf_path = root + patient + "\\" + patient + ".edf"
csv_path = root + patient + "\\behavior\\" + patient + "_"

# Read in raw data
data = mne.io.read_raw_edf(edf_path, preload=True)
channels = slib.create_channel_dict(data.ch_names)
n_chan = len(channels)
exp_times = slib.get_exp_endpoints(data, subject.NUM_EXP, patient)
print(exp_times)

# Create dataset of all trials
df_lst = []
trial_lst = []
width_arr = []  # FIXME: REMOVE
for i in range(num_stroop_exp):
    print(i)
    # Read in and augment behavior data
    experiment = "stroop" + str(i+1)
    path_csv = csv_path + experiment + ".csv"
    if patient == "p2":
        df = slib.augment_stroop_behavior_df(path_csv)
    else:
        df = slib.read_csv_file(path_csv)
    df_lst.append(df)

    # Read in raw data
    experiment_id = e_map[experiment]
    raw_data = data.get_data(start=exp_times[experiment_id][0], stop=exp_times[experiment_id][1])
    trig_chan = raw_data[channels["TRIG"]]

    # # Trigger width analysis
    # trig_diff = np.diff(trig_chan)
    # rising_edge = np.where(trig_diff == 1)[0][:-1]
    # falling_edge = np.where(trig_diff == -1)[0]
    # pulse_width = falling_edge - rising_edge
    # av = pulse_width.mean()
    # std = pulse_width.std()
    #
    # second_end = len(trig_chan) / 1000
    # ts = np.linspace(0, second_end, len(trig_chan))
    # plt.plot(ts, trig_chan)
    # plt.xlabel("Time (s)")
    # plt.title("Stroop example trigger")
    # plt.show()

    if patient == "p2":
        stroop_lbl = slib.label_stroop_events_july17(trig_chan)
    else:
        stroop_lbl = slib.label_stroop_events(trig_chan)

    # Collect trials based on event
    trial_start = stroop_lbl.loc[stroop_lbl['Event'] == event]['Time'].to_numpy()

    # # FIXME: REMOVE, QUANTIFICATION OF PULSE DELAYS. TODO: CHECK MATLAB TIMESTAMPS ARE BETTER?
    # from datetime import datetime
    # event1 = stroop_lbl.loc[stroop_lbl['Event'] == 1]['Time'].to_numpy()
    # event2 = stroop_lbl.loc[stroop_lbl['Event'] == 2]['Time'].to_numpy()
    # events = np.sort(np.concatenate((event1, event2)))
    # stim_time = df['stim_time'].to_list()
    # key_time = df['key_time'].to_list()
    # matlab_time = stim_time + key_time
    # diff_arr = []
    # for k in range(len(matlab_time)):
    #     if k == 0:
    #         offset = trial_start[0]
    #         t1 = datetime.strptime(stim_time[0], "%H:%M:%S.%f")
    #     try:
    #         t2 = datetime.strptime(matlab_time[k], "%H:%M:%S.%f")
    #     except:
    #         t2 = datetime.strptime(matlab_time[k], "%H:%M:%S")
    #     tdiff = t2 - t1
    #     diff_arr.append(1000*tdiff.total_seconds() + offset)
    # diff_arr.sort()
    # diff_np = np.array(diff_arr)
    # mse = np.sum(np.square(diff_np - events))
    # print(mse)
    # plt.plot(trig_chan)
    # plt.stem(diff_arr, 255*np.ones(len(diff_arr)), markerfmt='C0.', label="Matlab timestamps")
    # plt.plot(trig_chan, 'g', label="Natus trigger")
    # plt.legend()
    # plt.show()

    # rising_time = np.where(np.diff(trig_chan) == 1)[0]
    # falling_time = np.where(np.diff(trig_chan) == -1)[0]
    # for k in range(len(rising_time)-2):
    #     if i == 0:
    #         width_arr.append(falling_time[k+1]-rising_time[k])
    #     else:
    #         width_arr.append(falling_time[k] - rising_time[k])

    num_trials = int(len(trial_start))
    trial_arr = np.zeros((num_trials, int(raw_data.shape[0]), width))
    idx_start = 0 if alignment == 'left' else 1
    for j in np.arange(idx_start, num_trials-1):  # FIXME: CHECK, THIS IS WEIRD
        event_time = int(trial_start[j])
        if alignment == 'left':
            s1 = event_time
            s2 = event_time + width
        elif alignment == 'center':
            s1 = int(event_time - width/2)
            s2 = int(event_time + width/2)
        sig = 10**6 * raw_data[:, s1:s2]  # Get signal in uV
        trial_arr[j, :, :] = slib.band_noise_filter(sig, lower=0.1)
    trial_lst.append(trial_arr)


# Collect data into one mega object
behavior_df = pd.concat(df_lst)
trials = np.vstack(trial_lst)

# Save data into csv files
behavior_filename = patient+"_behavior_"+alignment+str(width)+"_"+event_name+".csv"
raw_filename = patient+"_trials_"+alignment+str(width)+"_"+event_name+".npy"
ch_filename = patient+"_ch.csv"
behavior_df.to_csv(behavior_filename)
with open(raw_filename, 'wb') as f:
    np.save(f, trials)
with open(ch_filename, "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, channels.keys())
    writer.writeheader()
    writer.writerow(channels)
