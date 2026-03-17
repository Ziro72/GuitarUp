from PIL import Image, ImageDraw
from Paint import Paint
from TabRow import TabRow
from Consts import *


class TabPaint(Paint):
    def __init__(self, size=TAB_ORIGINAL_SIZE,
                 background_dir=TAB_BACKGROUND_DIR,
                 draft_dir=TAB_DRAFT_DIR, columns=None,
                 tab_size=TAB_SIZE, global_name="tabs"):
        super().__init__(size, background_dir, draft_dir)
        if columns is None:
            columns = [TabRow() for _ in range(DEFAULT_NUMBER_OF_COLUMNS)]
        self.columns = columns
        self.tab_size = tab_size
        self.global_name = global_name

    def clear_one_position_final_image(self, position,
                                       name_finale_image=TAB_DRAFT_DIR,
                                       change_default_tablature=False):
        if self.columns[position[0]].tab_row[position[1]] == -2:
            return
        self.cut_rectangle(self.coordinates_by_position(position),
                           self.tab_size, name_finale_image)
        if change_default_tablature:
            self.columns[position[0]].tab_row[position[1]] = -2

    def clear_tab(self, name_finale_image=TAB_DRAFT_DIR,
                  change_default_tablature=False):
        for i in range(len(self.columns)):
            for j in range(len(self.columns[i].tab_row)):
                self.clear_one_position_final_image((i, j), name_finale_image,
                                                    change_default_tablature)

    def change_tab_row(self, position):
        self.cut_rectangle(self.coordinates_by_position(position),
                           self.tab_size)
        self.draw_a_picture_by_number(self.columns[position[0]].tab_row[position[1]],
                                      self.coordinates_by_position(position), self.tab_size)

    def draw_a_picture_by_number(self, number, coordinate, paste_image_size=TAB_SIZE,):
        paste_image = Image.new("RGBA", paste_image_size, TRANSPARENT)
        text_ = '-'
        match number:
            case int() as default if default <= -2:
                text_ = '-'
            case -1:
                text_ = 'x'
            case int() as default if default <= 50:
                text_ = str(number)
        draw = ImageDraw.Draw(paste_image)
        draw.text((0, 0), text_, font=self.font_small, fill=(255, 255, 255, 255))
        self.paste_member(coordinate, paste_image)

    def save(self, original_size=TAB_ORIGINAL_SIZE):
        name_tab = TAB_OUTPUT_FOLDER + self.global_name + ".png"
        with Image.open(self.background_dir) as background_image:
            background_image.save(name_tab)
        for i in range(len(self.columns)):
            for j in range(len(self.columns[i].tab_row)):
                # вот здесь чета какта кринжа
                self.change_tab_row((i, j), name_tab)

    def set_global_name(self, new_global_name):
        self.global_name = new_global_name

    def set_cell_status(self, row_number, new_name):
        self.columns[row_number].name = new_name

    def update_tab_position(self, position, new_tablature,
                            name_finale_image=TAB_DRAFT_DIR):
        if len(new_tablature) == 0 or new_tablature == 'x' or new_tablature == '-' or new_tablature.isdigit() or (new_tablature[0] == '-' and new_tablature[1:].isdigit()):
            if len(new_tablature) == 0 or new_tablature == '-':
                self.columns[position[0]].tab_row[position[1]] = -2
            elif new_tablature == 'x':
                self.columns[position[0]].tab_row[position[1]] = -1
            else:
                if int(new_tablature) <= -2:
                    self.columns[position[0]].tab_row[position[1]] = -2
                elif int(new_tablature) >= 50:
                    self.columns[position[0]].tab_row[position[1]] = 50
                else:
                    self.columns[position[0]].tab_row[position[1]] = int(new_tablature)
            self.change_tab_row(position)

    def get_global_name(self):
        return self.global_name

    def get_position_name(self, position):
        return self.columns[position].name

    def get_cell_status(self, position):
        if self.columns[position[0]].tab_row[position[1]] == -2:
            return "-"
        if self.columns[position[0]].tab_row[position[1]] == -1:
            return "x"
        return str(self.columns[position[0]].tab_row[position[1]])

    def coordinates_by_position(self, position):
        return 400 + position[0] * 380, 220 + position[1] * 120