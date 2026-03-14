import numpy as np
import pyaudio as pa

def generate_sine_wave(frequency, duration, sample_rate, amplitude=1.0):
    formula = 2 * np.pi * frequency * np.arange(sample_rate * duration) / sample_rate
    return amplitude * np.sin(formula)

def play_sound(audio_data, sample_rate):
    p = pa.PyAudio()
    stream = p.open(format=pa.paFloat32, channels=1, rate=sample_rate, output=True)
    stream.write(audio_data.astype(np.float32).tobytes())
    stream.stop_stream()
    stream.close()
    p.terminate()


audio = generate_sine_wave(440, 2, 44100)
play_sound(audio, 44100)