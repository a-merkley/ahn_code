'''
Library of functions used in all experiments
'''

import numpy as np
import csv
import serial
from serial.tools import list_ports


def return_arduino_port(arduino_plugin):
    if arduino_plugin:
        ports = list_ports.comports()
        if not ports:
            print("No ports available now. Please check if Arduino is plugged in.")
            exit()
        port = ports[-1].device
        a = serial.Serial(port, 115200)
    else:
        input("WARNING: YOU ARE RUNNING THE EXPERIMENT WITHOUT ARDUINO PLUGGED IN. PRESS ENTER TO PROCEED. ")
        a = None
    return a


def write_trigger(trig_type, a, arduino_plugin, exp_name):
    if exp_name == "dd" or exp_name == "ssrt" or exp_name == "stroop":
        switcher = {
            'start_experiment': (8, "uint8"),
            'stim_onset': (5, "uint8"),  # FIXME: check this for stroop
            'choice': (6, "uint8"),
            'end_experiment': (7, "uint8")
        }
    elif exp_name == "rutledge":
        switcher = {
            'start_experiment': (8, "uint8"),
            'stim_onset': (5, "uint8"),
            'choice': (6, "uint8"),
            'answer_showing': (7, "uint8")
        }
    elif exp_name == "bart":
        pass
    else:
        print("Invalid experiment name: " + exp_name)
    pin, dtype = switcher.get(trig_type, (-1, None))  # FIXME: possible error point, change from -1
    if pin != -1:
        data = np.array([pin], dtype=dtype)
        if arduino_plugin:
            a.write(data)


def return_timestr(d, conversion):
    ms = str(d.second)
    if conversion == 'time_only':
        timestr = str(d).split()
        timechar = timestr[1]
        return_time = f"{timechar[:-2]}{ms}"
    elif conversion == 'date_time':
        datechar = str(d)
        return_time = f"{datechar[:-2]}{ms}"
    return return_time


def save_data(fname, data_lst):
    with open(fname, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data_lst)