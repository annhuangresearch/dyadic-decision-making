import numpy as np
from draw_stimuli import *

def seconds_to_frames (seconds, REFRESH_RATE):
    return range( int( np.rint(seconds * REFRESH_RATE) ) )

# below functions are to be called once per frame

def pretrial_interval (choice, subjects, titration=False):
    """
    Draws the stimuli shown during each frame during the pretrial interval (stationary dots and fixation). Allows for titration mode.

    Arguments:
    choice (int) : integer to specify which dot patch to show.
    subjects     : depending on titration, either a list of subjects or a single subject.
    titration (bool): defaults to False for main (dyadic) experiment
    """
    if not titration:
        draw_stationary_dots(choice, subjects)
        draw_fixation("green", subjects)
    else:
        draw_stationary_dots(choice, subjects, titration=True)
        draw_fixation("green", subjects, titration=True)

def decision_interval (subjects, stimulus_s1, stimulus_s2, titration=False):
    if not titration:
        draw_moving_dots(subjects, stimulus_s1, stimulus_s2)
        draw_fixation("green", subjects)

    else:
        draw_moving_dots(subjects, stimulus_s1, None, titration=True)
        draw_fixation("green", subjects, titration=True)

def fixation_feedback (color, subjects, choice, rt_msg="NA", titration=False): # rt_msg is reaction-time message
    '''
        1. Display static dot screen
        2. Response indicated by fixation dot color: left/ yellow or right/ blue
        3. Both acting participant and their partner see a warning if the response time is too slow or too fast.

        Arguments:
        color (str) : Either green, yellow or blue.
        subjects    : Either a list with two subjects for dyadic experiment, or a single subject for titration
        choice (int): Choice of dot patch to show.
        rt_msg (str): A string specifying whether the response time was too slow ("slow") or too fast ("fast"). "NA" if neither applies.
        titration (bool): Whether to act in titration mode or not (defaults to dyadic experiment setting).
    '''
    if not titration:
        draw_stationary_dots(choice, subjects)
        draw_fixation(color, subjects)
    else:
        draw_stationary_dots(choice, subjects, titration=True)
        draw_fixation(color, subjects, titration=True)

    if rt_msg != "NA":
        if not titration:
            if subjects[0].state:
                subjects[0].indicatordict[rt_msg].draw()
                subjects[1].indicatordict["partner " + rt_msg].draw()
            else:
                subjects[1].indicatordict[rt_msg].draw()
                subjects[0].indicatordict["partner " + rt_msg].draw()


        else:
            subjects.indicatordict[rt_msg].draw()
