from PySide6.QtWidgets import QWidget, QVBoxLayout
from gui.controls import PlayerControls

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python Music Player")
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.controls = PlayerControls(self)
        layout.addWidget(self.controls.play_button)
        layout.addWidget(self.controls.stop_button)