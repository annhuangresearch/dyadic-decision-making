from experiment_utils import acting_states, moving_states
from keyboard_utils import *
from subject_utils import update_state
from text_instructions import *
import stimuli_random_dots as stimuli
#from intervals import seconds_to_frames
from intervals import *
from psychopy import visual, core, data
import numpy as np
import os
import json

def sound_familiarisation(subjects, window, REFRESH_RATE, n_times=5):
    """
    Shows and plays the two distinct beep sounds for the two subjects to familiarize them with their sound.

    Arguments:
    subjects : list of two subject objects
    window   : psychopy window to draw on
    REFRESH_RATE : Refresh rate of the monitors
    n_times (int) : How many times each participant will hear their beep.
    """
    your_beep = "When you hear this, it's your turn to respond."
    partner_beep = "When you hear this, your partner will respond."
    for _ in range(n_times):

        for frame in seconds_to_frames(1, REFRESH_RATE):
            visual.TextStim(window,
                    text=your_beep, pos=[0 + subjects[0].xoffset, 0],
                    color='green', height=20).draw()
            visual.TextStim(window,
                        text=partner_beep, pos=[0 + subjects[1].xoffset, 0],
                        color='red', height=20).draw()
            window.flip()
        nextflip = window.getFutureFlipTime(clock='ptb')
        subjects[0].beep.play(when=nextflip)

        for frame in seconds_to_frames(3, REFRESH_RATE):
            visual.TextStim(window,
                    text=your_beep, pos=[0 + subjects[0].xoffset, 0],
                    color='green', height=20).draw()
            visual.TextStim(window,
                        text=partner_beep, pos=[0 + subjects[1].xoffset, 0],
                        color='red', height=20).draw()

            window.flip()

        for frame in seconds_to_frames(1, REFRESH_RATE):
            visual.TextStim(window,
                    text=your_beep, pos=[0 + subjects[1].xoffset, 0],
                    color='green', height=20).draw()
            visual.TextStim(window,
                        text=partner_beep, pos=[0 + subjects[0].xoffset, 0],
                        color='red', height=20).draw()

            window.flip()
        subjects[0].beep.stop()
        nextflip = window.getFutureFlipTime(clock='ptb')
        subjects[1].beep.play(when=nextflip)

        for frame in seconds_to_frames(3, REFRESH_RATE):
            visual.TextStim(window,
                    text=your_beep, pos=[0 + subjects[1].xoffset, 0],
                    color='green', height=20).draw()
            visual.TextStim(window,
                        text=partner_beep, pos=[0 + subjects[0].xoffset, 0],
                        color='red', height=20).draw()
            window.flip()
        subjects[1].beep.stop()



