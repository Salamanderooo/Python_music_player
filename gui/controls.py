from PySide6.QtWidgets import QPushButton
from sequencer.sample_player import SamplePlayer

class PlayerControls:
    def __init__(self, parent):
        self.parent = parent

        # przyciski w GUI
        self.play_button = QPushButton("Play", parent)
        self.stop_button = QPushButton("Stop", parent)

        # instancja SamplePlayer
        self.player = SamplePlayer()

        # podłączenie przycisków do metod
        self.play_button.clicked.connect(self.play_clicked)
        self.stop_button.clicked.connect(self.stop_clicked)

    def play_clicked(self):
        # tutaj GUI może później podać wybrany plik
        filename = "assets/bell.wav"  # zmień na swoją ścieżkę
        self.player.play(filename)

    def stop_clicked(self):
        self.player.stop()