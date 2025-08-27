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
import ddm

# necessary on linux (stimpy, otherwise it does not work reliably)
import ctypes
xlib = ctypes.cdll.LoadLibrary("libX11.so")
xlib.XInitThreads()

# audio settings
prefs.hardware['audioLib'] = ['PTB', 'sounddevice', 'pyo', 'pygame']
from psychopy import sound
from psychopy.sound import Sound

###########################
##### Device Settings ##### (change this if you use different hardware)
###########################
button_box_name = "Black Box Toolkit Ltd. BBTK Response Box"
audio_device_name = 'USB Audio Device: - (hw:3,0)'
monitor_name = "DellU2412M"

sound.setDevice(audio_device_name)

# import experiment specific modules
from experiment_files.text_instructions_titration import show_practice_instructions, show_experiment_instructions, show_endscreen
from experiment_files.keyboard_utils import get_confirmation, get_keyboards
from experiment_files.subject_utils import subject, update_state
from experiment_files.experiment_parts import sound_familiarisation, titration
from experiment_files.psychometric_function_fitting import fit_ddm_psychometric_function, load_data

# get pair id via command-line argument
pair_id_is_int = False
while not pair_id_is_int:
    try:
        pair_id = int(sys.argv[1])
        pair_id_is_int = True
    except:
        print('Please enter a number as pair id as command-line argument!')

chamber = []
while not len(chamber):

    print("Enter chamber number (1 or 2):")
    chamber = input()

    if chamber not in ["1", "2"]:
        print("Incorrect chamber number. Enter chamber number (1 or 2):")
        continue

# set up monitor/window
# variables and settings for the monitors (distance to screen is set in stimuli_random_dots.py)
M_WIDTH = stimuli.M_WIDTH
M_HEIGHT = stimuli.M_HEIGHT
REFRESH_RATE = stimuli.REFRESH_RATE
N = stimuli.N
speed = stimuli.speed
ndots = stimuli.ndots
distance = stimuli.distance

my_mon = monitors.Monitor(monitor_name, width=M_WIDTH, distance=distance)
my_mon.setSizePix([M_WIDTH, M_HEIGHT])

window = visual.Window(size=(M_WIDTH, M_HEIGHT), units='pix', screen=int(chamber), fullscr=False, pos=None, color =[-1,-1,-1])

# hide cursor
window.mouseVisible = False

# register keyboards
keyboards = get_keyboards(button_box_name)

# create subject
if int(chamber) == 1:
    chamber_str = "chamber one"
elif int(chamber) == 2:
    chamber_str = "chamber two"

subject = subject(pair_id=pair_id,
                    subject_id=int(chamber),
                    N=N, window=window,
                    offset=0,
                    keyboard=keyboards[chamber_str][1],
                    speed=speed,
                    ndots=ndots,
                    titration=True)

# experiment info for the data file
experiment_info = {'pair': pair_id}

# specifications of output file
HOME = os.getcwd()
DATA = '/data/'
# create pair folder
if not os.path.exists(f'{HOME}{DATA}{experiment_info["pair"]}/'):
    os.makedirs(f'{HOME}{DATA}{experiment_info["pair"]}/')

experiment_name = 'DDM'
date = data.getDateStr()
filename = HOME + DATA + f'{experiment_name}_pair{experiment_info["pair"]}_{chamber}_titration{date}'

# the experiment handler will be used to save data to the file
experiment_handler = data.ExperimentHandler(name=experiment_name, extraInfo=experiment_info, saveWideText=True, dataFileName=filename)


##################################
############ PRACTICE ############
##################################
show_practice_instructions(subject, window)
get_confirmation(subject,titration=True)

repetitions = 40
coherences = [0.4]
accuracy=0
practice_count=0
practice_accuracy_threshold = 0.75
max_practice_runs = 3

while accuracy<practice_accuracy_threshold and practice_count<max_practice_runs:
    experiment_handler, accuracy = titration(repetitions, coherences, subject, window, REFRESH_RATE, experiment_handler, practice=True)
    practice_count+=1

show_experiment_instructions(subject,window)
get_confirmation(subject,titration=True)

##################################
############ TITRATION ###########
##################################
repetitions = 40
coherences = [0, 0.05, 0.1, 0.2, 0.4, 0.8]
experiment_handler = titration(repetitions, coherences, subject, window, REFRESH_RATE, experiment_handler, practice=False)

#make sure data is saved before script finishes
experiment_handler.saveAsWideText(filename+".csv")

##################################
### FIT PSYCHOMETRIC FUNCTION ####
##################################
sample = load_data(filename+".csv")

desired_accuracy = 0.75

#save_path = HOME + DATA + str(experiment_info["pair"]) + "/data" + str(chamber) + data.getDateStr() + '_psyfunc.svg'
save_path = f'{HOME}{DATA}{experiment_info["pair"]}/data{chamber}{data.getDateStr()}_psyfunc.svg'
threshold, drift_rate, bound = fit_ddm_psychometric_function(sample, requested_accuracy=desired_accuracy, save_plot_to=save_path)

##################################
###### SAVE RESULTS TO JSON ######
##################################

subject_data = {"pair_id": pair_id,
                "filepath": filename + ".csv",
                "threshold" : threshold,
                "chamber"   : chamber,
                "drift_rate": drift_rate,
                "bound" : bound}
with open(f'{HOME}{DATA}{experiment_info["pair"]}/data_chamber{chamber}.json', 'w') as fp:
    json.dump(subject_data, fp)
show_endscreen(subject,window)
core.wait(10)
