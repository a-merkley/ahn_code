'''
Rutledge task

Two random lotteries appear on the left and right side of the screen. Subject needs to select between left or right
lotteries. One lottery will always be a decoy, meaning it will always produce negative rewards and detract from a total.

Output csv file description:

- Observation setting
    1 = 25% (positive) reward, 2 = 50% reward, 3 = 75% reward
- Decoy setting
    0 = 0% dc1, 1 = 25% dc1, 2 = 50% dc1, 3 = 75% dc1, 4 = 100% dc1, where dc1 is the decoy1 reward
- decoy1 reward
    the randomized reward for decoy1
- decoy2 reward
    the randomized reward for decoy2
- observation position
    Describes whether observation lottery appears on left or right side
- choice
    None = did not respond, Observation = chose observation lottery, Decoy = chose decoy lottery
- gain
    which randomized reward the subject received
- total
    tracks the overall amount of money in the experiment
'''


from psychopy import visual, core, event
import rutledge_lib as rlib
import random
from serial.tools import list_ports
import serial
import numpy as np

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


#Trigger function
def write_trigger(trig_type, a):
  switcher = {
      'start_experiment': (8, "uint8"),
      'stim_onset': (5, "uint8"),
      'button_press': (6, "uint8"),
      'answer_showing': (7, "uint8")
  }
  pin, dtype = switcher.get(trig_type, (-1, None))
  if pin != -1:
    data = np.array([pin], dtype=dtype)
    a.write(data)  # FIXME: Uncomment when actual hardware is connected


trials = [["obs_setting", "decoy_setting", "decoy1_reward", "decoy2_reward", "obs_position", "choice", "gain", "total"]]
lottery_picks = [["Observation"]]


# Display instructions
win = visual.Window(fullscr=True)  #Instantiating a window space
# win = visual.Window([600, 600])  #Instantiating a window space  # for debugging

instructions = "Choose between two lotteries after the white fixation cross disappears: " \
               "press 'F' for left and 'J' for right. You then randomly receive one of the rewards." \
               "\n\nIf no option is chosen within 1.25 seconds, you will automatically lose $10.\nTry to maximize your reward!" \
               "\n\nPress 'Enter' to start."
visual.TextStim(win, text=instructions).draw()
win.flip()
event.waitKeys(keyList=['return'])



###########################################################################################################
###########################################################################################################
# Parameters: patient
patient = "p13"
num_trials = 10
root_path = "C:\\Users\\amand\\Documents\\Research\\Project_AHN\\DD\\Data_processing\\data\\" + patient + "\\"
save_name = patient + "_rutledge_behavior.csv"

# Parameters: experiment
delay_choice = 1.0
delay_outcome = 2.0
total_money = 500

probabilities = {
    0: rlib.draw_0,
    1: rlib.draw_25,
    2: rlib.draw_50,
    3: rlib.draw_75,
    4: rlib.draw_100
}

probabilities_answer = {
    0: rlib.draw_0,
    1: rlib.answer_25,
    2: rlib.answer_50,
    3: rlib.answer_75,
    4: rlib.draw_100
}

decoy_probabilities = {
    
    0: rlib.decoy_0,
    1: rlib.decoy_25,
    2: rlib.decoy_50,
    3: rlib.decoy_75,
    4: rlib.decoy_100
}

decoy_answer_probabilities = {
    
    0: rlib.decoy_answer_0,
    1: rlib.decoy_answer_25,
    2: rlib.decoy_answer_50,
    3: rlib.decoy_answer_75,
    4: rlib.decoy_answer_100
}

decoy_options = ["+$0", "-$1", "-$2", "-$3", "-$4", "-$5", "-$10"]

#########################################################################################################

write_trigger('start_experiment', a)

