import pyaudio
#import librosa
import numpy as np
from time import sleep


pa = pyaudio.PyAudio()

CHANNELS = 2
RATE = 44100

# ring buffer will keep the last 2 seconds worth of audio
# ringBuffer = RingBuffer(2 * 22050)


def callback(in_data, frame_count, time_info, flag):
    # audio_data = np.fromstring(in_data, dtype=np.float32)

    # we trained on audio with a sample rate of 22050 so we need to convert it
    # audio_data = librosa.resample(audio_data, 44100, 22050)
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
                 stream_callback=callback)

# start the stream
stream.start_stream()

while stream.is_active():
    sleep(0.1)

stream.close()
pa.terminate()
