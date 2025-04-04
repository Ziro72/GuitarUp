class Arrow:
    def __init__(self, type=0, status=0, direction=0, accent=0, name=""):
        self.type = type
        self.status = status
        self.direction = direction
        self.accent = accent
        self.name = name

    def new_type(self, new_type_):
        self.type = new_type_

    def new_accent(self, new_accent_):
        self.accent = new_accent_

    def new_status(self, new_status_):
        self.status = new_status_

    def new_direction(self, new_direction_):
        self.direction = new_direction_

    def new_name(self, new_name_):
        self.name = new_name_
