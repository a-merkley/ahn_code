import numpy as np
import pandas as pd
from datetime import datetime
from matplotlib import pyplot as plt
from scipy import signal
from copy import *
import seeg_constants as sconst
import numpy.linalg as npl


# Read a CSV file differently, depending on whether it is a stroop or bart experiment
# INPUTS
# - filename: string containing the path to the csv file
def read_csv_file(filename):
    if "stroop" in filename:
        return pd.read_csv(filename)
    elif "bart" in filename:
        return pd.read_csv(filename, header=None)


# Get start and end time points of experiments from raw data based on TRIG channel
# INPUTS
# - data: MNE data as read by read_raw_edf
# - num_experiments: the number of experiments done in this recording time (should be known by experimenter)
# - p_num: the patient number (to make hacky fixes for oddities in some patients)
def get_exp_endpoints(data, num_experiments, p_num):
    # Get trigger data
    raw_data = data.get_data()
    channels = data.ch_names
    channel_idx = np.where(np.array(channels) == 'TRIG')[0][0]

    num_experiments += 1  # FIXME: COULD HAVE PROBLEMS

    # Compute differences in time between trigger events
    trig_diff = np.diff(raw_data[channel_idx, :])
    nonzero_idx = np.where(abs(trig_diff) == 1)[0]
    idx_diffr = np.diff(nonzero_idx)
    idx_diffr[-1] = nonzero_idx[-1] + raw_data.shape[1]

    # ASSUMPTION: points with largest time difference are times between experiments, not between trials
    between_exp = np.sort(idx_diffr)[::-1][:num_experiments + 1]
    indices = np.where(idx_diffr > min(between_exp))[0]

    # Collect experiment start and end times
    start_end_tup = []
    for e in range(num_experiments):
        if e == 0:
            start = nonzero_idx[0]
        else:
            start = nonzero_idx[indices[e - 1] + 1]
        end = nonzero_idx[indices[e]]
        # plt.plot([start, start], [0, 255], 'r'); plt.plot([end, end], [0, 255], 'k')  # FOR DEBUGGING
        if end - start > 100:
            start_end_tup.append((start, end))
    return start_end_tup


# Create a dictionary with keys as channel names and indices as raw data row indices
def create_channel_dict(chan_lst):
    chan_idx = list(np.arange(0, len(chan_lst)))
    return dict(zip(chan_lst, chan_idx))


# At least for July 17 stroop experiments, augment the .mat content with stimulus congruency and response time
# INPUTS
# - path_csv: string containing the path to the csv file
def augment_stroop_behavior_df(path_csv):
    # Read in data
    behavior_df = read_csv_file(path_csv)

    # Augment column with stimulus congruency
    resp = []
    congruency = []
    for i, c in enumerate(behavior_df['color']):
        keypress = sconst.C_MAP[behavior_df['char'][i]]
        if c == keypress:
            resp.append('correct')
        elif behavior_df['word'][i] == keypress:
            resp.append('incorrect')
        else:
            resp.append('missed')
        if c == behavior_df['word'][i]:
            congruency.append(1)
        else:
            congruency.append(0)
    behavior_df['response'] = resp
    behavior_df['congruent'] = congruency

    # Augment column with elapsed time between stimulus appearance and keypress
    keypress_time = []
    fmt = '%H:%M:%S.%f'
    from datetime import datetime
    for i, t in enumerate(behavior_df['trial_end']):
        if i == 0:
            start_exp_split = behavior_df['start_experiment'].to_numpy()[-1].split()[1]
            formatted_start = datetime.strptime(start_exp_split, fmt)
            formatted_end = datetime.strptime(behavior_df['key_press'][0], fmt)
            elapsed = formatted_end - formatted_start
        elif i == len(resp)-1:
            formatted_start = datetime.strptime(t, fmt)
            end_exp_split = behavior_df['end_experiment'].to_numpy()[-1].split()[1]
            formatted_end = datetime.strptime(end_exp_split, fmt)
            elapsed = formatted_end - formatted_start
        else:
            key_time = datetime.strptime(behavior_df['key_press'][i+1], fmt)
            start_time = datetime.strptime(t, fmt)
            elapsed = key_time - start_time
        keypress_time.append(elapsed.seconds + elapsed.microseconds/10**6)
    behavior_df['elapsed'] = keypress_time

    return behavior_df


