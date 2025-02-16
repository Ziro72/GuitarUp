import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPixmap
from PyQt5 import uic


from Chord import Chord
from Finger import Finger
from Consts import *


class ChordWidget(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("../src/chord_widget.ui", self)

        self.chord = Chord()

        self.resetButton.clicked.connect(self.reset_pressed)
        self.submitButton.clicked.connect(self.submit_pressed)

        self.chooseBarre.currentTextChanged.connect(lambda: self.choose_barre_text_changed())

        self.chooseFret1.currentTextChanged.connect(lambda: self.choose_fret_text_changed(1))
        self.chooseString1.currentTextChanged.connect(lambda: self.choose_string_text_changed(1))

        self.chooseFret2.currentTextChanged.connect(lambda: self.choose_fret_text_changed(2))
        self.chooseString2.currentTextChanged.connect(lambda: self.choose_string_text_changed(2))

        self.chooseFret3.currentTextChanged.connect(lambda: self.choose_fret_text_changed(3))
        self.chooseString3.currentTextChanged.connect(lambda: self.choose_string_text_changed(3))

        self.chooseFret4.currentTextChanged.connect(lambda: self.choose_fret_text_changed(4))
        self.chooseString4.currentTextChanged.connect(lambda: self.choose_string_text_changed(4))

        self.chooseFret5.currentTextChanged.connect(lambda: self.choose_fret_text_changed(5))
        self.chooseString5.currentTextChanged.connect(lambda: self.choose_string_text_changed(5))

        self.CBString1.stateChanged.connect(lambda: self.string_status_changed(1))
        self.CBString2.stateChanged.connect(lambda: self.string_status_changed(2))
        self.CBString3.stateChanged.connect(lambda: self.string_status_changed(3))
        self.CBString4.stateChanged.connect(lambda: self.string_status_changed(4))
        self.CBString5.stateChanged.connect(lambda: self.string_status_changed(5))
        self.CBString6.stateChanged.connect(lambda: self.string_status_changed(6))

        self.chordName.textChanged.connect(self.chord_name_changed)
        self.startFret.textChanged.connect(self.start_fret_changed)

        self.active1.toggled.connect(lambda: self.change_enable_of_states(1))
        self.active2.toggled.connect(lambda: self.change_enable_of_states(2))
        self.active3.toggled.connect(lambda: self.change_enable_of_states(3))
        self.active4.toggled.connect(lambda: self.change_enable_of_states(4))
        self.active5.toggled.connect(lambda: self.change_enable_of_states(5))
        self.update_visual_display()

    def change_enable_of_states(self, ind):
        ch_strings = eval(f"self.chooseString{ind}")
        ch_frets = eval(f"self.chooseFret{ind}")

        ch_strings.setEnabled(not ch_strings.isEnabled())
        ch_frets.setEnabled(not ch_frets.isEnabled())

        if ind == 1:
            self.chooseBarre.setEnabled(not self.chooseBarre.isEnabled())

        if not ch_strings.isEnabled():
            ch_strings.setCurrentIndex(0)
            ch_frets.setCurrentIndex(0)
            if ind == 1:
                self.chooseBarre.setCurrentIndex(0)

    def reset_pressed(self):
        self.CBString1.setChecked(False)
        self.CBString2.setChecked(False)
        self.CBString3.setChecked(False)
        self.CBString4.setChecked(False)
        self.CBString5.setChecked(False)
        self.CBString6.setChecked(False)

        self.active1.setChecked(False)
        self.active2.setChecked(False)
        self.active3.setChecked(False)
        self.active4.setChecked(False)
        self.active5.setChecked(False)

        self.update_visual_display()

    def chord_name_changed(self, text):
        self.chord.change_name(text)
        self.update_visual_display()

    def start_fret_changed(self, text):
        self.chord.change_start_fret(text)
        self.update_visual_display()

    def submit_pressed(self):
        self.chord.save_chord()

    def string_status_changed(self, ind):
        label = eval(f"self.stringState{ind}")
        self.chord.change_string_state(ind - 1)
        # QtWidgets.QLabel.setText(self.chord.str_states[ind - 1])
        label.setText(self.chord.str_states[ind - 1])
        self.update_visual_display()

    def update_strings(self):
        self.chord.update_strings()
        for i in range(6):
            label = eval(f"self.stringState{i + 1}")
            label.setText(self.chord.str_states[i])
        self.update_visual_display()

    def update_barre_access(self, string):
        lst = [str(i) for i in range(7 - string)]
        model = QtCore.QStringListModel(lst)
        self.chooseBarre.setModel(model)

    def choose_string_text_changed(self, ind):
        widget = eval(f"self.chooseString{ind}")
        text = widget.currentText()

        finger: Finger = self.chord.finger(ind - 1)
        finger.edit_string(int(text))

        if ind == 1:
            self.update_barre_access(int(text))
        self.update_strings()

    def choose_fret_text_changed(self, ind):
        widget = eval(f"self.chooseFret{ind}")
        text = widget.currentText()

        finger: Finger = self.chord.finger(ind - 1)
        finger.edit_fret(int(text))

        self.update_strings()

    def choose_barre_text_changed(self):
        widget = self.chooseBarre
        text = widget.currentText()

        self.chord.edit_barre(int(text))
        self.update_strings()

    def update_visual_display(self):
        scene = QGraphicsScene()
        pixmap = QPixmap("./src/tmp/chord.png")
        width, height = DISPLAY_SIZE
        pixmap = pixmap.scaled(width, height)
        scene.addPixmap(pixmap)
        self.graphicsView.setScene(scene)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ChordWidget()
    ex.show()
    sys.exit(app.exec_())