while num_trials > 0:
    rlib.total_money_txt(win, total_money)

    # Fixation
    i = random.randint(1, 3)  # Randomizer for observation lottery
                              # 1 = 25% reward, 2 = 50% reward, 3 = 75% reward
    x = random.randint(0, 4)  # Randomizer for decoy lottery
                              # 0 = 0% dc1, 1 = 25% dc1, 2 = 50% dc1, 3 = 75% dc1, 4 = 100% dc1

    # Set randomized decoy rewards
    decoy1_idx = random.randint(0, len(decoy_options) - 1)
    decoy2_idx = random.randint(0, len(decoy_options) - 1)
    dc1 = decoy_options[decoy1_idx]
    dc2 = decoy_options[decoy2_idx]

    # Initialize decoy side (left or right)
    decoy_side = np.random.choice([-1, 1])  # -1 = left, 1 = right
    prob_side = -1 * decoy_side
    if prob_side == -1: prob_side_str = "left"
    else: prob_side_str = "right"

    # Save settings
    trials.append([str(i), str(x), rlib.decoy_str2int(dc1), rlib.decoy_str2int(dc2), prob_side_str])

    write_trigger('stim_onset', a)

    # Options
    trial_start = visual.TextStim(win, text='+', color=(255, 255, 255), height=0.5)
    trial_start.draw(win=None)
    trial_start.autoDraw = False  # Automatically draw each frame is set to false for this message
    probabilities[i](win, prob_side)
    decoy_probabilities[x](win, dc1, dc2, decoy_side)
    win.flip()
    core.wait(2.5)

    # Choice
    rlib.total_money_txt(win, total_money)
    probabilities[i](win, prob_side)
    decoy_probabilities[x](win, dc1, dc2, decoy_side)
    win.flip()
    keys = event.waitKeys(keyList=['f', 'j'], clearEvents=True, maxWait=1.25)
    write_trigger('button_press', a)  # indicates end of waiting time

    if keys == None:
        core.wait(0.3)  # Brief pause
        write_trigger('answer_showing', a)
        trials[-1].extend(["None", "None"])
        complete_loss_message = 'Time out! You have lost $10.'
        message = visual.TextStim(win, text=complete_loss_message)
        message.draw(win=None)
        message.autoDraw = False
        total_money -= 10
        rlib.total_money_txt(win, total_money)
        win.flip()
        core.wait(4.0)
    elif ('f' in keys and decoy_side == 1) or ('j' in keys and decoy_side == -1):
        # write_trigger('button_press', a)
        lottery_picks.append([1])
        # Delay
        probabilities[i](win, prob_side)
        rlib.total_money_txt(win, total_money)
        win.flip()
        core.wait(delay_choice)
        # Outcome
        write_trigger('answer_showing', a)
        gain = probabilities_answer[i](win, prob_side)
        total_money += gain
        rlib.total_money_txt(win, total_money)
        win.flip()
        core.wait(delay_outcome)
        trials[-1].extend(["Observation", str(gain)])
    elif ('j' in keys and decoy_side == 1) or ('f' in keys and decoy_side == -1):
        # write_trigger('button_press', a)
        lottery_picks.append([0])
        # Delay
        decoy_probabilities[x](win, dc1, dc2, decoy_side)
        rlib.total_money_txt(win, total_money)
        win.flip()
        core.wait(delay_choice)
        # Outcome
        write_trigger('answer_showing', a)
        gain = decoy_answer_probabilities[x](win, dc1, dc2, decoy_side)
        total_money += gain
        rlib.total_money_txt(win, total_money)
        win.flip()
        core.wait(delay_outcome)
        trials[-1].extend(["Decoy", str(-gain)])

    trials[-1].append(str(total_money))

    num_trials = num_trials - 1


write_trigger('end_experiment', a)

# Saving the data
rlib.save_data(save_name, trials)

# Display thank you message
end_str = "Task complete!\n\nYou earned $" + str(total_money) + "."
visual.TextStim(win, text=end_str).draw()
win.flip()
event.waitKeys()  # Wait for any keypress

# Close window
win.close()
