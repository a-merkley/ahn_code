from psychopy import visual
import random


reward_amt = 5
loss_amt = -5
observation_reward = "+$" + str(reward_amt)
observation_loss = "-$" + str(abs(loss_amt))


def total_money_txt(win, total_money):
    total_txt = "Total money: $" + str(total_money)
    total = visual.TextStim(win, text=total_txt, color=(255, 255, 255), height=0.1, pos=(0, 0.5))
    total.draw(win=None)
    total.autoDraw = False


def decoy_str2int(dc_str):
    return -int(dc_str[2:])


def draw_0(win, side):
    wedge = visual.Circle(win, fillColor=[1, 1, -1], radius=0.25, pos=(side*0.25, 0.0))
    wedge.draw(win=None)
    wedge.autoDraw = False
    pos_loss_txt = (side*0.25, 0.0)
    loss_txt = visual.TextStim(win, text=observation_loss, pos=pos_loss_txt)
    loss_txt.draw(win=None)
    loss_txt.autoDraw = False
    return loss_amt


def draw_25(win, side):
    wedge1 = visual.Pie(win, fillColor='pink', start=0, end=-side*90, radius=0.25, pos=(side*0.5, 0.0))
    wedge1.draw(win=None)
    wedge1.autoDraw = False
    wedge2 = visual.Pie(win, fillColor='blue', start=0, end=side*270, radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
    wedge2.draw(win=None)
    wedge2.autoDraw = False
    pos_reward_txt = (side * 0.4, 0.1)
    pos_loss_txt = (side * 0.6, -0.1)
    reward_txt = visual.TextStim(win, text=observation_reward, pos=pos_reward_txt)
    loss_txt = visual.TextStim(win, text=observation_loss, pos=pos_loss_txt)
    reward_txt.draw(win=None)
    reward_txt.autoDraw = False
    loss_txt.draw(win=None)
    loss_txt.autoDraw = False


def answer_25(win, side):
    y = random.randint(0, 3)

    if y == 0:
        # Draw wedge
        wedge1 = visual.Pie(win, fillColor='pink', start=0, end=-side * 90, radius=0.25, pos=(side * 0.5, 0.0))
        wedge1.draw(win=None)
        wedge1.autoDraw = False

        # Draw text
        pos_reward_txt = (side * 0.4, 0.1)
        reward_txt = visual.TextStim(win, text=observation_reward, pos=pos_reward_txt)
        reward_txt.draw(win=None)
        reward_txt.autoDraw = False
        return reward_amt
    else:
        # Draw wedge
        wedge2 = visual.Pie(win, fillColor='blue', start=0, end=side * 270, radius=0.25, pos=(side * 0.5, 0.0),
                            opacity=0.25)
        wedge2.draw(win=None)
        wedge2.autoDraw = False

        # Draw text
        pos_loss_txt = (side * 0.6, -0.1)
        loss_txt = visual.TextStim(win, text=observation_loss, pos=pos_loss_txt)
        loss_txt.draw(win=None)
        loss_txt.autoDraw = False
        return loss_amt


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
    reward_txt.draw(win=None)
    reward_txt.autoDraw = False
    loss_txt.draw(win=None)
    loss_txt.autoDraw = False


def answer_50(win, side):
    y = random.randint(0, 1)

    if y == 0:
        # Draw wedge
        wedge1 = visual.Pie(win, fillColor='blue', start=0, end=side * 180, radius=0.25, pos=(side * 0.5, 0.0),
                            opacity=0.25)
        wedge1.draw(win=None)
        wedge1.autoDraw = False

        # Draw text
        pos_reward_txt = (side * 0.6, 0.0)
        reward_txt = visual.TextStim(win, text=observation_reward, pos=pos_reward_txt)
        reward_txt.draw(win=None)
        reward_txt.autoDraw = False
        return reward_amt
    else:
        # Draw wedge
        wedge2 = visual.Pie(win, fillColor='pink', start=0, end=-side * 180, radius=0.25, pos=(side * 0.5, 0.0))
        wedge2.draw(win=None)
        wedge2.autoDraw = False

        # Draw text
        pos_loss_txt = (side * 0.4, 0.0)
        loss_txt = visual.TextStim(win, text=observation_loss, pos=pos_loss_txt)
        loss_txt.draw(win=None)
        loss_txt.autoDraw = False
        return loss_amt


def draw_75(win, side):
    wedge1 = visual.Pie(win, fillColor='pink', start=0, end=-side*270, radius=0.25, pos=(side*0.5, 0.0))
    wedge1.draw(win=None)
    wedge1.autoDraw = False
    wedge2 = visual.Pie(win, fillColor='blue', start=0, end=side*90, radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
    wedge2.draw(win=None)
    wedge2.autoDraw = False
    pos_reward_txt = (side * 0.4, -0.1)
    pos_loss_txt = (side * 0.6, 0.1)
    reward_txt = visual.TextStim(win, text=observation_reward, pos=pos_reward_txt)
    loss_txt = visual.TextStim(win, text=observation_loss, pos=pos_loss_txt)
    reward_txt.draw(win=None)
    reward_txt.autoDraw = False
    loss_txt.draw(win=None)
    loss_txt.autoDraw = False


def answer_75(win, side):
    y = random.randint(0, 3)

    if y == 3:
        # Draw wedge
        wedge2 = visual.Pie(win, fillColor='blue', start=0, end=side * 90, radius=0.25, pos=(side * 0.5, 0.0),
                            opacity=0.25)
        wedge2.draw(win=None)
        wedge2.autoDraw = False

        # Draw text
        pos_loss_txt = (side * 0.6, 0.1)
        loss_txt = visual.TextStim(win, text=observation_loss, pos=pos_loss_txt)
        loss_txt.draw(win=None)
        loss_txt.autoDraw = False
        return loss_amt
    else:
        # Draw wedge
        wedge1 = visual.Pie(win, fillColor='pink', start=0, end=-side * 270, radius=0.25, pos=(side * 0.5, 0.0))
        wedge1.draw(win=None)
        wedge1.autoDraw = False

        # Draw text
        pos_reward_txt = (side * 0.4, -0.1)
        reward_txt = visual.TextStim(win, text=observation_reward, pos=pos_reward_txt)
        reward_txt.draw(win=None)
        reward_txt.autoDraw = False
        return reward_amt


def draw_100(win, side):
    wedge = visual.Circle(win, fillColor=[-1, 1, -1], radius=0.25, pos=(side*0.25, 0.0))
    wedge.draw(win=None)
    wedge.autoDraw = False
    pos_reward_txt = (side*0.25, 0.0)
    reward_txt = visual.TextStim(win, text=observation_reward, pos=pos_reward_txt)
    reward_txt.draw(win=None)
    reward_txt.autoDraw = False
    return reward_amt





def decoy_0(win, dc1, dc2, side):
    wedge = visual.Circle(win, fillColor='green', radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
    wedge.draw(win=None)
    wedge.autoDraw = False
    pos_loss_decoy = (side*0.5, 0.0)
    decoy_loss_txt = visual.TextStim(win, text=dc2, pos=pos_loss_decoy)
    decoy_loss_txt.draw(win=None)
    decoy_loss_txt.autoDraw = False


def decoy_answer_0(win, dc1, dc2, side):
    # Draw wedge
    wedge = visual.Circle(win, fillColor='green', radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
    wedge.draw(win=None)
    wedge.autoDraw = False

    # Draw text
    pos_loss_decoy = (side*0.5, 0.0)
    decoy_loss_txt = visual.TextStim(win, text=dc2, pos=pos_loss_decoy)
    decoy_loss_txt.draw(win=None)
    decoy_loss_txt.autoDraw = False
    return decoy_str2int(dc2)


def decoy_25(win, dc1, dc2, side):
    wedge1 = visual.Pie(win, fillColor='blue', start=0, end=-side*90, radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
    wedge1.draw(win=None)
    wedge1.autoDraw = False
    wedge2 = visual.Pie(win, fillColor='green', start=0, end=side*270, radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
    wedge2.draw(win=None)
    wedge2.autoDraw = False
    pos_reward_decoy = (side*0.4, 0.1)
    pos_loss_decoy = (side*0.6, -0.1)
    decoy_reward_txt = visual.TextStim(win, text=dc1, pos=pos_reward_decoy)
    decoy_loss_txt = visual.TextStim(win, text=dc2, pos=pos_loss_decoy)
    decoy_reward_txt.draw(win=None)
    decoy_reward_txt.autoDraw = False
    decoy_loss_txt.draw(win=None)
    decoy_loss_txt.autoDraw = False


def decoy_answer_25(win, dc1, dc2, side):
    y = random.randint(0, 3)

    if y == 0:
        # Draw wedge
        wedge1 = visual.Pie(win, fillColor='blue', start=0, end=-side * 90, radius=0.25, pos=(side * 0.5, 0.0),
                            opacity=0.25)
        wedge1.draw(win=None)
        wedge1.autoDraw = False

        # Draw text
        pos_reward_decoy = (side * 0.4, 0.1)
        decoy_reward_txt = visual.TextStim(win, text=dc1, pos=pos_reward_decoy)
        decoy_reward_txt.draw(win=None)
        decoy_reward_txt.autoDraw = False
        return decoy_str2int(dc1)
    else:
        # Draw wedge
        wedge2 = visual.Pie(win, fillColor='green', start=0, end=side * 270, radius=0.25, pos=(side * 0.5, 0.0),
                            opacity=0.25)
        wedge2.draw(win=None)
        wedge2.autoDraw = False

        # Draw text
        pos_loss_decoy = (side * 0.6, -0.1)
        decoy_loss_txt = visual.TextStim(win, text=dc2, pos=pos_loss_decoy)
        decoy_loss_txt.draw(win=None)
        decoy_loss_txt.autoDraw = False
        return decoy_str2int(dc2)


def decoy_50(win, dc1, dc2, side):
    wedge1 = visual.Pie(win, fillColor='blue', start=0, end=-side*180, radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
    wedge1.draw(win=None)
    wedge1.autoDraw = False
    wedge2 = visual.Pie(win, fillColor='green', start=0, end=side*180, radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
    wedge2.draw(win=None)
    wedge2.autoDraw = False
    pos_reward_decoy = (side*0.4, 0.0)
    pos_loss_decoy = (side*0.6, 0.0)
    decoy_reward_txt = visual.TextStim(win, text=dc1, pos=pos_reward_decoy)
    decoy_loss_txt = visual.TextStim(win, text=dc2, pos=pos_loss_decoy)
    decoy_reward_txt.draw(win=None)
    decoy_reward_txt.autoDraw = False
    decoy_loss_txt.draw(win=None)
    decoy_loss_txt.autoDraw = False


def decoy_answer_50(win, dc1, dc2, side):
    y = random.randint(0, 1)

    if y == 0:
        # Draw wedge
        wedge1 = visual.Pie(win, fillColor='blue', start=0, end=-side * 180, radius=0.25, pos=(side * 0.5, 0.0),
                            opacity=0.25)
        wedge1.draw(win=None)
        wedge1.autoDraw = False

        # Draw text
        pos_reward_decoy = (side * 0.4, 0.0)
        decoy_reward_txt = visual.TextStim(win, text=dc1, pos=pos_reward_decoy)
        decoy_reward_txt.draw(win=None)
        decoy_reward_txt.autoDraw = False
        return decoy_str2int(dc1)
    else:
        # Draw wedge
        pos_loss_decoy = (side * 0.6, 0.0)
        wedge2 = visual.Pie(win, fillColor='green', start=0, end=side * 180, radius=0.25, pos=(side * 0.5, 0.0),
                            opacity=0.25)
        wedge2.draw(win=None)
        wedge2.autoDraw = False

        # Draw text
        decoy_loss_txt = visual.TextStim(win, text=dc2, pos=pos_loss_decoy)
        decoy_loss_txt.draw(win=None)
        decoy_loss_txt.autoDraw = False
        return decoy_str2int(dc2)


def decoy_75(win, dc1, dc2, side):
    wedge1 = visual.Pie(win, fillColor='blue', start=0, end=-side*270, radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
    wedge1.draw(win=None)
    wedge1.autoDraw = False
    wedge2 = visual.Pie(win, fillColor='green', start=0, end=side*90, radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
    wedge2.draw(win=None)
    wedge2.autoDraw = False
    pos_reward_decoy = (side*0.4, -0.1)
    pos_loss_decoy = (side*0.6, 0.1)
    decoy_reward_txt = visual.TextStim(win, text=dc1, pos=pos_reward_decoy)
    decoy_loss_txt = visual.TextStim(win, text=dc2, pos=pos_loss_decoy)
    decoy_reward_txt.draw(win=None)
    decoy_reward_txt.autoDraw = False
    decoy_loss_txt.draw(win=None)
    decoy_loss_txt.autoDraw = False


def decoy_answer_75(win, dc1, dc2, side):
    y = random.randint(0, 3)

    if y == 3:
        # Draw wedge
        wedge2 = visual.Pie(win, fillColor='green', start=0, end=side * 90, radius=0.25, pos=(side * 0.5, 0.0),
                            opacity=0.25)
        wedge2.draw(win=None)
        wedge2.autoDraw = False

        # Draw text
        pos_loss_decoy = (side * 0.6, 0.1)
        decoy_loss_txt = visual.TextStim(win, text=dc2, pos=pos_loss_decoy)
        decoy_loss_txt.draw(win=None)
        decoy_loss_txt.autoDraw = False
        return decoy_str2int(dc2)
    else:
        # Draw wedge
        wedge1 = visual.Pie(win, fillColor='blue', start=0, end=-side * 270, radius=0.25, pos=(side * 0.5, 0.0),
                            opacity=0.25)
        wedge1.draw(win=None)
        wedge1.autoDraw = False

        # Draw text
        pos_reward_decoy = (side * 0.4, -0.1)
        decoy_reward_txt = visual.TextStim(win, text=dc1, pos=pos_reward_decoy)
        decoy_reward_txt.draw(win=None)
        decoy_reward_txt.autoDraw = False
        return decoy_str2int(dc1)


def decoy_100(win, dc1, dc2, side):
    wedge = visual.Circle(win, fillColor='blue', radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
    wedge.draw(win=None)
    wedge.autoDraw = False
    pos_reward_decoy = (side*0.5, 0.0)
    decoy_reward_txt = visual.TextStim(win, text=dc1, pos=pos_reward_decoy)
    decoy_reward_txt.draw(win=None)
    decoy_reward_txt.autoDraw = False


def decoy_answer_100(win, dc1, dc2, side):
    # Draw wedge
    wedge = visual.Circle(win, fillColor='blue', radius=0.25, pos=(side*0.5, 0.0), opacity=0.25)
    wedge.draw(win=None)
    wedge.autoDraw = False

    # Draw text
    pos_reward_decoy = (side*0.5, 0.0)
    decoy_reward_txt = visual.TextStim(win, text=dc1, pos=pos_reward_decoy)
    decoy_reward_txt.draw(win=None)
    decoy_reward_txt.autoDraw = False
    return decoy_str2int(dc1)

