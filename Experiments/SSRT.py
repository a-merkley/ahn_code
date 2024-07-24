from psychopy import core, data, event, gui, sound, visual
import numpy as np
import array as arr
import random
import csv
import serial
import psychtoolbox as ptb
from psychopy.visual.circle import Circle

num_go_trials = 96
num_stop_trials = 32
num_trials = num_go_trials + num_stop_trials
ssd = 0.250

arduino_plugin = True
if arduino_plugin:
    ports = serial.tools.list_ports.comports()
    if not ports:
        print("No ports available now. Please check if Arduino is plugged in.")
    port = ports[-1].device
    a = serial.Serial(port, 115200)
else:
    a = None


import struct
from scipy import signal as sg

sampling_rate = 44100
freq = 440
samples = 44100
x = np.arange(samples)

# y = 100*np.sin(2*np.pi*freq*x/sampling_rate)
# f = open("test.wav", 'wb')
# for i in y:
#     f.write(struct.pack('b', int(i)))
# f.close()


# import random, struct
# import wave
#
# SAMPLE_LEN = 1323000  # 30 seconds of random audio
#
# noise_output = wave.open('noise2.wav', 'w')
# noise_output.setparams((2, 2, 44100, 0, 'NONE', 'not compressed'))
#
# values = []
#
# for i in range(0, SAMPLE_LEN):
#         value = random.randint(-32767, 32767)
#         packed_value = struct.pack('h', value)
#         values.append(packed_value)
#         values.append(packed_value)
#
# value_str = ''.join(values)
# noise_output.writeframes(value_str)
#
# noise_output.close()
#
#
#
# from playsound import playsound
# print("Testing")
# playsound('C:\\Users\\amand\\Documents\\Research\\Project_AHN\\Data_processing\\ahn_code\\Experiments\\test.wav')
#
# from pydub import AudioSegment
# from pydub.playback import play
#
# # for playing wav file
# song = AudioSegment.from_wav("C:\\Users\\amand\\Documents\\Research\\Project_AHN\\Data_processing\\ahn_code\\Experiments\\test.wav")
# print('playing sound using  pydub')
# play(song)


# mySound = sound.Sound('A')
# now = ptb.GetSecs()
# mySound.play(when=now+0.5)

#Trigger function
def write_trigger(trig_type, a):
  switcher = {
      'start_experiment': (8, "uint8"),
      'stim_onset': (5, "uint8"),
      'button_press': (6, "uint8"),
      'successful_stop': (7, "uint8")
  }
  pin, dtype = switcher.get(trig_type, (-1, None))
  if pin != -1:
    data = np.array([pin], dtype=dtype)
    a.write(data)  # FIXME: Uncomment when actual hardware is connected


# Display instructions
win = visual.Window([600,600])
message = visual.TextStim(win, text="Press 'F' as fast as possible if you see a circle and 'J' as fast as possible if you see a square. "
                                     "But on some trials, a sound will play shortly after the shape is presented. "
                                     "If you hear the sound, do NOT press any key."
                                    "\n\nPress 'Enter' to start.",
                          height=0.07)
message.draw(win=None)
message.autoDraw = False
win.flip()
event.waitKeys(keyList=['return'])

message = visual.TextStim(win, text="Let's start with some practice trials")
message.draw(win=None)
message.autoDraw = False  # Automatically draw every frame
win.flip()
core.wait(5.0)

#Creating a clock to measure response times
respClock = core.Clock()

# Create place to store trial data
trials = data.TrialHandler(trialList=[], nReps=2)
go_trials = [["Reaction time"]]
stop_trials = [["ssd", "Stop trial outcome"]]


def save_data(fname, data_lst):
    with open(fname, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data_lst)


# displays the start of a new trial
def trialStart():
    trial_start = visual.TextStim(win, text='+', color=(255, 255, 255), height=0.5)
    trial_start.draw(win=None)
    trial_start.autoDraw = False  # Automatically draw every frame
    win.flip()
    core.wait(0.250)


