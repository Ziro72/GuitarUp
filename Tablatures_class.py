from Consts import *

class Tablatures:
    def __init__(self, name="", tablatures=None):
        self.name = name
        if tablatures is None:
            tablatures = [-2 for _ in range(DEFAULT_NUMBER_OF_LINES)]
        self.tablatures = tablatures

    def get_name(self):
        return self.name

    def get_tablatures(self):
        return self.tablatures

    def get_tablature(self, position):
        return self.tablatures[position]

    def update_all_tablatures(self, new_tablatures=None):
        if new_tablatures is None:
            new_tablatures = [-2 for _ in range(len(self.tablatures))]
        self.tablatures = new_tablatures

    def update_position_in_tablatures(self, position, new_tablature=-2):
        self.tablatures[position] = new_tablature

    def update_name(self, new_name):
        self.name = new_name