from Finger import Finger
from ChordName import ChordName
from Consts import *

from os import path
from PIL import Image, ImageDraw, ImageFont


class Chord:
    def __init__(self, name="", fret=0):
        self.name = ChordName(name)
        self.start_fret = fret
        self.barre = 0
        self.fingers = [Finger() for _ in range(5)]
        self.str_states = ["Open" for _ in range(6)]

        self.font = ImageFont.truetype(f"./src/{FONT_FILE}", FONT_SIZE)
        self.small_font = ImageFont.truetype(f"./src/{FONT_FILE}", FONT_SMALL_SIZE)

        self.clear_default_chord()

    def clear_default_chord(self):
        new_chord = Image.open(f"src/chords/chord0.png")
        new_chord.save(f"./src/tmp/chord.png")

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

    def draw_string(self, chord_image, number):
        if self.str_states[number] == 'Pinched':
            return
        state_image = Image.open(f"./src/states/{self.str_states[number]}.png")
        position = (GRID_XS[number] - SHIFT_STRINGS, STATUS_Y - SHIFT_STRINGS)
        chord_image.paste(state_image, position, state_image)

    def draw_barre(self, chord_image):
    if self.barre > 0:
        # Проверка, что barre находится в допустимом диапазоне
        if self.barre - 1 >= len(FRET_XS):
            app.logger.error(f"Barre fret {self.barre} exceeds FRET_XS length {len(FRET_XS)}")
            return  # Пропускаем отрисовку барре
        
        fret_x = FRET_XS[self.barre - 1]

        for finger in self.fingers:
            if finger.is_barre:
                # Проверка, что string находится в допустимом диапазоне
                if finger.string - 1 >= len(STRING_YS):
                    app.logger.error(f"String {finger.string} exceeds STRING_YS length {len(STRING_YS)}")
                    continue  # Пропускаем этот палец

                string_y = STRING_YS[finger.string - 1]

                position = (
                    fret_x - SHIFT_FINGERS,
                    string_y - SHIFT_FINGERS,
                    fret_x + SHIFT_FINGERS,
                    string_y + SHIFT_FINGERS
                )

                app.logger.info(f"Drawing barre at position: {position}")

                # Отрисовка барре (например, прямоугольника)
                chord_image.rectangle(position, fill="black")


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
        self.name.replace('-', '/')
        name_parts = self.name.array
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
        new_chord.save(f"./src/tmp/chord.png")

    def save_chord(self):
        new_chord = Image.open(f"./src/tmp/chord.png")
        self.name.replace('/', '-')
        new_name = self.name.name
        counter = 1
        while path.exists(f"./chords/{new_name}_{counter}.png"):
            counter += 1
        new_chord.save(f"./chords/{new_name}_{counter}.png")
