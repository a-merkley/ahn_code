from psychopy import core, data, event, sound, visual
import numpy as np
from psychopy.visual.circle import Circle
import csv

respClock = core.Clock()


# Trigger function
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


def save_data(fname, data_lst):
    with open(fname, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data_lst)


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


# displays the start of a new trial
def trialStart(win):
    trial_start = visual.TextStim(win, text='+', color=(255, 255, 255), height=0.5)
    trial_start.draw(win=None)
    trial_start.autoDraw = False  # Automatically draw every frame
    win.flip()
    core.wait(0.250)


#################################################################################################################
############################################## STIMULUS #########################################################
#################################################################################################################
# displays one go signal
def actual_right_go_signal(win):
    # Draw shape
    trialStart(win)
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

    # Wait for response
    event.waitKeys(keyList=['j'])


# displays the other go signal
def actual_left_go_signal(win):
    # Draw shape
    trialStart(win)
    go_signal_left = visual.circle.Circle(win, radius=0.25, lineWidth=20, lineColor=(255, 255, 255), fillColor=None)
    go_signal_left.draw(win=None)
    go_signal_left.autoDraw = False
    win.flip()

    # Wait for response
    event.waitKeys(keyList=['f'])


def actual_right_stop_signal(win, ssd):
    # Draw shape
    trialStart(win)
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

    # Show stop signal
    core.wait(ssd)
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
    stop_circle = visual.circle.Circle(win, radius=0.03, lineColor='red', fillColor='red')
    stop_circle.draw(win=None)
    stop_circle.autoDraw = False
    win.flip()

    # Wait for response
    keys = event.waitKeys(maxWait=1.25, keyList=['j'])
    if keys != None:
        flag = "Fail"
        ssd = ssd - 0.050
    else:
        flag = "Success"
        ssd = ssd + 0.050
    return ssd, flag


# Displays other stop signal
def actual_left_stop_signal(win, ssd):
    # Draw shape
    trialStart(win)
    stop_signal_left = visual.circle.Circle(win, radius=0.25, lineWidth=20,
                                            lineColor=(255, 255, 255), fillColor=None)
    stop_signal_left.draw(win=None)
    stop_signal_left.autoDraw = False
    win.flip()

    # Show stop signal
    core.wait(ssd)
    stop_signal_left.draw(win=None)
    stop_signal_left.autoDraw = False
    stop_circle = visual.circle.Circle(win, radius=0.03, lineColor='red', fillColor='red')
    stop_circle.draw(win=None)
    stop_circle.autoDraw = False
    win.flip()

    # Wait for response
    keys = event.waitKeys(maxWait=1.25, keyList=['f'])
    if keys != None:
        flag = "Fail"
        ssd = ssd - 0.050
    else:
        flag = "Success"
        ssd = ssd + 0.050
    return ssd, flag




#################################################################################################################
############################################## PRACTICE #########################################################
#################################################################################################################
def practice_right_go_signal(win):
    trialStart(win)
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
    # go_trials.append([rt_go1])


def practice_left_go_signal(win):
    trialStart(win)
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


def practice_left_stop_signal(win, ssd):
    trialStart(win)
    stop_signal_left = visual.circle.Circle(win, radius=0.25, lineWidth=20,
                                            lineColor=(255, 255, 255), fillColor=None)
    stop_signal_left.draw(win=None)
    stop_signal_left.autoDraw = False
    win.flip()
    # show stop signal
    core.wait(ssd)
    stop_signal_left.draw(win=None)
    stop_signal_left.autoDraw = False
    stop_circle = visual.circle.Circle(win, radius=0.03, lineColor='red', fillColor='red')
    stop_circle.draw(win=None)
    stop_circle.autoDraw = False
    win.flip()
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


def practice_right_stop_signal(win, ssd):
    trialStart(win)
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
    # show stop signal
    core.wait(ssd)
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
    stop_circle = visual.circle.Circle(win, radius=0.03, lineColor='red', fillColor='red')
    stop_circle.draw(win=None)
    stop_circle.autoDraw = False
    win.flip()
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