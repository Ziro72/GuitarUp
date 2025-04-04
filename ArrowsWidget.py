import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPixmap
from PyQt5 import uic

from Arrows_paint import ArrowPaint, Image
from Consts import NAME_ARROW_WIDGET, NAME_COPY_ARROW_WIDGET
from Arrow_class import Arrow


class ArrowsWidget(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("src/arrows_widget.ui", self)

        self.arrows = ArrowPaint()
        self.arrows.clear_all_arrows_copy(NAME_COPY_ARROW_WIDGET)

        self.resetButton.clicked.connect(self.reset_pressed)
        self.submitButton.clicked.connect(self.submit_pressed)

        self.actual_arrow = 0

        self.position_01.clicked.connect(lambda: self.change_actual_arrow(1))
        self.position_02.clicked.connect(lambda: self.change_actual_arrow(2))
        self.position_03.clicked.connect(lambda: self.change_actual_arrow(3))
        self.position_04.clicked.connect(lambda: self.change_actual_arrow(4))
        self.position_05.clicked.connect(lambda: self.change_actual_arrow(5))
        self.position_06.clicked.connect(lambda: self.change_actual_arrow(6))
        self.position_07.clicked.connect(lambda: self.change_actual_arrow(7))
        self.position_08.clicked.connect(lambda: self.change_actual_arrow(8))
        self.position_09.clicked.connect(lambda: self.change_actual_arrow(9))
        self.position_10.clicked.connect(lambda: self.change_actual_arrow(10))
        self.position_11.clicked.connect(lambda: self.change_actual_arrow(11))
        self.position_12.clicked.connect(lambda: self.change_actual_arrow(12))
        self.position_13.clicked.connect(lambda: self.change_actual_arrow(13))
        self.position_14.clicked.connect(lambda: self.change_actual_arrow(14))
        self.position_15.clicked.connect(lambda: self.change_actual_arrow(15))
        self.position_16.clicked.connect(lambda: self.change_actual_arrow(16))

        self.lineEditChord.textChanged.connect(self.arrow_chord_changed)
        self.comboBoxType.currentTextChanged.connect(self.arrow_type_changed)
        self.comboBoxState.currentTextChanged.connect(self.arrow_state_changed)
        self.checkBoxAccent.stateChanged.connect(self.arrow_accent_changed)

        self.radioButtonUp.clicked.connect(self.arrow_direction_changed)
        self.radioButtonDown.clicked.connect(self.arrow_direction_changed)

        self.lineEditName.textChanged.connect(self.arrows_name_changed)

    def update_arrow_menu(self):
        index = self.actual_arrow
        self.lineEditChord.setText(self.arrows.get_name(index))
        self.comboBoxType.setCurrentIndex(self.arrows.get_type(index))
        self.comboBoxState.setCurrentIndex(self.arrows.get_status(index))
        self.checkBoxAccent.setChecked(self.arrows.get_accent(index))

        is_down = self.arrows.get_direction(index)
        self.radioButtonDown.setChecked(is_down)
        self.radioButtonUp.setChecked(not is_down)

    def change_actual_arrow(self, index):
        self.actual_arrow = index - 1
        self.update_arrow_menu()

    def arrow_chord_changed(self):
        new_name = self.lineEditChord.text()
        self.arrows.set_name(self.actual_arrow, new_name)
        self.update_visual_display()

    def arrow_type_changed(self):
        new_type = self.comboBoxType.currentIndex()
        self.arrows.set_type(self.actual_arrow, int(new_type))
        self.update_visual_display()

    def arrow_state_changed(self):
        new_state = self.comboBoxState.currentIndex()
        self.arrows.set_status(self.actual_arrow, int(new_state))
        self.update_visual_display()

    def arrow_accent_changed(self):
        status = self.checkBoxAccent.isChecked()
        self.arrows.set_accent(self.actual_arrow, int(status))
        self.update_visual_display()

    def arrow_direction_changed(self):
        status = self.radioButtonDown.isChecked()
        self.arrows.set_direction(self.actual_arrow, int(status))
        self.update_visual_display()

    def submit_pressed(self):
        self.arrows.draw()

    def reset_pressed(self):
        self.arrows.clear_all_arrows_copy(NAME_COPY_ARROW_WIDGET)
        self.update_arrow_menu()
        self.update_visual_display()

    def arrows_name_changed(self, text):
        self.arrows.set_global_name(text)

    def update_visual_display(self):
        scene = QGraphicsScene()
        pixmap = QPixmap(NAME_ARROW_WIDGET)
        scene.addPixmap(pixmap)
        self.graphicsView.setScene(scene)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ArrowsWidget()
    ex.show()
    app.aboutToQuit.connect(ex.arrows.clear_copy)
    sys.exit(app.exec_())