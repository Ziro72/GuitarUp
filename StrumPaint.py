from PIL import Image

from StrumCell import Cell

from Paint import Paint

from Consts import *


class StrumPaint(Paint):
    def __init__(self, size=ORIGINAL_SIZE,
                 background_dir=STRUM_BACKGROUND_DIR,
                 draft_dir=STRUM_DRAFT_DIR,
                 cells=None, new_global_name="arrow"):
        super().__init__(size, background_dir, draft_dir)
        self.global_name = new_global_name
        if cells is None:
            cells = [Cell() for _ in range(CELLS_CAP)]
        self.cells_ = cells

    def clear_cell(self, number, reset_value=False):
        self.cut_rectangle(self.get_position_by_number(number), CELL_SIZE)
        if reset_value:
            self.cells_[number] = Cell()

    def clear_strum(self, reset_value=False):
        for index in range(len(self.cells_)):
            self.clear_cell(index, reset_value)

    def redraw_cell_draft(self, number):  # , is_filled=True
        self.clear_cell(number)
        cell = self.cells_[number]
        if cell.category_ == 0 and cell.state_ == 0:
            return
        cell_image_dir = (CELL_IMAGES_DIR + cell.get_cell_code() + '1.png')
        pos = (CELL_INDENT + number * (CELL_WIDTH + CELL_INDENT), (self.size[1] - CELL_HEIGHT) // 2)
        self.paste_member_by_dir(pos, cell_image_dir)

    def draw_cell(self, number, is_filled=True):
        cell = self.cells_[number]
        if cell.category_ == 0 and cell.state_ == 0:
            return
        cell_image_dir = (CELL_IMAGES_DIR + cell.get_cell_code() + str(int(is_filled)) + '.png')
        pos = (CELL_INDENT + number * (CELL_WIDTH + CELL_INDENT), (self.size[1] - CELL_HEIGHT) // 2)
        self.draw_member_by_dir(pos, cell_image_dir)

    def save(self, is_filled=True):
        original_size = ORIGINAL_SIZE
        strum_name = self.global_name + (HIDE_SUFFIX if not is_filled else "") + ".png"
        image = Image.new("RGBA", original_size, TRANSPARENT)
        image.save(STRUMS_OUTPUT_FOLDER + strum_name)
        image.close()
        del image
        self.save_dir = STRUMS_OUTPUT_FOLDER + strum_name
        for index in range(len(self.cells_)):
            self.draw_cell(index, is_filled)

    def update_storage_all(self, new_arrow_array):
        self.cells_ = new_arrow_array
        for index in range(len(new_arrow_array)):
            self.redraw_cell_draft(index)

    def get_chord(self, index):
        return self.cells_[index].chord_

    def get_category(self, index):
        return self.cells_[index].category_

    def get_accent(self, index):
        return self.cells_[index].accent_

    def get_state(self, index):
        return self.cells_[index].state_

    def get_option(self, index):
        return self.cells_[index].option_

    def get_global_name(self):
        return self.global_name

    def set_global_name(self, new_global_name="arrow"):
        self.global_name = new_global_name

    def set_chord(self, index, chord):
        self.cells_[index].set_chord(chord)
        self.redraw_cell_draft(index)

    def set_category(self, index, category):
        self.cells_[index].set_category(category)
        self.redraw_cell_draft(index)

    def set_state(self, index, state):
        self.cells_[index].set_state(state)
        self.redraw_cell_draft(index)

    def set_option(self, index, option):
        self.cells_[index].set_option(option)
        self.redraw_cell_draft(index)

    def set_accent(self, index, accent):
        self.cells_[index].set_accent(accent)
        self.redraw_cell_draft(index)

    def reset_cell(self, index):
        self.cells_[index].reset()

    def get_position_by_number(self, number):
        position = (CELL_INDENT + number * (CELL_SIZE[0] + CELL_INDENT), (self.size[1] - CELL_SIZE[1] + 1) // 2)
        return position
