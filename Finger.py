from Consts import *

from PIL import Image


class Finger:
    def __init__(self, fret=0, string=0, barre_length=0):
        self.is_pinch = bool(fret)
        self.barre = bool(barre_length)
        self.fret = fret
        self.string = string
        self.barre_length = barre_length

    def edit(self, fret=0, string=0, barre_length=0):
        self.is_pinch = bool(fret)
        self.barre = bool(barre_length)
        self.fret = fret
        self.string = string
        self.barre_length = barre_length

    def edit_fret(self, fret):
        self.fret = fret

    def edit_string(self, string):
        self.string = string

    def edit_barre_length(self, barre_length):
        self.barre_length = barre_length

    def draw_finger(self, chord_image, finger_number):
        if self.string == 0 or self.fret == 0:
            return
        finger_image = Image.open(f"src/finger{finger_number}.png")
        for i in range(self.barre_length + 1):
            position = (GRID_XS[self.string - 1 + i] - SHIFT_FINGERS,
                        GRID_YS[self.fret - 1] - SHIFT_FINGERS)
            chord_image.paste(finger_image, position, finger_image)
