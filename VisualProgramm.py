import sys
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

        self.string1.currentTextChanged.connect(lambda: self.stringTextChanged(1))
        self.string2.currentTextChanged.connect(lambda: self.stringTextChanged(2))
        self.string3.currentTextChanged.connect(lambda: self.stringTextChanged(3))
        self.string4.currentTextChanged.connect(lambda: self.stringTextChanged(4))
        self.string5.currentTextChanged.connect(lambda: self.stringTextChanged(5))
        self.string6.currentTextChanged.connect(lambda: self.stringTextChanged(6))

        self.chooseString1.currentTextChanged.connect(lambda: self.chooseStringTextChanged(1))
        self.chooseString2.currentTextChanged.connect(lambda: self.chooseStringTextChanged(2))
        self.chooseString3.currentTextChanged.connect(lambda: self.chooseStringTextChanged(3))
        self.chooseString4.currentTextChanged.connect(lambda: self.chooseStringTextChanged(4))
        self.chooseString5.currentTextChanged.connect(lambda: self.chooseStringTextChanged(5))

        self.chooseFret1.currentTextChanged.connect(lambda: self.chooseFretTextChanged(1))
        self.chooseFret2.currentTextChanged.connect(lambda: self.chooseFretTextChanged(2))
        self.chooseFret3.currentTextChanged.connect(lambda: self.chooseFretTextChanged(3))
        self.chooseFret4.currentTextChanged.connect(lambda: self.chooseFretTextChanged(4))
        self.chooseFret5.currentTextChanged.connect(lambda: self.chooseFretTextChanged(5))

        self.chooseBarreLen1.currentTextChanged.connect(lambda: self.chooseBarreLenTextChanged(1))
        self.chooseBarreLen2.currentTextChanged.connect(lambda: self.chooseBarreLenTextChanged(2))
        self.chooseBarreLen3.currentTextChanged.connect(lambda: self.chooseBarreLenTextChanged(3))
        self.chooseBarreLen4.currentTextChanged.connect(lambda: self.chooseBarreLenTextChanged(4))
        self.chooseBarreLen5.currentTextChanged.connect(lambda: self.chooseBarreLenTextChanged(5))

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
        chBL = eval(f"self.chooseBarreLen{ind}")

        chS.setEnabled(not chS.isEnabled())
        chF.setEnabled(not chF.isEnabled())
        chBL.setEnabled(not chBL.isEnabled())

        if not chS.isEnabled():
            chS.setCurrentIndex(0)
            chF.setCurrentIndex(0)
            chBL.setCurrentIndex(0)

    def resetPressed(self):
        self.string1.setCurrentIndex(0)
        self.string2.setCurrentIndex(0)
        self.string3.setCurrentIndex(0)
        self.string4.setCurrentIndex(0)
        self.string5.setCurrentIndex(0)
        self.string6.setCurrentIndex(0)

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

        self.chooseBarreLen1.setCurrentIndex(0)
        self.chooseBarreLen2.setCurrentIndex(0)
        self.chooseBarreLen3.setCurrentIndex(0)
        self.chooseBarreLen4.setCurrentIndex(0)
        self.chooseBarreLen5.setCurrentIndex(0)

    def chordNameChanged(self, text):
        self.chord.change_name(text)

    def startFretChanged(self, text):
        self.chord.change_start_fret(text)

    def submitPressed(self):
        self.chord.draw_chord()

    def stringTextChanged(self, ind):
        widget = eval(f"self.string{ind}")
        text = str(widget.currentText())
        self.chord.assign_string(ind - 1, text.upper())
        # if text == "Pinched":
        #     pass
        # elif text == "Muted":
        #     pass

    def chooseStringTextChanged(self, ind):
        widget = eval(f"self.chooseString{ind}")
        text = widget.currentText()

        finger: Finger = self.chord.finger(ind - 1)
        finger.edit_string(int(text))

    def chooseFretTextChanged(self, ind):
        widget = eval(f"self.chooseFret{ind}")
        text = widget.currentText()

        finger: Finger = self.chord.finger(ind - 1)
        finger.edit_fret(int(text))

    def chooseBarreLenTextChanged(self, ind):
        widget = eval(f"self.chooseBarreLen{ind}")
        text = widget.currentText()

        finger: Finger = self.chord.finger(ind - 1)
        finger.edit_barre_length(int(text))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Widget()
    ex.show()
    sys.exit(app.exec_())
