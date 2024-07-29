from psychopy import event, visual, core
from datetime import datetime
import random
import ssrt_lib as sslib
import Experiments.experiment_lib as exlib  # Library is in a parent folder called "Experiments"


# Parameters: patient
pnum = input("Enter patient number: ")
run = int(input("Enter run number: "))
patient = "p" + pnum
exp_name = "ssrt"
root_path = "C:\\Users\\amand\\Documents\\Research\\Project_AHN\\DD\\Data_processing\\data\\" + patient + "\\"
save_name = patient + "_" + exp_name + str(run) + ".csv"

# Parameters: experiment
if run == 1:
    num_go_trials = 7
    num_stop_trials = 3
else:
    num_go_trials = 70
    num_stop_trials = 30
num_trials = num_go_trials + num_stop_trials
ssd = 0.250

# Behavior metadata
trials = [["stop_signal", "Shape", "stim_time", "rxn_time", "correct", "ssd", "exp_start", "exp_end"]]

# Generate trials
trial_array = [0] * num_trials
x = num_stop_trials
while x > 0:
    stop_trial_index = random.randint(0, (num_trials - 1))
    if trial_array[stop_trial_index] == 0:
        trial_array[stop_trial_index] = 1
        x = x - 1

# Get Arduino port
arduino_plugin = True
a = exlib.return_arduino_port(arduino_plugin)


# Display instructions
win = visual.Window(fullscr=True)
instructions = "Press 'F' as fast as possible if you see a circle and 'J' as fast as possible if you see a square. " \
               "\n\nBut on some trials, a blue dot will appear in the center of the screen after a brief delay. " \
               "\nIf you see the blue dot, do NOT press any key." \
               "\n\nPress 'Enter' to start."
message = visual.TextStim(win, text=instructions, height=0.07)
message.draw(win=None)
message.autoDraw = False
win.flip()
event.waitKeys(keyList=['return'])

#########################################################################################################

# Start the experiment
exlib.write_trigger('start_experiment', a, arduino_plugin, exp_name)
start_time = datetime.now()
exp_start = exlib.return_timestr(start_time, 'date_time')


# # Practice
# message = visual.TextStim(win, text="Let's start with some practice trials")
# message.draw(win=None)
# message.autoDraw = False  # Automatically draw every frame
# win.flip()
# core.wait(2.0)
#
# # practice trials: total of 20
# sslib.practice_right_go_signal(win)
# sslib.practice_right_go_signal(win)
# sslib.practice_left_go_signal(win)
# sslib.practice_right_stop_signal(win, ssd)
# for i in range(16):
#     trial_type = random.randint(0, 1)
#     direction = random.randint(0, 1)
#     if trial_type == 0:
#         if direction == 0:
#             sslib.practice_right_go_signal(win)
#         elif direction == 1:
#             sslib.practice_left_go_signal(win)
#     else:
#         if direction == 0:
#             sslib.practice_right_stop_signal(win, ssd)
#         elif direction == 1:
#             sslib.practice_left_stop_signal(win, ssd)
#
# message = visual.TextStim(win,
#                           text="Now, let's move on to the experiment. Remember: click the 'f' key if you see a circle and the 'j' key if you see a square. Make your responses as fast as possible. However, if you see the red dot, do not press either key.")
# message.draw(win=None)
# message.autoDraw = False  # Automatically draw every frame
# win.flip()
# core.wait(5.0)

# message = visual.TextStim(win, text="Starting now")
# message.draw(win=None)
# message.autoDraw = False  # Automatically draw every frame
# win.flip()
# core.wait(1.5)

# print to make sure it's properly randomized
# print(trial_array)

# Actual Experiment
for i in range(num_trials):
    abs_time = datetime.now()
    seconds = (abs_time - start_time).total_seconds()

    # Pick shape/direction
    trial_type = trial_array[i]
    direction = random.randint(0, 1)

    if direction == 0: shape = "square"
    else: shape = "circle"
    trials.append([trial_type, shape])

    exlib.write_trigger('stim_onset', a, arduino_plugin, exp_name)
    trials[-1].append(exlib.return_timestr(datetime.now(), 'time_only'))
    core.wait(0.5)

    if trial_type == 1:
        if direction == 0:  # right stop signal
            new_ssd, success_flag = sslib.actual_right_stop_signal(win, run, ssd, seconds)

            exlib.write_trigger('choice', a, arduino_plugin, exp_name)
            trials[-1].extend([exlib.return_timestr(datetime.now(), 'time_only'), success_flag, new_ssd])

            ssd = new_ssd
        else:
            new_ssd, success_flag = sslib.actual_left_stop_signal(win, run, ssd, seconds)

            exlib.write_trigger('choice', a, arduino_plugin, exp_name)
            trials[-1].extend([exlib.return_timestr(datetime.now(), 'time_only'), success_flag, new_ssd])

            ssd = new_ssd
    else:
        if direction == 0:  # right go signal
            sslib.actual_right_go_signal(win, run, seconds)

            exlib.write_trigger('choice', a, arduino_plugin, exp_name)
            trials[-1].extend([exlib.return_timestr(datetime.now(), 'time_only'), "None", ssd])
        elif direction == 1:
            sslib.actual_left_go_signal(win, run, seconds)
            exlib.write_trigger('choice', a, arduino_plugin, exp_name)
            trials[-1].extend([exlib.return_timestr(datetime.now(), 'time_only'), "None", ssd])

    if i < num_trials-1:
        trials[-1].extend(['', ''])  # blank spaces for experiment start and end times

    # Blank screen + small delay
    sslib.draw_time(win, seconds)
    win.flip()
    core.wait(0.4)


# End experiment
exlib.write_trigger('end_experiment', a, arduino_plugin, exp_name)
trials[-1].extend([exp_start, exlib.return_timestr(datetime.now(), 'date_time')])


# Saving the data
exlib.save_data(save_name, trials)

# Display thank you message
end_str = f"Task complete!\n\nYou took " + str(round(seconds, 1)) + " seconds."
visual.TextStim(win, text=end_str).draw()
win.flip()
event.waitKeys()  # Wait for any keypress

# Close window
win.close()
