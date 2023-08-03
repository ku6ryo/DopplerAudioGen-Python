import numpy as np
from pydub import AudioSegment

sample_rate = 48000
audio_length = 6
dt = 1 / sample_rate
N = int(sample_rate * audio_length) # number of samples
max_volume = 20000

y = 10
start_x = 100
source_speed = 300 * 1000 / 3600 
freq = 300
sound_speed = 343

channels = 2

data = []
for i in range(N * channels):
  data.append(0)

for i in range(N):
  x = start_x - source_speed * i * dt
  d = np.sqrt(x**2 + y**2)
  delay = d / sound_speed
  source_speed_for_doppler = source_speed * x / d
  f_doppler = freq * sound_speed / (sound_speed - source_speed_for_doppler)
  j = int(delay / sample_rate) + i
  engine_rotaion_factor = (1 + np.sin(dt * i * 2 * np.pi * 40)) / 2
  volume = 10000 / (d**2) * 1000 * engine_rotaion_factor
  phase = 2 * np.pi * freq * i * dt + 2 * np.pi * f_doppler * delay
  v = volume * np.sin(phase)
  cos = x / d
  if j < N:
    data[2 * j] += v * (1 + cos)
    data[2 * j + 1] += v * (1 - cos)

max_value = np.max(np.abs(data))

for i in range(N * channels):
  data[i] = data[i] / max_value * max_volume

shifted_data = np.int16(data)

shifted_audio = AudioSegment(
    shifted_data.tobytes(),
    frame_rate=sample_rate,
    sample_width=shifted_data.dtype.itemsize,
    channels=channels
)

shifted_audio.export('out.mp3', format="mp3")