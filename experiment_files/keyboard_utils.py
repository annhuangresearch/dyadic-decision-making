from psychopy.hardware import keyboard as psychopy_keyboard

def get_keyboards(button_box_name, keys_subject_1=["1","2"], keys_subject_2=["7","8"]):
    '''
        Search for the appropriate button box in each of the chambers
        Once a button has been pressed on each of the button boxes,
            create a keyboard object for each subject button box and assign it to them

    Arguments:
    button_box_name (str) : hardware name that will be found by psychopy. Use print([k["product"] for k in keyboard.getKeyboards()]) to find out which keyboards are connected.
    keys_subject_1 (list) : list of keys that subject 1 can press.
    keys_subject_2 (list) : list of keys that subject 2 can press.
    '''
    keyboards = psychopy_keyboard.getKeyboards()

    keys_pressed = {"chamber one" : None, "chamber two" : None}

    button_boxes = [keyboard for keyboard in keyboards if keyboard['product'] == button_box_name]

    for button_box in button_boxes:
        keytemp = psychopy_keyboard.Keyboard(button_box['index'])
        keypress = keytemp.waitKeys(keyList=keys_subject_1 +keys_subject_2)
        if keypress[0].name in keys_subject_1:
            keys_pressed['chamber one'] = (button_box['index'], keytemp)
        elif keypress[0].name in keys_subject_2:
            keys_pressed['chamber two'] = (button_box['index'], keytemp)

    return keys_pressed
def get_button_presses (subjects, titration=False):
    '''
        Get the button box input from the acting subject. Also has a mode for single subjects (titration)
        Return the response (the pressed key) and the reaction time
    '''
    if not titration:
        for s in subjects:
            if not s.state:
                continue
            else:
                temp = s.keyboard.getKeys(keyList=s.buttons.keys(), clear=True)

                if len(temp) == 0:
                    resp = []
                    s.response = s.buttons[None]
                else:
                    keystroke = temp[0].name
                    s.response = s.buttons[keystroke]
                    resp = [s.buttons[keystroke], temp[0].rt]
    # SINGLE SUBJECT (TITRATION)
    else:
        temp = subjects.keyboard.getKeys(keyList=subjects.buttons.keys(), clear=True)
        if len(temp) == 0:
            resp = []
            subjects.response = subjects.buttons[None]
        else:
            keystroke = temp[0].name
            subjects.response = subjects.buttons[keystroke]
            resp = [subjects.buttons[keystroke], temp[0].rt]
    return resp


def get_confirmation(subjects, titration=False):
    '''
        Wait until both subjects have confirmed they are ready by pressing "yes"
    '''
    if not titration:

        confirmed_s1, confirmed_s2 = None, None

        while (confirmed_s1 != 'right') or (confirmed_s2 != 'right'):
            response_s1 = subjects[0].keyboard.getKeys(clear=False)
            response_s2 = subjects[1].keyboard.getKeys(clear=False)

            if response_s1:
                for r in response_s1:
                    if confirmed_s1 != 'right':
                        confirmed_s1 = subjects[0].buttons[ r.name ]
            if response_s2:
                for r in response_s2:
                    if confirmed_s2 != 'right':
                        confirmed_s2 = subjects[1].buttons[ r.name ]
        subjects[0].keyboard.clearEvents(eventType="keyboard")
        subjects[1].keyboard.clearEvents(eventType="keyboard")

    # FOR SINGLE SUBJECT MODE (TITRATION)
    else:
        confirmed_s1 = None
        while (confirmed_s1 != 'right'):
            response_s1 = subjects.keyboard.getKeys(clear=False)
            if response_s1:
                for r in response_s1:
                    if confirmed_s1 != 'right':
                        confirmed_s1 = subjects.buttons[ r.name ]
        subjects.keyboard.clearEvents(eventType="keyboard")
