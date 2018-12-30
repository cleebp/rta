from pygame import draw


class Bar:

    def __init__(self, x, y, width, height, thickness, color, screen):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.thickness = thickness
        self.color = color
        self.screen = screen

    def update(self, x, y, height, color):
        self.x, self.y = x, y
        self.height = height
        self.color = color

    def draw(self):
        draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height), self.thickness)
