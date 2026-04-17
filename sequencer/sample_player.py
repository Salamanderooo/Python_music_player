import wave
import pyaudio
import threading
import time


CHUNK = 1024


class SamplePlayer:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.thread = None
        self.filename = None
        self.stop_flag = False 
        self.lock = threading.Lock()
        self.play_start_time = None
        self.total_frames = 0
        self.sample_rate = 0

    def play(self, filename):
        with self.lock:
            self.stop()
            self.filename = filename
            self.stop_flag = False
            self._play_start_time = None
            self._total_frames = 0
            self._sample_rate = 0

            self.thread = threading.Thread(target=self._run, daemon=True)
            self.thread.start()

    def stop(self):
        self.stop_flag = True

        # daj chwilę na domknięcie write()
        time.sleep(0.02)

    def _run(self):
        wf = None
        stream = None

        try:
            wf = wave.open(self.filename, 'rb')
            self.total_frames = wf.getnframes()
            self.sample_rate = wf.getframerate()

            stream = self.p.open(
                format=self.p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True
            )
            self._play_start_time = time.time()

            data = wf.readframes(CHUNK)
            while data and not self.stop_flag:
                try:
                    stream.write(data)
                except:
                    break
                data = wf.readframes(CHUNK)

        finally:
            # SAFE cleanup
            if stream:
                try:
                    stream.stop_stream()
                    stream.close()
                except:
                    pass

            if wf:
                try:
                    wf.close()
                except:
                    pass
    
    def get_duration(self) -> float:
        
        if self._sample_rate and self._total_frames:
            return self._total_frames / float(self._sample_rate)
        if not self.filename:
            return 0.0
        try:
            with wave.open(self.filename, 'rb') as wf:
                return wf.getnframes() / float(wf.getframerate())
        except:
            return 0.0
        
    def get_position(self) -> float:
        if self._play_start_time is None:
            return 0.0
        elapsed = time.time() - self._play_start_time
        return min(elapsed, self.get_duration())