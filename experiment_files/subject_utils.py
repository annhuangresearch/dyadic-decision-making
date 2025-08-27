#import stimuli_random_dots as stimuli
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import stimuli_random_dots as stimuli
import json
import psychopy
from psychopy.sound import Sound
from psychometric_function_fitting import *

class subject:
    def __init__(self, pair_id, subject_id, N, window, offset, keyboard, speed, ndots, titration=False):

        '''
            Subject class deals with everything about the subject including psychometric function updating,
            individualized stimuli, beeps and other attributes.

            Besides the init method, there is an update_threshold method to update the coherence threshold to achieve a certain level of mean correctness.
            It uses the titration data combined with the main experiment data to compute a new version of the psychometric function using a proportional drift rate model (see Palmer et al 2005).

            Arguments:
            pair_id (int) : The pair id for this experiment run. Has to match with the location of the titration files (inside /data/pair_id/...)
            subject_id (int) : 1 for subject 1 (chamber 1) and 2 for subject 2 (chamber 2)
            N (int) : Number of dot patches to prepare
            window : psychopy window to draw on
            offset (int) : where on the window that is extended over two screens to draw stimuli for this subject
            keyboard (psychopy keyboard) : keyboard (button box) for this subject.
            speed (int or float) : speed of the moving dots
            ndots (int) : number of dots
            titration (bool) : whether to prepare the subject object for titration or for the main experiment. Defaults to dyadic experiment mode, expecting titration to have already been done.
        '''

        self.titration = titration


        if not titration:
            # the button boxes produce either 1(left), 2(right) or 8(left), 7(right)
            keys = ["1", "2"] if subject_id == 1 else ["8", "7"]
            self.titration_fp = "data/" + str(pair_id) + "/data_chamber" + str(subject_id) + ".json"

            # loading subject titration threshold from the corresponding json file
            try:
                with open(self.titration_fp, "r") as f:
                    data = json.load(f)
                #f = open("data/" + str(pair_id) + "/data_chamber" + str(subject_id) + ".json", "r")
            except FileNotFoundError:
                print("Titration file not found for subject in chamber {}".format(subject_id))
                exit(-1)
            else:

                self.coherence = data["threshold"]
                self.coherence_list = [data["threshold"]]
                self.titration_csv = data["filepath"]
                self.drift_rate = data["drift_rate"]
                self.drift_rates = [data["drift_rate"]]
                self.bound = data["bound"]
                self.bounds = [data["bound"]]
                self.offset = 0 #initial offset is zero
                self.offsets = [0]


            self.ndots= ndots
            self.speed= speed
            self.N= N
            self.id = subject_id
            self.pair_id = pair_id
            self.keyboard = keyboard
            self.state = False # state=False means it's not the subject's turn to decide
            # set the offset for the window
            self.xoffset = offset
            # initialize the response to be None.
            self.response = None

            # set the beep sound depending on subject_id (1 is left chamber, 2 is right chamber)
            if subject_id == 1:
                self.beep = Sound('C', secs=0.5, volume=0.1, octave=5, name="S1")
            else:
                self.beep = Sound('F', secs=0.5, volume=0.1, octave=4, name="S2")

            # incorporate the stimulus from stimuli_random_dots.py N, window, xoffset, coherence, ndots, speed
            self.stimulus = stimuli.MainStimulus(self.N, window=window, xoffset=self.xoffset, coherence=self.coherence, ndots=self.ndots, speed=self.speed)

            # dictionary with keys (1,2 or 7,8) to response string mapping.
            self.buttons = {
                    keys[0] : "left",
                    keys[1] : "right",
                    None : "noresponse"
                    }

            # stationary dot patches for pretrial and feedback phase
            self.stationarydotslist = self.stimulus.stationaryDotsList

            # moving dot patches for decision phase in practice trials
            self.movingrightdotslistpractice = self.stimulus.movingRightDotsListPractice
            self.movingleftdotslistpractice = self.stimulus.movingLeftDotsListPractice

            # moving dot patches for decision phase in main experiment
            self.movingrightdotslist = self.stimulus.movingRightDotsList
            self.movingleftdotslist = self.stimulus.movingLeftDotsList

            # light blue fixation cross for decision phase
            self.bluecross = self.stimulus.fixation_blue

            # green fixation dot for feedback period (green = right)
            self.greencross = self.stimulus.fixation_green

            # red fixation dot for feedback period (red = left)
            self.yellowcross = self.stimulus.fixation_yellow

            # passing the response speed feedback to the stim object
            self.indicatordict = self.stimulus.indicatordict

        #TITRATION-SETUP
        else:
            # set the beep sound depending on subject_id (1 is left chamber, 2 is right chamber)
            if subject_id == 1:
                self.beep = Sound('C', secs=0.5, volume=0.1, octave=5, name="S1")
            else:
                self.beep = Sound('F', secs=0.5, volume=0.1, octave=4, name="S2")

            keys = ["1", "2"] if subject_id == 1 else ["8", "7"]
            self.titration_fp = "data/" + str(pair_id) + "/data_chamber" + str(subject_id) + ".json"
            self.ndots= ndots
            self.speed= speed
            self.N= N
            self.id = subject_id
            self.keyboard = keyboard
            self.state = True # state=False means it's not the subject's turn to decide
            # set the offset for the window
            self.xoffset = offset
            # initialize the response to be None.
            self.response = None

            # incorporate the stimulus from stimuli_random_dots.py N, window, xoffset, coherence, ndots, speed
            self.stimulus = stimuli.MainStimulus(self.N, window=window, xoffset=self.xoffset, coherence=0.4, ndots=self.ndots, speed=self.speed)

            # dictionary with keys (1,2 or 7,8) to response string mapping.
            self.buttons = {
                    keys[0] : "left",
                    keys[1] : "right",
                    None : "noresponse"
                    }

            # stationary dot patches for pretrial and feedback phase
            self.stationarydotslist = self.stimulus.stationaryDotsList

            # moving dot patches for decision phase in practice trials
            self.movingrightdotslistpractice = self.stimulus.movingRightDotsListPractice
            self.movingleftdotslistpractice = self.stimulus.movingLeftDotsListPractice

            # moving dot patches for decision phase in main experiment
            self.movingrightdotslist = self.stimulus.movingRightDotsList
            self.movingleftdotslist = self.stimulus.movingLeftDotsList

            # light blue fixation cross for decision phase0.16707
            self.bluecross = self.stimulus.fixation_blue

            # green fixation dot for feedback period (green = right)
            self.greencross = self.stimulus.fixation_green

            # red fixation dot for feedback period (red = left)
            self.yellowcross = self.stimulus.fixation_yellow

            # passing the response speed feedback to the stim object
            self.indicatordict = self.stimulus.indicatordict
        print("subject created")

    def __repr__ (self):
        return str(self.id)


    def update_threshold(self, data_filepath, window, requested_accuracy=0.75, save_plot_to=None, horizontal_shifting=True, recompute_ddm=False):
        """
        Updates the coherence and psychometric data of this subject by fitting a DDM model to the combined data from titration and the main experiment.

        Arguments:
        data_filepath (str) : filepath of the main experiment data
        window (psychopy window): window to reinitialize stimuli with the new coherence value for this subject.
        requested_accuracy (float) : A float between 0.5 and 1.0, specifying the desired accuracy of participants.
        save_plot_to (str)    : filepath to save the psychometric curve plot as an svg
        horizontal_shifting (bool) : Whether to additionally shift the new psychometric curve to perfectly align with the mean correctness data from the last block.

        """
        s1_state = bool(self.id % 2)
        if recompute_ddm:
            sample = load_combined_data(self.titration_csv, data_filepath, s1_state=s1_state)
            # recompute psychometric function taking into account the new data
            threshold, drift_rate, bound = fit_ddm_psychometric_function(sample, requested_accuracy, save_plot_to=save_plot_to)

        else:
            threshold = self.coherence
            drift_rate = self.drift_rate
            bound = self.bound
            offset = 0

        # shift to align with most recent data
        if horizontal_shifting:
            # load data from last block and get the empirical accuracy
            df = pd.read_csv(data_filepath)
            df = df[df["s1_state"]==s1_state]
            df = df[df['block'] == np.max(df["block"])]
            df = df[df["rt"]<1.5]
            df = df[df["rt"]>0.1]
            df["correct"] = df["direction"] == df["response"]
            empirical_accuracy = df["correct"].mean()

            if empirical_accuracy == 1.0:
                empirical_accuracy = 0.995

            offset = -np.log((1/empirical_accuracy)-1)/(2*bound*drift_rate) - threshold
            shifted_threshold = psychometric_inverse(requested_accuracy, bound, drift_rate, offset=offset)

            if shifted_threshold < 1.0 and shifted_threshold > 0.0:
                threshold = shifted_threshold
                self.offsets.append(offset)
        else:
            offset = self.offset
        if threshold > 1.0 or threshold < 0.0:
            threshold = self.coherence_list[-1] #if the function fitting doesn't work, we stick with the old coherence value\
            bound = self.bounds[-1]
            drift_rate = self.drift_rates[-1]
            offset = 0

        self.coherence = threshold
        self.drift_rate = drift_rate
        self.bound = bound
        self.offset = offset

        self.coherence_list.append(threshold)
        self.drift_rates.append(drift_rate)
        self.bounds.append(bound)

        # plot new psychometric curve
        smooth_intensities = np.linspace(0, 1, 200)
        fig, ax = plt.subplots(1, 1)
        ax.plot(smooth_intensities, psychometric_function(smooth_intensities + self.offset, self.bound, self.drift_rate), '-')
        ax.axhline(requested_accuracy, linestyle='-', color='orange')
        ax.axvline(self.coherence, linestyle='-', color='orange')
        plt.title('coherence threshold = %0.3f' % self.coherence)
        plt.xlabel('Coherence')
        plt.ylabel("Accuracy")
        #plt.plot(df['coherence'], df['correct'], 'o')
        plt.ylim([0, 1])
        plt.savefig(save_plot_to)

        #update stimuli for new coherence value
        self.stimulus = stimuli.MainStimulus(self.N, window=window, xoffset=self.xoffset, coherence=self.coherence, ndots=self.ndots, speed=self.speed)
        # stationary dot patches for pretrial and feedback phase
        self.stationarydotslist = self.stimulus.stationaryDotsList

        # moving dot patches for decision phase in practice trials
        self.movingrightdotslistpractice = self.stimulus.movingRightDotsListPractice
        self.movingleftdotslistpractice = self.stimulus.movingLeftDotsListPractice

        # moving dot patches for decision phase in main experiment
        self.movingrightdotslist = self.stimulus.movingRightDotsList
        self.movingleftdotslist = self.stimulus.movingLeftDotsList

def update_state(subjects, states_iterator, titration=False):
    '''
        Update whose turn it is.
    '''
    if not titration:
        subjects[0].state = next(states_iterator)
        subjects[1].state = bool(1 - subjects[0].state)

    else:
        subjects.state=True
