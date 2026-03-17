class String:
    def __init__(self):
        self.is_muted = False
        self.fret = ()
        self.open_note = "A"  # for future

    def set_fret(self, fret):
        self.is_pinched = bool(fret)
        self.fret = fret

    def set_mute_status(self, status):
        self.is_muted = status
