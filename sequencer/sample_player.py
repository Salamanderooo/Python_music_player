import wave
import pyaudio
from PySide6.QtCore import QThread, Signal

CHUNK = 1024

class SamplePlayer(QThread):
    finished = Signal()

    def __init__(self):
        super().__init__()
        self.filename = None
        self.stop_flag =False

    def play(self, filename):
        self.filename = filename
        self.stop_flag = False
        if not self.isRunning():
            self.start()

    def run(self):
        wf = wave.open(self.filename, 'rb')
        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        
        data = wf.readframes(CHUNK)
        while data and not self.stop_flag:
            stream.write(data)
            data = wf.readframes(CHUNK) 

        stream.close()
        p.terminate()
        wf.close()
        self.finished.emit()

    def stop(self):
        self.stop_flag = True        