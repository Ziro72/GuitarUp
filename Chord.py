from ChordFinger import Finger
from ChordString import String
from Paint import Paint
from ChordName import ChordName
from Consts import *

from os import path


class Chord():
    def __init__(self, name="", fret=1):
        self.name = ChordName(name)
        self.start_fret = fret
        self.barre = 0
        self.fingers = [Finger() for _ in range(5)]
        self.strings = [String() for _ in range(6)]

    def set_name(self, name):
        self.name.update(name)

    def set_start_fret(self, fret):
        self.start_fret = fret

    def set_barre(self, barre):
        self.barre = barre

    def get_finger(self, number):
        return self.fingers[number]

    def get_string(self, number):
        return self.strings[number]

    def set_finger(self, number, fret, string):
        # string


        self.fingers[number].edit(fret, string)

    def update_finger(self, index):
        string = self.fingers[index].string
        fret = self.fingers[index].fret
        if string == 0 or fret == 0:
            return
        for cur_string in range(string, string + int(index == 0) * self.barre + 1):
            if self.strings[cur_string - 1] == 'Open':
                self.strings[cur_string - 1] = 'Pinched'

    def update_string_states(self): # NEED DELETE
        self.strings = ['Open' if state == 'Pinched' else state for state in self.strings]
        for index in range(5):
            self.update_finger(index)
        self.draw_strings()

    def switch_string_state(self, number):
        self.remove_string_state(number)
        if self.strings[number] == 'MutedP':
            self.strings[number] = 'Pinched'
            return
        if self.strings[number] == 'MutedO':
            self.strings[number] = 'Open'
        else:
            self.strings[number] = 'Muted' + self.strings[number][0]
        self.draw_string_state(number)

    def remove_string_state(self, number):
        if self.strings[number] != 'Pinched':
            return
        pos = self.get_state_pos(number)
        self.cut_rectangle(pos, STATE_SIZE)

    def draw_string_state(self, number):
        if self.strings[number] == 'Pinched':
            return
        if self.strings[number][0] == "M":
            states_name = f"./src/states/{self.strings[number][:-1]}.png"
        else:
            states_name = f"./src/states/{self.strings[number]}.png"
        pos = self.get_state_pos(number)
        self.paste_member_by_dir(pos, states_name)

    ### NONOON
    def draw_strings(self):
        # self.cut_rectangle(GRID_POS, GRID_SIZE)
        for i in range(5):
            self.draw_finger(i)

    # nononon
    def draw_states(self):
        for i in range(6):
            self.remove_string_state(i)
            self.draw_string_state(i)

    def save_chord(self):
        self.name.replace('/', '-')
        new_name = self.name.name
        counter = 1
        while path.exists(f"./chords/{new_name}_{counter}.png"):
            counter += 1
        with Image.open(self.draft_dir) as image:
            image.save(f"./chords/{new_name}_{counter}.png")

    def get_finger_pos(self, number, barre=0):
        string = self.fingers[number].string - 1
        fret = self.fingers[number].fret - 1
        return GRID_XS[string + barre] - SHIFT_FINGERS, GRID_YS[fret] - SHIFT_FINGERS

    def get_state_pos(self, number):
        return GRID_XS[number] - SHIFT_STRINGS, STATUS_Y - SHIFT_STRINGS
