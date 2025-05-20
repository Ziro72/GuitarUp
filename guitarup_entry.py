import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget,
    QWidget, QHBoxLayout, QSizePolicy
)
from PyQt5.QtCore import Qt
from filedrop_widget import FileDropWidget
from parser_widget import ParserWidget
from ChordWidget import ChordWidget
from ArrowsWidget import ArrowsWidget
from ТabWidget import TabWidget


class ParserTab(QWidget):
    """Вкладка «Парсер GP-XML»: слева зона дропа, справа сам ParserWidget."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.drop = FileDropWidget()
        self.parser = ParserWidget()

        for w in (self.drop, self.parser):
            w.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.drop.fileLoaded.connect(self.parser.load_file)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.drop, 1)
        layout.addWidget(self.parser, 2)


class GuitarUpMainWindow(QMainWindow):
    """Главное окно приложения GuitarUp с тремя вкладками."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("GuitarUp")

        # создаём QTabWidget
        self.tabs = QTabWidget()
        parser_tab = ParserTab()
        chord_tab = ChordWidget()
        arrows_tab = ArrowsWidget()
        tablatures_tab = TabWidget()

        for w in (parser_tab, chord_tab, arrows_tab, tablatures_tab):
            w.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.tabs.addTab(parser_tab, "Парсер GP-XML")
        self.tabs.addTab(chord_tab, "Редактор аккордов")
        self.tabs.addTab(arrows_tab, "Редактор стрелок")
        self.tabs.addTab(tablatures_tab, "Редактор табулатур")

        self.tabs.currentChanged.connect(self._on_tab_changed)

        self.setCentralWidget(self.tabs)

        # сразу подстроим окно под первую вкладку
        self._on_tab_changed(0)

    def _on_tab_changed(self, index: int):
        # 1) размер содержимого вкладки
        page = self.tabs.widget(index)
        page_hint = page.sizeHint()

        # 2) таббар сверху
        tabbar = self.tabs.tabBar()
        tabbar_h = tabbar.sizeHint().height()

        # 3) внутренние отступы QTabWidget
        m = self.tabs.contentsMargins()
        widget_w = page_hint.width() + m.left() + m.right()
        widget_h = page_hint.height() + tabbar_h + m.top() + m.bottom()

        # 4) рамки/декорации окна
        win_frame = self.frameGeometry()
        win_geom = self.geometry()
        delta_w = win_frame.width() - win_geom.width()
        delta_h = win_frame.height() - win_geom.height()

        # 5) итоговый размер окна
        new_w = widget_w + delta_w
        new_h = widget_h + delta_h

        self.resize(new_w, new_h)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = GuitarUpMainWindow()
    win.show()
    sys.exit(app.exec_())