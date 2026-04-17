17.04.2025
    1. licznik przeczytanych danych
    frames_read += CHUNK

    2. sample rate
    z WAV:
    wf.getframerate()

    3. wzór czasu
    current_time = frames_read / sample_rate