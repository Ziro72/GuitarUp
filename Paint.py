from PIL import Image, ImageDraw, ImageOps
from Consts import *
class Paint:
    def __init__(self, size, name_image,
                 name_background_image=DEFAULT_NAME_BACKGROUND_IMAGE):
        self.size = size
        self.name_background_image = name_background_image
        self.name_image = name_image
    def clear_rectangle(self, coordinate=((0, 0), (0, 0))):
        with Image.open(self.name_image) as image:
            image_pixels = image.load()
            for x in range(coordinate[0][0], coordinate[1][0] + 1):
                for y in range(coordinate[0][1], coordinate[1][1] + 1):
                    image_pixels[x, y] = WHITE_TRANSPARENT
            image.save(self.name_image)
    def clear_backgrounds_position(self, coordinate=((0, 0), (0, 0)),
                          name_image=DEFAULT_NAME_FINALE_IMAGE):
        self.clear_rectangle(coordinate)
    def clear_all(self):
        self.clear_rectangle((0, 0),
                             (self.size[0] - 1, self.size[1] - 1))
    def merge_backgrounds(self):
        with (Image.open(self.name_image) as image,
              Image.open(self.name_background_image) as background_image):
            finale_image = Image.new("RGBA", self.size, WHITE_TRANSPARENT)
            finale_image.paste(background_image, (0, 0),
                               background_image)
            finale_image.paste(image, (0, 0),
                               image)
            return finale_image