import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPixmap
from PyQt5 import uic

from StrumPaint import StrumPaint

from Consts import STRUM_DRAFT_DIR, CELL_STATE_COMBO_BOX_ITEMS


class StrumWidget(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("src/ui/strum_widget.ui", self)

        self.is_copy_mode_active = False
        self.mode_ = 0

        self.painter = StrumPaint()
        self.painter.clear_strum(False)

        self.resetButton.clicked.connect(self.reset_pressed)
        self.submitButton.clicked.connect(self.submit_pressed)

        self.curr_cell = 0

        self.position_01.clicked.connect(lambda: self.select_cell(1))
        self.position_02.clicked.connect(lambda: self.select_cell(2))
        self.position_03.clicked.connect(lambda: self.select_cell(3))
        self.position_04.clicked.connect(lambda: self.select_cell(4))
        self.position_05.clicked.connect(lambda: self.select_cell(5))
        self.position_06.clicked.connect(lambda: self.select_cell(6))
        self.position_07.clicked.connect(lambda: self.select_cell(7))
        self.position_08.clicked.connect(lambda: self.select_cell(8))
        self.position_09.clicked.connect(lambda: self.select_cell(9))
        self.position_10.clicked.connect(lambda: self.select_cell(10))
        self.position_11.clicked.connect(lambda: self.select_cell(11))
        self.position_12.clicked.connect(lambda: self.select_cell(12))
        self.position_13.clicked.connect(lambda: self.select_cell(13))
        self.position_14.clicked.connect(lambda: self.select_cell(14))
        self.position_15.clicked.connect(lambda: self.select_cell(15))
        self.position_16.clicked.connect(lambda: self.select_cell(16))

        self.lineEditChord.textChanged.connect(self.change_cell_chord)
        self.comboBoxCategory.activated.connect(self.change_cell_category)
        
        self.comboBoxState.activated.connect(self.change_arrow_state)
        self.checkBoxAccent.stateChanged.connect(self.change_cell_accent)

        self.radioButtonOption1.clicked.connect(self.change_cell_option)
        self.radioButtonOption2.clicked.connect(self.change_cell_option)
        
        self.radioButtonEmpty.clicked.connect(lambda: self.change_symbol_state(0))
        self.radioButtonHummerOn.clicked.connect(lambda: self.change_symbol_state(1))
        self.radioButtonPullOff.clicked.connect(lambda: self.change_symbol_state(2))

        self.buttonCopy.clicked.connect(self.switch_copy_mode)

        self.lineEditName.textChanged.connect(self.change_arrows_name)

        self.position_01.click()
        self.change_cell_category()
        self.update_edit_menu()

    def update_edit_menu(self):
        self.update_mode((self.painter.get_category(self.curr_cell) + 2) // 3)

        index = self.curr_cell
        self.lineEditChord.setText(self.painter.get_chord(index))
        self.comboBoxCategory.setCurrentIndex(self.painter.get_category(index))  # -> change_cell_category

        if self.mode_ == 0:
            state = self.painter.get_state(index)
            self.radioButtonEmpty.setChecked(state == 0)
            self.radioButtonHummerOn.setChecked(state == 1)
            self.radioButtonPullOff.setChecked(state == 2)
        else:
            self.comboBoxState.setCurrentIndex(self.painter.get_state(index))
            self.checkBoxAccent.setChecked(self.painter.get_accent(index))

            is_down = self.painter.get_option(index)
            self.radioButtonOption1.setChecked(not is_down)
            self.radioButtonOption2.setChecked(is_down)

    def update_mode(self, mode):
        if self.mode_ == mode:
            return

        # moved to change_cell_category
        # self.painter.reset_cell(self.curr_cell)

        if mode != 0:
            # need only in change_cell_category and done in reset_cell
            # self.painter.set_state(self.curr_cell, 0)
            self.comboBoxState.clear()
            self.comboBoxState.addItems(CELL_STATE_COMBO_BOX_ITEMS[mode - 1])

            if mode == 1:
                self.radioButtonOption1.setText("Up")
                self.radioButtonOption2.setText("Down")
            else:
                self.radioButtonOption1.setText("Sn")
                self.radioButtonOption2.setText("Bass")

        if mode == 0 or self.mode_ == 0:
            self.stackedElemMode.setCurrentIndex(mode == 0)

        self.mode_ = mode
        # self.update_edit_menu()

    def copy_cell(self, index):
        self.painter.set_chord(self.curr_cell, self.painter.get_chord(index))
        self.painter.set_category(self.curr_cell, self.painter.get_category(index))
        self.update_mode((self.painter.get_category(self.curr_cell) + 2) // 3)

        self.painter.set_state(self.curr_cell, self.painter.get_state(index))
        self.painter.set_option(self.curr_cell, self.painter.get_option(index))
        self.painter.set_accent(self.curr_cell, self.painter.get_accent(index))
        self.update_edit_menu()

        self.update_visual_display()

    def select_cell(self, index):
        self.lineEditChord.setFocus()

        if self.is_copy_mode_active:
            self.copy_cell(index - 1)
            self.switch_copy_mode()
            return

        exec(f'self.position_{("0" + str(self.curr_cell + 1))[-2:]}.setEnabled(True)')
        exec(f'self.position_{("0" + str(index))[-2:]}.setEnabled(False)')

        self.curr_cell = index - 1
        self.update_edit_menu()

    def change_cell_chord(self):
        new_chord = self.lineEditChord.text()
        self.painter.set_chord(self.curr_cell, new_chord)
        self.update_visual_display()

    def change_cell_category(self):
        new_category = self.comboBoxCategory.currentIndex()
        new_mode = (new_category + 2) // 3
        self.painter.set_category(self.curr_cell, new_category)
        if self.mode_ != new_mode:
            self.painter.reset_cell(self.curr_cell)
            self.update_edit_menu()
        self.update_visual_display()

    def change_arrow_state(self):
        new_state = self.comboBoxState.currentIndex()
        self.painter.set_state(self.curr_cell, new_state)
        self.update_visual_display()
    
    def change_symbol_state(self, index):
        self.painter.set_state(self.curr_cell, index)
        self.update_visual_display()

    def change_cell_accent(self):
        is_checked = self.checkBoxAccent.isChecked()
        self.painter.set_accent(self.curr_cell, int(is_checked))
        self.update_visual_display()

    def change_cell_option(self):
        is_checked = self.radioButtonOption2.isChecked()
        self.painter.set_option(self.curr_cell, int(is_checked))
        self.update_visual_display()

    def switch_copy_mode(self):
        self.is_copy_mode_active = not self.is_copy_mode_active
        self.buttonCopy.setChecked(self.is_copy_mode_active)
        if self.is_copy_mode_active:
            self.position_01.setFocus()

    def submit_pressed(self):
        self.painter.save(True)
        self.painter.save(False)

    def reset_pressed(self):
        self.painter.clear_strum(True)
        self.update_edit_menu()
        self.update_visual_display()

    def change_arrows_name(self, text):
        self.painter.set_global_name(text)

    def update_visual_display(self):
        scene = QGraphicsScene()
        pixmap = QPixmap(STRUM_DRAFT_DIR)
        scene.addPixmap(pixmap)
        self.graphicsView.setScene(scene)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StrumWidget()
    ex.show()
    sys.exit(app.exec_())