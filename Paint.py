from PIL import Image, ImageDraw, ImageFont
from Consts import *

resampling = [Image.Resampling.NEAREST, Image.Resampling.BOX,
              Image.Resampling.BILINEAR, Image.Resampling.HAMMING,
              Image.Resampling.BICUBIC, Image.Resampling.LANCZOS]
resampling_index = 5

def clear_image(name_image, coordinate, size_part):
    if size_part == 0:
        return
    with Image.open(name_image) as image:
        draw = ImageDraw.Draw(image)
        draw.rectangle([coordinate[0], coordinate[1],
                        coordinate[0] + size_part[0],
                        coordinate[1] + size_part[1]],
                       fill=WHITE_TRANSPARENT)
        image.save(name_image)

class Paint:
    def __init__(self, size, name_background_image,
                 name_image=DEFAULT_NAME_IMAGE, font=BASE_FONT, font_size=TABLATURES_FONT_SIZE):
        self.size = size
        self.name_background_image = name_background_image
        self.name_image = name_image
        self.font_small = ImageFont.truetype(font, font_size)
        print(self.font_small)
        self.quick_update_size()

    def clear_rectangle_background(self, coordinate, paste_size):
        clear_image(self.name_image, coordinate, paste_size)

    def clear_rectangle_finale_image(self, coordinate, paste_size,
                          name_finale_image=DEFAULT_NAME_FINALE_IMAGE, clear_background=False):
        if clear_background:
            clear_image(self.name_image, coordinate, paste_size)
        with (Image.open(self.name_background_image) as background_image,
              Image.open(name_finale_image) as finale_image):
            size_finale_image = finale_image.size
            finale_coordinate = ((coordinate[0] * size_finale_image[0] + self.size[0] - 1) // self.size[0],
                                 (coordinate[1] * size_finale_image[1] + self.size[1] - 1) // self.size[1])
            finale_paste_size = ((paste_size[0] * size_finale_image[0]) // self.size[0],
                                 (paste_size[1] * size_finale_image[1]) // self.size[1])
            variable_part_background_image = (
                background_image.crop((coordinate[0], coordinate[1],
                                       coordinate[0] + paste_size[0],
                                       coordinate[1] + paste_size[1]))).resize(finale_paste_size, resampling[resampling_index])
            finale_image.paste(variable_part_background_image, finale_coordinate)
            finale_image.save(name_finale_image)

    def clear_all_background(self):
        clear_image(self.name_image, (0, 0), self.size)

    def clear_all_finale_image(self, name_finale_image=DEFAULT_NAME_FINALE_IMAGE,
                              clear_background=False):
        self.clear_rectangle_finale_image((0, 0), self.size,
                                        name_finale_image, clear_background)

    def update_backgrounds(self,
                           name_finale_image=DEFAULT_NAME_FINALE_IMAGE):
        self.clear_all_finale_image(name_finale_image)
        with (Image.open(self.name_image) as image,
              Image.open(self.name_background_image) as background_image,
              Image.open(name_finale_image) as finale_image):
            background_image = background_image.resize(finale_image.size, resampling[resampling_index])
            image = image.resize(finale_image.size, resampling[resampling_index])
            finale_image = Image.alpha_composite(background_image, image)
            finale_image.save(name_finale_image)

    def merge_backgrounds(self):
        with (Image.open(self.name_image) as image,
              Image.open(self.name_background_image) as background_image):
            finale_image = Image.new("RGBA", self.size, WHITE_TRANSPARENT)
            finale_image.alpha_composite(background_image, image)
            return finale_image

    def change_rectangle_background(self, coordinate, name_paste_image):
        with (Image.open(self.name_image) as image,
            Image.open(name_paste_image) as paste_image):
            image.paste(paste_image, coordinate)
            image.save(self.name_image)

    def change_rectangle_finale_image(self, coordinate, past_size, name_paste_image,
                        name_finale_image=DEFAULT_NAME_FINALE_IMAGE, change_background=True):
        if change_background:
            self.change_rectangle_background(coordinate, name_paste_image)
        with (Image.open(self.name_background_image) as background_image,
              Image.open(name_paste_image) as paste_image,
              Image.open(name_finale_image) as finale_image):
            finale_image_paste_size = ((past_size[0] * finale_image.size[0]) // self.size[0],
                          (past_size[1] * finale_image.size[1]) // self.size[1])
            finale_image_coordinate = ((coordinate[0] * finale_image.size[0] + self.size[0] - 1) // self.size[0],
                              (coordinate[1] * finale_image.size[1] + self.size[1] - 1) // self.size[1])
            part_of_the_background = (background_image.crop((coordinate[0], coordinate[1], coordinate[0] + past_size[0], coordinate[1] + past_size[1]))).resize(finale_image_paste_size, resampling[resampling_index])
            paste_image = paste_image.resize(finale_image_paste_size, resampling[resampling_index])
            finale_paste_image = Image.alpha_composite(part_of_the_background, paste_image)
            finale_image.paste(finale_paste_image, finale_image_coordinate, finale_paste_image)
            finale_image.save(name_finale_image)

    def change_rectangle_finale_image_paste_image(self, coordinate, paste_image,
                        name_finale_image=DEFAULT_NAME_FINALE_IMAGE):
        past_size = paste_image.size
        with (Image.open(self.name_background_image) as background_image,
              Image.open(name_finale_image) as finale_image):
            finale_image_paste_size = ((past_size[0] * finale_image.size[0]) // self.size[0],
                          (past_size[1] * finale_image.size[1]) // self.size[1])
            finale_image_coordinate = ((coordinate[0] * finale_image.size[0] + self.size[0] - 1) // self.size[0],
                              (coordinate[1] * finale_image.size[1] + self.size[1] - 1) // self.size[1])
            part_of_the_background = (background_image.crop((coordinate[0], coordinate[1], coordinate[0] + past_size[0], coordinate[1] + past_size[1]))).resize(finale_image_paste_size, resampling[resampling_index])
            paste_image = paste_image.resize(finale_image_paste_size, resampling[resampling_index])
            finale_paste_image = Image.alpha_composite(part_of_the_background, paste_image)
            finale_image.paste(finale_paste_image, finale_image_coordinate, finale_paste_image)
            finale_image.save(name_finale_image)

    def change_rectangle_finale_image_default_paste_size(self, coordinate, name_paste_image,
                        name_finale_image=DEFAULT_NAME_FINALE_IMAGE, change_background=True):
        size = (0, 0)
        with Image.open(name_paste_image) as paste_image:
            size = paste_image.size
        self.change_rectangle_finale_image(coordinate, size, name_paste_image, name_finale_image, change_background)

    def draw_a_picture_by_number(self, number, coordinate, paste_image_size=TABLATURES_SIZE,
                                 name_finale_image=DEFAULT_NAME_FINALE_IMAGE):
        paste_image = Image.new("RGBA", paste_image_size, WHITE_TRANSPARENT)
        draw = ImageDraw.Draw(paste_image)
        text_ = '-'
        match number:
            case int() as default if default <= -2:
                text_ = '-'
            case -1:
                text_ = 'x'
            case int() as default if default <= 50:
                text_ = str(number)
        draw.text((0, 0), text_, font=self.font_small, fill=(255, 255, 255, 255))
        self.change_rectangle_finale_image_paste_image(coordinate, paste_image, name_finale_image)

    def quick_change_size(self, new_size):
        self.size = new_size

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

    def quick_update_size(self):
        with (Image.open(self.name_image) as image,
              Image.open(self.name_background_image) as background):
            if self.size == image.size and self.size == background.size:
                return
            if self.size != image.size:
                (image.resize(self.size, Image.Resampling.LANCZOS)).save(self.name_image)
            if self.size != background.size:
                (background.resize(self.size, Image.Resampling.LANCZOS)).save(self.name_background_image)

class PaintImage(Paint):
    def __init__(self, size, name_background_image,
                 name_image, name_finale_image):
        super().__init__(size, name_background_image, name_image)
        self.background_image = Image.open(name_finale_image)
        self.image = Image.open(name_image)
        self.finale_image = Image.open(name_finale_image)
