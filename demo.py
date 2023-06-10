import pyaudio
import numpy as np

def generate_carrier(frequency, duration, sampling_rate, vol):
    samples = (np.sin(2 * np.pi * np.arange(int(sampling_rate * duration)) * frequency / sampling_rate)).astype(np.float32)
    return (samples*vol)


def modulate_data(binary_data, mark_frequency, space_frequency, sampling_rate, duration, vol):
    carrier = generate_carrier(mark_frequency, duration, sampling_rate, vol)
    # length = len(carrier.tobytes())
    # t = np.arange(0, length )
    modulated_signal = bytearray()

    for i, bit in enumerate(binary_data):
        frequency = mark_frequency if bit == 1 else space_frequency
        carrier = generate_carrier(frequency, duration, sampling_rate, vol)
        bcarrier = carrier.tobytes()
        for i in range(len(bcarrier)):
            modulated_signal.append(bcarrier[i])

    return modulated_signal

def make_parity(packet_data):
    res = 0
    for i in range(len(packet_data)):
        res ^= packet_data[i]
    
    return res

def make_packet(bin_data, bodySize=12):
    packet = bytearray()
    for i in range(0, len(bin_data), bodySize):
        packet.append(1)
        packet.append(0)
        packet.append(1)
        packet.append(0)
        for j in range(0, bodySize):
            try:
                packet.append(bin_data[i+j])
            except IndexError:
                packet.append(0)

        packet.append(make_parity(packet[i:i+4+bodySize]))
    return packet





paudio = pyaudio.PyAudio()
vol = 0.2
sr = 48000
duration = 0.7
mark_frequency = 8000  # 1
space_frequency = 12000 # 0

# Read file and convert to binary data
with open('testfile', 'rb') as file:
    content = file.read()

binary_data = np.unpackbits(np.frombuffer(content, dtype=np.uint8))
binary_data = list(make_packet(binary_data))
modulated_signal = modulate_data(binary_data, mark_frequency, space_frequency, sr, duration, vol)

ostream = paudio.open(format=pyaudio.paFloat32, channels=1, rate=sr, output=True)
ostream.write(bytes(modulated_signal))
ostream.close()
paudio.terminate()
