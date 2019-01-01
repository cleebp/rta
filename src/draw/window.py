"""window.py

PyGame drawing reference:
- (0, 0) Upper Left
- (0, SCREEN_HEIGHT) Lower Left
- (SCREEN_WIDTH, 0) Upper Right
- (SCREEN_WIDTH, SCREEN_HEIGHT) Lower Right
"""
from pygame import font, display

from config import BLACK, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE
from draw.canvas import Canvas


class Window:

    def __init__(self, screen, clock):
        self.screen = screen
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.canvas = self._init_canvas()

        # for fps counter
        self.font = font.Font(None, 30)
        self.clock = clock

    def update(self):
        self.screen.fill(BLACK)

    def draw(self, data):
        self.update()  # could refactor into an update decorator on all draw calls
        self.canvas.draw(data)
        self._draw_fps()

    def _init_canvas(self):
        canvas_width = self.width*0.666  # \m/
        canvas_height = self.height*0.666  # \m/
        margin = ((self.width - canvas_width)/2, (self.height - canvas_height)/2)
        return Canvas(self.screen, canvas_width, canvas_height, margin)

    def _draw_fps(self):
        self.clock.tick(18)
        fps = self.font.render(str(int(self.clock.get_fps())), True, WHITE)
        self.screen.blit(fps, (self.width - 50, 25))  # 25px down, 50px from right edge
        display.flip()
