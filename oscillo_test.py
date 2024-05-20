import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime


root = "C:\\Users\\amand\\Documents\\Research\\Project_AHN\\Data_processing\\data\\oscillo_test\\"
py_path = root + "mat_5ms.csv"
os_path = root + "os_5ms_mat.csv"

# Set oscilloscope sampling parameters
srate = 2500  # Sample rate in samples/s
num_sample = 60000
t = np.linspace(0, num_sample/srate, num_sample)

# Get raw Python/Matlab and oscilloscope data
py_pd = np.squeeze(pd.read_csv(py_path).to_numpy())  # FIXME: COULD HAVE ISSUES
os_time = pd.read_csv(os_path, header=None).drop([0, 1])
os_time.rename(columns={1: 'voltage'}, inplace=True)

# Get oscilloscope values and times
volts = os_time['voltage'].astype('float64').to_numpy()
vdiff = np.diff(volts)
vdiff = np.array([0 if (v < 2.4 and v > -2.45) else v for v in vdiff])
rising_time = np.where(vdiff > 0)[0] / srate
falling_time = np.where(vdiff < 0)[0] / srate
fdiff = np.diff(falling_time)

# Get relative python times
# t_ref = datetime.strptime(py_pd[0].split()[1], '%H:%M:%S.%f')  # FIXME: UNCOMMENT FOR PYTHON
t_ref = datetime.strptime(py_pd[0], '%H:%M:%S.%f')
offset = rising_time[0]
py_time = []
for i in range(len(py_pd)):
    # t_i = datetime.strptime(py_pd[i].split()[1], '%H:%M:%S.%f')  # FIXME: UNCOMMENT FOR PYTHON
    t_i = datetime.strptime(py_pd[i], '%H:%M:%S.%f')
    py_time.append((t_i - t_ref).total_seconds() + offset)

# Pulse width statistics
pulse_width = [falling_time[i] - rising_time[i] for i in range(len(rising_time))]
width_av = 1000*np.mean(pulse_width)  # Average width in ms
width_stderr = np.std(pulse_width) / len(pulse_width)

# Python/Matlab-Arduino delay
py_ar_delay = [py_time[i] - rising_time[i] for i in range(len(rising_time))]
py_delay_av = 1000*np.mean(py_ar_delay)  # Average delay in ms
py_delay_stderr = np.std(py_ar_delay) / len(py_ar_delay)

plt.stem(py_time, 5*np.ones(len(py_time)))
# plt.stem(rising_time, 5*np.ones(len(rising_time)), 'r')
# plt.stem(falling_time, 5*np.ones(len(falling_time)), 'k')
plt.plot(t, volts)
plt.show()

print("Hi")
