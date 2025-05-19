from PIL import Image

from Arrow_class import Arrow

from Paint import Paint

from Consts import *

class ArrowPaint(Paint):
    def __init__(self, size=ORIGINAL_SIZE,
                 name_background_image=DEFAULT_NAME_ARROW_BACKGROUND_IMAGE,
                 name_image=DEFAULT_NAME_ARROW_IMAGE,
                 arrow_array=None, new_global_name="arrow"):
        super().__init__(size, name_background_image, name_image)
        self.global_name = new_global_name
        if arrow_array is None:
            arrow_array = [Arrow() for _ in range(MASSIVE_SIZE)]
        self.arrow_array = arrow_array

    def clear_one_arrow_background(self, position, resetting_the_value=True):
        self.clear_rectangle_background(self.coordinates_of_the_arrow_in_the_picture(position), ARROW_SIZE)
        if resetting_the_value:
            self.arrow_array[position] = Arrow()

    def clear_one_arrow_from_finale_image(self, position,
                         name_finale_image=DEFAULT_NAME_FINALE_ARROW_IMAGE, clear_background=False, resetting_the_value=False):
        if clear_background:
            self.clear_one_arrow_background(position, False)
        self.clear_rectangle_finale_image(self.coordinates_of_the_arrow_in_the_picture(position), ARROW_SIZE,
                                          name_finale_image)
        if resetting_the_value:
            self.arrow_array[position] = Arrow()

    def clear_all_arrows_background(self, resetting_the_value=True):
        for position in range(len(self.arrow_array)):
            self.clear_one_arrow_background(position, resetting_the_value)

    def clear_all_arrows_from_finale_image(self, name_finale_image=DEFAULT_NAME_FINALE_ARROW_IMAGE,
                                           clear_background=False, resetting_the_value=False):
        for position in range(len(self.arrow_array)):
            self.clear_one_arrow_from_finale_image(position, name_finale_image, clear_background, resetting_the_value)

    def change_one_arrow_in_background(self, position, view_arrow=DEFAULT_ARROW_END):
        self.clear_one_arrow_background(position)
        arrow = self.arrow_array[position]
        if arrow.type == 0:
            return
        arrow_name = (PATH_ARROWS_WIDGET + str(arrow.type) + str(arrow.status) +
                      str(arrow.direction) + str(arrow.accent) + view_arrow)
        self.change_rectangle_background(self.coordinates_of_the_arrow_in_the_picture(position), arrow_name)

    def change_one_arrow_in_finale_image(self, name_finale_image, position, view_arrow=DEFAULT_ARROW_END,
                                         change_background=False):
        self.clear_one_arrow_from_finale_image(position, name_finale_image, change_background)
        arrow = self.arrow_array[position]
        if arrow.type == 0:
            return
        arrow_name = (PATH_ARROWS_WIDGET + str(arrow.type) + str(arrow.status) +
                      str(arrow.direction) + str(arrow.accent) + view_arrow)
        with Image.open(arrow_name) as image_arrow:
            coordinate = (DISTANCE_BETWEEN_ARROWS + position * (ARROW_SIZE[0] + DISTANCE_BETWEEN_ARROWS),
                          (self.size[1] - ARROW_HEIGHT + 1) // 2 + ARROW_HEIGHT - image_arrow.size[1])
            paste_size = image_arrow.size
            self.change_rectangle_finale_image(coordinate, paste_size, arrow_name, name_finale_image, change_background)

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
            self.change_one_arrow_in_finale_image(name_hide_arrow, position, DEFAULT_HIDE_ARROW_END)
            self.change_one_arrow_in_finale_image(name_arrow, position, DEFAULT_ARROW_END)

    def update_storage_all(self, new_arrow_array,
                           name_finale_image=DEFAULT_NAME_FINALE_ARROW_IMAGE):
        self.arrow_array = new_arrow_array
        for position in range(len(new_arrow_array)):
            self.update_storage_position(position, name_finale_image)

    def update_storage_position(self, position, name_finale_image=DEFAULT_NAME_FINALE_ARROW_IMAGE):
        self.change_one_arrow_in_finale_image(name_finale_image, position)

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

    def coordinates_of_the_arrow_in_the_picture(self, position):
        coordinate = (DISTANCE_BETWEEN_ARROWS + position * (ARROW_SIZE[0] + DISTANCE_BETWEEN_ARROWS),
                      (self.size[1] - ARROW_SIZE[1] + 1) // 2)
        return coordinate
