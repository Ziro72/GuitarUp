class Finger:
    def __init__(self, fret=0, string=0):
        self.is_pinch = bool(fret)
        self.fret = fret
        self.string = string

    def edit(self, fret=0, string=0):
        self.is_pinch = bool(fret)
        self.fret = fret
        self.string = string

    def edit_fret(self, fret):
        self.fret = fret

    def edit_string(self, string):
        self.string = string
