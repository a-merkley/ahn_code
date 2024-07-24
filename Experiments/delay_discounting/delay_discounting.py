# Delayed Discounting
# edits 6/25
# 7/23: minor adjustments to keypress, screen, and meta file save

from psychopy import visual, gui, event, sound, data, core, logging
import random
import numpy as np
import serial
import serial.tools.list_ports
import psychtoolbox as ptb
import csv


# Parameters
patient = "p13"
root_path = "C:\\Users\\amand\\Documents\\Research\\Project_AHN\\DD\\Data_processing\\data\\" + patient + "\\"
save_name = patient + "_dd_behavior.csv"
arduino_plugin = True

# Set screen
win = visual.Window(fullscr=True)
scr_len = win.size[0]
scr_hgt = win.size[1]
x_mid = scr_len / 32
y_mid = scr_hgt / 32

reward_delay_combos = [[200, "10 days"], [200, "1 month"], [200, "2 months"], [200, "3 months"], 
[200, "6 months"], [200, "1 year"], [500, "10 days"], [500, "1 month"], [500, "2 months"], [500, "3 months"], 
[500, "1 year"], [500, "6 months"], [1000, "10 days"], [1000, "1 month"], [1000, "2 months"], 
[1000, "3 months"], [1000, "6 months"], [1000, "1 year"], [2000, "10 days"], [2000, "1 month"], [2000, "2 months"], 
[2000, "3 months"], [2000, "6 months"], [2000, "1 year"]]

chosen = []  #a listto keep track of which options have been chosen already

#reward_options = [50, 100, 200]
delay_options = ["10 days", "1 month", "2 months", "3 months", "6 months", "1 year"]  # to display to participants
delay_options_days = [10, 30, 60, 90, 180, 365]  # to calculate area under the curve
num_combinations = 5
data = [["Delayed reward", "Delay", "Indifference point"]]  # to store data

instructionsClock = core.Clock()
instructionsStim = visual.ImageStim(win=win, name='InstructionsStim',
    image='sin', mask=None,
    ori=0, pos=[0, 0], size=[1500, 1125],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)

instructions = "Choose the option you prefer with 'F' (left) or 'J' (right)." \
               "\n\nPress 'Enter' to start."
message = visual.TextStim(win, text=instructions)
message.draw(win=None)
message.autoDraw = False
win.flip()
event.waitKeys(keyList=['return'])


def write_trigger(trig_type, a):
    switcher = {
        'start_experiment': (8, "uint8"),
        'stim_onset': (5, "uint8"),
        'pt_choice': (6, "uint8"), 
        'end_experiment': (7, "uint8")
    }
    pin, dtype = switcher.get(trig_type, (-1, None))  # FIXME: possible error point, change from -1
    if pin != -1:
        data = np.array([pin], dtype=dtype)
        a.write(data)  # FIXME: Uncomment when actual hardware is connected


if arduino_plugin:
    ports = serial.tools.list_ports.comports()
    if not ports:
        print("No ports available now. Please check if Arduino is plugged in.")
        exit()
    port = ports[-1].device
    a = serial.Serial(port, 115200)
else:
    a = None
    

write_trigger('start_experiment', a)
while num_combinations > 0:
    i = random.randint(0, 23)  # 24 potential options
    if not i in chosen: 
        reward_delay_option = reward_delay_combos[i]
        immediate_reward = reward_delay_option[0]*0.5
        reward_adjustment = immediate_reward*0.5
        delayed_reward = reward_delay_option[0]
        delay = reward_delay_option[1] 
        chosen.append(i) 
        text_clr = 'black'
        text_dim = 35
        for i in range(5): 
            write_trigger('stim_onset', a)

            immediate_message = "Gain $" + str(round(immediate_reward, 2)) + " today\n('F')"
            message_immediate = visual.TextStim(win, text=immediate_message, pos=(-0.5, 0.0), bold=True)
            message_immediate.draw(win=None)
            message_immediate.autoDraw = False

            delayed_reward_msg = "Gain $" + str(delayed_reward) + " in " + delay + "\n('J')"
            message_delayed = visual.TextStim(win, text=delayed_reward_msg, pos=(0.5, 0.0), bold=True)
            message_delayed.draw(win=None)
            message_delayed.autoDraw = False
            win.flip()

            keys = event.waitKeys(keyList=['f', 'j'], clearEvents=True)
            if 'f' in keys:
                write_trigger('pt_choice', a)
                immediate_reward = immediate_reward - reward_adjustment
            elif 'j' in keys:
                write_trigger('pt_choice', a)
                immediate_reward = immediate_reward + reward_adjustment
            reward_adjustment = reward_adjustment*0.5
            blank_screen = visual.rect.Rect(win, width=0.5, height=0.5, lineWidth=20,
                                            lineColor=win.color, pos=(0, 0))
            blank_screen.draw(win=None)
            blank_screen.autoDraw = False
            win.flip() 
            core.wait(0.75)
        delay_index = delay_options.index(delay)
        delay_days = delay_options_days[delay_index] 
        data.append([delayed_reward, delay_days, immediate_reward])
        num_combinations = num_combinations - 1
    
        
        
write_trigger('end_experiment', a)


with open(save_name, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data) 


