from psychopy import visual
def show_text (instructions, subject, window):
    '''
        Generate text on both subject screens.

    Arguments:
    instructions (str) : instruction text to show on screen
    subject : subject object
    window : psychopy window object to draw text on.
    '''
    visual.TextStim(window,
                    text=instructions, pos=[0 + subject.xoffset, 0],
                    color='white', height=20).draw()
    window.flip()

def show_practice_instructions(subject, window):
    instructions = "Welcome to our experiment!\n\n\
    Please read the instructions carefully.\n\n\
    1. Please fixate your eyes on the dot in the center of the screen throughout the experiment.\n\n\
    2. After the beep, you will see moving dots. If they are moving LEFT, hit the LEFT (YELLOW) button. If the dots are moving RIGHT, hit the RIGHT (BLUE) button.\n\n\
    3. Please respond as accurately and importantly also as fast as possible. There should be no too slow warnings!\n\n\
    3. Press the BLUE button to continue"

    show_text(instructions, subject, window)

def show_experiment_instructions(subject, window):
    instructions = "You have made it through the practice test! Please read the instructions carefully.\n\n\
    1. Please fixate your eyes on the dot in the center of the screen throughout the experiment.\n\n\
    2. After the beep, you will see moving dots. If they are moving LEFT, hit the LEFT (YELLOW) button. If the dots are moving RIGHT, hit the RIGHT (BLUE) button.\n\n\
    3. Press the BLUE button to continue"

    show_text(instructions, subject, window)

def show_endscreen(subject, window):
    instructions = "The first (individual) part of the experiment is finished!"

    show_text(instructions, subject, window)
