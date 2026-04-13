from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget
from gui.controls import PlayerControls

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python Music Player")
        layout = QVBoxLayout()
        self.setLayout(layout)
        # widżet do wyświetlania playlisty
        self.playlist_widget = QListWidget()        
        layout.addWidget(self.playlist_widget)
       
        

        # kontrolki odtwarzacza
        self.controls = PlayerControls(self)
        layout.addWidget(self.controls.play_button)
        layout.addWidget(self.controls.stop_button)
        layout.addWidget(self.controls.select_song)
        layout.addWidget(self.controls.next_button)
        layout.addWidget(self.controls.prev_button)
       
