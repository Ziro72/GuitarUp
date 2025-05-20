import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPixmap
from PyQt5 import uic

from TabPaint import TabPaint

from Consts import DEFAULT_NAME_FINALE_TABLATURES_IMAGE


class TabWidget(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("src/tab_widget.ui", self)

        self.tabs = TabPaint()
        self.tabs.clear_all_finale_image(DEFAULT_NAME_FINALE_TABLATURES_IMAGE, False)

        self.resetButton.clicked.connect(self.reset_pressed)
        self.submitButton.clicked.connect(self.submit_pressed)

        self.actual_row = 0

        self.position_01.clicked.connect(lambda: self.change_actual_row(1))
        self.position_02.clicked.connect(lambda: self.change_actual_row(2))
        self.position_03.clicked.connect(lambda: self.change_actual_row(3))
        self.position_04.clicked.connect(lambda: self.change_actual_row(4))
        self.position_05.clicked.connect(lambda: self.change_actual_row(5))
        self.position_06.clicked.connect(lambda: self.change_actual_row(6))
        self.position_07.clicked.connect(lambda: self.change_actual_row(7))
        self.position_08.clicked.connect(lambda: self.change_actual_row(8))
        self.position_09.clicked.connect(lambda: self.change_actual_row(9))
        self.position_10.clicked.connect(lambda: self.change_actual_row(10))
        self.position_11.clicked.connect(lambda: self.change_actual_row(11))
        self.position_12.clicked.connect(lambda: self.change_actual_row(12))
        self.position_13.clicked.connect(lambda: self.change_actual_row(13))
        self.position_14.clicked.connect(lambda: self.change_actual_row(14))
        self.position_15.clicked.connect(lambda: self.change_actual_row(15))
        self.position_16.clicked.connect(lambda: self.change_actual_row(16))

        self.lineEditChord.textChanged.connect(self.tab_chord_changed)

        self.lineEditString_1.textChanged.connect(lambda: self.string_status_changed(1))
        self.lineEditString_2.textChanged.connect(lambda: self.string_status_changed(2))
        self.lineEditString_3.textChanged.connect(lambda: self.string_status_changed(3))
        self.lineEditString_4.textChanged.connect(lambda: self.string_status_changed(4))
        self.lineEditString_5.textChanged.connect(lambda: self.string_status_changed(5))
        self.lineEditString_6.textChanged.connect(lambda: self.string_status_changed(6))

        self.lineEditName.textChanged.connect(self.tabs_name_changed)
        self.refresh_global_name_input()

    def update_tab_menu(self):
        index = self.actual_row
        self.lineEditString_1.textChanged.connect(lambda: self.tabs.get_cell_status((index, 0)))
        self.lineEditString_2.textChanged.connect(lambda: self.tabs.get_cell_status((index, 1)))
        self.lineEditString_3.textChanged.connect(lambda: self.tabs.get_cell_status((index, 2)))
        self.lineEditString_4.textChanged.connect(lambda: self.tabs.get_cell_status((index, 3)))
        self.lineEditString_5.textChanged.connect(lambda: self.tabs.get_cell_status((index, 4)))
        self.lineEditString_6.textChanged.connect(lambda: self.tabs.get_cell_status((index, 5)))
        self.lineEditChord.textChanged.connect(lambda: self.tabs.get_position_name(index))

    def change_actual_row(self, index):
        self.actual_row = index - 1
        self.update_tab_menu()
        self.refresh_string_inputs()
        self.refresh_chord_input()

    def refresh_chord_input(self):
        name = self.tabs.get_position_name(self.actual_row)
        self.lineEditChord.blockSignals(True)
        self.lineEditChord.setText(str(name))
        self.lineEditChord.blockSignals(False)

    def refresh_string_inputs(self):
        for string_idx in range(6):
            val = self.tabs.get_cell_status((self.actual_row, string_idx))
            le: QtWidgets.QLineEdit = getattr(self, f"lineEditString_{string_idx + 1}")
            le.blockSignals(True)
            le.setText(str(val))
            le.blockSignals(False)

    def refresh_global_name_input(self):
        global_name = self.tabs.get_global_name()
        self.lineEditName.blockSignals(True)
        self.lineEditName.setText(str(global_name))
        self.lineEditName.blockSignals(False)

    def tab_chord_changed(self):
        new_name = self.lineEditChord.text()
        self.tabs.set_cell_status(self.actual_row, new_name)
        self.update_visual_display()

    def string_status_changed(self, index):
        string = eval(f"self.lineEditString_{index}")
        new_element = string.text()
        self.tabs.update_tablatures_position((self.actual_row, index - 1), new_element)
        self.update_visual_display()

    def submit_pressed(self):
        self.tabs.save()

    def reset_pressed(self):
        self.tabs.clear_all_tablatures(DEFAULT_NAME_FINALE_TABLATURES_IMAGE, True)
        self.refresh_global_name_input()
        self.update_tab_menu()
        self.update_visual_display()

    def tabs_name_changed(self, new_name):
        self.tabs.set_global_name(new_name)

    def update_visual_display(self):
        scene = QGraphicsScene()
        pixmap = QPixmap(DEFAULT_NAME_FINALE_TABLATURES_IMAGE)
        scene.addPixmap(pixmap)
        self.graphicsView.setScene(scene)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TabWidget()
    ex.show()
    sys.exit(app.exec_())