# displays one go signal
def actual_right_go_signal():
    trialStart()
    go_signal_right = visual.rect.Rect(win, width=0.5, height=0.5, lineWidth=20, lineColor=(255, 255, 255), pos=(0, 0))
    go_signal_right.draw(win=None)
    go_signal_right.autoDraw = False
    visual.rect.Rect(win, width=0.022, height=0.022, lineColor=(255, 255, 255), pos=(0.25, 0.25), fillColor=True).draw(
        win=None)
    visual.rect.Rect(win, width=0.022, height=0.022, lineColor=(255, 255, 255), pos=(-0.25, 0.25), fillColor=True).draw(
        win=None)
    visual.rect.Rect(win, width=0.022, height=0.022, lineColor=(255, 255, 255), pos=(0.25, -0.25), fillColor=True).draw(
        win=None)
    visual.rect.Rect(win, width=0.022, height=0.022, lineColor=(255, 255, 255), pos=(-0.25, -0.25),
                     fillColor=True).draw(win=None)
    win.flip()
    respClock.reset()
    # wait for response
    keys = event.waitKeys(keyList=['j'])
    write_trigger('button_press', a)
    rt_go1 = respClock.getTime()  # metadata
    # trials.addData('go trial reaction times', rt_go1)
    go_trials.append([rt_go1])


def practice_right_go_signal():
    trialStart()
    go_signal_right = visual.rect.Rect(win, width=0.5, height=0.5, lineWidth=20, lineColor=(255, 255, 255), pos=(0, 0))
    go_signal_right.draw(win=None)
    go_signal_right.autoDraw = False
    visual.rect.Rect(win, width=0.022, height=0.022, lineColor=(255, 255, 255), pos=(0.25, 0.25), fillColor=True).draw(
        win=None)
    visual.rect.Rect(win, width=0.022, height=0.022, lineColor=(255, 255, 255), pos=(-0.25, 0.25), fillColor=True).draw(
        win=None)
    visual.rect.Rect(win, width=0.022, height=0.022, lineColor=(255, 255, 255), pos=(0.25, -0.25), fillColor=True).draw(
        win=None)
    visual.rect.Rect(win, width=0.022, height=0.022, lineColor=(255, 255, 255), pos=(-0.25, -0.25),
                     fillColor=True).draw(win=None)
    win.flip()
    respClock.reset()
    # wait for response
    keys = event.waitKeys(keyList=['j'])
    rt_go1 = respClock.getTime()  # metadata
    # trials.addData('go trial reaction times', rt_go1)
    go_trials.append([rt_go1])


# displays the other go signal
def actual_left_go_signal():
    trialStart()
    go_signal_left = visual.circle.Circle(win, radius=0.25, lineWidth=20, lineColor=(255, 255, 255), fillColor=None)
    go_signal_left.draw(win=None)
    go_signal_left.autoDraw = False
    win.flip()
    respClock.reset()
    # wait for response
    keys = event.waitKeys(keyList=['f'])
    write_trigger('button_press', a)
    rt_go2 = respClock.getTime()  # metadata
    # trials.addData('go trial reaction times', rt_go2)
    go_trials.append([rt_go2])


def practice_left_go_signal():
    trialStart()
    go_signal_left = visual.circle.Circle(win, radius=0.25, lineWidth=20, lineColor=(255, 255, 255), fillColor=None)
    go_signal_left.draw(win=None)
    go_signal_left.autoDraw = False
    win.flip()
    respClock.reset()
    # wait for response
    keys = event.waitKeys(keyList=['f'])
    rt_go2 = respClock.getTime()  # metadata
    # trials.addData('go trial reaction times', rt_go2)
    go_trials.append([rt_go2])


