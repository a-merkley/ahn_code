# Delayed Discounting
# edits 6/25
# 7/23: minor adjustments to keypress, screen, and meta file save

from psychopy import visual, event, core
import random
from datetime import datetime
import Experiments.experiment_lib as exlib  # Library is in a parent folder called "Experiments"


# Parameters: patient
pnum = input("Enter patient number: ")
run = int(input("Enter run number: "))
patient = "p" + pnum
exp_name = "dd"
root_path = "C:\\Users\\amand\\Documents\\Research\\Project_AHN\\DD\\Data_processing\\data\\" + patient + "\\"
save_name = patient + "_" + exp_name + "_behavior_run" + str(run) + ".csv"

# Parameters: experiment
num_combinations = 15


# Behavior metadata
trials = [["today_reward", "delay_reward", "delay", "choice", "stim_time", "choice_time", "exp_start", "exp_end"]]

# Trial type specification
reward_delay_combos = [[200, "10 days"], [200, "1 month"], [200, "2 months"], [200, "3 months"], 
[200, "6 months"], [200, "1 year"], [500, "10 days"], [500, "1 month"], [500, "2 months"], [500, "3 months"], 
[500, "1 year"], [500, "6 months"], [1000, "10 days"], [1000, "1 month"], [1000, "2 months"], 
[1000, "3 months"], [1000, "6 months"], [1000, "1 year"], [2000, "10 days"], [2000, "1 month"], [2000, "2 months"], 
[2000, "3 months"], [2000, "6 months"], [2000, "1 year"]]

delay_options = ["10 days", "1 month", "2 months", "3 months", "6 months", "1 year"]  # to display to participants
delay_options_days = [10, 30, 60, 90, 180, 365]  # to calculate area under the curve

chosen = []  # a list to keep track of which options have been chosen already


# Get Arduino port
arduino_plugin = True
a = exlib.return_arduino_port(arduino_plugin)


# Display instructions
win = visual.Window(fullscr=True)

instructions = "Choose the option you prefer with 'F' (left) or 'J' (right)." \
               "\n\nPress 'Enter' to start."
message = visual.TextStim(win, text=instructions)
message.draw(win=None)
message.autoDraw = False
win.flip()
event.waitKeys(keyList=['return'])

#########################################################################################################

# Start the experiment
exlib.write_trigger('start_experiment', a, arduino_plugin, exp_name)
exp_start = exlib.return_timestr(datetime.now(), 'date_time')

while num_combinations > 0:
    i = random.randint(0, 23)  # 24 potential options
    if i not in chosen:
        reward_delay_option = reward_delay_combos[i]
        immediate_reward = reward_delay_option[0]*0.5
        reward_adjustment = immediate_reward*0.5
        delayed_reward = reward_delay_option[0]
        delay = reward_delay_option[1] 
        chosen.append(i) 
        text_clr = 'black'
        text_dim = 35
        for i in range(5): 
            exlib.write_trigger('stim_onset', a, arduino_plugin, exp_name)
            stim_time = exlib.return_timestr(datetime.now(), 'time_only')

            immediate_message = "Gain $" + str(round(immediate_reward, 2)) + " today\n(F)"
            message_immediate = visual.TextStim(win, text=immediate_message, pos=(-0.5, 0.0), bold=True)
            message_immediate.draw(win=None)
            message_immediate.autoDraw = False

            trials.append([immediate_reward, delayed_reward, delay])

            delayed_reward_msg = "Gain $" + str(delayed_reward) + " in " + delay + "\n(J)"
            message_delayed = visual.TextStim(win, text=delayed_reward_msg, pos=(0.5, 0.0), bold=True)
            message_delayed.draw(win=None)
            message_delayed.autoDraw = False
            win.flip()

            keys = event.waitKeys(keyList=['f', 'j'], clearEvents=True)
            if 'f' in keys:
                exlib.write_trigger('choice', a, arduino_plugin, exp_name)
                immediate_reward = immediate_reward - reward_adjustment
                trials[-1].append('immediate')
            elif 'j' in keys:
                exlib.write_trigger('choice', a, arduino_plugin, exp_name)
                immediate_reward = immediate_reward + reward_adjustment
                trials[-1].append('delay')

            choice_time = exlib.return_timestr(datetime.now(), 'time_only')
            trials[-1].extend([stim_time, choice_time])

            reward_adjustment = reward_adjustment*0.5
            core.wait(0.3)

        # Empty the screen
        blank_screen = visual.rect.Rect(win, width=0.5, height=0.5, lineWidth=20,
                                        lineColor=win.color, pos=(0, 0))
        blank_screen.draw(win=None)
        blank_screen.autoDraw = False
        win.flip()
        core.wait(0.5)

        num_combinations = num_combinations - 1


# End experiment
exlib.write_trigger('end_experiment', a, arduino_plugin, exp_name)
trials[-1].extend([exp_start, exlib.return_timestr(datetime.now(), 'date_time')])


# Save file
exlib.save_data(save_name, trials)

# Display thank you message
end_str = f"Task complete!"
visual.TextStim(win, text=end_str).draw()
win.flip()
event.waitKeys()  # Wait for any keypress


