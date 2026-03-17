class Cell:
    def __init__(self, category=0, state=0, option=0, accent=0, chord=""):
        # 0 - symbol; 1 - default; 2 - top; 3 - bottom; 4 - drums
        self.category_ = category

        # type 0: 0 - empty; 1 - hummerOn; 2 - pullOff
        # type 1-3: 0 - free; 1 - PM; 2 - muted
        # type 4: 0 - clear; 1 - added
        self.state_ = state

        # only for types 1-4
        # type 1-3: 0 - up; 1 - down
        # type 4: 0 - snare; 1 - bass
        self.option_ = option

        # only for types 1-4
        self.accent_ = accent

        self.chord_ = chord

    def set_category(self, category):
        self.category_ = category

    def set_state(self, state):
        self.state_ = state

    def set_option(self, option):
        self.option_ = option

    def set_accent(self, accent):
        self.accent_ = accent

    def set_chord(self, chord):
        self.chord_ = chord

    def reset(self):
        self.state_ = 0
        self.option_ = 0
        self.accent_ = 0

    def get_cell_code(self):
        code = str(self.category_) + str(self.state_)
        if self.category_ != 0:
            code += str(self.option_) + str(self.accent_)
        return code