# Displays one stop signal
def actual_right_stop_signal(ssd):
    trialStart()
    stop_signal_right = visual.rect.Rect(win, width=0.5, height=0.5, lineWidth=20,
                                         lineColor=(255, 255, 255), pos=(0, 0))
    stop_signal_right.draw(win=None)
    stop_signal_right.autoDraw = False
    visual.rect.Rect(win, width=0.022, height=0.022, lineColor=(255, 255, 255), pos=(0.25, 0.25), fillColor=True).draw(
        win=None)
    visual.rect.Rect(win, width=0.022, height=0.022, lineColor=(255, 255, 255), pos=(-0.25, 0.25), fillColor=True).draw(
        win=None)
    visual.rect.Rect(win, width=0.022, height=0.022, lineColor=(255, 255, 255), pos=(0.25, -0.25), fillColor=True).draw(
        win=None)
    visual.rect.Rect(win, width=0.022, height=0.022, lineColor=(255, 255, 255), pos=(-0.25, -0.25),
                     fillColor=True).draw(win=None)
    win.flip()
    respClock.reset()
    # Play sound cue
    mySound = sound.Sound('A')
    now = ptb.GetSecs()
    mySound.play(when=ssd)
    keys = event.waitKeys(maxWait=1.25, keyList=['j'])
    if keys != None:
        write_trigger('button_press', a)
        # trials.addData('failed stops', 1)
        stop_trials.append([ssd, "Failure"])
        ssd = ssd - 0.050
    else:
        # trials.addData('successful stops', 1)
        write_trigger('successful_stop', a)
        stop_trials.append([ssd, "Success"])
        ssd = ssd + 0.050
    return ssd


def practice_right_stop_signal(ssd):
    trialStart()
    stop_signal_right = visual.rect.Rect(win, width=0.5, height=0.5, lineWidth=20,
                                         lineColor=(255, 255, 255), pos=(0, 0))
    stop_signal_right.draw(win=None)
    stop_signal_right.autoDraw = False
    visual.rect.Rect(win, width=0.022, height=0.022, lineColor=(255, 255, 255), pos=(0.25, 0.25), fillColor=True).draw(
        win=None)
    visual.rect.Rect(win, width=0.022, height=0.022, lineColor=(255, 255, 255), pos=(-0.25, 0.25), fillColor=True).draw(
        win=None)
    visual.rect.Rect(win, width=0.022, height=0.022, lineColor=(255, 255, 255), pos=(0.25, -0.25), fillColor=True).draw(
        win=None)
    visual.rect.Rect(win, width=0.022, height=0.022, lineColor=(255, 255, 255), pos=(-0.25, -0.25),
                     fillColor=True).draw(win=None)
    win.flip()
    respClock.reset()
    # Play sound cue
    mySound = sound.Sound('A')
    now = ptb.GetSecs()
    mySound.play(when=ssd)
    keys = event.waitKeys(maxWait=1.25, keyList=['j'])
    if keys != None:
        message = visual.TextStim(win, text='Failure!')
        message.draw(win=None)
        message.autoDraw = False
        win.flip()
        core.wait(2.0)
        # trials.addData('failed stops', 1)
        stop_trials.append([ssd, "Failure"])
        ssd = ssd - 0.050
    else:
        message = visual.TextStim(win, text='Success!')
        message.draw(win=None)
        message.autoDraw = False
        # count = count+1
        win.flip()
        core.wait(2.0)
        # trials.addData('successful stops', 1)
        stop_trials.append([ssd, "Success"])
        ssd = ssd + 0.050
    return ssd


# Displays other stop signal
def actual_left_stop_signal(ssd):
    trialStart()
    stop_signal_left = visual.circle.Circle(win, radius=0.25, lineWidth=20,
                                            lineColor=(255, 255, 255), fillColor=None)
    stop_signal_left.draw(win=None)
    stop_signal_left.autoDraw = False
    win.flip()
    respClock.reset()
    # Play sound cue
    mySound = sound.Sound('A')
    now = ptb.GetSecs()
    mySound.play(when=ssd)  # Play in exactly 0.25s
    keys = event.waitKeys(maxWait=1.25, keyList=['f'])
    if keys != None:
        write_trigger('button_press', a)
        # trials.addData('failed stops', 1)
        stop_trials.append([ssd, "Failure"])
        ssd = ssd - 0.050
    else:
        # trials.addData('successful stops', 1)
        write_trigger('successful_stop', a)
        stop_trials.append([ssd, "Success"])
        ssd = ssd + 0.050
    return ssd


