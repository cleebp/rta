"""window.py

PyGame drawing reference:
- (0, 0) Upper Left
- (0, SCREEN_HEIGHT) Lower Left
- (SCREEN_WIDTH, 0) Upper Right
- (SCREEN_WIDTH, SCREEN_HEIGHT) Lower Right
"""
from colorsys import hsv_to_rgb

import numpy as np
import pygame

from config import *


class Analyser:

    def __init__(self, screen, clock):
        self.screen = screen
        self.font = pygame.font.Font(None, 30)
        self.clock = clock
        self.hue = 0

    def process_data(self, data):
        self._draw_spectrum(data)

    def update(self):
        self.clock.tick(24)
        fps = self.font.render(str(int(self.clock.get_fps())), True, WHITE)
        self.screen.blit(fps, (SCREEN_WIDTH - 50, 25))

        pygame.display.flip()

    def _draw_spectrum(self, spectrum):
        self.screen.fill(BLACK)

        spectrum_length = int(len(spectrum))
        chunk_size = int(spectrum_length / SCREEN_WIDTH)
        amp_step = SCREEN_HEIGHT/20

        index = -1
        for i in range(0, spectrum_length, chunk_size):
            index += 1
            chunk_arrays = [spectrum[i]]
            for j in range(i+1, i+chunk_size):
                if j == spectrum_length:
                    break
                chunk_arrays.append(spectrum[j])
            with np.errstate(all='ignore'):
                mean_array = np.mean(chunk_arrays)

            if np.isfinite(mean_array):
                amp = mean_array * amp_step
                y = SCREEN_HEIGHT/2 + amp
                height = amp * -2
            else:
                y = SCREEN_HEIGHT / 2
                height = 0

            color = self._hsv2rgb(self.hue, 1, 1)
            pygame.draw.rect(self.screen, color, (index, y, 1, height), 0)

        self._bump_hue(0.001)
        self.update()

    def _bump_hue(self, factor):
        self.hue += factor
        if self.hue == 1:
            self.hue = 0

    @staticmethod
    def _hsv2rgb(hue, sat, val):
        return tuple(round(i * 255) for i in hsv_to_rgb(hue, sat, val))
