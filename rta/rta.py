# https://gist.github.com/mailletf/c49063d005dfc51a2df6#file-gistfile1-py
# soundflower tutorial: https://apple.stackexchange.com/questions/221980/os-x-route-audio-output-to-audio-input
# soundflower: https://github.com/mattingalls/Soundflower

import pyaudio
from librosa import resample
from librosa.onset import onset_strength
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
    y = np.fromstring(in_data, dtype=np.float32)
    print('Audio data:', y)

    # onset_env = onset_strength(y)
    # tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=RATE)
    # dtempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr, aggregate=None)

    # print('Onset strength:', onset_env)
    # print('Tempo:', tempo)
    # print('DTempo:', dtempo)

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
                 output=False,
                 input=True,
                 stream_callback=callback,
                 input_device_index=4,
                 frames_per_buffer=CHUNK)

# start the stream
stream.start_stream()

while stream.is_active():
    sleep(0.25)

stream.close()
pa.terminate()