# Stroop triggering for all experiments after July
def label_stroop_events(trig):
    rising_time = np.where(np.diff(trig) == 1)[0]  # 1: rising edge, -1: falling edge
    event_time = np.zeros((len(rising_time), 2))
    for i, r in enumerate(rising_time):
        if i % 2 == 0:
            event_time[i, 1] = 1  # stimulus appear
        elif i % 2 == 1:
            event_time[i, 1] = 2  # button press
        else:
            event_time[i, 1] = 0
        event_time[i, 0] = r
    zero_idx = np.where(event_time[:, 1] == 0)[0]
    return pd.DataFrame(np.delete(event_time, zero_idx, 0), columns=["Time", "Event"])


def label_stroop_events_july17(trig):
    rising_time = np.where(np.diff(trig) == 1)[0]  # 1: rising edge, -1: falling edge
    event_time = np.zeros((len(rising_time), 2))
    for i, r in enumerate(rising_time):
        if i % 6 == 0:
            event_time[i, 1] = 3  # trial start
        elif i % 6 == 1:
            event_time[i, 1] = 1  # stimulus appear
        elif i % 6 == 3:
            event_time[i, 1] = 2  # button press
        else:
            event_time[i, 1] = 0
        event_time[i, 0] = r
    zero_idx = np.where(event_time[:, 1] == 0)[0]
    return pd.DataFrame(np.delete(event_time, zero_idx, 0), columns=["Time", "Event"])


def band_noise_filter(sig, lower=0.5, upper=511, noise_freq=60, fs=1024):
    '''
    Inputs:
        sig     - the AnalogSignalArray to be bandpass filtered and notched for noise removal.
        lower      - the lower cutoff frequency for the bandpass filter. Must be greater than 0 Hz,
                     default is 0.1 Hz.
        upper      - the upper cutoff frequency for the bandpass filter, default is 360 Hz.
        noise_freq - the frequency to be removed, along with its harmonics, representing line noise.

    Outputs:
        An AnalogSignalArray containing the bandpass filtered, notched signal with the same support
        as the input signal.
    '''

    # High pass filter to remove slow signal drift
    b, a = signal.cheby1(4, 5, (lower, upper), btype='bandpass', fs=fs)
    # b, a = signal.butter(4, (lower, upper), btype='bandpass', fs=fs)
    hpass = signal.filtfilt(b, a, sig)
    denoising = deepcopy(hpass)

    # Notch filter to remove 60 Hz noise and its harmonics
    for num in range(1, int(fs / (2 * noise_freq))):
        harmonic = num * noise_freq
        b, a = signal.iirnotch(harmonic, 10, fs)
        notch_inc = signal.filtfilt(b, a, denoising)
        denoising = deepcopy(notch_inc)

    # Create ASA with same support as asa_in, but change signal content
    no_stim_band_noiseless = deepcopy(denoising)
    return no_stim_band_noiseless


# Convert stroop colors into numeric values
# c_arr: color array that is a pandas series (selected from column of pd dataframe)
# Let 'red'=0, 'green'=1, 'blue'=2
def stroop_color2numeric(c_arr):
    c_arr = c_arr.to_list()
    num_c = len(c_arr)

    n_arr = np.zeros(num_c)
    for i in range(num_c):
        if c_arr[i] == 'red':
            n_arr[i] = 0
        elif c_arr[i] == 'green':
            n_arr[i] = 1
        elif c_arr[i] == 'blue':
            n_arr[i] = 2
        elif c_arr[i] == 'black':
            n_arr[i] = 3
        else:
            print("INVALID COLOR: " + c_arr[i])
    return n_arr


