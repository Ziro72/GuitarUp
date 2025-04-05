from PIL import Image, ImageDraw, ImageOps
from Consts import *
from functools import singledispatch

@singledispatch
def convert(image):
    return image.copy()

@convert.register(str)
def convert_str(name):
    with Image.open(name) as image:
        return image.copy()

def clear_image(name_image, coordinate):
    with Image.open(name_image) as image:
        image_pixels = image.load()
        for x in range(coordinate[0][0], coordinate[1][0] + 1):
            for y in range(coordinate[0][1], coordinate[1][1] + 1):
                image_pixels[x, y] = WHITE_TRANSPARENT
        image.save(name_image)

class Paint:
    def __init__(self, size, name_image,
                 name_background_image=DEFAULT_NAME_BACKGROUND_IMAGE):
        self.size = size
        self.name_background_image = name_background_image
        self.name_image = name_image

    def clear_rectangle(self, coordinate):
        clear_image(self.name_image, coordinate)

    def clear_backgrounds_position(self, coordinate,
                          name_finale_image=DEFAULT_NAME_FINALE_IMAGE):
        self.clear_rectangle(coordinate)
        clear_image(name_finale_image, coordinate)
        with (Image.open(self.name_background_image) as background_image,
              Image.open(name_finale_image) as finale_image):
            variable_part_background_image = (
                background_image.crop(coordinate))
            finale_image.paste(variable_part_background_image, coordinate)
            finale_image.save(name_finale_image)

    def clear_all(self):
        self.clear_rectangle(((0, 0),
                             (self.size[0] - 1, self.size[1] - 1)))
    def merge_backgrounds(self):
        with (Image.open(self.name_image) as image,
              Image.open(self.name_background_image) as background_image):
            finale_image = Image.new("RGBA", self.size, WHITE_TRANSPARENT)
            finale_image.paste(background_image, (0, 0),
                               background_image)
            finale_image.paste(image, (0, 0),
                               image)
            return finale_image.copy()

    def change_rectangle(self, coordinate,
                                  new_image):
        with Image.open(self.name_image) as image:
            image.paste(convert(new_image), coordinate)
            image.save(self.name_image)

    def change_position(self, coordinate, new_image,
                        name_finale_image=DEFAULT_NAME_FINALE_IMAGE):
        self.clear_backgrounds_position(coordinate, name_finale_image)
        self.change_rectangle(coordinate, new_image)
        with (Image.open(self.name_image) as image,
              Image.open(name_finale_image) as finale_image):
            variable_part_background_image = image.crop(coordinate)
            finale_image.paste(variable_part_background_image,
                               coordinate)
            finale_image.save(name_finale_image)