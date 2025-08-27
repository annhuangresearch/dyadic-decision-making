import os
import sys
from subprocess import run
import numpy as np
import psychtoolbox as ptb
from psychopy import visual, core, gui, data, prefs, monitors, hardware
from psychopy.hardware import keyboard
import random
import json
import experiment_files.stimuli_random_dots as stimuli

# necessary on linux (stimpy, otherwise it does not work reliably)
import ctypes
xlib = ctypes.cdll.LoadLibrary("libX11.so")
xlib.XInitThreads()

# audio settings (audio device name)
prefs.hardware['audioLib'] = ['PTB', 'sounddevice', 'pyo', 'pygame']
from psychopy import sound
from psychopy.sound import Sound
button_box_name = "Black Box Toolkit Ltd. BBTK Response Box"
audio_device_name = 'USB Audio Device: - (hw:3,0)'
monitor_name = 'DellU2412M'
sound.setDevice(audio_device_name)

# import experiment specific modules
from experiment_files.text_instructions import show_startscreen, show_practice_instructions, show_experiment_instructions, show_breakscreen, show_mandatory_breakscreen, show_endscreen
from experiment_files.keyboard_utils import get_confirmation, get_keyboards
from experiment_files.subject_utils import subject, update_state
from experiment_files.experiment_parts import sound_familiarisation, experiment

# how many practice trials
n_practice_trials = 40
# specify how many blocks and trials per block for the main experiment
blocks = [0,10]
n_trials = 100

# get pair id via command-line argument
pair_id_is_int = False
while not pair_id_is_int:
    try:
        pair_id = int(sys.argv[1])
        pair_id_is_int = True
    except:
        print('Please enter a number as pair id as command-line argument!')

# variables and settings for the monitors (distance to screen is set in stimuli_random_dots.py)
M_WIDTH = stimuli.M_WIDTH*2
M_HEIGHT = stimuli.M_HEIGHT
REFRESH_RATE = stimuli.REFRESH_RATE
N = stimuli.N
speed = stimuli.speed
ndots = stimuli.ndots

window = monitors.Monitor(monitor_name, width=M_WIDTH, distance=stimuli.distance)
window.setSizePix([M_WIDTH, M_HEIGHT])

window = visual.Window(size=(M_WIDTH, M_HEIGHT), monitor=window,
                       color="black", pos=(0,0), units='pix', blendMode='avg', # have to use 'avg' to avoid artefacts
                       fullscr=False, allowGUI=False)

# hide cursor
window.mouseVisible = False

keyboards = get_keyboards(button_box_name)

subject_1 = subject(pair_id=pair_id, subject_id=1, N=N, window=window, offset=int(window.size[0]//4), keyboard=keyboards["chamber one"][1], speed=speed, ndots=ndots)
subject_2 = subject(pair_id=pair_id, subject_id=2, N=N, window=window, offset=-int(window.size[0]//4), keyboard=keyboards["chamber two"][1], speed=speed, ndots=ndots)
subjects = [subject_1, subject_2]

# experiment info for the data file
experiment_info = {'pair': pair_id}

# specifications of output file
_thisDir = os.path.dirname(os.path.abspath(__file__))
experiment_name = 'DDM'
filename = f"{_thisDir}/data/{experiment_name}_pair{experiment_info['pair']}_{data.getDateStr()}"
#_thisDir + os.sep + u'data/%s_pair%s_%s' % (experiment_name, experiment_info['pair'], data.getDateStr())

# the experiment handler will be used to save data to the file
exphandler = data.ExperimentHandler(name=experiment_name, extraInfo=experiment_info, saveWideText=True, dataFileName=filename)

##################################
##### SOUND FAMILIARIZATION #####
##################################

sound_familiarisation(subjects, window, REFRESH_RATE)

##################################
##### PRACTICE TRIALS  START #####
##################################

show_practice_instructions(subjects, window)
get_confirmation(subjects)

exphandler = experiment(blocks=[0,1], n_trials=n_practice_trials,
            N=N,
            subjects=subjects,
            window=window,
            REFRESH_RATE=REFRESH_RATE,
            experiment_handler=exphandler,
            filepath=filename,
            main_experiment=False)

#################################
##### MAIN EXPERIMENT START #####
#################################

show_experiment_instructions(subjects, window)
get_confirmation(subjects)

experiment(blocks=blocks,
            n_trials=n_trials,
            N=N,
            subjects=subjects,
            window=window,
            REFRESH_RATE=REFRESH_RATE,
            experiment_handler=exphandler,
            filepath=filename,
            main_experiment=True)

################################
###### EXPERIMENT END-SCREEN #####
################################

show_endscreen(subjects, window)
core.wait(15)
