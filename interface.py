from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

from defs import items
from defs import currencies
from defs import id_to_char


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.button_is_checked = True
        
        self.setWindowTitle("Steam USD|Price parser")
        self.setMinimumSize(1200, 800)
        self.setMaximumSize(1920, 1080)

        self.button = QPushButton("Press me bitch.")
        self.button.setCheckable(True)
        self.button.clicked.connect(self.the_button_was_clicked)

        self.setCentralWidget(self.button)

    def the_button_was_clicked(self):
        self.button.setText("You already clicked me")
        self.button.setEnabled(False)


app = QApplication ([])

window = MainWindow ()
window.show ()

app.exec ()