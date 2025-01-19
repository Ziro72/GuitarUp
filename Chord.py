from Finger import Finger
from Consts import *

from os import path
from PIL import Image, ImageDraw, ImageFont


class Chord:
    def __init__(self, name="", fret=0):
        self.name = name
        self.start_fret = fret
        self.barre = 0
        self.fingers = [Finger() for _ in range(5)]
        self.str_states = ["Open" for _ in range(6)]

        self.font = ImageFont.truetype("./src/ARLRDBD.TTF", CHORD_NAME_FONT)
        self.small_font = ImageFont.truetype("./src/ARLRDBD.TTF", CHORD_NAME_SMALL_FONT)

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

    def check_key(self, name, key):
        if len(name) <= len(key) or name[:len(key)] != key:
            return 0
        res = len(key) + 1
        if len(name) > res and name[res].isdigit():
            res += 1
        return res

    def word_push(self, array, word, state):
        if word:
            array.append((word, state))
        return ''

    def refactor_name(self, name):
        array = []
        index = 0
        word = ''
        while index < len(name):
            if name[index] == '(':
                word = self.word_push(array, word, False)
                while index != len(name) and name[index - 1] != ')':
                    word += name[index]
                    index += 1
                word = self.word_push(array, word, True)
                continue
            for key in KEY_WORDS:
                word_length = self.check_key(name[index:], key)
                if word_length == 0:
                    continue
                word = self.word_push(array, word, False)
                array.append((name[index:index + word_length], True))
                index += word_length
                break
            else:
                word += name[index]
                index += 1
        self.word_push(array, word, False)
        return array

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
        image = Image.new("RGBA", NAME_SIZE, (0, 0, 0, 0))
        name_parts = self.refactor_name(self.name.replace('-', '/'))
        drawer = ImageDraw.Draw(image)
        x, y = NAME_CORDS
        for part in name_parts:
            font = self.small_font if part[1] else self.font
            drawer.text((x, y + 96 * int(part[1])), part[0], font=font, fill=(255, 255, 255, 255))
            x += font.getlength(part[0])
        chord_image.paste(image, (0, 0), image)

    def draw_chord(self):
        new_chord = Image.open(f"src/chords/chord{self.start_fret}.png")
        for i in range(5):
            self.draw_finger(new_chord, i)
        for i in range(6):
            self.draw_string(new_chord, i)

        self.draw_name(new_chord)
        new_name = self.name.replace('/', '-')
        counter = 1
        while path.exists(f"./python-server/chords/{new_name}_{counter}.png"):
            counter += 1
        new_chord.save(f"./python-server/chords/{new_name}_{counter}.png")
