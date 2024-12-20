from Finger import Finger
from Consts import *

from PIL import Image, ImageDraw, ImageFont


class Chord:
    def __init__(self, name="", fret=0):
        self.name = name
        self.start_fret = fret
        self.barre = 0
        self.fingers = [Finger() for _ in range(5)]
        self.str_states = ["Open" for _ in range(6)]

        self.font = ImageFont.truetype("./src/ARLRDBD.TTF", 224)

    def change_name(self, name):
        self.name = name

    def change_start_fret(self, fret):
        self.start_fret = fret

    def edit_barre(self, barre):
        self.barre = barre

    def assign_finger(self, number, fret, string):
        self.fingers[number].edit(fret, string)

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
        for cur_string in range(string, string + (1 if finger != self.finger(0) else self.barre + 1)):
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
        state_image = Image.open(f"./src/states/{self.str_states[number]}.png")
        position = (GRID_XS[number] - SHIFT_STRINGS, STATUS_Y - SHIFT_STRINGS)
        chord_image.paste(state_image, position, state_image)

    def draw_barre(self, chord_image):
        finger = self.finger(0)
        finger_image = Image.open(f"src/barres/barre{self.barre}.png")
        position = (GRID_XS[finger.string - 1 + self.barre] - SHIFT_FINGERS,
                    GRID_YS[finger.fret - 1] - SHIFT_FINGERS)
        chord_image.paste(finger_image, position, finger_image)

    def draw_finger(self, chord_image, number):
        finger = self.finger(number)
        if finger.string == 0 or finger.fret == 0:
            return
        if number == 0 and self.barre != 0:
            self.draw_barre(chord_image)
            return

        finger_image = Image.open(f"src/fingers/finger{number + 1}.png")
        position = (GRID_XS[finger.string - 1] - SHIFT_FINGERS,
                    GRID_YS[finger.fret - 1] - SHIFT_FINGERS)
        chord_image.paste(finger_image, position, finger_image)

    def draw_name(self, chord_image):
        width, height = 900, 300
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        drawer = ImageDraw.Draw(image)
        drawer.text(NAME_CORDS, self.name, font=self.font, fill=(255, 255, 255, 255))
        chord_image.paste(image, (0, 0), image)

    def draw_chord(self):
        new_chord = Image.open(f"src/chords/chord{self.start_fret}.png")
        for i in range(5):
            self.draw_finger(new_chord, i)
        for i in range(6):
            self.draw_string(new_chord, i)

        self.draw_name(new_chord)
        new_chord.save(f"./chords/{self.name}.png")
