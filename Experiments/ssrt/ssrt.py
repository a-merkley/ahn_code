from psychopy import event, visual
from datetime import datetime
import random
from serial.tools import list_ports
import serial
import ssrt_lib as sslib


# Parameters: patient
patient = "p13"
root_path = "C:\\Users\\amand\\Documents\\Research\\Project_AHN\\DD\\Data_processing\\data\\" + patient + "\\"
save_name = patient + "_ssrt_behavior.csv"

# Parameters: experiment
num_go_trials = 100
num_stop_trials = 50
num_trials = num_go_trials + num_stop_trials
ssd = 0.250

# Create place to store trial data
trials = [["Type", "Shape", "stim_time", "rxn_time", "correct", "ssd"]]

# Generate trials
trial_array = [0] * num_trials
x = num_stop_trials
while x > 0:
    stop_trial_index = random.randint(0, (num_trials - 1))
    if trial_array[stop_trial_index] == 0:
        trial_array[stop_trial_index] = 1
        x = x - 1

arduino_plugin = True
if arduino_plugin:
    ports = list_ports.comports()
    if not ports:
        print("No ports available now. Please check if Arduino is plugged in.")
    port = ports[-1].device
    a = serial.Serial(port, 115200)
else:
    input("WARNING: YOU ARE RUNNING THE EXPERIMENT WITHOUT ARDUINO PLUGGED IN. PRESS ENTER TO PROCEED. ")
    a = None


# Display instructions
win = visual.Window(fullscr=True)
# win = visual.Window([600, 600])
instructions = "Press 'F' as fast as possible if you see a circle and 'J' as fast as possible if you see a square. " \
               "\n\nBut on some trials, a red dot will appear in the center of the screen after a brief delay. " \
               "\nIf you see the red dot, do NOT press any key." \
               "\n\nPress 'Enter' to start."
message = visual.TextStim(win, text=instructions, height=0.07)
message.draw(win=None)
message.autoDraw = False
win.flip()
event.waitKeys(keyList=['return'])

# Start the experiment
sslib.write_trigger('start_experiment', a)


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
    # Pick shape/direction
    trial_type = trial_array[i]
    direction = random.randint(0, 1)

    if direction == 0: shape = "square"
    else: shape = "circle"
    trials.append([trial_type, shape])

    sslib.write_trigger('stim_onset', a)
    trials[-1].append(sslib.return_timestr(datetime.now(), 'time_only'))

    if trial_type == 1:
        if direction == 0:  # right stop signal
            new_ssd, success_flag = sslib.actual_right_stop_signal(win, ssd)

            sslib.write_trigger('button_press', a)  # FIXME: check arduino for difference btw button_press & successful stop
            trials[-1].extend([sslib.return_timestr(datetime.now(), 'time_only'), success_flag, new_ssd])

            ssd = new_ssd
        else:
            new_ssd, success_flag = sslib.actual_left_stop_signal(win, ssd)

            sslib.write_trigger('button_press', a)  # FIXME: check arduino for difference btw button_press & successful stop
            trials[-1].extend([sslib.return_timestr(datetime.now(), 'time_only'), success_flag, new_ssd])

            ssd = new_ssd
    else:
        if direction == 0:  # right go signal
            sslib.actual_right_go_signal(win)

            sslib.write_trigger('button_press', a)
            trials[-1].extend([sslib.return_timestr(datetime.now(), 'time_only'), "None", ssd])
        elif direction == 1:
            sslib.actual_left_go_signal(win)
            sslib.write_trigger('button_press', a)
            trials[-1].extend([sslib.return_timestr(datetime.now(), 'time_only'), "None", ssd])


# Saving the data
sslib.save_data(save_name, trials)

# Display thank you message
end_str = f"Task complete!"
visual.TextStim(win, text=end_str).draw()
win.flip()
event.waitKeys()  # Wait for any keypress

# Close window
win.close()
