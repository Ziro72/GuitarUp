class Arrow:
    def __init__(self, type=0, color=0, status=0, direction=0, name=""):
        self.type = type
        self.color = color
        self.status = status
        self.direction = direction
        self.name = name

    def new_size(self, new_type):
        self.type = new_type

    def new_color(self, new_color):
        self.color = new_color

    def new_side(self, new_status):
        self.status = new_status

    def new_direction(self, new_direction):
        self.direction = new_direction

    def new_name(self, new_name):
        self.name = new_name
