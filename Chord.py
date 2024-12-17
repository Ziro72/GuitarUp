from Finger import Finger
from Consts import *

from PIL import Image


class Chord:
    def __init__(self, name="", fret=""):
        self.name = name
        self.start_fret = fret
        self.fingers = [Finger() for i in range(5)]
        self.str_states = ["OPEN" for i in range(6)]

    def change_name(self, name):
        self.name = name

    def change_start_fret(self, fret):
        self.start_fret = fret

    def assign_finger(self, number, fret, string, barre_length=0):
        self.fingers[number].edit(fret, string, barre_length)

    def finger(self, number):
        return self.fingers[number]

    def assign_string(self, number, statement='OPEN'):
        self.str_states[number] = statement

    def draw_string(self, chord_image, number):
        if self.str_states[number] == 'PINCHED':
            return
        status_image = Image.open(f"src/{self.str_states[number]}.png")
        position = (GRID_XS[number] - SHIFT_STRINGS, STATUS_Y - SHIFT_STRINGS)
        chord_image.paste(status_image, position, status_image)

    def draw_chord(self):
        new_chord = Image.open("../PycharmProjects/GuitarUp/src/chord.png")
        for i in range(5):
            self.fingers[i].draw_finger(new_chord, i + 1)
        for i in range(6):
            self.draw_string(new_chord, i)
        new_chord.save(f"chords/{self.name}.png")
