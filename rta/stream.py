"""stream.py

On board audio routing, analysis, and pass-through.
"""
from time import sleep

from librosa import beat
from librosa.onset import onset_strength
import numpy as np
from pyaudio import PyAudio, paContinue, paFloat32


pa = PyAudio()

CHUNK = 1024
CHANNELS = 2
RATE = 96000


def callback(in_data, frame_count, time_info, flag):
    """
    :param in_data: audio data from input source
    :param frame_count: 1024
    :param time_info: {'input_buffer_adc_time': ..., 'current_time': ..., 'output_buffer_dac_time': ...}
    :param flag: 0 or 1
    """
    y = np.fromstring(in_data, dtype=np.float32)
    print('Audio data:', y)

    return in_data, paContinue


stream = pa.open(format=paFloat32,
                 channels=CHANNELS,
                 rate=RATE,
                 output=False,
                 input=True,
                 stream_callback=callback,
                 input_device_index=2,
                 frames_per_buffer=CHUNK)

# start the stream
stream.start_stream()

while stream.is_active():
    sleep(0.25)

stream.close()
pa.terminate()


def _shitty_librosa_code_that_doesnt_work(in_data):
    onset_env = onset_strength(y=in_data, sr=RATE)
    tempo = beat.tempo(onset_envelope=onset_env, sr=RATE)
    dtempo = beat.tempo(onset_envelope=onset_env, sr=RATE, aggregate=None)

    print('Onset strength:', onset_env)
    print('Tempo:', tempo)
    print('DTempo:', dtempo)