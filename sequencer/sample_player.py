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

    def play(self, filename):
        with self.lock:
            self.stop()

            self.filename = filename
            self.stop_flag = False

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

            stream = self.p.open(
                format=self.p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True
            )

            data = wf.readframes(CHUNK)

            while data and not self.stop_flag:
                try:
                    stream.write(data)
                except:
                    break
                data = wf.readframes(CHUNK)

        finally:
            # SAFE cleanup (lokalnie, nie globalnie)
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