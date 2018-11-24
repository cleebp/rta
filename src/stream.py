"""stream.py

On board audio routing, analysis, and pass-through.
"""
import pygame
import random
from time import sleep, time

from librosa import beat
from librosa.onset import onset_strength
import numpy as np
from pyaudio import PyAudio, paContinue, paFloat32, Stream

from config import *
from analyser import Analyser


class Stream:

    stream = Stream

    def __init__(self, screen, start_time):
        self._analyser = Analyser(window_size=WINDOW_SIZE, segments_buf=RING_BUFFER_SIZE,
                                  screen=screen)
        self.last_time = start_time

    def run(self):
        pa = PyAudio()

        self.stream = pa.open(format=paFloat32,
                              channels=CHANNELS,
                              rate=SAMPLE_RATE,
                              output=False,
                              input=True,
                              stream_callback=self.callback,
                              input_device_index=2,
                              frames_per_buffer=CHUNK)

        # start the stream
        self.stream.start_stream()

        while self.stream.is_active():
            self._fps()
            sleep(0.24)

        self.stream.stop_stream()
        self.stream.close()
        pa.terminate()

    def callback(self, in_data, frame_count, time_info, flag):
        """
        :param in_data: audio data from input source
        :param frame_count: 1024
        :param time_info: {'input_buffer_adc_time': ..., 'current_time': ..., 'output_buffer_dac_time': ...}
        :param flag: 0 or 1
        """
        y = np.fromstring(in_data, dtype=np.float32)

        '''for i in range(len(y)):
            self.screen_array.fill(i)
            pygame.surfarray.blit_array(self.screen, self.screen_array)
            pygame.display.flip()'''

        # print('Audio data:', y)
        freq = self._analyser.process_data(y)
        if freq:
            # onset
            print("Onset detected; fundamental frequency:", freq)

        return in_data, paContinue

    def _fps(self):
        t2 = time()
        time_delta = (t2 - self.last_time) * 100
        self.last_time = t2
        print('FPS:', time_delta)


if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE), pygame.DOUBLEBUF)
    screen = pygame.display.get_surface()
    stream = Stream(screen=screen, start_time=time())
    stream.run()

def _shitty_librosa_code_that_doesnt_work(in_data):
    onset_env = onset_strength(y=in_data, sr=SAMPLE_RATE)
    tempo = beat.tempo(onset_envelope=onset_env, sr=SAMPLE_RATE)
    dtempo = beat.tempo(onset_envelope=onset_env, sr=SAMPLE_RATE, aggregate=None)

    print('Onset strength:', onset_env)
    print('Tempo:', tempo)
    print('DTempo:', dtempo)
