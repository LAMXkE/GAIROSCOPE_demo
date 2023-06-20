import pyaudio
import numpy as np
from datetime import datetime
from pytz import timezone
import json
import time

def generate_carrier(frequency, duration, sampling_rate, vol):
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    samples = np.sin(2 * np.pi * frequency * t).astype(np.float32)
    return (samples*vol)


def modulate_data(binary_data, mark_frequency, space_frequency, sampling_rate, duration, vol):
    # carrier = generate_carrier(mark_frequency, duration, sampling_rate, vol)
    modulated_signals = []
    for packet in binary_data:
        modulated_signal = np.array([])
        for i, bit in enumerate(packet):
            frequency = mark_frequency if bit == 1 else space_frequency
            carrier = generate_carrier(frequency, duration, sampling_rate, vol)
            bcarrier = carrier.tobytes()
        
            modulated_signal = np.append(modulated_signal, bcarrier)
        modulated_signals.append(modulated_signal)

    return modulated_signals

def make_parity(packet_data):
    res = 0
    for bit in packet_data:
        if bit == 1:
            res += 1
    
    if res % 2 == 0:
        return 0
    else:
        return 1

def make_packet(bin_data, bodySize=16):
    packets = []
    for i in range(0, len(bin_data), bodySize):
        packet = []
        packet.append(1)
        packet.append(0)
        packet.append(1)
        packet.append(0)
        for j in range(0, bodySize):
            try:
                packet.append(bin_data[i+j])
            except IndexError:
                packet.append(0)
        packet.append(make_parity(packet[0:bodySize+5]))
        packets.append(list(packet))
    return packets

def play_sound(packet, mark_frequency, space_frequency, sampling_rate, duration, vol):
    for i in range(len(packet)):
        if packet[i] == 0:
            ostream = paudio.open(format=pyaudio.paFloat32, channels=1, rate=sr, output=True)
            carrier = generate_carrier(space_frequency, duration, 48000, 0.3)
            ostream.write(carrier.tobytes())
            ostream.close()
        else:
            ostream = paudio.open(format=pyaudio.paFloat32, channels=1, rate=sr, output=True)
            carrier = generate_carrier(mark_frequency, duration, 48000, 0.3)
            ostream.write(carrier.tobytes())
            ostream.close()

def test_resonance():
    hzfile = open('./timetable', 'w')
    times = {}
    for i in range(20100, 20200, 10):
        print(datetime.now(timezone('Asia/Seoul')).strftime('%s'), i)
        times[datetime.now(timezone('Asia/Seoul')).strftime('%s')] = i
        ostream = paudio.open(format=pyaudio.paFloat32, channels=1, rate=sr, output=True)
        carrier = generate_carrier(i, 2, 48000, 0.3)
        ostream.write(carrier.tobytes())
        ostream.close()
    
    hzfile.write(json.dumps(times))
    hzfile.close()



paudio = pyaudio.PyAudio()
vol = 0.5
sr = 48000
duration = 0.625
mark_frequency = 20150  # 1
space_frequency = 20400 # 0

# Read file and convert to binary data
with open('testfile', 'rb') as file:
    content = file.read()
binary_data = np.unpackbits(np.frombuffer(content, dtype=np.uint8))
#binary_data = [0,0,1,0,1,1,0,0,1,1,0,0,1,1,0,0]
#binary_data = [1, 1,1,1,1,1,1,1,1,1]
binary_data = list(make_packet(binary_data, 8))
#test_resonance() 

# Uncomment to play the sound
print(binary_data)
# for packet in binary_data:  
#     play_sound(packet, mark_frequency, space_frequency, sr, duration, vol)
#     time.sleep(2)
#binary_data = [[1,0,1,0,1,1,1,1]]
modulated_signals = modulate_data(binary_data, mark_frequency, space_frequency, sr, duration, vol)
#print(modulated_signal.tobytes())
for modulated_signal in modulated_signals:
    time.sleep(1.5)
    ostream = paudio.open(format=pyaudio.paFloat32, channels=1, rate=sr, output=True)
    ostream.write(modulated_signal.tobytes())
    ostream.close()
    
paudio.terminate()
