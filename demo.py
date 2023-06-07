import os
import pyaudio
import numpy as np
import time

SYN = "1010"
DURATION = 0.5
VOLUME = 0.3
BODY_SIZE = 12  #bit count for body
paudio = pyaudio.PyAudio()
def play_sound(freq):
    """
      play_sound
      arg : frequency that will be played
      make a sin wave and play it
    """
    vol = VOLUME
    sr = 48000
    duration = DURATION


    samples = (np.sin(2*np.pi * np.arange(sr * duration) * freq/sr)).astype(np.float32)

    ostream = paudio.open(format=pyaudio.paFloat32, channels=1, rate=sr, output=True)
    start_time = time.time()
    ostream.write((vol*samples))
    print("Played {:} for {:.2f} seconds".format(freq, time.time() - start_time))
    ostream.close()
    

def modulate_packet(packet):
    """
      modulate_packet
      arg : packet
      read packet and turn it to specific frequency
    """
    for i in range(len(packet)):
        if packet[i] == '1':
            play_sound(19056)
        elif packet[i] == '0'   :
            play_sound(19059)

def calculate_parity_bit(packet):
    """
      calculate_parity_bit
      arg : packet
      xor all the bit in the binary and returns it
    """
    pb = 0
    for i in range(len(packet)):
        if packet[i] == '1':
            pb ^ 1
        elif packet[i] == '0':
            pb ^ 0
    return pb


def make_packet(body):
  """
    make_packet
     arg : body of the packet
     make a packet by concating preamble(SYN) and body and parity bit
  """
  if(len(body) > 12):
      return 0
  parity_bit = calculate_parity_bit(body)
  packet = SYN + body + str(parity_bit)
  return packet

def read_file_and_make_sound(files):
  """
    read_file_and_make_sound
    arg : list of names of files
    open, read and expose the files given
  """
  for file in files:
     with open(file, "rb") as fp:
          body = ""
          while True:
              byte = fp.read(1)

              if not byte:
                  break
              body += bin(int.from_bytes(byte, byteorder='big'))[2:]
          for offset in range(0, len(body) // BODY_SIZE):

              packet = make_packet(body[offset*12:offset*12+12])
              if not packet:
                  print("ERROR")
                  break
              modulate_packet(packet)

if __name__ == "__main__":
    directory = ''  #Directory to the folder you want to expose
    files = []
    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)):
            if file == 'testfile':  #for test purpose
                files.append(file)


    print(files)
    read_file_and_make_sound(files)
    paudio.terminate()
