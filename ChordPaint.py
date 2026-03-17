from ChordFinger import Finger
from Paint import Paint
from ChordName import ChordName
from Consts import *

from os import path
from PIL import Image, ImageDraw, ImageFont


class ChordPaint(Paint):
    def __init__(self, name="", size=CHORD_IMAGE_SIZE,
                 background_dir=CHORD_BACKGROUND_DIR,
                 draft_dir=CHORD_DRAFT_DIR, fret=1):
        super().__init__(size, background_dir, draft_dir)
        self.name = ChordName(name)
        self.start_fret = fret
        self.barre = 0
        self.fingers = [Finger() for _ in range(5)]
        self.str_states = ["Open" for _ in range(6)]

        font_file = ADDITIONAL_FONT_FILE

        # size_option = int(input("""Please, choose font
        # 1 - bigger
        # 2 - smaller\n"""))
        font_size = ADDITIONAL_FONT_SIZE
        font_small_size = ADDITIONAL_FONT_SMALL_SIZE

        self.font = ImageFont.truetype(f"src/fonts/{font_file}", font_size)
        self.small_font = ImageFont.truetype(f"src/fonts/{font_file}", font_small_size)

        self.clear_default_chord()
        self.draw_states()
        self.set_start_fret(0)

    def clear_default_chord(self):
        self.clear_draft()

    def set_name(self, name):
        self.name.update(name)
        self.draw_name()

    def draw_name(self):
        self.cut_rectangle((0, 0), NAME_SIZE)
        image = Image.new("RGBA", NAME_SIZE, (0, 0, 0, 0))
        self.name.replace('-', '/')
        name_parts = self.name.array
        drawer = ImageDraw.Draw(image)
        x, y = NAME_POS
        for part in name_parts:
            font = self.small_font if part[1] else self.font
            drawer.text((x, y + 96 * int(part[1])), part[0], font=font, fill=(255, 255, 255, 255))
            x += font.getlength(part[0])
        self.paste_member((0, 0), image)

    def set_start_fret(self, fret):
        if self.start_fret == fret:
            return
        self.start_fret = fret
        self.cut_rectangle((0, 0), FRET_SIZE)
        self.paste_member_by_dir((0, 0), f"src/frets/fret{fret}.png")

    def set_barre(self, barre):
        self.barre = barre
        if barre != 0:
            self.draw_barre()
        self.draw_states()  # сомнительно

    def draw_barre(self):
        barre_name = f"src/barres/barre{self.barre}.png"
        pos = self.get_finger_pos(0, barre=self.barre)
        self.paste_member_by_dir(pos, barre_name)

    def finger(self, number):
        return self.fingers[number]

    def remove_finger(self, number, barre=0):
        self.draw_string_state(self.fingers[number].string - 1)
        if not self.fingers[number].is_pinched:
            return
        pos = self.get_finger_pos(number)
        self.cut_rectangle(pos, FINGER_SIZE)

    def set_finger(self, number, fret, string):
        self.remove_finger(number)
        self.fingers[number].edit(fret, string)
        self.remove_string_state(self.fingers[number].string)
        self.draw_finger(number)
        # no barre

    def update_finger(self, index):
        string = self.fingers[index].string
        fret = self.fingers[index].fret
        if string == 0 or fret == 0:
            return
        for cur_string in range(string, string + int(index == 0) * self.barre + 1):
            if self.str_states[cur_string - 1] == 'Open':
                self.str_states[cur_string - 1] = 'Pinched'

    def draw_finger(self, number):
        finger = self.finger(number)
        self.draw_string_state(finger.string - 1)
        if not finger.is_pinched:
            return
        if number == 0 and self.barre != 0:
            self.draw_barre()
            return
        finger_dir = f"src/fingers/finger{number + 1}.png"
        pos = self.get_finger_pos(number)
        self.paste_member_by_dir(pos, finger_dir)

    def update_string_states(self): # NEED DELETE
        self.str_states = ['Open' if state == 'Pinched' else state for state in self.str_states]
        for index in range(5):
            self.update_finger(index)
        self.draw_strings()

    def switch_string_state(self, number):
        self.remove_string_state(number)
        if self.str_states[number] == 'MutedP':
            self.str_states[number] = 'Pinched'
            return
        if self.str_states[number] == 'MutedO':
            self.str_states[number] = 'Open'
        else:
            self.str_states[number] = 'Muted' + self.str_states[number][0]
        self.draw_string_state(number)

    def remove_string_state(self, number):
        if self.str_states[number] != 'Pinched':
            return
        pos = self.get_state_pos(number)
        self.cut_rectangle(pos, STATE_SIZE)

    def draw_string_state(self, number):
        if self.str_states[number] == 'Pinched':
            return
        if self.str_states[number][0] == "M":
            states_name = f"./src/states/{self.str_states[number][:-1]}.png"
        else:
            states_name = f"./src/states/{self.str_states[number]}.png"
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
