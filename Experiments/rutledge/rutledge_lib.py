from psychopy import visual
import random


observation_reward = "+$5"
observation_loss = "-$5"

# decoy_options = ["+$0", "-$1", "-$2", "-$3", "-$4", "-$5", "-$10"]
# decoy1_idx = random.randint(0, len(decoy_options)-1)
# decoy2_idx = random.randint(0, len(decoy_options)-1)
# decoy_1 = decoy_options[decoy1_idx]
# decoy_2 = decoy_options[decoy2_idx]


def total_money_txt(win, total_money):
    total_txt = "Total money: $" + str(total_money)
    total = visual.TextStim(win, text=total_txt, color=(255, 255, 255), height=0.1, pos=(0, 0.5))
    total.draw(win=None)
    total.autoDraw = False


def draw_0(win, side):
    wedge = visual.Circle(win, fillColor=[1, 1, -1], radius=0.25, pos=(side*0.25, 0.0))
    wedge.draw(win=None)
    wedge.autoDraw = False
    # pos_reward_txt = (-0.25, 0.5)
    pos_loss_txt = (side*0.25, 0.0)
    # reward_txt = visual.TextStim(win, text=observation_reward, pos=pos_reward_txt)
    loss_txt = visual.TextStim(win, text=observation_loss, pos=pos_loss_txt)
    # trial_start = visual.TextStim(win, text = '+', color=(255, 255, 255), height = 0.5)
    # trial_start.draw(win=None)
    # trial_start.autoDraw = False
    # reward_txt.draw(win=None)
    # reward_txt.autoDraw = False
    loss_txt.draw(win=None)
    loss_txt.autoDraw = False
    return -5


