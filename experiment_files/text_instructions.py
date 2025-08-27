from psychopy import visual
def show_text (instructions, subjects, window):
    '''
        Generate text on both subject screens.

    Arguments:
    instructions (str): The text to show
    subjects : list of subject objects
    window : window to draw on
    '''
    for s in subjects:
        visual.TextStim(window,
                        text=instructions, pos=[0 + s.xoffset, 0],
                        color='white', height=20).draw()

    window.flip()

def show_startscreen(subjects, window):
    instructions = "Welcome to the main part of the experiment! \n\n\
    Press the right (blue) button to continue"

    show_text(instructions, subjects, window)

def show_practice_instructions(subjects, window):
    instructions = "Please read the instructions carefully.\n\n\
    1. Please fixate on the center dot cross at all times.\n\n\
    2. You will complete this task together with your partner.\n\n\
    3. First you will perform a few practice trials.\n\n\
    4. You will again see a cloud of moving dots. Please listen to the beep and respond according to their motion.\n\n\
    5. Press the YELLOW button if the dots move LEFT, and the BLUE button if they move RIGHT.\n\n\
    6. Please respond as quickly and as accurately as possible!\n\n\
    Press the BLUE button to continue :)"

    show_text(instructions, subjects, window)

def show_experiment_instructions(subjects, window):
    instructions = "Now you’re ready to start the next part of the experiment. Please remember:\n\n\
    1. Fixate on the dot in the center at all times.\n\n\
    2. Please respond as quickly and as accurately as possible.\n\n\
    3. You will have a break after every two blocks.\n\n\
    4. There will be a total of 10 blocks.\n\n\
    Press the BLUE button when you’re ready to start the experiment :)"

    show_text(instructions, subjects, window)

def show_breakscreen(subjects, window):
    '''
        Show the screen for a non-mandatory break (used after odd block numbers)
    '''

    instructions = "Are you ready for the next block?\n\n\
    Press the BLUE button when you're ready to resume"

    show_text(instructions, subjects, window)

def show_mandatory_breakscreen(subjects, window):
    '''
        Show the text for a mandatory break (used after every second block)
    '''

    instructions = "Enjoy your break:) Please inform the experimenter.\n\n\
    The experimenter will resume the experiment after a short mandatory break."

    show_text(instructions, subjects, window)

def show_endscreen(subjects, window):
    instructions = "The experiment is finished! Thank you for your time!"

    show_text(instructions, subjects, window)
