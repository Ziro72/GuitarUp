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

    def update_all_tablatures(self, new_tablatures):
        self.tablatures = new_tablatures

