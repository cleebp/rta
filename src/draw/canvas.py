from colorsys import hsv_to_rgb

import numpy as np

from config import SCREEN_HEIGHT, WINDOW_SIZE
from draw.bar import Bar


class Canvas:

    def __init__(self, screen, width, height, margin):
        self.screen = screen
        self.width, self.height = width, height
        self.margin = margin

        self.hue = 0
        self.color = self._hsv2rgb(self.hue, 1, 1)

        self.offset = 2  # pixels between bars
        self.spectrum_bars = self._init_spectrum_bars()
        self.amp_step = self.height/15

    def update(self, spectrum):
        self._bump_hue(0.001)
        self._update_spectrum_bars(spectrum)

    def draw(self, spectrum):
        self.update(spectrum)

    def _init_spectrum_bars(self):
        spectrum_bars = []
        x = self.offset + self.margin[0]
        y, height = SCREEN_HEIGHT/2, 0
        width = (self.width / 50) - self.offset

        for i in range(50):
            spectrum_range = ((WINDOW_SIZE // 50) * i, (WINDOW_SIZE // 50) * (i+1))
            bar = Bar(x, y, width, height, 0, self.color, self.screen, spectrum_range)
            spectrum_bars.append(bar)
            x += width + self.offset

        return spectrum_bars

    def _update_spectrum_bars(self, spectrum):
        for bar in self.spectrum_bars:
            with np.errstate(all='ignore'):
                mean_amp = np.mean([spectrum[bar.spectrum_range[0]:bar.spectrum_range[1]]])

            if np.isfinite(mean_amp):
                mean_amp *= self.amp_step
                y = SCREEN_HEIGHT/2 + mean_amp
                height = mean_amp * -2
            else:
                y = SCREEN_HEIGHT/2
                height = 0

            bar.update(y, height, self.color)
            bar.draw()

    def _bump_hue(self, factor):
        self.hue += factor
        if self.hue == 1:
            self.hue = 0
        self.color = self._hsv2rgb(self.hue, 1, 1)

    @staticmethod
    def _hsv2rgb(hue, sat, val):
        return tuple(round(i * 255) for i in hsv_to_rgb(hue, sat, val))
