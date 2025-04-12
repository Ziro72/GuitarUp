from PIL import Image

from Arrow_class import Arrow

from Paint import Paint

from Consts import *

class ArrowPaint(Paint):
    def __init__(self, size=ORIGINAL_SIZE,
                 name_background_image=DEFAULT_NAME_ARROW_BACKGROUND_IMAGE,
                 name_image=DEFAULT_NAME_ARROW_IMAGE,
                 arrow_array=None, new_global_name="arrow",
                 compression=COMPRESSION_RATIO):
        super().__init__(size, name_background_image, name_image)
        self.global_name = new_global_name
        self.compression = compression
        if arrow_array is None:
            arrow_array = [Arrow() for _ in range(MASSIVE_SIZE)]
        self.arrow_array = arrow_array

    def clear_one(self, position, flag=True):
        arrow_size = (int(ARROW_SIZE[0] * self.compression[0]),
                      int(ARROW_SIZE[1] * self.compression[1]))
        image_position = (int((DISTANCE_BETWEEN_ARROWS + position *
                               (ARROW_SIZE[0] + DISTANCE_BETWEEN_ARROWS)) * self.compression[0]),
                          (self.size[1] - int(self.compression[1] * ARROW_SIZE[1]) + 1) // 2)
        self.clear_rectangle(image_position, arrow_size)
        if flag:
            self.arrow_array[position] = Arrow()

    def clear_one_global(self, position,
                         name_image=DEFAULT_NAME_FINALE_ARROW_IMAGE):
        arrow_size = (int(ARROW_SIZE[0] * self.compression[0]),
                      int(ARROW_SIZE[1] * self.compression[1]))
        image_position = (int((DISTANCE_BETWEEN_ARROWS + position *
                               (ARROW_SIZE[0] + DISTANCE_BETWEEN_ARROWS)) * self.compression[0]),
                          (self.size[1] - int(self.compression[1] * ARROW_SIZE[1]) + 1) // 2)
        self.clear_backgrounds_position(image_position, arrow_size, name_image)
        self.arrow_array[position] = Arrow()

    def clear_all_arrows(self):
        for position in range(len(self.arrow_array)):
            self.clear_one(position)

    def clear_all_arrows_global(self, name_image=DEFAULT_NAME_FINALE_ARROW_IMAGE):
        for position in range(len(self.arrow_array)):
            self.clear_one_global(position, name_image)

    def paste_arrow(self, name_image, position, view_arrow=DEFAULT_ARROW_END,
                        compression_ratio=COMPRESSION_RATIO):
        arrow = self.arrow_array[position]
        if arrow.type == 0:
            return
        arrow_name = (PATH_ARROWS_WIDGET + str(arrow.type) + str(arrow.status) +
                      str(arrow.direction) + str(arrow.accent) + view_arrow)
        with Image.open(arrow_name) as image_arrow:
            image_arrow = image_arrow.resize((int(image_arrow.size[0] * compression_ratio[0] *
                                                  self.compression[0]),
                                                 int(image_arrow.size[1] * compression_ratio[1] *
                                                     self.compression[1])),
                                                 Image.Resampling.LANCZOS)
            coordinate = (int((DISTANCE_BETWEEN_ARROWS + position
                               * (ARROW_SIZE[0] + DISTANCE_BETWEEN_ARROWS)) *
                              self.compression[0]),
                          (self.size[1] - int(self.compression[1] * ARROW_HEIGHT) + 1) // 2 +
                          int(self.compression[1] * ARROW_HEIGHT) - image_arrow.size[1])
            self.change_position(coordinate, (coordinate[0] + int(ARROW_SIZE[0] * self.compression[0]),
                                              coordinate[1] + int(ARROW_SIZE[1] * self.compression[1])),
                                 image_arrow, name_image)

    def save(self, original_size=ORIGINAL_SIZE):
        name_arrow = PATH_ARROWS + self.global_name + ".png"
        name_hide_arrow = PATH_HIDE_ARROWS + self.global_name + ".png"
        image = Image.new("RGBA", original_size, (255, 255, 255, 0))
        hide_image = Image.new("RGBA", original_size, (255, 255, 255, 0))
        image.save(name_arrow)
        hide_image.save(name_hide_arrow)
        image.close()
        hide_image.close()
        del image
        del hide_image
        for position in range(len(self.arrow_array)):
            self.paste_arrow(name_arrow, position)
            self.paste_arrow(name_hide_arrow, position, DEFAULT_HIDE_ARROW_END)
        with Image.open(name_arrow) as image_arrow:
            image_arrow.save(self.name_image)

    def update_storage_all(self, new_arrow_array,
                           name_arrows=DEFAULT_NAME_FINALE_ARROW_IMAGE):
        self.clear_all_arrows()
        self.arrow_array = new_arrow_array
        for position in range(len(new_arrow_array)):
            self.update_storage_position(position, name_arrows)

    def new_compression(self, compression_ratio=COMPRESSION_RATIO):
        self.compression = compression_ratio

    def update_storage_position(self, position,
                                name_arrows=DEFAULT_NAME_FINALE_ARROW_IMAGE,
                                new_size=PICTURE_SIZE):
        self.clear_one(position, False)
        self.paste_arrow(name_arrows, position)
        with Image.open(self.name_image) as image:
            (image.resize(new_size, Image.Resampling.LANCZOS)).save(name_arrows)

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
                 name_arrows=DEFAULT_NAME_FINALE_ARROW_IMAGE):
        self.arrow_array[position].name = new_name
        self.update_storage_position(position, name_arrows)

    def set_type(self, position, new_type,
                 name_arrows=DEFAULT_NAME_FINALE_ARROW_IMAGE):
        self.arrow_array[position].type = new_type
        self.update_storage_position(position, name_arrows)

    def set_accent(self, position, new_accent,
                   name_arrows=DEFAULT_NAME_FINALE_ARROW_IMAGE):
        self.arrow_array[position].accent = new_accent
        self.update_storage_position(position, name_arrows)

    def set_status(self, position, new_status,
                   name_arrows=DEFAULT_NAME_FINALE_ARROW_IMAGE):
        self.arrow_array[position].status = new_status
        self.update_storage_position(position, name_arrows)

    def set_direction(self, position, new_direction,
                      name_arrows=DEFAULT_NAME_FINALE_ARROW_IMAGE):
        self.arrow_array[position].direction = new_direction
        self.update_storage_position(position, name_arrows)