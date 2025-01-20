import sys

import subprocess
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QVBoxLayout
from ArrowsWidget import *

from ArrowsWidget import ArrowsWidget
from ChordWidget import ChordWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("src/main_page.ui", self)

        self.chordButton.clicked.connect(self.chord_pressed)
        self.arrowsButton.clicked.connect(self.arrows_pressed)

    def chord_pressed(self, ind):
        self.chord_window = ChordWidget()  # Создаем экземпляр второго окна
        self.chord_window.show()  # Показываем второе окно
        # self.close()

    def arrows_pressed(self):
        self.arrows_window = ArrowsWidget()  # Создаем экземпляр второго окна
        self.arrows_window.show()  # Показываем второе окно
        # self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())

