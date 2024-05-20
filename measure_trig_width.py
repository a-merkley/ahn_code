# Measure the width of arbitrary signals for stroop task. Can be adapted to BART as well
# Stroop pulse ID: There are a total of 6 pulses and 12 total spacings
# 0: 1st pulse (trial start), 1: time between trial start/stim appear pulse, 2: stim appear pulse 1,
# 3: space between stim appear pulses, 4: stim appear pulse 2, 5: reaction time, 6: keypress pulse 1,
# 7: time between keypress pulse 1 and 2, 8: keypress pulse 2, 9: time between keypress pulse 2 and 3
# 10: keypress pulse 3, 11: time between last keypress pulse and next trial start
import numpy as np
import mne
import seeg_library as slib
import seeg_constants as sconst

# Read in raw data
path_edf = "C:\\Users\\amand\\Documents\\Research\\Project_AHN\\Data_processing\\data\\july_17_2023\\p2_July17.edf"
data = mne.io.read_raw_edf(path_edf, preload=True)
channels = slib.create_channel_dict(data.ch_names)
exp_times = slib.get_exp_endpoints(data, sconst.NUM_EXP_JULY17)

# Create dataset of all trials
df_lst = []
trial_lst = []
pulse_id = 5  # read upper comments for possible choices here
for i in range(sconst.NUM_EXP_JULY17-2):
    # Read in raw data
    experiment = "stroop" + str(i + 1)
    experiment_id = sconst.E_MAP_JULY17[experiment]
    raw_data = data.get_data(start=exp_times[experiment_id][0], stop=exp_times[experiment_id][1])
    trig_chan = raw_data[channels["TRIG"]]
    trig_diff = np.diff(np.where(np.diff(trig_chan) != 0)[0])  # differences between all rising and falling edges

    # Compute pulse widths
    pulse_lst = [j for j in range(len(trig_diff)) if j % 12 == pulse_id]
    trig_at_mod = trig_diff[pulse_lst]
    av_pulse_length = np.mean(trig_at_mod)
    std_pulse_length = np.std(trig_at_mod)
    print("Breakpoint")
