from PySide6.QtWidgets import QPushButton, QFileDialog
from sequencer.sample_player import SamplePlayer

class PlayerControls:
    def __init__(self, parent):
        self.parent = parent

        # przyciski w GUI
        self.play_button = QPushButton("Play", parent)
        self.stop_button = QPushButton("Stop", parent)
        self.select_song = QPushButton("Select Sample", parent)

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

    def open_file_dialog(self, parent):
        self.select_song.clicked.connect(self.open_file_dialog)
        filename, _ = QFileDialog.getOpenFileName(parent, "Wybierz plik dźwiękowy", "", "Audio Files (*.wav *.mp3)")
        if filename:
            self.player.play(filename)
