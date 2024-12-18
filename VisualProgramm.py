import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
from Chord import Chord
from Finger import Finger


class Widget(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("src/main_page.ui", self)

        self.chord = Chord()

        self.resetButton.clicked.connect(self.resetPressed)
        self.submitButton.clicked.connect(self.submitPressed)

        fingers_settings_gbs = list(self.fingersSettings.children())
        fingers_settings_gbs.sort(key=lambda x: x.objectName())

        self.chooseBarre1.currentTextChanged.connect(lambda: self.chooseBarreTextChanged(1))
        self.chooseFret1.currentTextChanged.connect(lambda: self.chooseFretTextChanged(1))
        self.chooseString1.currentTextChanged.connect(lambda: self.chooseStringTextChanged(1))

        self.chooseBarre2.currentTextChanged.connect(lambda: self.chooseBarreTextChanged(2))
        self.chooseFret2.currentTextChanged.connect(lambda: self.chooseFretTextChanged(2))
        self.chooseString2.currentTextChanged.connect(lambda: self.chooseStringTextChanged(2))

        self.chooseBarre3.currentTextChanged.connect(lambda: self.chooseBarreTextChanged(3))
        self.chooseFret3.currentTextChanged.connect(lambda: self.chooseFretTextChanged(3))
        self.chooseString3.currentTextChanged.connect(lambda: self.chooseStringTextChanged(3))

        self.chooseBarre4.currentTextChanged.connect(lambda: self.chooseBarreTextChanged(4))
        self.chooseFret4.currentTextChanged.connect(lambda: self.chooseFretTextChanged(4))
        self.chooseString4.currentTextChanged.connect(lambda: self.chooseStringTextChanged(4))

        self.chooseBarre5.currentTextChanged.connect(lambda: self.chooseBarreTextChanged(5))
        self.chooseFret5.currentTextChanged.connect(lambda: self.chooseFretTextChanged(5))
        self.chooseString5.currentTextChanged.connect(lambda: self.chooseStringTextChanged(5))

        self.CBString1.stateChanged.connect(lambda: self.stringStatusChanged(1))
        self.CBString2.stateChanged.connect(lambda: self.stringStatusChanged(2))
        self.CBString3.stateChanged.connect(lambda: self.stringStatusChanged(3))
        self.CBString4.stateChanged.connect(lambda: self.stringStatusChanged(4))
        self.CBString5.stateChanged.connect(lambda: self.stringStatusChanged(5))
        self.CBString6.stateChanged.connect(lambda: self.stringStatusChanged(6))

        self.chordName.textChanged.connect(self.chordNameChanged)
        self.startFret.textChanged.connect(self.startFretChanged)

        self.active1.toggled.connect(lambda: self.changeEnableOfStates(1))
        self.active2.toggled.connect(lambda: self.changeEnableOfStates(2))
        self.active3.toggled.connect(lambda: self.changeEnableOfStates(3))
        self.active4.toggled.connect(lambda: self.changeEnableOfStates(4))
        self.active5.toggled.connect(lambda: self.changeEnableOfStates(5))

        self.chord = Chord()

    def changeEnableOfStates(self, ind):
        chS = eval(f"self.chooseString{ind}")
        chF = eval(f"self.chooseFret{ind}")
        chBL = eval(f"self.chooseBarre{ind}")

        chS.setEnabled(not chS.isEnabled())
        chF.setEnabled(not chF.isEnabled())
        chBL.setEnabled(not chBL.isEnabled())

        if not chS.isEnabled():
            chS.setCurrentIndex(0)
            chF.setCurrentIndex(0)
            chBL.setCurrentIndex(0)

    def resetPressed(self):
        self.CBString1.setChecked(False)
        self.CBString2.setChecked(False)
        self.CBString3.setChecked(False)
        self.CBString4.setChecked(False)
        self.CBString5.setChecked(False)
        self.CBString6.setChecked(False)

        self.chooseString1.setCurrentIndex(0)
        self.chooseString2.setCurrentIndex(0)
        self.chooseString3.setCurrentIndex(0)
        self.chooseString4.setCurrentIndex(0)
        self.chooseString5.setCurrentIndex(0)

        self.chooseFret1.setCurrentIndex(0)
        self.chooseFret2.setCurrentIndex(0)
        self.chooseFret3.setCurrentIndex(0)
        self.chooseFret4.setCurrentIndex(0)
        self.chooseFret5.setCurrentIndex(0)

        self.chooseBarre1.setCurrentIndex(0)
        self.chooseBarre2.setCurrentIndex(0)
        self.chooseBarre3.setCurrentIndex(0)
        self.chooseBarre4.setCurrentIndex(0)
        self.chooseBarre5.setCurrentIndex(0)

    def chordNameChanged(self, text):
        self.chord.change_name(text)

    def startFretChanged(self, text):
        self.chord.change_start_fret(text)

    def submitPressed(self):
        self.chord.draw_chord()

    def stringStatusChanged(self, ind):
        label = eval(f"self.stringState{ind}")
        self.chord.change_string_state(ind - 1)
        # QtWidgets.QLabel.setText(self.chord.str_states[ind - 1])
        label.setText(self.chord.str_states[ind - 1])

    def updateStrings(self):
        self.chord.update_strings()
        for i in range(6):
            label = eval(f"self.stringState{i + 1}")
            label.setText(self.chord.str_states[i])

    def chooseStringTextChanged(self, ind):
        widget = eval(f"self.chooseString{ind}")
        text = widget.currentText()

        finger: Finger = self.chord.finger(ind - 1)
        finger.edit_string(int(text))

        self.updateStrings()

    def chooseFretTextChanged(self, ind):
        widget = eval(f"self.chooseFret{ind}")
        text = widget.currentText()

        finger: Finger = self.chord.finger(ind - 1)
        finger.edit_fret(int(text))

        self.updateStrings()

    def chooseBarreTextChanged(self, ind):
        widget = eval(f"self.chooseBarre{ind}")
        text = widget.currentText()

        finger: Finger = self.chord.finger(ind - 1)
        finger.edit_barre_length(int(text))

        self.updateStrings()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Widget()
    ex.show()
    sys.exit(app.exec_())
