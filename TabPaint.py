from PIL import Image
from Paint import Paint
from TabRow import TabRow
from Consts import *


class TabPaint(Paint):
    def __init__(self, size=TABLATURES_ORIGINAL_SIZE,
                 name_background_image=DEFAULT_NAME_TABLATURES_BACKGROUND_IMAGE,
                 name_image=DEFAULT_NAME_TABLATURES_IMAGE, columns=None,
                 tablatures_size=TABLATURES_SIZE, global_name="tablatures"):
        super().__init__(size, name_background_image, name_image)
        if columns is None:
            columns = [TabRow() for _ in range(DEFAULT_NUMBER_OF_COLUMNS)]
        self.columns = columns
        self.tablatures_size = tablatures_size
        self.global_name = global_name

    def clear_one_position_finale_image(self, position,
                                        name_finale_image=DEFAULT_NAME_FINALE_TABLATURES_IMAGE,
                                        change_default_tablature=False):
        if self.columns[position[0]].tab_row[position[1]] == -2:
            return
        self.clear_rectangle_finale_image(self.coordinates_by_position(position),
                                          self.tablatures_size, name_finale_image)
        if change_default_tablature:
            self.columns[position[0]].tab_row[position[1]] = -2

    def clear_all_tablatures(self, name_finale_image=DEFAULT_NAME_FINALE_TABLATURES_IMAGE,
                             change_default_tablature=False):
        for i in range(len(self.columns)):
            for j in range(len(self.columns[i].tab_row)):
                self.clear_one_position_finale_image((i, j), name_finale_image,
                                                     change_default_tablature)

    def change_one_tablatures(self, position, name_finale_image=DEFAULT_NAME_FINALE_TABLATURES_IMAGE):
        self.clear_rectangle_finale_image(self.coordinates_by_position(position),
                                          self.tablatures_size, name_finale_image)
        self.draw_a_picture_by_number(self.columns[position[0]].tab_row[position[1]],
                                      self.coordinates_by_position(position), self.tablatures_size,
                                      name_finale_image)

    def save(self, original_size=TABLATURES_ORIGINAL_SIZE):
        name_tablatures = PATH_TABLATURES + self.global_name + ".png"
        with Image.open(self.name_background_image) as background_image:
            background_image.save(name_tablatures)
        for i in range(len(self.columns)):
            for j in range(len(self.columns[i].tab_row)):
                self.change_one_tablatures((i, j), name_tablatures)

    def set_global_name(self, new_global_name):
        self.global_name = new_global_name

    def set_cell_status(self, row_number, new_name):
        self.columns[row_number].name = new_name

    def update_tablatures_position(self, position, new_tablature,
                                   name_finale_image=DEFAULT_NAME_FINALE_TABLATURES_IMAGE):
        if len(new_tablature) == 0 or new_tablature == 'x' or new_tablature == '-' or new_tablature.isdigit() or (new_tablature[0] == '-' and new_tablature[1:].isdigit()):
            if len(new_tablature) == 0 or new_tablature == '-':
                self.columns[position[0]].tab_row[position[1]] = -2
            elif new_tablature == 'x':
                self.columns[position[0]].tab_row[position[1]] = -1
            else:
                self.columns[position[0]].tab_row[position[1]] = int(new_tablature)
            self.change_one_tablatures(position, name_finale_image)

    def get_global_name(self):
        return self.global_name

    def get_position_name(self, position):
        return self.columns[position].name

    def get_cell_status(self, position):
        return self.columns[position[0]].tab_row[position[1]]

    def coordinates_by_position(self, position):
        return 400 + position[0] * 380, 220 + position[1] * 120