def draw_25(win, side):
    wedge1 = visual.Pie(win, fillColor='pink', start=0, end=-90, radius=0.25, pos=(side*0.5, 0.0))
    wedge1.draw(win=None)
    wedge1.autoDraw = False
    wedge2 = visual.Pie(win, fillColor='blue', start=0, end=270, radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
    wedge2.draw(win=None)
    wedge2.autoDraw = False
    pos_reward_txt = side*(0.6, 0.1)
    pos_loss_txt = side*(0.4, -0.1)
    reward_txt = visual.TextStim(win, text=observation_reward, pos=pos_reward_txt)
    loss_txt = visual.TextStim(win, text=observation_loss, pos=pos_loss_txt)
    # trial_start = visual.TextStim(win, text = '+', color=(255, 255, 255), height = 0.5)
    # trial_start.draw(win=None)
    # trial_start.autoDraw = False
    reward_txt.draw(win=None)
    reward_txt.autoDraw = False
    loss_txt.draw(win=None)
    loss_txt.autoDraw = False


def answer_25(win, side):
    wedge1 = visual.Pie(win, fillColor='pink', start=0, end=-90, radius=0.25, pos=(side*0.5, 0.0))
    wedge1.draw(win=None)
    wedge1.autoDraw = False
    wedge2 = visual.Pie(win, fillColor='blue', start=0, end=270, radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
    wedge2.draw(win=None)
    wedge2.autoDraw = False
    pos_reward_txt = side*(0.6, 0.1)
    pos_loss_txt = side*(0.4, -0.1)
    reward_txt = visual.TextStim(win, text=observation_reward, pos=pos_reward_txt)
    loss_txt = visual.TextStim(win, text=observation_loss, pos=pos_loss_txt)
    # trial_start = visual.TextStim(win, text = '+', color=(255, 255, 255), height = 0.5)
    # trial_start.draw(win=None)
    # trial_start.autoDraw = False
    reward_txt.draw(win=None)
    reward_txt.autoDraw = False
    loss_txt.draw(win=None)
    loss_txt.autoDraw = False

    y = random.randint(0, 3)

    if y == 0:
        wedge1 = visual.Pie(win, fillColor='orange', start=0, end=-90, radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
        wedge1.draw(win=None)
        wedge1.autoDraw = False
        return 5
    else:
        wedge2 = visual.Pie(win, fillColor='orange', start=0, end=270, radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
        wedge2.draw(win=None)
        wedge2.autoDraw = False
        return -5


def draw_50(win, side):
    wedge1 = visual.Pie(win, fillColor='pink', start=0, end=-side*180, radius=0.25, pos=(side*0.5, 0.0))
    wedge1.draw(win=None)
    wedge1.autoDraw = False
    wedge2 = visual.Pie(win, fillColor='blue', start=0, end=side*180, radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
    wedge2.draw(win=None)
    wedge2.autoDraw = False
    pos_reward_txt = (side*0.6, 0.0)
    pos_loss_txt = (side*0.4, 0.0)
    reward_txt = visual.TextStim(win, text=observation_reward, pos=pos_reward_txt)
    loss_txt = visual.TextStim(win, text=observation_loss, pos=pos_loss_txt)
    # trial_start = visual.TextStim(win, text = '+', color=(255, 255, 255), height = 0.5)
    # trial_start.draw(win=None)
    # trial_start.autoDraw = False
    reward_txt.draw(win=None)
    reward_txt.autoDraw = False
    loss_txt.draw(win=None)
    loss_txt.autoDraw = False


def answer_50(win, side):
    wedge1 = visual.Pie(win, fillColor='pink', start=0, end=-side*180, radius=0.25, pos=(side*0.5, 0.0))
    wedge1.draw(win=None)
    wedge1.autoDraw = False
    wedge2 = visual.Pie(win, fillColor='blue', start=0, end=side*180, radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
    wedge2.draw(win=None)
    wedge2.autoDraw = False
    pos_reward_txt = (side*0.6, 0.0)
    pos_loss_txt = (side*0.4, 0.0)
    reward_txt = visual.TextStim(win, text=observation_reward, pos=pos_reward_txt)
    loss_txt = visual.TextStim(win, text=observation_loss, pos=pos_loss_txt)
    # trial_start = visual.TextStim(win, text = '+', color=(255, 255, 255), height = 0.5)
    # trial_start.draw(win=None)
    # trial_start.autoDraw = False
    reward_txt.draw(win=None)
    reward_txt.autoDraw = False
    loss_txt.draw(win=None)
    loss_txt.autoDraw = False

    y = random.randint(0, 1)

    if y == 0:
        wedge1 = visual.Pie(win, fillColor='orange', start=0, end=side*180, radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
        wedge1.draw(win=None)
        wedge1.autoDraw = False
        return 5
    else:
        wedge2 = visual.Pie(win, fillColor='orange', start=0, end=-side*180, radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
        wedge2.draw(win=None)
        wedge2.autoDraw = False
        return -5


def draw_75(win, side):
    if side == 1: txt_side = -1
    else: txt_side = 1
    wedge1 = visual.Pie(win, fillColor='pink', start=0, end=-270, radius=0.25, pos=(side*0.5, 0.0))
    wedge1.draw(win=None)
    wedge1.autoDraw = False
    wedge2 = visual.Pie(win, fillColor='blue', start=0, end=90, radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
    wedge2.draw(win=None)
    wedge2.autoDraw = False
    pos_reward_txt = (0.6, -0.1)
    pos_loss_txt = (0.4, 0.1)
    reward_txt = visual.TextStim(win, text=observation_reward, pos=pos_reward_txt)
    loss_txt = visual.TextStim(win, text=observation_loss, pos=pos_loss_txt)
    # trial_start = visual.TextStim(win, text = '+', color=(255, 255, 255), height = 0.5)
    # trial_start.draw(win=None)
    # trial_start.autoDraw = False
    reward_txt.draw(win=None)
    reward_txt.autoDraw = False
    loss_txt.draw(win=None)
    loss_txt.autoDraw = False


def answer_75(win, side):
    wedge1 = visual.Pie(win, fillColor='pink', start=0, end=-270, radius=0.25, pos=(side*0.5, 0.0))
    wedge1.draw(win=None)
    wedge1.autoDraw = False
    wedge2 = visual.Pie(win, fillColor='blue', start=0, end=90, radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
    wedge2.draw(win=None)
    wedge2.autoDraw = False
    pos_reward_txt = (side*0.6, -0.1)
    pos_loss_txt = (side*0.4, 0.1)
    reward_txt = visual.TextStim(win, text=observation_reward, pos=pos_reward_txt)
    loss_txt = visual.TextStim(win, text=observation_loss, pos=pos_loss_txt)
    # trial_start = visual.TextStim(win, text = '+', color=(255, 255, 255), height = 0.5)
    # trial_start.draw(win=None)
    # trial_start.autoDraw = False
    reward_txt.draw(win=None)
    reward_txt.autoDraw = False
    loss_txt.draw(win=None)
    loss_txt.autoDraw = False

    y = random.randint(0, 3)

    if y == 3:
        wedge2 = visual.Pie(win, fillColor='orange', start=0, end=90, radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
        wedge2.draw(win=None)
        wedge2.autoDraw = False
        return -5
    else:
        wedge1 = visual.Pie(win, fillColor='orange', start=0, end=-270, radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
        wedge1.draw(win=None)
        wedge1.autoDraw = False
        return 5


def draw_100(win, side):
    wedge = visual.Circle(win, fillColor=[-1, 1, -1], radius=0.25, pos=(side*0.25, 0.0))
    wedge.draw(win=None)
    wedge.autoDraw = False
    pos_reward_txt = (side*0.25, 0.0)
    # pos_loss_txt = (0.5, 0.0)
    reward_txt = visual.TextStim(win, text=observation_reward, pos=pos_reward_txt)
    # loss_txt = visual.TextStim(win, text=observation_loss, pos=pos_loss_txt)
    # trial_start = visual.TextStim(win, text = '+', color=(255, 255, 255), height = 0.5)
    # trial_start.draw(win=None)
    # trial_start.autoDraw = False
    reward_txt.draw(win=None)
    reward_txt.autoDraw = False
    # loss_txt.draw(win=None)
    # loss_txt.autoDraw = False
    return 5





def decoy_0(win, dc1, dc2, side):
    wedge = visual.Circle(win, fillColor='green', radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
    wedge.draw(win=None)
    wedge.autoDraw = False
    # pos_reward_txt = (-0.25, 0.5)
    pos_loss_decoy = (side*0.5, 0.0)
    # reward_txt = visual.TextStim(win, text=observation_reward, pos=pos_reward_txt)
    decoy_loss_txt = visual.TextStim(win, text=dc2, pos=pos_loss_decoy)
    # trial_start = visual.TextStim(win, text = '+', color=(255, 255, 255), height = 0.5)
    # trial_start.draw(win=None)
    # trial_start.autoDraw = False
    # reward_txt.draw(win=None)
    # reward_txt.autoDraw = False
    decoy_loss_txt.draw(win=None)
    decoy_loss_txt.autoDraw = False


def decoy_answer_0(win, dc1, dc2, side):
    wedge = visual.Circle(win, fillColor='green', radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
    wedge.draw(win=None)
    wedge.autoDraw = False
    # pos_reward_txt = (-0.25, 0.5)
    pos_loss_decoy = (side*0.5, 0.0)
    # reward_txt = visual.TextStim(win, text=observation_reward, pos=pos_reward_txt)
    decoy_loss_txt = visual.TextStim(win, text=dc2, pos=pos_loss_decoy)
    # trial_start = visual.TextStim(win, text = '+', color=(255, 255, 255), height = 0.5)
    # trial_start.draw(win=None)
    # trial_start.autoDraw = False
    # reward_txt.draw(win=None)
    # reward_txt.autoDraw = False
    decoy_loss_txt.draw(win=None)
    decoy_loss_txt.autoDraw = False

    wedge = visual.Circle(win, fillColor='orange', radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
    wedge.draw(win=None)
    wedge.autoDraw = False


def decoy_25(win, dc1, dc2, side):
    wedge1 = visual.Pie(win, fillColor='blue', start=0, end=-90, radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
    wedge1.draw(win=None)
    wedge1.autoDraw = False
    wedge2 = visual.Pie(win, fillColor='green', start=0, end=270, radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
    wedge2.draw(win=None)
    wedge2.autoDraw = False
    pos_reward_decoy = (side*0.4, 0.1)
    pos_loss_decoy = (side*0.6, -0.1)
    decoy_reward_txt = visual.TextStim(win, text=dc1, pos=pos_reward_decoy)
    decoy_loss_txt = visual.TextStim(win, text=dc2, pos=pos_loss_decoy)
    # trial_start = visual.TextStim(win, text = '+', color=(255, 255, 255), height = 0.5)
    # trial_start.draw(win=None)
    # trial_start.autoDraw = False
    decoy_reward_txt.draw(win=None)
    decoy_reward_txt.autoDraw = False
    decoy_loss_txt.draw(win=None)
    decoy_loss_txt.autoDraw = False


def decoy_answer_25(win, dc1, dc2, side):
    wedge1 = visual.Pie(win, fillColor='blue', start=0, end=-90, radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
    wedge1.draw(win=None)
    wedge1.autoDraw = False
    wedge2 = visual.Pie(win, fillColor='green', start=0, end=270, radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
    wedge2.draw(win=None)
    wedge2.autoDraw = False
    pos_reward_decoy = (side*0.4, 0.1)
    pos_loss_decoy = (side*0.6, -0.1)
    decoy_reward_txt = visual.TextStim(win, text=dc1, pos=pos_reward_decoy)
    decoy_loss_txt = visual.TextStim(win, text=dc2, pos=pos_loss_decoy)
    # trial_start = visual.TextStim(win, text = '+', color=(255, 255, 255), height = 0.5)
    # trial_start.draw(win=None)
    # trial_start.autoDraw = False
    decoy_reward_txt.draw(win=None)
    decoy_reward_txt.autoDraw = False
    decoy_loss_txt.draw(win=None)
    decoy_loss_txt.autoDraw = False

    y = random.randint(0, 3)

    if y == 0:
        wedge1 = visual.Pie(win, fillColor='orange', start=0, end=-90, radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
        wedge1.draw(win=None)
        wedge1.autoDraw = False
    else:
        wedge2 = visual.Pie(win, fillColor='orange', start=0, end=270, radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
        wedge2.draw(win=None)
        wedge2.autoDraw = False


def decoy_50(win, dc1, dc2, side):
    wedge1 = visual.Pie(win, fillColor='blue', start=0, end=-180, radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
    wedge1.draw(win=None)
    wedge1.autoDraw = False
    wedge2 = visual.Pie(win, fillColor='green', start=0, end=180, radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
    wedge2.draw(win=None)
    wedge2.autoDraw = False
    pos_reward_decoy = (side*0.4, 0.0)
    pos_loss_decoy = (side*0.6, 0.0)
    decoy_reward_txt = visual.TextStim(win, text=dc1, pos=pos_reward_decoy)
    decoy_loss_txt = visual.TextStim(win, text=dc2, pos=pos_loss_decoy)
    # trial_start = visual.TextStim(win, text = '+', color=(255, 255, 255), height = 0.5)
    # trial_start.draw(win=None)
    # trial_start.autoDraw = False
    decoy_reward_txt.draw(win=None)
    decoy_reward_txt.autoDraw = False
    decoy_loss_txt.draw(win=None)
    decoy_loss_txt.autoDraw = False


def decoy_answer_50(win, dc1, dc2, side):
    wedge1 = visual.Pie(win, fillColor='blue', start=0, end=-180, radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
    wedge1.draw(win=None)
    wedge1.autoDraw = False
    wedge2 = visual.Pie(win, fillColor='green', start=0, end=180, radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
    wedge2.draw(win=None)
    wedge2.autoDraw = False
    pos_reward_decoy = (side*0.4, 0.0)
    pos_loss_decoy = (side*0.6, 0.0)
    decoy_reward_txt = visual.TextStim(win, text=dc1, pos=pos_reward_decoy)
    decoy_loss_txt = visual.TextStim(win, text=dc2, pos=pos_loss_decoy)
    # trial_start = visual.TextStim(win, text = '+', color=(255, 255, 255), height = 0.5)
    # trial_start.draw(win=None)
    # trial_start.autoDraw = False
    decoy_reward_txt.draw(win=None)
    decoy_reward_txt.autoDraw = False
    decoy_loss_txt.draw(win=None)
    decoy_loss_txt.autoDraw = False

    y = random.randint(0, 1)

    if y == 0:
        wedge1 = visual.Pie(win, fillColor='orange', start=0, end=-180, radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
        wedge1.draw(win=None)
        wedge1.autoDraw = False
    else:
        wedge2 = visual.Pie(win, fillColor='orange', start=0, end=180, radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
        wedge2.draw(win=None)
        wedge2.autoDraw = False


def decoy_75(win, dc1, dc2, side):
    wedge1 = visual.Pie(win, fillColor='blue', start=0, end=-270, radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
    wedge1.draw(win=None)
    wedge1.autoDraw = False
    wedge2 = visual.Pie(win, fillColor='green', start=0, end=90, radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
    wedge2.draw(win=None)
    wedge2.autoDraw = False
    pos_reward_decoy = (side*0.4, -0.1)
    pos_loss_decoy = (side*0.6, 0.1)
    decoy_reward_txt = visual.TextStim(win, text=dc1, pos=pos_reward_decoy)
    decoy_loss_txt = visual.TextStim(win, text=dc2, pos=pos_loss_decoy)
    # trial_start = visual.TextStim(win, text = '+', color=(255, 255, 255), height = 0.5)
    # trial_start.draw(win=None)
    # trial_start.autoDraw = False
    decoy_reward_txt.draw(win=None)
    decoy_reward_txt.autoDraw = False
    decoy_loss_txt.draw(win=None)
    decoy_loss_txt.autoDraw = False


def decoy_answer_75(win, dc1, dc2, side):
    wedge1 = visual.Pie(win, fillColor='blue', start=0, end=-270, radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
    wedge1.draw(win=None)
    wedge1.autoDraw = False
    wedge2 = visual.Pie(win, fillColor='green', start=0, end=90, radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
    wedge2.draw(win=None)
    wedge2.autoDraw = False
    pos_reward_decoy = (side*0.4, -0.1)
    pos_loss_decoy = (side*0.6, 0.1)
    decoy_reward_txt = visual.TextStim(win, text=dc1, pos=pos_reward_decoy)
    decoy_loss_txt = visual.TextStim(win, text=dc2, pos=pos_loss_decoy)
    # trial_start = visual.TextStim(win, text = '+', color=(255, 255, 255), height = 0.5)
    # trial_start.draw(win=None)
    # trial_start.autoDraw = False
    decoy_reward_txt.draw(win=None)
    decoy_reward_txt.autoDraw = False
    decoy_loss_txt.draw(win=None)
    decoy_loss_txt.autoDraw = False

    y = random.randint(0, 3)

    if y == 3:
        wedge2 = visual.Pie(win, fillColor='orange', start=0, end=90, radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
        wedge2.draw(win=None)
        wedge2.autoDraw = False
    else:
        wedge1 = visual.Pie(win, fillColor='orange', start=0, end=-270, radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
        wedge1.draw(win=None)
        wedge1.autoDraw = False


def decoy_100(win, dc1, dc2, side):
    wedge = visual.Circle(win, fillColor='blue', radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
    wedge.draw(win=None)
    wedge.autoDraw = False
    pos_reward_decoy = (side*0.5, 0.0)
    # pos_loss_decoy = (0.0, 0.0)
    decoy_reward_txt = visual.TextStim(win, text=dc1, pos=pos_reward_decoy)
    # decoy_loss_txt = visual.TextStim(win, text=dc2, pos=pos_loss_decoy)
    # trial_start = visual.TextStim(win, text = '+', color=(255, 255, 255), height = 0.5)
    # trial_start.draw(win=None)
    # trial_start.autoDraw = False
    decoy_reward_txt.draw(win=None)
    decoy_reward_txt.autoDraw = False
    # decoy_loss_txt.draw(win=None)
    # decoy_loss_txt.autoDraw = False


def decoy_answer_100(win, dc1, dc2, side):
    wedge = visual.Circle(win, fillColor='blue', radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
    wedge.draw(win=None)
    wedge.autoDraw = False
    pos_reward_decoy = (side*0.5, 0.0)
    # pos_loss_decoy = (0.0, 0.0)
    decoy_reward_txt = visual.TextStim(win, text=dc1, pos=pos_reward_decoy)
    # decoy_loss_txt = visual.TextStim(win, text=dc2, pos=pos_loss_decoy)
    # trial_start = visual.TextStim(win, text = '+', color=(255, 255, 255), height = 0.5)
    # trial_start.draw(win=None)
    # trial_start.autoDraw = False
    decoy_reward_txt.draw(win=None)
    decoy_reward_txt.autoDraw = False
    # decoy_loss_txt.draw(win=None)
    # decoy_loss_txt.autoDraw = False

    wedge = visual.Circle(win, fillColor='orange', radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
    wedge.draw(win=None)
    wedge.autoDraw = False

