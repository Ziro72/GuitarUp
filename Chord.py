from Finger import Finger
from Consts import *

from PIL import Image, ImageDraw, ImageFont


class Chord:
    def __init__(self, name="", fret=""):
        self.name = name
        self.start_fret = fret
        self.fingers = [Finger() for i in range(5)]
        self.str_states = ["Open" for i in range(6)]

        self.font = ImageFont.truetype("./src/ARLRDBD.TTF", 224)

    def change_name(self, name):
        self.name = name

    def change_start_fret(self, fret):
        self.start_fret = fret

    def assign_finger(self, number, fret, string, barre_length=0):
        self.fingers[number].edit(fret, string, barre_length)

    def finger(self, number):
        return self.fingers[number]

    def change_string_state(self, number):
        if self.str_states[number] == 'Muted':
            self.str_states[number] = 'Open'
            self.update_strings()
        else:
            self.str_states[number] = 'Muted'

    def update_finger(self, finger, states):
        string = finger.string
        if string == 0 or finger.fret == 0:
            return
        for cur_string in range(string, string + finger.barre_length + 1):
            if states[cur_string - 1] == 'Open':
                states[cur_string - 1] = 'Pinched'

    def update_strings(self):
        new_states = ['Open' if state == 'Pinched' else state for state in self.str_states]
        for i in range(5):
            self.update_finger(self.fingers[i], new_states)
        self.str_states = new_states

    def draw_string(self, chord_image, number):
        if self.str_states[number] == 'Pinched':
            return
        status_image = Image.open(f"./src/{self.str_states[number]}.png")
        position = (GRID_XS[number] - SHIFT_STRINGS, STATUS_Y - SHIFT_STRINGS)
        chord_image.paste(status_image, position, status_image)

    def draw_name(self, chord_image):
        width, height = 900, 300
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        drawer = ImageDraw.Draw(image)
        drawer.text((140, 10), self.name, font=self.font, fill=(255, 255, 255, 255))
        chord_image.paste(image, (0, 0), image)

    def draw_chord(self):
        new_chord = Image.open("./src/chord.png")
        for i in range(5):
            self.fingers[i].draw_finger(new_chord, i + 1)
        for i in range(6):
            self.draw_string(new_chord, i)

        self.draw_name(new_chord)
        new_chord.save(f"./chords/{self.name}.png")
