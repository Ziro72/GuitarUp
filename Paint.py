import random
from PIL import Image, ImageDraw, ImageOps
from Arrow import Arrow
from Consts import *


class Paint:
    def __init__(self, arrow_array=[], new_global_name="", width=PICTURE_WIDTH, height=PICTURE_HEIGHT):
        self.size = (width, height)
        self.global_name = new_global_name
        if not arrow_array:
            self.arrow_array = [Arrow() for i in range(MASSIVE_SIZE)]
            return
        self.arrow_array = arrow_array

    def clear_one(self, image, column_number, line_number, width=WIDTH_ARROW, height=HEIGHT_ARROW):
        pixels = image.load()
        for x in range(column_number, column_number + width):
            for y in range(line_number, line_number + height):
                pixels[x, y] = (255, 255, 255, 0)
        image.save("./src/tmp/arrows.png")

    def clear(self, images, column_number, line_number, width=WIDTH_ARROW, height=HEIGHT_ARROW):
        for image in images:
            pixels = image.load()
            for x in range(column_number, column_number + width):
                for y in range(line_number, line_number + height):
                    pixels[x, y] = (255, 255, 255, 0)
            image.save("./src/tmp/arrows.png")

    def clear_all(self, name="./src/tmp/arrows.png"):
        for i in range(len(self.arrow_array)):
            self.arrow_array[i] = Arrow()
        with Image.open(name) as image:
            self.clear_one(image, 0, (self.size[1] - HEIGHT_ARROW + 1) // 2, self.size[0])

    def draw_arrow_two(self, images, number, column_number,
                   line_number, width=WIDTH_ARROW, height=HEIGHT_ARROW):
        position = (column_number, line_number)
        size = (width, height)
        arrow = self.arrow_array[number]
        if arrow.type == 0:
            return
        c = "-" * (arrow.direction == 1)
        arrow_name = "./src/arrows/" + c + str(arrow.type) + str(arrow.color) + str(arrow.side)
        with Image.open(arrow_name + ".png") as image_arrow:
            new_image_arrow = image_arrow.resize(size, Image.Resampling.LANCZOS)
            images[0].paste(new_image_arrow, position, new_image_arrow)
        with Image.open(arrow_name + "0.png") as image_arrow:
            new_image_arrow = image_arrow.resize(size, Image.Resampling.LANCZOS)
            images[1].paste(new_image_arrow, position, new_image_arrow)


    def draw_arrow_one(self, image, number, column_number,
                   line_number, width=WIDTH_ARROW, height=HEIGHT_ARROW):
        position = (column_number, line_number)
        size = (width, height)
        arrow = self.arrow_array[number]
        if arrow.type == 0:
            return
        c = "-" * (arrow.direction == 1)
        arrow_name = "./src/arrows/" + c + str(arrow.type) + str(arrow.color) + str(arrow.side)
        with Image.open(arrow_name + ".png") as image_arrow:
            new_image_arrow = image_arrow.resize(size, Image.Resampling.LANCZOS)
            image.paste(new_image_arrow, position, new_image_arrow)

    def draw_line(self, images, size=(PICTURE_WIDTH, PICTURE_HEIGHT)):
        width, height = size
        line_number = (height - HEIGHT_ARROW + 1) // 2
        count = len(self.arrow_array)
        width_one_arrow = width // count
        for position in range(count):
            x = position * width_one_arrow
            self.draw_arrow_two(images, position, x, line_number, width_one_arrow)# Две последние можно вообще не указывать,
                                                                              # если хочется сохранить качество стрелочек

    def draw(self, name_arrow=NAME_ARROWS, name_hide_arrow=NAME_HIDE_ARROWS, new_size=(PICTURE_WIDTH, PICTURE_HEIGHT)):
        image = Image.new("RGBA", new_size, (255, 255, 255, 0))
        hide_image = Image.new("RGBA", new_size, (255, 255, 255, 0))
        self.size = new_size
        name_arrow = "./arrows/" + self.global_name + ".png"
        name_hide_arrow = "./arrows/hide_" + self.global_name + ".png"
        self.draw_line((image, hide_image), new_size)
        image.save(name_arrow)
        hide_image.save(name_hide_arrow)

    def update_storage_all(self, new_arrows, name_arrow=NAME_ARROWS,
                           name_hide_arrow=NAME_HIDE_ARROWS):
        with Image.open(name_arrow) as image, Image.open(name_hide_arrow) as hide_image:
            self.clear((image, hide_image), 0, (self.size[1] - HEIGHT_ARROW + 1) // 2,
                       self.size[0])
        self.arrow_array = new_arrows
        self.draw(name_arrow, name_hide_arrow)

    def update_storage_position(self, position, name_arrow="./src/tmp/arrows.png"):
        with Image.open(name_arrow) as image:
            width_one_arrow = self.size[0] // len(self.arrow_array)
            self.clear_one(image, position * width_one_arrow,
                       (self.size[1] - HEIGHT_ARROW + 1) // 2, width_one_arrow)
            self.draw_arrow_one(image, position, position * width_one_arrow,
                            (self.size[1] - HEIGHT_ARROW + 1) // 2, width_one_arrow)
            image.save(name_arrow)

    def get_name(self, position):
        return self.arrow_array[position].name

    def get_type(self, position):
        return self.arrow_array[position].type

    def get_color(self, position):
        return self.arrow_array[position].color

    def get_side(self, position):
        return self.arrow_array[position].side

    def get_direction(self, position):
        return self.arrow_array[position].direction

    def get_global_name(self):
        return self.global_name

    def set_global_name(self, new_global_name):
        self.global_name = new_global_name

    def set_name(self, position, new_name, name_arrow="./src/tmp/arrows.png"):
        self.arrow_array[position].name = new_name
        self.update_storage_position(position, name_arrow)

    def set_type(self, position, new_type, name_arrow="./src/tmp/arrows.png"):
        self.arrow_array[position].type = new_type
        self.update_storage_position(position, name_arrow)

    def set_color(self, position, new_color, name_arrow="./src/tmp/arrows.png"):
        self.arrow_array[position].color = new_color
        self.update_storage_position(position, name_arrow)

    def set_side(self, position, new_side, name_arrow="./src/tmp/arrows.png"):
        self.arrow_array[position].side = new_side
        self.update_storage_position(position, name_arrow)

    def set_direction(self, position, new_direction, name_arrows="./src/tmp/arrows.png"):
        self.arrow_array[position].direction = new_direction
        self.update_storage_position(position, name_arrows)
