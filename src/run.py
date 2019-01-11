"""run.py

On board audio routing, analysis, and pass-through.
"""
from time import sleep

import numpy as np
from pyaudio import PyAudio, paContinue, paFloat32, Stream
import pygame

from config import *
from draw.window import Window


class Driver:

    def __init__(self, screen, clock):
        self.window = Window(screen, clock)
        self.stream = Stream

    def run(self):
        pa = PyAudio()

        self.stream = pa.open(format=paFloat32,
                              channels=CHANNELS,
                              rate=SAMPLE_RATE,
                              output=False,
                              input=True,
                              stream_callback=self.callback,
                              input_device_index=INPUT_DEVICE_INDEX,
                              frames_per_buffer=CHUNK)

        self.stream.start_stream()

        pyquit = False
        while self.stream.is_active() and not pyquit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pyquit = True
                if event.type == pygame.KEYDOWN:
                    self._process_input(event.key)
            sleep(0.82)  # 18 fps

        self.stream.stop_stream()
        self.stream.close()
        pa.terminate()
        pygame.quit()

    def callback(self, in_data, frame_count, time_info, flag):
        """
        :param in_data: audio data from input source
        :param frame_count: 1024
        :param time_info: {'input_buffer_adc_time': ..., 'current_time': ..., 'output_buffer_dac_time': ...}
        :param flag: 0 or 1
        """
        y = np.fromstring(in_data, dtype=np.float32)
        with np.errstate(all='ignore'):
            spectrum = np.nan_to_num(np.log(y))
        self.window.draw(spectrum)

        return in_data, paContinue

    def _process_input(self, key):
        if key == pygame.K_TAB:
            print('TAB pressed')
        if key == pygame.K_c:
            print('c pressed')
        if key == pygame.K_f:
            print('f pressed')


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF)
    pygame.display.set_caption('rta - rip winamp')
    driver = Driver(screen=pygame.display.get_surface(), clock=pygame.time.Clock())

    driver.run()
