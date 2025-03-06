import random
from PIL import Image, ImageDraw, ImageOps
from Arrow import Arrow
from Consts import *


class Paint:
    def __init__(self, arrow_array=[], new_global_name="arrow", width=PICTURE_WIDTH, height=PICTURE_HEIGHT):
        self.size = (width, height)
        self.global_name = new_global_name
        if not arrow_array:
            self.arrow_array = [Arrow() for i in range(MASSIVE_SIZE)]
            return
        self.arrow_array = arrow_array

    def clear_one(self, image, column_number, line_number, name="./src/tmp/arrows.png", width=WIDTH_ARROW, height=HEIGHT_ARROW):
        pixels = image.load()
        for x in range(column_number, column_number + width):
            for y in range(line_number, line_number + height):
                pixels[x, y] = (255, 255, 255, 0)
        image.save(name)

    def clear_all(self, name="./src/tmp/arrows.png"):
        for i in range(len(self.arrow_array)):
            self.arrow_array[i] = Arrow()
        with Image.open(name) as image:
            self.clear_one(image, 0, 0, name, image.size[0], image.size[1])

    def draw_arrow_two(self, images, number, column_number,
                       line_number, width=WIDTH_ARROW,
                       distance=DISTANCE_BETWEEN_ARROWS,
                       height=HEIGHT_ARROW):
        position = (column_number, line_number)
        size = (width, height)
        arrow = self.arrow_array[number]
        if arrow.type == 0:
            return
        arrow_name = "./src/arrows/" + str(arrow.type) + str(arrow.status) + str(arrow.direction) + str(arrow.accent)
        with Image.open(arrow_name + "0.png") as image_arrow:
            images[0].paste(image_arrow, (position[0],
                                          position[1] + height - image_arrow.size[1]),
                            image_arrow)
        with Image.open(arrow_name + "1.png") as image_arrow:
            images[1].paste(image_arrow, (position[0],
                                          position[1] + height - image_arrow.size[1]), image_arrow)


    def draw_arrow_one(self, image, number, column_number,
                       line_number, width=WIDTH_ARROW, height=HEIGHT_ARROW,
                       compression_width=COMPRESSION_RATIO_BY_WIDTH,
                       compression_height=COMPRESSION_RATIO_BY_HEIGHT):
        position = (column_number, line_number)
        arrow = self.arrow_array[number]
        if arrow.type == 0:
            return
        arrow_name = "./src/arrows/" + str(arrow.type) + str(arrow.status) + str(arrow.direction) + str(arrow.accent)
        with Image.open(arrow_name + "1.png") as image_arrow:
            new_image_arrow = image_arrow.resize((int(image_arrow.size[0] * compression_width),
                                                 int(image_arrow.size[1] * compression_height)), Image.Resampling.LANCZOS)
            image.paste(new_image_arrow, (position[0], position[1] + int(height * compression_height) - new_image_arrow.size[1]),
                        new_image_arrow)

    def draw_line(self, images, size=(PICTURE_WIDTH, PICTURE_HEIGHT),
                  width_one_arrow = WIDTH_ARROW, distance_one_arrow = DISTANCE_BETWEEN_ARROWS):
        width, height = size
        line_number = (height - HEIGHT_ARROW + 1) // 2
        count = len(self.arrow_array)
        for position in range(count):
            x = distance_one_arrow + position * (width_one_arrow + distance_one_arrow)
            self.draw_arrow_two(images, position, x, line_number,
                                width_one_arrow,
                                distance_one_arrow)# Две последние можно вообще не указывать,
                                                                              # если хочется сохранить качество стрелочек

    def draw(self, original_size=(DISTANCE_BETWEEN_ARROWS +
                                  MASSIVE_SIZE * (WIDTH_ARROW + DISTANCE_BETWEEN_ARROWS), 3 * HEIGHT_ARROW)):
        image = Image.new("RGBA", original_size, (255, 255, 255, 0))
        hide_image = Image.new("RGBA", original_size, (255, 255, 255, 0))
        self.size = original_size
        name_arrow = "./arrows/" + self.global_name + ".png"
        name_hide_arrow = "./arrows/hide_" + self.global_name + ".png"
        self.draw_line((hide_image, image), original_size)
        image.save(name_arrow)
        hide_image.save(name_hide_arrow)

    def update_storage_all(self, new_arrows, name_arrow=NAME_ARROWS,
                           name_hide_arrow=NAME_HIDE_ARROWS):
        with Image.open(name_arrow) as image:
            self.clear_one(image, 0, (self.size[1] - HEIGHT_ARROW + 1) // 2, name_arrow,
                       self.size[0])
        with Image.open(name_hide_arrow) as hide_image:
            self.clear_one(image, 0, (self.size[1] - HEIGHT_ARROW + 1) // 2, name_hide_arrow,
                           self.size[0])
        self.arrow_array = new_arrows
        self.draw(name_arrow, name_hide_arrow)

    def update_storage_position(self, position, copy_name_arrow="./src/tmp/copy_arrows.png",
                                name_arrow="./src/tmp/arrows.png",
                                width_one_arrow=WIDTH_ARROW,
                                height_one_arrow=HEIGHT_ARROW,
                                new_size=(PICTURE_WIDTH, PICTURE_HEIGHT),
                                distance=DISTANCE_BETWEEN_ARROWS,
                                original_size=(DISTANCE_BETWEEN_ARROWS + MASSIVE_SIZE
                                               * (WIDTH_ARROW + DISTANCE_BETWEEN_ARROWS), 3 * HEIGHT_ARROW),
                                compression_width=COMPRESSION_RATIO_BY_WIDTH,
                                compression_height=COMPRESSION_RATIO_BY_HEIGHT):
        with Image.open(copy_name_arrow) as image:
            if int(original_size[0] * compression_width) != image.size[0] or int(original_size[1] * compression_height) != image.size[1]:
                image = image.resize((int(original_size[0] * compression_width), int(original_size[1] * compression_height)), Image.Resampling.LANCZOS)
            self.size = image.size
            self.clear_one(image, int((distance + position * (width_one_arrow + distance)) * compression_width),
                           (self.size[1] - int(compression_height * HEIGHT_ARROW) + 1) // 2, copy_name_arrow, int(width_one_arrow * compression_width),
                           int(height_one_arrow * compression_height))
            self.draw_arrow_one(image, position, int((distance + position * (width_one_arrow + distance)) * compression_width),
                                (self.size[1] - int(compression_height * HEIGHT_ARROW) + 1) // 2)
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

    def set_name(self, position, new_name, name_arrow="./src/tmp/copy_arrows.png"):
        self.arrow_array[position].name = new_name
        self.update_storage_position(position, name_arrow)

    def set_type(self, position, new_type, name_arrow="./src/tmp/copy_arrows.png"):
        self.arrow_array[position].type = new_type
        self.update_storage_position(position, name_arrow)

    def set_accent(self, position, new_accent, name_arrow="./src/tmp/copy_arrows.png"):
        self.arrow_array[position].accent = new_accent
        self.update_storage_position(position, name_arrow)

    def set_status(self, position, new_status, name_arrow="./src/tmp/copy_arrows.png"):
        self.arrow_array[position].status = new_status
        self.update_storage_position(position, name_arrow)

    def set_direction(self, position, new_direction, name_arrows="./src/tmp/copy_arrows.png"):
        self.arrow_array[position].direction = new_direction
        self.update_storage_position(position, name_arrows)
