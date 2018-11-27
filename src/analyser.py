"""analyser.py

"""

import numpy as np
import pygame

from config import *


class Analyser:
    FREQUENCY_RANGE = (500, 1200)

    def __init__(self, screen, clock, window_size=None, segments_buf=None):
        self.screen_array = np.zeros((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen = screen
        self.font = pygame.font.Font(None, 30)
        self.clock = clock

    def _draw_spectrum(self, spectrum):
        # lower right = (0, SCREEN_HEIGHT)
        spectrum_length = int(len(spectrum))
        chunk_size = int(spectrum_length / SCREEN_WIDTH)
        normal = 0 if spectrum.max() == 0 else SCREEN_HEIGHT/spectrum.max()

        index = -1
        for i in range(0, spectrum_length, chunk_size):
            index += 1
            chunk_arrays = [spectrum[i]*normal]
            for j in range(i+1, i+chunk_size):
                if j == spectrum_length:
                    break
                chunk_arrays.append(spectrum[j]*normal)
            mean_array = np.mean(chunk_arrays, axis=0)

            x = index
            y = SCREEN_HEIGHT - int(mean_array)
            width = 1
            height = SCREEN_HEIGHT
            pygame.draw.rect(self.screen, GREEN, (x, y, width, height), 0)

        self.update()

    def update(self):
        fps = self.font.render(str(int(self.clock.get_fps())), True, WHITE)
        self.screen.blit(fps, (SCREEN_WIDTH - 50, 25))

        pygame.display.flip()

        self.clock.tick(24)
        self.screen.fill(BLACK)

    def process_data(self, data):
        self._draw_spectrum(data)
