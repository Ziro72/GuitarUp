from Finger import Finger
from Paint import Paint
from ChordName import ChordName
from Consts import *

from os import path
from PIL import Image, ImageDraw, ImageFont

class ChordPaint(Paint):
    def __init__(self, name="", size=CHORD_IMAGE_SIZE,
                 name_background_image=DEFAULT_NAME_CHORD_BACKGROUND_IMAGE,
                 name_image=DEFAULT_NAME_CHORD_IMAGE, fret=0):
        super().__init__(size, name_background_image, name_image)
        self.name = ChordName(name)
        self.start_fret = fret
        self.barre = 0
        self.fingers = [Finger() for _ in range(5)]
        self.str_states = ["Open" for _ in range(6)]

        self.font = ImageFont.truetype(f"./src/{FONT_FILE}", FONT_SIZE)
        self.small_font = ImageFont.truetype(f"./src/{FONT_FILE}", FONT_SMALL_SIZE)

        self.clear_default_chord()

    def clear_default_chord(self):
        self.clear_all_finale_image(self.name_image)

    def change_name(self, name):
        self.name.update(name)
        self.draw_chord()

    def change_start_fret(self, fret):
        self.start_fret = fret
        self.draw_chord()

    def edit_barre(self, barre):
        self.barre = barre
        self.draw_chord()

    def assign_finger(self, number, fret, string):
        self.fingers[number].edit(fret, string)
        self.draw_chord()

    def finger(self, number):
        return self.fingers[number]

    def change_string_state(self, number):
        if self.str_states[number] == 'Muted':
            self.str_states[number] = 'Open'
            self.update_strings()
        else:
            self.str_states[number] = 'Muted'
        self.draw_chord()

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
        self.draw_chord()

    def draw_string(self, number):
        if self.str_states[number] == 'Pinched':
            return
        states_name = f"./src/states/{self.str_states[number]}.png"
        coordinate = (GRID_XS[number] - SHIFT_STRINGS, STATUS_Y - SHIFT_STRINGS)
        self.change_rectangle_finale_image_default_paste_size(coordinate, states_name, self.name_image, False)

    def draw_barre(self):
        finger = self.finger(0)
        finger_name = f"src/barres/barre{self.barre}.png"
        coordinate = (GRID_XS[finger.string - 1 + self.barre] - SHIFT_FINGERS,
                    GRID_YS[finger.fret - 1] - SHIFT_FINGERS)
        self.change_rectangle_finale_image_default_paste_size(coordinate, finger_name, self.name_image, False)

    def draw_finger(self, number):
        finger = self.finger(number)
        if finger.string == 0 or finger.fret == 0:
            return
        if number == 0 and self.barre != 0:
            self.draw_barre()
            return
        finger_name = f"src/fingers/finger{number + 1}.png"
        coordinate = (GRID_XS[finger.string - 1] - SHIFT_FINGERS,
                    GRID_YS[finger.fret - 1] - SHIFT_FINGERS)
        self.change_rectangle_finale_image_default_paste_size(coordinate, finger_name, self.name_image, False)

    def draw_name(self):
        image = Image.new("RGBA", NAME_SIZE, (0, 0, 0, 0))
        self.name.replace('-', '/')
        name_parts = self.name.array
        drawer = ImageDraw.Draw(image)
        x, y = NAME_CORDS
        for part in name_parts:
            font = self.small_font if part[1] else self.font
            drawer.text((x, y + 96 * int(part[1])), part[0], font=font, fill=(255, 255, 255, 255))
            x += font.getlength(part[0])
        self.change_rectangle_finale_image_paste_image((0, 0), image, self.name_image)

    def draw_chord(self):
        self.change_name_background_image_global(f"src/chords/chord{self.start_fret}.png", self.name_image)
        for i in range(5):
            self.draw_finger(i)
        for i in range(6):
            self.draw_string(i)
        self.draw_name()

    def save_chord(self):
        self.name.replace('/', '-')
        new_name = self.name.name
        counter = 1
        while path.exists(f"./chords/{new_name}_{counter}.png"):
            counter += 1
        with Image.open(self.name_image) as image:
            image.save(f"./chords/{new_name}_{counter}.png")
