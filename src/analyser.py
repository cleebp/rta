"""analyser.py

PyGame drawing reference:
- (0, 0) Upper Left
- (0, SCREEN_HEIGHT) Lower Left
- (SCREEN_WIDTH, 0) Upper Right
- (SCREEN_WIDTH, SCREEN_HEIGHT) Lower Right
"""

import numpy as np
import pygame

from config import *


class Analyser:
    FREQUENCY_RANGE = (500, 1200)

    def __init__(self, screen, clock):
        self.screen_array = np.zeros((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen = screen
        self.font = pygame.font.Font(None, 30)
        self.clock = clock

    def _draw_spectrum(self, spectrum):
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
            mean_array = np.mean(chunk_arrays)

            if np.isfinite(mean_array):
                amp = mean_array * amp_step
                y = SCREEN_HEIGHT/2 + amp
                height = amp * -2
            else:
                y = SCREEN_HEIGHT / 2
                height = 0

            x = index
            width = 1
            pygame.draw.rect(self.screen, RED, (x, y, width, height), 0)

        self.update()

    def update(self):
        fps = self.font.render(str(int(self.clock.get_fps())), True, WHITE)
        self.screen.blit(fps, (SCREEN_WIDTH - 50, 25))

        pygame.display.flip()

        self.clock.tick(24)
        self.screen.fill(BLACK)

    def process_data(self, data):
        self._draw_spectrum(data)
