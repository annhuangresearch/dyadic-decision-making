def draw_fixation(color, subjects, titration=False):
    '''
        Draw the fixation crosses for both subjects or for a single subject.

        Arguments:
        color (str) : either green, yellow or blue.
        subjects    : either a list of subject objects or a single subject object if titration is set to True.
        titration (bool): Defaults to False for the main experiment. Can be set to True for a single subject setting.
    '''
    if not titration:
        subject_one, subject_two = subjects

    if color == "green":
        if not titration:
            for grating_one, grating_two in zip(subject_one.greencross, subject_two.greencross):
                grating_one.draw()
                grating_two.draw()
        else:
            for grating in subjects.greencross:
                grating.draw()

    elif color == "yellow":
        if not titration:
            for grating_one, grating_two in zip(subject_one.yellowcross, subject_two.yellowcross):
                grating_one.draw()
                grating_two.draw()
        else:
            for grating in subjects.yellowcross:
                grating.draw()

    elif color == "blue":
        if not titration:
            for grating_one, grating_two in zip(subject_one.bluecross, subject_two.bluecross):
                grating_one.draw()
                grating_two.draw()
        else:
            for grating in subjects.bluecross:
                grating.draw()

def draw_stationary_dots(choice, subjects, titration=False):
    '''
        draw the stationary dot patch for both subjects or for a single subject during titration.

        Arguments:
        choice (int) : Index of the dot patch to use.
        subjects     : either a list of subject objects or a single subject object if titration is set to True.
        titration (bool): Defaults to False for the main experiment. Can be set to True for a single subject setting.
    '''
    if not titration:
        for s in subjects:
            s.stationarydotslist[choice].draw()
    else:
        subjects.stationarydotslist[choice].draw()

def draw_moving_dots(subjects, stimulus_s1, stimulus_s2, titration=False):
    '''
        draw the moving dot patch for both subjects for the
        main experiment or for a single subject during titration.

        Arguments:
        subjects     : either a list of subject objects or a single subject object if titration is set to True.
        stimulus_s1  : stimulus for subject 1
        stimulus_s2  : stimulus for subject 2 (can be None if titration is set to True)
        titration (bool): Defaults to False for the main experiment. Can be set to True for a single subject setting.
    '''
    if not titration:
        stimulus_s1.draw()
        stimulus_s2.draw()
    else:
        stimulus_s1.draw()
