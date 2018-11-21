# https://gist.github.com/mailletf/c49063d005dfc51a2df6#file-gistfile1-py

import pyaudio
#import librosa
import numpy as np
from time import sleep


pa = pyaudio.PyAudio()

CHUNK = 1024
CHANNELS = 2
RATE = 44100

# ring buffer will keep the last 2 seconds worth of audio
# ringBuffer = RingBuffer(2 * 22050)


def callback(in_data, frame_count, time_info, flag):
    """
    :param in_data: audio data from input source
    :param frame_count: 1024
    :param time_info: {'input_buffer_adc_time': ..., 'current_time': ..., 'output_buffer_dac_time': ...}
    :param flag: 0 or 1
    """
    audio_data = np.fromstring(in_data, dtype=np.float32)

    # ringBuffer.extend(audio_data)
    # process data array using librosa
    # ...

    return in_data, pyaudio.paContinue


# function that finds the index of the Soundflower
# input device and HDMI output device
# dev_indexes = findAudioDevices()

stream = pa.open(format=pyaudio.paFloat32,
                 channels=CHANNELS,
                 rate=RATE,
                 output=True,
                 input=True,
                 stream_callback=callback,
                 frames_per_buffer=CHUNK)

# start the stream
stream.start_stream()

while stream.is_active():
    sleep(0.1)

stream.close()
pa.terminate()
