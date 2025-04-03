import random
from PIL import Image, ImageDraw, ImageOps
from Arrow import Arrow
from Consts import *


class Paint:
    def __init__(self, arrow_array=[], new_global_name="arrow",
                 compression=COMPRESSION_RATIO, size=PICTURE_SIZE):
        self.size = size
        self.global_name = new_global_name
        self.compression = compression
        if not arrow_array:
            self.arrow_array = [Arrow() for i in range(MASSIVE_SIZE)]
            return
        self.arrow_array = arrow_array

    def clear_one(self, image, position, name=NAME_ARROW_WIDGET):
        pixels = image.load()
        arrow_size = (int(ARROW_SIZE[0] * self.compression[0]),
                      int(ARROW_SIZE[1] * self.compression[1]))
        image_position = (int((DISTANCE_BETWEEN_ARROWS + position * (ARROW_SIZE[0] + DISTANCE_BETWEEN_ARROWS)) * self.compression[0]),
                          (image.size[1] - int(self.compression[1] * ARROW_SIZE[1]) + 1) // 2 +
                          int(self.compression[1] * ARROW_SIZE[1]) - int(self.compression[1] * arrow_size[1]))
        for x in range(image_position[0], image_position[0] + arrow_size[0]):
            for y in range(image_position[1], image_position[1] + arrow_size[1]):
                pixels[x, y] = (255, 255, 255, 0)
        image.save(name)

    def clear_all_arrows(self, name=NAME_ARROW_WIDGET):
        with Image.open(name) as image:
            for position in range(len(self.arrow_array)):
                if self.arrow_array[position].type != 0:
                    self.clear_one(image, position, name)
                self.arrow_array[position] = Arrow()

    def clear_all_image(self, name=NAME_COPY_ARROW_WIDGET):
        with Image.open(name) as image:
            pixels = image.load()
            for i in range(image.size[0]):
                for j in range(image.size[1]):
                    pixels[i, j] = (255, 255, 255, 0)
            image.save(name)

    def clear_all_arrows_copy(self, name=NAME_COPY_ARROW_WIDGET,
                              name_arrow=NAME_ARROW_WIDGET):
        self.clear_all_arrows(name)
        with Image.open(name) as image:
            (image.resize(self.size, Image.Resampling.LANCZOS)).save(name_arrow)


    def clear_copy(self, name_copy=NAME_COPY_ARROW_WIDGET,
                   name_arrow=NAME_ARROW_WIDGET):
        self.clear_all_image(name_copy)
        with Image.open(name_copy) as image:
            (image.resize(self.size, Image.Resampling.LANCZOS)).save(name_arrow)

    def draw_arrow_two(self, images, number, position, arrow_size=ARROW_SIZE):
        arrow = self.arrow_array[number]
        if arrow.type == 0:
            return
        arrow_name = (PATH_ARROWS_WIDGET + str(arrow.type) + str(arrow.status) +
                      str(arrow.direction) + str(arrow.accent))
        with Image.open(arrow_name + "0.png") as image_arrow:
            images[0].paste(image_arrow, (position[0],
                                          position[1] + arrow_size[1] - image_arrow.size[1]),
                            image_arrow)
        with Image.open(arrow_name + "1.png") as image_arrow:
            images[1].paste(image_arrow, (position[0],
                                          position[1] + arrow_size[1] - image_arrow.size[1]),
                            image_arrow)


    def draw_arrow_one(self, image, number, position, arrow_size=ARROW_SIZE,
                       compression_ratio=COMPRESSION_RATIO):
        arrow = self.arrow_array[number]
        if arrow.type == 0:
            return
        arrow_name = (PATH_ARROWS_WIDGET + str(arrow.type) + str(arrow.status) +
                      str(arrow.direction) + str(arrow.accent))
        with Image.open(arrow_name + "1.png") as image_arrow:

            new_image_arrow = image_arrow.resize((int(image_arrow.size[0] * compression_ratio[0]),
                                                 int(image_arrow.size[1] * compression_ratio[1])),
                                                 Image.Resampling.LANCZOS)
            image.paste(new_image_arrow, (position[0], position[1] +
                                          int(arrow_size[1] * compression_ratio[1]) -
                                          new_image_arrow.size[1]),
                        new_image_arrow)

    def draw_line(self, images, size=(PICTURE_WIDTH, PICTURE_HEIGHT),
                  arrow_size=ARROW_SIZE, distance_one_arrow = DISTANCE_BETWEEN_ARROWS):
        width, height = size
        line_number = (height - ARROW_HEIGHT + 1) // 2
        count = len(self.arrow_array)
        for position in range(count):
            width_projection = distance_one_arrow + position * (arrow_size[0] + distance_one_arrow)
            image_position = (width_projection, line_number)
            self.draw_arrow_two(images, position, image_position, arrow_size)

    def draw(self, original_size=ORIGINAL_SIZE):
        image = Image.new("RGBA", original_size, (255, 255, 255, 0))
        hide_image = Image.new("RGBA", original_size, (255, 255, 255, 0))
        name_arrow = PATH_ARROWS + self.global_name + ".png"
        name_hide_arrow = PATH_HIDE_ARROWS + self.global_name + ".png"
        self.draw_line((hide_image, image), original_size)
        image.save(name_arrow)
        hide_image.save(name_hide_arrow)

    def update_storage_all(self, new_arrows, copy_name_arrow=NAME_COPY_ARROW_WIDGET,
                           name_arrow=NAME_ARROW_WIDGET, compression_ratio=COMPRESSION_RATIO):
        self.clear_all_arrows(copy_name_arrow)
        self.arrow_array = new_arrows
        for i in range(len(new_arrows)):
            self.update_storage_position(i, copy_name_arrow, name_arrow, compression_ratio)

    def quick_change_size(self, copy_arrow=NAME_COPY_ARROW_WIDGET,
                          new_size=ORIGINAL_SIZE):
        with Image.open(copy_arrow) as image:
            (image.resize(new_size, Image.Resampling.LANCZOS)).save(copy_arrow)

    def new_compression(self, copy_name=NAME_COPY_ARROW_WIDGET, compression_ratio=COMPRESSION_RATIO):
        self.compression = compression_ratio
        with Image.open(copy_name) as image:
            image = image.resize((int(image.size[0] * compression_ratio[0]),
                                  int(image.size[1] * compression_ratio[1])),
                                 Image.Resampling.LANCZOS)
            image.save(copy_name)

    def update_storage_position(self, position, copy_name_arrow=NAME_COPY_ARROW_WIDGET,
                                name_arrow=NAME_ARROW_WIDGET, new_size=PICTURE_SIZE):
        with (Image.open(copy_name_arrow) as image):
            coordinate = (int((DISTANCE_BETWEEN_ARROWS + position * (ARROW_SIZE[0] + DISTANCE_BETWEEN_ARROWS)) * self.compression[0]),
                        (image.size[1] - int(self.compression[1] * ARROW_HEIGHT) + 1) // 2)
            self.clear_one(image, position, copy_name_arrow)
            self.draw_arrow_one(image, position, coordinate)
            image.save(copy_name_arrow)
            (image.resize(new_size, Image.Resampling.LANCZOS)).save(name_arrow)

    def get_name(self, position):
        return self.arrow_array[position].name

    def get_type(self, position):
        return self.arrow_array[position].type

    def get_accent(self, position):
        return self.arrow_array[position].accent

    def get_status(self, position):
        return self.arrow_array[position].status

    def get_direction(self, position):
        return self.arrow_array[position].direction

    def get_global_name(self):
        return self.global_name

    def set_global_name(self, new_global_name="arrow"):
        self.global_name = new_global_name

    def set_name(self, position, new_name,
                 name_arrow=NAME_COPY_ARROW_WIDGET):
        self.arrow_array[position].name = new_name
        self.update_storage_position(position, name_arrow)

    def set_type(self, position, new_type,
                 name_arrow=NAME_COPY_ARROW_WIDGET):
        self.arrow_array[position].type = new_type
        self.update_storage_position(position, name_arrow)

    def set_accent(self, position, new_accent,
                   name_arrow=NAME_COPY_ARROW_WIDGET):
        self.arrow_array[position].accent = new_accent
        self.update_storage_position(position, name_arrow)

    def set_status(self, position, new_status,
                   name_arrow=NAME_COPY_ARROW_WIDGET):
        self.arrow_array[position].status = new_status
        self.update_storage_position(position, name_arrow)

    def set_direction(self, position, new_direction,
                      name_arrows=NAME_COPY_ARROW_WIDGET):
        self.arrow_array[position].direction = new_direction
        self.update_storage_position(position, name_arrows)