def experiment(blocks, n_trials, N, subjects, window, REFRESH_RATE, experiment_handler, filepath, main_experiment):
    """
    This function runs the main dyadic experiment as well as the practice for it.

    Arguments:
    blocks (tuple or list) : an iterable containing two ints, specifying the start block (usually 0) and end block (+1) (usually 10). For practice, set this to (0,1)
    n_trials (int) : number of trials during each block.
    N (int)        : Number of dot patches created in the subject class.
    subjects (list): Contains the two subject classes
    window         : The psychopy window object
    REFRESH_RATE (int)  : The refresh rate of the monitor (used to determine how many frames intervals are shown)
    experiment_handler : Psychopy experiment handler object initialized with a filepath to save to in order to save data.
    filepath     (str)  : filepath that was used to create the experiment handler.
    main_experiment (bool) : True for main experiment, False for practice.

    Returns: None
    """


    n_correct = 0

    for block_number in range(blocks[0],blocks[1]):
        subject_1_correctness = []
        subject_2_correctness = []

        iterstates = iter(acting_states(n_trials))
        movingstates = iter(moving_states(n_trials))
        for trial_number in range(n_trials):

            # subject state update
            update_state(subjects, iterstates)
            timing_flag = "NA"

            # whose turn it is defines which beep is played
            beep = subjects[0].beep if subjects[0].state == 1 else subjects[1].beep

            # pretrial interval: display light blue fixation cross & stationary dots for 1 - 2 s (uniformly distributed)
            if trial_number == 0:
                for frame in seconds_to_frames(np.random.uniform(1, 2), REFRESH_RATE):
                    pretrial_interval(choice=0, subjects=subjects)
                    window.flip()
            else:
                for frame in seconds_to_frames(np.random.uniform(1, 2), REFRESH_RATE):
                    pretrial_interval(choice=stationary_choice, subjects=subjects)

                    window.flip()

            # reset subject keyboards and timer
            for s in subjects:
                s.keyboard.clearEvents(eventType="keyboard")
                s.keyboard.clock.reset()

            # preparing time for next window flip, to precisely co-ordinate window flip and beep
            nextflip = window.getFutureFlipTime(clock='ptb')

            beep.play(when=nextflip)

            # make random choice for stationary dot patches that should be used
            dotpatch_choice = np.random.randint(0, N)
            moving_direction = next(movingstates)


            # decision interval: light blue cross & moving dots
            response = []  # we have no response yet
            if moving_direction == 'right':
                stimulus_s1 = subjects[0].movingrightdotslist[dotpatch_choice]
                stimulus_s2 = subjects[1].movingrightdotslist[dotpatch_choice]
            else:
                stimulus_s1 = subjects[0].movingleftdotslist[dotpatch_choice]
                stimulus_s2 = subjects[1].movingleftdotslist[dotpatch_choice]

            for frame in seconds_to_frames(100, REFRESH_RATE):

                if frame % 3 == 0:
                    decision_interval(subjects, stimulus_s1[0], stimulus_s2[0])

                elif frame % 3 == 1:
                    decision_interval(subjects, stimulus_s1[1], stimulus_s2[1])

                elif frame % 3 == 2:
                    decision_interval(subjects, stimulus_s1[2], stimulus_s2[2])

                window.flip()

                # get button presses
                if not response:
                    response = get_button_presses(subjects)
                else:
                    break

            # need to explicity call stop() to go back to the beginning of the beep audio
            beep.stop()

            # prepare feedback interval: color of fixation cross depends on response
            if not response:
                color = "green"
            else:
                if response[0] == "left":  # left
                    color = "yellow"
                elif response[0] == "right":  # right
                    color = "blue"

                if response[0] == moving_direction:  # correct response
                    n_correct += 1
                if response[1] > 1.5:
                    timing_flag = "slow"
                elif response[1] < 0.1:
                    timing_flag = "fast"

            # make random choice for stationary dot patch that should be used
            stationary_choice = np.random.randint(0, N)

            # show feedback interval: display the fixation cross color based on the correctness of response & stationary dots for 1s
            for frame in seconds_to_frames(1, REFRESH_RATE):
                fixation_feedback(color, subjects, stationary_choice, timing_flag)
                window.flip()

            # after one trial is over
            if not main_experiment:
                block_number= -0.5

            # save response to file
            experiment_handler.addData('block', block_number)
            experiment_handler.addData('trial', trial_number)
            experiment_handler.addData('s1_state', subjects[0].state)
            experiment_handler.addData('direction', moving_direction)

            if subjects[0].state:
                experiment_handler.addData("coherence", subjects[0].coherence)

            else:
                experiment_handler.addData("coherence", subjects[1].coherence)
            experiment_handler.addData('response', response[0])
            experiment_handler.addData('rt', response[1])
            # save psychometric curve parameters
            experiment_handler.addData("drift_rate_1", subjects[0].drift_rate)
            experiment_handler.addData("drift_rate_2", subjects[1].drift_rate)
            experiment_handler.addData("bound_1", subjects[0].bound)
            experiment_handler.addData("bound_2", subjects[1].bound)
            experiment_handler.addData("offset_1", subjects[0].offset)
            experiment_handler.addData("offset_2", subjects[1].offset)

            # move to next row in output file
            experiment_handler.nextEntry()

            # add correctness to list
            correct = response[0] == moving_direction #[0.05, 0.1, 0.2, 0.4, 0.8] * 40
            if subjects[0].state:
                subject_1_correctness.append(correct)
            else:
                subject_2_correctness.append(correct)

        # after one block is over
        if main_experiment:

            # after every second block (unless after the last block), there will be a mandatory break which only the experimenter can end
            if (block_number+1) % 2 == 0 and (block_number+1) != (blocks[1]):
                show_mandatory_breakscreen(subjects, window)

            elif (block_number+1) != (blocks[1]):
                show_breakscreen(subjects, window)
            #experiment_handler.saveAsWideText(filepath +"TEMP" + ".csv", fileCollisionMethod="rename")
            if not block_number+1 == blocks[1]:
                experiment_handler.saveAsWideText(filepath +"TEMP" + ".csv", fileCollisionMethod="rename")
                #define filepath to save psychometric curve graphs to
                time = data.getDateStr()
                save_plot_path = "data/" + str(subjects[0].pair_id) + "/data"

                subjects[0].update_threshold(filepath+"TEMP.csv", window=window, save_plot_to=save_plot_path + str(subjects[0].id) + time + ".svg", horizontal_shifting=False, recompute_ddm=True)
                subjects[1].update_threshold(filepath+"TEMP.csv", window=window,  save_plot_to=save_plot_path + str(subjects[1].id) + time + ".svg",horizontal_shifting=False, recompute_ddm=True)

                os.remove(filepath+"TEMP"+".csv")

                get_confirmation(subjects)

            print(f"Done with block {block_number}")


    # after all blocks are over
    if not main_experiment:
        # Print correctness on the terminal for Practice Trials
        print("{0:*>31s} {1:<5.2%}".format('Practice Trials Correct: ',n_correct/n_trials))

    return experiment_handler


