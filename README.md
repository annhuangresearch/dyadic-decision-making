# Dyadic Decision Making Experiment Code
Written by @mathispink

This is the experiment code used for the Dyadic Decision Making project.

**Required packages** are:  
PsychoPy  
PyDDM  
Numpy  
Pandas  
Scipy  
Matplotlib  
_______________________________________________________________________________________________________________________________________________________________________________________

To run the experiment, run the two scripts described below in the terminal (in the experiment_files folder) with PAIR_ID being an integer number:


**titration_random_dots.py**:
This script runs the titration experiment for one subject. Upon running, you need to specify the chamber and register all connected button boxes. It then proceeds with up to 3 practice runs of 40 trials with a coherence set to 40%, depending on whether
the participant reaches a 75% mean correctness threshold. Participants who do not reach this level of performance are excluded (as done in Murphy et al 2014). During both the practice and main titration experiment, data is saved to a csv file.
This data includes the shown coherence values, the direction of the dots, and the response by the participant as well as the response time. For the main titration experiment, coherences in the set {0.05,0.1,0.2,0.4,0.8} are shown 40 times each, in a random order.
The non-practice data is then used to fit a simple DDM model, whose drift rate and decision bound parameters are
then used to parameterize a psychometric function (as it is done in Palmer et al 2005). The final output file is a json file with the psychometric parameters and the estimated 75% mean correctness threshold.

**dyadic_random_dots.py**:
This script is used to run the main experiment (having two screens connected as well as two button boxes and a usb audio device). It expects the titration script to have run before.

To make this work with different hardware than what we used in the EEG lab, change the variable strings in dyadic_random_dots and titration_random_dots to the used hardware: **monitor_name**, **audio_device_name**, **button_box_name**

Depending on your operating system, you may need to change the following lines of code in dyadic_random_dots.py and titration_random_dots.py:  

import ctypes  
xlib = ctypes.cdll.LoadLibrary("libX11.so")  
xlib.XInitThreads()

_______________________________________________________________________________________________________________________________________________________________________________________

The following scripts/modules are not meant to be run individually. Rather, they present the common backbone of what happens in titration_random_dots and dyadic_random_dots.

**stimuli_random_dots.py**:
This file contains the specifics of the stimuli that will be shown. This includes the speed, size, number, and lifetime of the dots, the fixation cross, lexical warnings and screen settings (resolution and screen width/height)

**experiment_parts.py**:
This is the main backbone of both titration and dyadic main experiment. The functions experiment and titration deal with presenting the stimuli, tracking response times and saving data. Everything during the experiment is done through these functions.
In comparison to this module, the titration and dyadic_random_dots scripts deal with the setup that allows to have the main experiment and titration. Both the experiment and the titration functions allow for a practice mode.

**subject_utils.py**:
This module contains the subject class which keeps track of everything subject related (each subject has its own individualized stimuli, its own psychometric parameters, titration data filepath, designated keyboard etc.)

**experiment_utils.py**:
This module contains two small functions to choose whose turn it is.

**intervals.py**:
This module contains what is shown on each frame during pretrial, decision, and fixation feedback intervals. The times these are shown are contained in experiment_parts.py

**draw_stimuli.py**:
This module contains the necessary functions to draw both stationary and moving dots as well as the fixation cross.

**psychometric_function_fitting.py**:
This module contains parts that are relevant for DDM fitting and psychometric calculations used during titration and in between blocks during the main experiment.

**keyboard_utils.py**:
This module contains utilities to register the keyboards with psychopy/psychtoolbox

**text_instructions.py**:
This module contains the texts to be shown as instruction before the main experiment, as well as during breaks between blocks and at the end of the experiment.

**text_instructions_titration.py**:
Same as text_instructions.py, this file contains the instructions shown during titration.
