import numpy as np
import random
def acting_states (trials):
    '''
        Randomly generate list including the subject states (act/ observe)

        Arguments:
        trials (int) : number of trials
    '''
    return np.random.choice(a=[True, False], size=trials)

def moving_states (trials):
    '''
        Generates list that contains the movement direction of the moving
        dot patch (left/ right)

        Arguments:
        trials(int) : number of trials
    '''
    movingstates = ['left'] * (trials//2) + ['right'] * (trials//2)
    return random.sample(movingstates, len(movingstates))