def practice_left_stop_signal(ssd):
    trialStart()
    stop_signal_left = visual.circle.Circle(win, radius=0.25, lineWidth=20,
                                            lineColor=(255, 255, 255), fillColor=None)
    stop_signal_left.draw(win=None)
    stop_signal_left.autoDraw = False
    win.flip()
    respClock.reset()
    # Play sound cue
    mySound = sound.Sound('A')
    now = ptb.GetSecs()
    mySound.play(when=ssd)  # Play in exactly 0.25s
    keys = event.waitKeys(maxWait=1.25, keyList=['f'])
    if keys != None:
        message = visual.TextStim(win, text='Failure!')
        message.draw(win=None)
        message.autoDraw = False
        win.flip()
        core.wait(2.0)
        # trials.addData('failed stops', 1)
        stop_trials.append([ssd, "Failure"])
        ssd = ssd - 0.050
    else:
        message = visual.TextStim(win, text='Success!')
        message.draw(win=None)
        message.autoDraw = False
        # count = count+1
        win.flip()
        core.wait(2.0)
        # trials.addData('successful stops', 1)
        stop_trials.append([ssd, "Success"])
        ssd = ssd + 0.050
    return ssd


# practice trials: total of 20
practice_right_go_signal()
practice_right_go_signal()
practice_left_go_signal()
practice_right_stop_signal(ssd)
for i in range(16):
    trial_type = random.randint(0, 1)
    direction = random.randint(0, 1)
    if trial_type == 0:
        if direction == 0:
            practice_right_go_signal()
        elif direction == 1:
            practice_left_go_signal()
    else:
        if direction == 0:
            practice_right_stop_signal(ssd)
        elif direction == 1:
            practice_left_stop_signal(ssd)

write_trigger('start_experiment', a)
message = visual.TextStim(win,
                          text="Now, let's move on to the experiment. Remember: click the 'f' key if you see a circle and the 'j' key if you see a square. Make your responses as fast as possible. However, if you hear the sound, do not press either key.")
message.draw(win=None)
message.autoDraw = False  # Automatically draw every frame
win.flip()
core.wait(5.0)

message = visual.TextStim(win, text="Starting now")
message.draw(win=None)
message.autoDraw = False  # Automatically draw every frame
win.flip()
core.wait(1.5)

trial_array = [0] * num_trials
x = num_stop_trials
while x > 0:
    stop_trial_index = random.randint(0, (num_trials - 1))
    if trial_array[stop_trial_index] == 0:
        trial_array[stop_trial_index] = 1
        x = x - 1

# print to make sure it's properly randomized
# print(trial_array)

# Actual Experiment
for i in range(num_trials):
    # trial_type = random.randint(0, 1)
    trial_type = trial_array[i]
    direction = random.randint(0, 1)
    write_trigger('stim_onset', a)
    if trial_type == 1:
        # if num_stop_trials > 0:
        if direction == 0:  # right stop signal
            new_ssd = actual_right_stop_signal(ssd)
            ssd = new_ssd
        else:
            new_ssd = actual_left_stop_signal(ssd)
            ssd = new_ssd
            # num_stop_trials = num_stop_trials - 1
    else:
        if direction == 0:  # right go signal
            actual_right_go_signal()
        elif direction == 1:
            actual_left_go_signal()
        # num_go_trials = num_go_trials - 1

# Saving the data
save_data("default_filename.csv", go_trials)
save_data("default_filename2.csv", stop_trials)

# Display thank you message
end_str = f"You made it to the end of the trial! Thanks, and please click any key to close the window!"
visual.TextStim(win, text=end_str).draw()
win.flip()
event.waitKeys()  # Wait for any keypress
# Close window
win.close()