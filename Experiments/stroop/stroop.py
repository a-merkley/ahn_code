# Stroop word-color task

from psychopy import visual, event, core
import numpy.random as npr
from datetime import datetime
import Experiments.experiment_lib as exlib  # Library is in a parent folder called "Experiments"


# Parameters: patient
pnum = input("Enter patient number: ")
run = int(input("Enter run number: "))
patient = "p" + pnum
exp_name = "stroop"
root_path = "C:\\Users\\amand\\Documents\\Research\\Project_AHN\\DD\\Data_processing\\data\\" + patient + "\\"
save_name = patient + "_" + exp_name + str(run) + ".csv"

# Parameters: experiment
if run == 1:
    num_trials = 10
    delay_keywait = 3.0
else:
    num_trials = 50
    delay_keywait = 1.5
percent_ctrl = 0.2
delay_fixation = 2.0

# Behavior metadata
trials = [["word", "color", "control", "congruent", "response", "correct",
           "stim_time", "key_time", "start_experiment", "end_experiment"]]

color_arr = ["red", "green", "blue"]
word_arr = ["RED", "GREEN", "BLUE"]
control_words = ["CHAIR", "MUG", "BLANKET", "BIRD", "TABLE", "PEN"]  #FIXME: NEED CITATIONS


def generate_trials(num_trials, percent_ctrl, c_arr, w_arr, ctrl_arr):
    num_ctrl = round(num_trials * percent_ctrl)
    num_true = num_trials - num_ctrl
    num_cgr = round(0.5*num_true)
    num_icgr = num_true - num_cgr

    # Create control sequence
    ctrl_w = list(npr.choice(ctrl_arr, num_ctrl))
    ctrl_c = list(npr.choice(c_arr, num_ctrl))

    # Create balanced incongruent sequence
    icgr_w_idx_raw = num_icgr * [0, 1, 2]
    rand_start = npr.choice([0, 1])
    icgr_w_idx = npr.permutation(icgr_w_idx_raw[rand_start:num_icgr+rand_start])
    rand_sum_raw = num_icgr * [1, 2]
    rand_sum = npr.permutation(rand_sum_raw[:num_icgr])
    icgr_c_idx = (icgr_w_idx + rand_sum) % 3  # FIXME: check balancing on this
    icgr_w = [w_arr[j] for j in icgr_w_idx]
    icgr_c = [c_arr[j] for j in icgr_c_idx]

    # Create congruent sequence
    cgr_w = num_cgr * [0, 1, 2]
    rand_start = npr.choice([0, 1])
    cgr_idx = npr.permutation(cgr_w[rand_start:num_cgr+rand_start])
    cgr_w = [w_arr[j] for j in cgr_idx]
    cgr_c = [c_arr[j] for j in cgr_idx]

    # Concatenate and mix up words/colors
    word_seq = ctrl_w + icgr_w + cgr_w
    color_seq = ctrl_c + icgr_c + cgr_c
    mixer = npr.permutation(list(zip(word_seq, color_seq)))
    word_seq, color_seq = zip(*mixer)

    return list(word_seq), list(color_seq)


# Generate trials
words, colors = generate_trials(num_trials, percent_ctrl, color_arr, word_arr, control_words)


# Get Arduino port
arduino_plugin = False
a = exlib.return_arduino_port(arduino_plugin)


# Display instructions
win = visual.Window(fullscr=True)
instructions = "Words written in different colors will be presented to you." \
               "Choose the *COLOR* of the word as either RED (1), GREEN (2), or BLUE (3)." \
               "\n\nYou have " + str(delay_keywait) + "s to respond after the word appears." \
               "\n\nPress 'Enter' to start."
message = visual.TextStim(win, text=instructions)
message.draw(win=None)
message.autoDraw = False
win.flip()
event.waitKeys(keyList=['return'])




#########################################################################################################

# Start the experiment
exlib.write_trigger('start_experiment', a, arduino_plugin, exp_name)
start_time = exlib.return_timestr(datetime.now(), 'date_time')

for i in range(num_trials):
    # Save experiment parameters
    if words[i] in word_arr: ctrl_flag = 0
    else: ctrl_flag = 1
    if words[i].lower() == colors[i].lower(): cgr_flag = 1
    else: cgr_flag = 0
    trials.append([words[i], colors[i], ctrl_flag, cgr_flag])

    # Show white fixation cross
    trial_start = visual.TextStim(win, text='+', color=(255, 255, 255), height=0.5)
    trial_start.draw(win=None)
    trial_start.autoDraw = False  # Automatically draw each frame is set to false for this message
    win.flip()
    core.wait(delay_fixation)

    # Show word/color for limited time
    total = visual.TextStim(win, text=words[i], color=colors[i], height=0.5)
    total.draw(win=None)
    total.autoDraw = False
    win.flip()
    exlib.write_trigger('stim_onset', a, arduino_plugin, exp_name)  # indicates end of waiting time
    stim_time = exlib.return_timestr(datetime.now(), 'time_only')

    # Record button press or end of trial
    keys = event.waitKeys(keyList=['1', '2', '3'], clearEvents=True, maxWait=delay_keywait)
    exlib.write_trigger('choice', a, arduino_plugin, exp_name)  # indicates end of waiting time
    choice_time = exlib.return_timestr(datetime.now(), 'time_only')

    # Save choices
    if keys is None: choice = "None"
    elif keys[0] == '1': choice = "red"
    elif keys[0] == '2': choice = "green"
    elif keys[0] == '3': choice = "blue"
    if choice == colors[i]: correct_flag = 1
    else: correct_flag = 0
    trials[-1].extend([choice, correct_flag, stim_time, choice_time])

    # Small delay
    core.wait(0.3)


# End experiment
exlib.write_trigger('end_experiment', a, arduino_plugin, exp_name)  # indicates end of waiting time
end_time = exlib.return_timestr(datetime.now(), 'date_time')
trials[-1].extend([start_time, end_time])

# Save file
exlib.save_data(save_name, trials)

# Display thank you message
end_str = f"Task complete!"
visual.TextStim(win, text=end_str).draw()
win.flip()
event.waitKeys()  # Wait for any keypress
