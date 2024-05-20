# Imports
import nelpy as nel
import scipy.io
from scipy import signal
from copy import *


def band_noise_filter(asa_in, lower=0.1, upper=360, noise_freq=60):
    '''
    Inputs:
        asa_in     - the AnalogSignalArray to be bandpass filtered and notched for noise removal.
        lower      - the lower cutoff frequency for the bandpass filter. Must be greater than 0 Hz, 
                     default is 0.1 Hz.
        upper      - the upper cutoff frequency for the bandpass filter, default is 360 Hz.
        noise_freq - the frequency to be removed, along with its harmonics, representing line noise.
    
    Outputs:
        An AnalogSignalArray containing the bandpass filtered, notched signal with the same support
        as the input signal.
    '''

    # High pass filter to remove slow signal drift
    b,a = signal.butter(4, lower, btype='highpass', fs=asa_in.fs)
    hpass = signal.filtfilt(b, a, asa_in.data)
    denoising = deepcopy(hpass)

    # Notch filter to remove 60 Hz noise and its harmonics
    for num in range(1, int(asa_in.fs/(2*noise_freq))):
        harmonic = num*noise_freq
        b, a = signal.iirnotch(harmonic, 100, asa_in.fs)
        notch_inc = signal.filtfilt(b, a, denoising)
        denoising = deepcopy(notch_inc)

    # Create ASA with same support as asa_in, but change signal content
    no_stim_band_noiseless = deepcopy(asa_in)
    no_stim_band_noiseless.data = denoising
    return no_stim_band_noiseless