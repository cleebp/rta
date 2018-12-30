from pygame import draw


class Bar:

    def __init__(self, x, y, width, height, thickness, color, screen, spectrum_range):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.thickness = thickness
        self.color = color
        self.screen = screen
        self.spectrum_range = spectrum_range

    def update(self, y, height, color):
        self.y = y
        self.height = height
        self.color = color

    def draw(self):
        draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height), self.thickness)
