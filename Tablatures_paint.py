from PIL import Image
from Paint import Paint
from Tablatures_class import Tablatures
from Consts import *

class TablaturesPaint(Paint):
    def __init__(self, size=TABLATURES_ORIGINAL_SIZE,
                 name_background_image=DEFAULT_NAME_TABLATURES_BACKGROUND_IMAGE,
                 name_image=DEFAULT_NAME_TABLATURES_IMAGE, columns=None,
                 tablatures_size=TABLATURES_SIZE, global_name="tablatures"):
        super().__init__(size, name_background_image, name_image)
        if columns is None:
            columns = [Tablatures() for _ in range(DEFAULT_NUMBER_OF_COLUMNS)]
        self.columns = columns
        self.tablatures_size = tablatures_size
        self.global_name = global_name

    def clear_one_position_finale_image(self, position,
                                        name_finale_image=DEFAULT_NAME_FINALE_TABLATURES_IMAGE,
                                        change_default_tablature=False):
        if self.columns[position[0]].tablatures[position[1]] == -2:
            return
        self.clear_rectangle_finale_image(self.coordinates_by_position(position),
                                          self.tablatures_size, name_finale_image)
        if change_default_tablature:
            self.columns[position[0]].tablatures[position[1]] = -2

    def clear_all_tablatures(self, name_finale_image=DEFAULT_NAME_FINALE_TABLATURES_IMAGE,
                             change_default_tablature=False):
        for i in range(len(self.columns)):
            for j in range(len(self.columns[i].tablatures)):
                self.clear_one_position_finale_image((i, j), name_finale_image,
                                                     change_default_tablature)

    def change_one_tablatures(self, position, name_finale_image=DEFAULT_NAME_FINALE_TABLATURES_IMAGE):
        self.clear_rectangle_finale_image(self.coordinates_by_position(position),
                                          self.tablatures_size, name_finale_image)
        self.draw_a_picture_by_number(self.columns[position[0]].tablatures[position[1]],
                                      self.coordinates_by_position(position),  self.tablatures_size,
                                      name_finale_image)

    def save(self, original_size=TABLATURES_ORIGINAL_SIZE):
        name_tablatures = PATH_TABLATURES + self.global_name + ".png"
        image = Image.new("RGBA", original_size, (255, 255, 255, 0))
        image.save(name_tablatures)
        image.close()
        del image
        for i in range(len(self.columns)):
            for j in range(len(self.columns[i].tablatures)):
                self.change_one_tablatures((i, j), name_tablatures)

    def set_global_name(self, name):
        self.global_name = name

    def set_cell_status(self, position, new_status,
                        name_finale_image=DEFAULT_NAME_FINALE_TABLATURES_IMAGE):
        self.columns[position[0]].tablatures[position[1]] = new_status
        self.change_one_tablatures(position, name_finale_image)

    def get_position_name(self, position):
        return self.columns[position[0]].tablatures.name

    def get_cell_status(self, position):
        return self.columns[position[0]].tablatures[position[1]]

    def coordinates_by_position(self, position):
        return (position[0] + 1) * DEFAULT_WIDTH_DISTANCE, (position[1] + 1) * DEFAULT_HEIGHT_DISTANCE