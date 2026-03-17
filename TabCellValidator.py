from PyQt5.QtWidgets import QApplication, QLineEdit, QWidget, QVBoxLayout
from PyQt5.QtGui import QValidator


class TabCellValidator(QValidator):
    def validate(self, input_text, pos):
        if input_text == '':
            return (QValidator.Intermediate, input_text, pos)

        if input_text in ('x', '-'):
            return (QValidator.Acceptable, input_text, pos)

        if not input_text.isdigit():
            return (QValidator.Invalid, input_text, pos)

        num = int(input_text)
        length = len(input_text)

        if (length == len(str(num))) and (0 <= num <= 25):
            return (QValidator.Acceptable, input_text, pos)

        return (QValidator.Invalid, input_text, pos)


class InputWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setValidator(TabCellValidator())
        layout.addWidget(self.input_field)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication([])
    window = InputWidget()
    window.show()
    app.exec_()