from PySide6.QtWidgets import QListWidget, QListWidgetItem, QPushButton, QFileDialog, QWidget, QSlider, QLabel
from PySide6.QtCore import Qt, QTimer
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
        # song Progress bar
        self.position_slider = QSlider(Qt.Horizontal, parent)
        self.position_slider.setMinimum(0)
        self.position_slider.setMaximum(1000)
        # timer for actuall song position
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_position)
        self.time_label = QLabel("0:00 / 0:00", parent)
        

        # instation SamplePlayer
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
        self.timer.stop()  # stops the timer 
        self.reset_position()   # resets the position slider to 0
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
            self.player.stop()      # zatrzymaj aktualnie odtwarzany utwór
            self.current_index = index
            self.player.play(self.playlist[self.current_index])
            self.sync_ui()
            self.reset_position()   # snaps slider to 0
            self.timer.start()      # starts the timer to update position slider

    def update_position(self):
        # postion caller every 100ms by timer
        position = self.player.get_position()
        duration = self.player.get_duration()

        if duration > 0:
            # convert to milliseconds and update slider
            self.position_slider.setValue(int(position * 1000))
            self.position_slider.setMaximum(int(duration * 1000))
            self.time_label.setText(f"{self.format_time(position)} / {self.format_time(duration)}")

    def reset_position(self):
        self.position_slider.setValue(0)    

    def format_time(self, seconds):
        seconds = int(seconds)
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}:{secs:02d}" # :02d means "always 2 digits", so 3 becomes 03


        