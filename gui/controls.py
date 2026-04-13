from PySide6.QtWidgets import QListWidget, QListWidgetItem, QPushButton, QFileDialog, QWidget
from PySide6.QtCore import Qt
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
        self.next_button.clicked.connect(self.next_clicked)
        self.prev_button.clicked.connect(self.prev_clicked)

    def play_clicked(self):
        if self.current_index < len(self.playlist):
            self.set_current_index(self.current_index)

    def stop_clicked(self):
        self.player.stop()
        self.sync_ui()

    def next_clicked(self):
        if self.playlist:
            self.set_current_index((self.current_index + 1) % len(self.playlist))

    def prev_clicked(self):
        if self.playlist:
            self.set_current_index((self.current_index - 1) % len(self.playlist))

    def open_file_dialog(self):
        filename, _ = QFileDialog.getOpenFileNames(self.parent, "Wybierz plik dźwiękowy", "", "Audio Files (*.wav *.mp3)")
        for file in filename:
            self.add_to_playlist(file)

    def add_to_playlist(self, file):
        self.playlist.append(file)
        self.parent.playlist_widget.addItem(QListWidgetItem(file))
        if len(self.playlist) == 1:  # jeśli to pierwszy dodany utwór, od razu go odtwarzamy
            self.set_current_index(0)
        

    def sync_ui(self):
        self.parent.playlist_widget.setCurrentRow(self.current_index)
        
    def set_current_index(self, index):
        if 0 <= index < len(self.playlist):
            self.player.stop()  # zatrzymaj aktualnie odtwarzany utwór
            self.current_index = index
            self.player.play(self.playlist[self.current_index])
            self.sync_ui()
        