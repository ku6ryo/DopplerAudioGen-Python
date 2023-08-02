import numpy as np
from pydub import AudioSegment

sample_rate = 44100
audio_length = 6
dt = 1 / sample_rate
N = int(sample_rate * audio_length) # number of samples
max_volume = 12000

y = 10
start_x = 100
speed = 200 * 1000 / 3600 
freq = 200
sound_speed = 343

data = []
for i in range(N * 2):
  data.append(0)

for i in range(N):
  x = start_x - speed * i * dt
  d = np.sqrt(x**2 + y**2)
  delay = d / sound_speed
  df = freq * speed * x / d / sound_speed
  f = freq + df
  j = int(delay / sample_rate) + i
  engine_rotaion_factor = (1 + np.sin(dt * i * 2 * np.pi * 40)) / 2
  volume = 10000 / (d**2) * 1000 * engine_rotaion_factor
  v = volume * np.sin(2 * np.pi * f * i * dt)
  cos = x / d
  if j < N:
    data[2 * j] += v * (1 + cos)
    data[2 * j + 1] += v * (1 - cos)

max_value = np.max(np.abs(data))

for i in range(N * 2):
  data[i] = data[i] / max_value * max_volume

shifted_data = np.int16(data)

shifted_audio = AudioSegment(
    shifted_data.tobytes(),
    frame_rate=sample_rate,
    sample_width=shifted_data.dtype.itemsize,
    channels=2
)

shifted_audio.export('out.mp3', format="mp3")