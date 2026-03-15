from PySide6.QtWidgets import QPushButton, QFileDialog
from sequencer.sample_player import SamplePlayer


class PlayerControls:
    def __init__(self, parent):
        self.parent = parent
        self.playlist = []
        self.current_index = 0

        # przyciski w GUI
        self.play_button = QPushButton("Play", parent)
        self.stop_button = QPushButton("Stop", parent)
        self.select_song = QPushButton("Select Sample", parent)
        self.next_button = QPushButton("Next", parent)
        self.prev_button = QPushButton("Previous", parent)

        # instancja SamplePlayer
        self.player = SamplePlayer()
        
        # podłączenie przycisków do metod
        self.play_button.clicked.connect(self.play_clicked)
        self.stop_button.clicked.connect(self.stop_clicked)
        self.select_song.clicked.connect(self.open_file_dialog)

    def play_clicked(self):
        if self.playlist:
            self.player.play(self.playlist[self.current_index])

    def stop_clicked(self):
        self.player.stop()

    def open_file_dialog(self):
        filename, _ = QFileDialog.getOpenFileNames(self.parent, "Wybierz plik dźwiękowy", "", "Audio Files (*.wav *.mp3)")
        self.playlist.extend(filename)
        self.current_index = len(self.playlist) - 1
        
        