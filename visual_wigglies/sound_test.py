import pyaudio

p = pyaudio.PyAudio()

# Print the available audio input devices
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    if info['maxInputChannels'] > 0:  # Only list input devices
        print(f"Device {i}: {info['name']} (Input Channels: {info['maxInputChannels']})")

p.terminate()