# A is a (features x samples) matrix
# M is a (samples) vector
# returns the set of regression vectors of size (features x features). Vectors indexed by columns
def iterative_regression(A, M, dims=-1):
    num_feat = A.shape[0]
    if dims > num_feat:
        input("ERROR. CANNOT REQUEST MORE DIMENSIONS THAN # FEATURES IN A!\nPress enter.")
    if dims == -1:
        dims = num_feat
    v_ir = np.zeros((num_feat, dims))

    A = (A.T - np.mean(A, axis=1)).T
    M = M - np.mean(M)
    vmax = npl.inv(A@A.T) @ A @ M
    v_ir[:, 0] = vmax.T / npl.norm(vmax)

    for i in np.arange(1, dims):
        A_clean = A
        for j in range(i):
            vj = np.expand_dims(v_ir[:, i-1], axis=1)
            A_clean -= vj @ vj.T @ A
        # Reduce the dimension of data matrix by one and compute new regression
        A_reduce = A_clean[:-i, :]
        vmax1 = npl.inv(A_reduce@A_reduce.T) @ A_reduce @ M
        # Boost the new vector up to n dimensions
        boost = np.zeros(i)
        vmax = np.expand_dims(np.append(vmax1, boost), axis=1)
        # Gram-Schmidt
        for j in range(i):
            u = np.expand_dims(v_ir[:, j], axis=1)
            vmax -= np.dot(vmax.T, u) / np.dot(u.T, u) * u
        v_ir[:, i] = vmax.T / npl.norm(vmax)
    return v_ir


# # A is a (features x samples) matrix
# # M is a (samples) vector
# # alpha and beta are weights on elastic net penalties
# # returns the set of regression vectors of size (features x features). Vectors indexed by columns
# def elastic_ir(A, M, dims=-1, alpha=0, beta=0):
#     num_feat = A.shape[0]
#     if dims > num_feat:
#         input("ERROR. CANNOT REQUEST MORE DIMENSIONS THAN # FEATURES IN A!\nPress enter.")
#     if dims == -1:
#         dims = num_feat
#     v_ir = np.zeros((num_feat, dims))
#
#     A = (A.T - np.mean(A, axis=1)).T
#     M = M - np.mean(M)
#
#     # Train initial model
#     enm = ElasticNet(alpha=alpha, l1_ratio=beta)  # define elastic net model
#     enm.fit(A.T, M)
#     vmax = enm.coef_
#     v_ir[:, 0] = vmax.T / npl.norm(vmax)
#
#     for i in np.arange(1, dims):
#         A_clean = A
#         for j in range(i):
#             vj = np.expand_dims(v_ir[:, i-1], axis=1)
#             A_clean -= vj @ vj.T @ A
#         # FIXME: MOVE THE GRAM SCHMIDT TO A FUNCTION!!!
#         # Reduce the dimension of data matrix by one and compute new regression
#         A_reduce = A_clean[:-i, :]
#         enm.fit(A_reduce.T, M)
#         vmax1 = enm.coef_
#         # Boost the new vector up to n dimensions
#         boost = np.zeros(i)
#         vmax = np.expand_dims(np.append(vmax1, boost), axis=1)
#         for j in range(i):
#             u = np.expand_dims(v_ir[:, j], axis=1)
#             vmax -= np.dot(vmax.T, u) / np.dot(u.T, u) * u
#         v_ir[:, i] = vmax.T / npl.norm(vmax)
#     return v_ir


# Calculate the time difference between many instances of two events, i.e. stroop stim to key time
# e1 and e2 are lists of strings that represent times. e1 is considered as the first event (earlier in time)
# time_format is a string saying how to decode elements in e1, e2
def time_btw_events(e1, e2, time_format="%H:%M:%S.%f"):
    e1 = e1.to_numpy()
    e2 = e2.to_numpy()
    delta = [(datetime.strptime(e2[i], time_format) - datetime.strptime(e1[i], time_format)).total_seconds()
             for i in range(len(e1))]
    return delta


# Augment the stroop dataset with "sham" stimuli (black visual stimulus after keypress)
# f1, f2 are names of files, whose data to concatenate
# fcsv is the behavior data file path, shared between f1 and f2
def sham_augment(f1, f2, fcsv):
    # Read in data
    behavior1 = pd.read_csv(fcsv)  # This will be copied
    with open(f1, 'rb') as f:
        trials1 = np.load(f)
    with open(f2, 'rb') as f:
        trials2 = np.load(f)

    # Augment the data
    trials = np.concatenate((trials1, trials2), axis=0)
    behavior2 = behavior1.copy(deep=True)
    behavior2['color'] = 'black'
    behavior2['word'] = 'black'
    behavior2['congruent'] = 1
    behavior = pd.concat([behavior1, behavior2])

    # FIXME: SHUFFLE DATA?

    return trials, behavior