def titration(repetitions, coherences, subject, window, REFRESH_RATE, experiment_handler, practice=False):
    """
    This function runs the titration procedure (without the psychometric function fitting) and saves the data to a file (as specified in the experiment_handler).

    Arguments:
    repetitions (int) : Number of repetitions to show each element in coherences.
    coherences (list) : a list of float values between 0 and 1.
    subject           : A single subject object (see subject_utils.py)
    window            : A psychopy window
    REFRESH_RATE      : The refresh rate of the screen
    experiment_handler: A psychopy experiment handler to save data to a csv file.
    practice (bool)   : To specify whether it is practice or not. For practice, the block number will be set to -2. For main titration, it will be -1.

    Returns: if practice is set to True, (experiment_handler, accuracy). For the main titration only the experiment_handler is returned.
    """
    correct_list = []

    trials = coherences * repetitions

    np.random.shuffle(trials)

    for trial_number, coherence_trial in enumerate(trials):
        response = []
        direction = np.random.choice(np.array([0, 180]))
        if direction == 180:

            direction_str = 'left'
        else:

            direction_str = 'right'
        dotpatch = subject.stimulus.createMovingDots(1, window, 0, direction, coherence_trial, stimuli.ndots, stimuli.dotlife, stimuli.speed, titration=True)

        # pretrial interval: display light blue fixation cross & stationary dots for 1 - 2 s (uniformly distributed)
        if trial_number == 0:
            for frame in seconds_to_frames(np.random.uniform(1, 2), REFRESH_RATE):
                pretrial_interval(choice=0, subjects=subject, titration=True)
                window.flip()
        else:
            for frame in seconds_to_frames(np.random.uniform(1, 2), REFRESH_RATE):
                pretrial_interval(choice=stationary_choice, subjects=subject, titration=True)
                window.flip()

        # reset subject keyboards and timer

        subject.keyboard.clearEvents(eventType="keyboard")
        subject.keyboard.clock.reset()

        # preparing time for next window flip, to precisely co-ordinate window flip and beep
        nextflip = window.getFutureFlipTime(clock='ptb')

        subject.beep.play(when=nextflip)


        # DECISION INTERVAL
        for frame in seconds_to_frames(100, REFRESH_RATE):

            if frame % 3 == 0:
                decision_interval(subject, dotpatch[0], None, titration=True)

            elif frame % 3 == 1:
                decision_interval(subject, dotpatch[1], None, titration=True)

            elif frame % 3 == 2:
                decision_interval(subject, dotpatch[2], None, titration=True)

            else:
                print('an error occured')

            window.flip()

            # get button presses
            if not response:
                response = get_button_presses(subject, titration=True)
            else:
                break

        subject.beep.stop()

        if response[0] == "left":  # left
            color = "yellow"
        if response[0] == "right":  # right
            color = "blue"

        if response[0] == direction_str:  # correct response
            correct = 1
        else:
            correct = 0
        if response[1] > 1.5:
            timing_flag = "slow"
        elif response[1] < 0.1:
            timing_flag = "fast"
        else:
            timing_flag = "NA"

        stationary_choice = np.random.randint(0, subject.N)
        # add correctness to list
        correct_list.append(correct)
        #FEEDBACK interval

        # feedback interval: display the fixation cross color based on the correctness of response & stationary dots for 1s
        for frame in seconds_to_frames(1, REFRESH_RATE):
            if correct:
                visual.TextStim(window,
                                text="correct!", pos=(-0, -150),
                                color='green', height=30).draw()
            else:
                visual.TextStim(window,
                                text="incorrect", pos=(-0, -150),
                                color='red', height=30).draw()
            fixation_feedback(color, subject, stationary_choice, timing_flag, titration=True)
            window.flip()

        if not practice:
            block_number=-1
        else:
            block_number=-2

        experiment_handler.addData('block', block_number)
        experiment_handler.addData('trial', trial_number)
        experiment_handler.addData('subject_id', subject.id)
        experiment_handler.addData('direction', direction_str)
        experiment_handler.addData("coherence", coherence_trial)
        experiment_handler.addData("practice", int(practice))
        experiment_handler.addData('response', response[0])
        experiment_handler.addData('rt', response[1])

        # move to next row in output file
        experiment_handler.nextEntry()

    print(f"A: {np.mean(correct_list)}")

    if practice:
        return experiment_handler, np.mean(correct_list)
    else:
        return experiment_handler
