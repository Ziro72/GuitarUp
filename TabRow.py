from Consts import *


class TabRow:
    def __init__(self, name="", tab_row=None):
        self.name = name
        if tab_row is None:
            tab_row = [-2 for _ in range(DEFAULT_NUMBER_OF_LINES)]
        self.tab_row = tab_row

    def get_name(self):
        return self.name

    def get_row(self):
        return self.tab_row

    def get_cell(self, position):
        return self.tab_row[position]

    def set_row(self, new_tab_row=None):
        if new_tab_row is None:
            new_tab_row = [-2 for _ in range(len(self.tab_row))]
        self.tab_row = new_tab_row

    def set_cell(self, position, new_cell=-2):
        self.tab_row[position] = new_cell


    def set_name(self, new_name):
        self.name = new_name