from PIL import Image
from Consts import *
from functools import singledispatch

@singledispatch
def convert(image):
    return image.copy()

@convert.register(str)
def convert_str(name):
    with Image.open(name) as image:
        return image.copy()

def clear_image(name_image, coordinate, size_part):
    paste_image = Image.new("RGBA", size_part, WHITE_TRANSPARENT)
    with Image.open(name_image) as image:
        image.paste(paste_image, coordinate)
        image.save(name_image)
    paste_image.close()
    del paste_image

class Paint:
    def __init__(self, size, name_background_image,
                 name_image=DEFAULT_NAME_IMAGE):
        self.size = size
        self.name_background_image = name_background_image
        self.name_image = name_image

    def clear_rectangle(self, coordinate, paste_size):
        clear_image(self.name_image, coordinate, paste_size)

    def clear_backgrounds_position(self, coordinate, paste_size,
                          name_finale_image=DEFAULT_NAME_FINALE_IMAGE):
        self.clear_rectangle(coordinate, paste_size)
        clear_image(name_finale_image, coordinate, paste_size)
        with (Image.open(self.name_background_image) as background_image,
              Image.open(name_finale_image) as finale_image):
            variable_part_background_image = (
                background_image.crop((coordinate[0],
                                       coordinate[1],
                                       coordinate[0] + paste_size[0],
                                       coordinate[1] + paste_size[1])))
            finale_image.paste(variable_part_background_image, coordinate)
            finale_image.save(name_finale_image)

    def clear_all_backgrounds(self, name_finale_image=DEFAULT_NAME_FINALE_IMAGE):
        self.clear_backgrounds_position((0, 0), self.size,
                                        name_finale_image)

    def clear_all(self):
        self.clear_rectangle((0, 0), self.size)

    def update_backgrounds(self,
                           name_finale_image=DEFAULT_NAME_FINALE_IMAGE):
        clear_image(name_finale_image, (0, 0), self.size)
        with (Image.open(self.name_image) as image,
              Image.open(self.name_background_image) as background_image,
              Image.open(name_finale_image) as finale_image):
            finale_image.paste(background_image, (0, 0))
            finale_image.paste(image, (0, 0))
            finale_image.save(name_finale_image)

    def merge_backgrounds(self):
        with (Image.open(self.name_image) as image,
              Image.open(self.name_background_image) as background_image):
            finale_image = Image.new("RGBA", self.size, WHITE_TRANSPARENT)
            finale_image.paste(background_image, (0, 0))
            finale_image.paste(image, (0, 0))
            return finale_image

    def change_rectangle(self, coordinate_left_up, coordinate_right_down, new_image):
        paste_image = convert(new_image)
        clear_image(self.name_image, coordinate_left_up,
                    (coordinate_right_down[0] - coordinate_left_up[0],
                     coordinate_right_down[1] - coordinate_left_up[1]))
        with Image.open(self.name_image) as image:
            image.paste(paste_image, coordinate_left_up)
            image.save(self.name_image)
        paste_image.close()
        del paste_image

    def change_position(self, coordinate_left_up, coordinate_right_down, new_image,
                        name_finale_image=DEFAULT_NAME_FINALE_IMAGE):
        paste_image = convert(new_image)
        clear_image(name_finale_image, coordinate_left_up,
                    (coordinate_right_down[0] - coordinate_left_up[0],
                     coordinate_right_down[1] - coordinate_left_up[1]))
        self.change_rectangle(coordinate_left_up, coordinate_right_down, paste_image)
        with (Image.open(self.name_image) as image,
              Image.open(name_finale_image) as finale_image):
            variable_part_background_image = image.crop((
                    coordinate_left_up[0], coordinate_left_up[1],
                    coordinate_left_up[0] + paste_image.size[0],
                    coordinate_left_up[1] + paste_image.size[1]))
            finale_image.paste(variable_part_background_image,
                               coordinate_left_up)
            finale_image.save(name_finale_image)
        paste_image.close()
        del paste_image

    def quick_change_size(self, new_size):
        self.size = new_size
        with (Image.open(self.name_image) as image,
              Image.open(self.name_background_image) as background_image):
            (image.resize(new_size, Image.Resampling.LANCZOS)).save(self.name_image)
            (background_image.resize(new_size, Image.Resampling.LANCZOS)).save(self.name_background_image)

    def get_name_image(self):
        return self.name_image

    def get_name_background_image(self):
        return self.name_background_image

    def get_size(self):
        return self.size

    def change_name_image(self, new_name_image):
        self.name_image = new_name_image

    def change_name_image_global(self, new_name_image,
                                 name_finale_image=DEFAULT_NAME_FINALE_IMAGE):
        self.name_image = new_name_image
        self.update_backgrounds(name_finale_image)

    def change_name_background_image(self,
                                     new_name_background_image):
        self.name_background_image = new_name_background_image

    def change_name_background_image_global(self,
            new_name_background_image,
            name_finale_image=DEFAULT_NAME_FINALE_IMAGE):
        self.name_background_image = new_name_background_image
        self.update_backgrounds(name_finale_image)