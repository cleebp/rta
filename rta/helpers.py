import pyaudio


pa = pyaudio.PyAudio()


def list_input_devices():
    info = pa.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')

    for i in range(0, numdevices):
        if (pa.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", pa.get_device_info_by_host_api_device_index(0, i).get('name'))


list_input_devices()
