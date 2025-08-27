from __future__ import division
from __future__ import print_function

from psychopy import visual, event, core
from random import choice
from math import tan, pi, atan

# monitor specs global variables
M_WIDTH = 1920
M_WIDTH_CM = 51.84
M_HEIGHT = 1200
REFRESH_RATE = 60

my_dpi = 96 # dpi of the lab monitor
distance = 60 # distance to screen in cm
N = 250

ndots = 328
dotlife = 5
speed = 199*3 / REFRESH_RATE

class MainStimulus:
    """
    Contains the stimuli that will be located inside the subject objects.
    """

    def __init__(self, N, window, xoffset, coherence, ndots, speed, dotlife = dotlife):
        """
        Arguments:
        N (int) : How many dot patches to prepare
        window : Psychopy window to draw on
        xoffset (int): horizontal offset of stimuli for dyadic experiment with extended screen
        coherence (float) : coherence level for the stimuli
        ndots (int) : Number of dots
        speed (int) : Speed of the dots (in pixels per second)
        dotlife (int) : Frames for each dot to be shown
        """
        self.coherence = coherence
        self.dotlife = dotlife
        # list of differently distributed startionary dots
        self.stationaryDotsList = self.createStationaryDots(N, window, xoffset, coherence, ndots)

        # lists of differently distributed moving dots (first for direction=0,
        # second for direction=180) for main experiment
        self.movingRightDotsList = self.createMovingDots(N, window, xoffset, 0, coherence, ndots, dotlife, speed)  #N, window, xoffset, dir, coherence, ndots, dotlife, speed
        self.movingRightDotsListPractice = self.createMovingDots(N, window, xoffset, 0, coherence, ndots, dotlife, speed)
        self.movingLeftDotsList = self.createMovingDots(N, window, xoffset, 180, coherence, ndots, dotlife, speed)
        self.movingLeftDotsListPractice = self.createMovingDots(N, window, xoffset, 180, coherence, ndots, dotlife, speed)
        # fixation composite targets
        self.fixation_green = self.createFixation(window, xoffset, "forestgreen")
        self.fixation_blue = self.createFixation(window, xoffset, "deepskyblue")
        self.fixation_yellow = self.createFixation(window, xoffset, "yellow")


        #For response time related warning to be shown on top of fixation cross
        #a. if response time < 100 ms: Too Fast
        #b. response time > 1500 ms: Too Slow
        self.indicatordict = {
            "slow": visual.TextStim(
                win=window, text="Too Slow", units='pix', pos=[xoffset, 0], color='red'
            ),
            "fast": visual.TextStim(
                win=window, text="Too Fast", units='pix', pos=[xoffset, 0], color='red'
            ),
            "partner slow": visual.TextStim(
                win=window, text="Partner Too Slow", units='pix', pos=[xoffset, 0], color='red'
            ),

            "partner fast": visual.TextStim(
                win=window, text="Partner Too Fast", units='pix', pos=[xoffset, 0], color='red'
            )
        }

    def createDots (self, window, xoffset, dir, ndots, dotlife, speed, coherence):
        return visual.DotStim(
            window,
            color=(1.0, 1.0, 1.0),
            dir = dir,
            units='pix',
            nDots=ndots,
            fieldShape='circle',
            fieldPos=[0 + xoffset, 0],
            fieldSize=199, #degrees_to_pix(5),
            dotLife=dotlife, # number of frames for each dot to be drawn
            dotSize=3,
            signalDots='same',
            noiseDots='direction', # do the noise dots follow random- 'walk', 'direction', or 'position'
            speed=speed, #  degrees_to_pix(5) / REFRESH_RATE
            coherence=coherence
        )

    def createStationaryDots (self, N, window, xoffset, coherence, ndots, titration=False):
        '''
            creates N different patches of randomly distributed stationary dots
        '''
        dotsList = []

        for _ in range(N):
            dotsList.append(self.createDots(window, xoffset, 0, ndots, -1, 0, coherence))
        if not titration:
            return dotsList
        else:
            return dotsList[0]

    def createMovingDots (self, N, window, xoffset, dir, coherence, ndots, dotlife, speed, titration=False):
        '''
            creates 3xN different patches of randomly distributed moving dots
            3 patches are then used for the interleaving frames
        '''
        dots = []
        dotsList = []

        for _ in range(N):
            for count in range(3):
                    dots.append(self.createDots(window, xoffset, dir, ndots//3, dotlife, speed, coherence))

            dotsList.append(dots)

        if not titration:
            return dotsList
        else:
            return dotsList[0]

    def createFixation (self, window, xoffset, color):
        fixationList = [
            visual.GratingStim(
                win=window, size=21, units='pix', pos=[0 + xoffset, 0],
                sf=0, color=color, mask='circle'
            ),

            visual.GratingStim(
                win=window, size=25, units="pix",  pos=[0 + xoffset, 0],
                sf=0, color="black", mask="cross"
            ),

            visual.GratingStim(
                win=window, size=7, units='pix', pos=[0 + xoffset, 0],
                sf=0, color=color, mask='circle'
            )
        ]
        return fixationList
