from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget,
    QPushButton, QProgressBar, QFileDialog, QMessageBox
)
from PyQt5.QtCore import QObject, QThread, pyqtSignal

from parser import GPXMLParser

class _Worker(QObject):
    progress = pyqtSignal(int)      # 0..100
    finished = pyqtSignal(list)     # list of chord-names

    def __init__(self, path: str):
        super().__init__()
        self.path = path

    def run(self):
        print(f"DEBUG: Worker.run() for {self.path}")
        parser = GPXMLParser(self.path)
        total = parser.total_harmony or 1
        done = 0
        names = []
        # *** ТОЛЬКО ИЗВЛЕКАЕМ СТРОКИ ИМЕН ***
        for nm in parser.iter_chord_names():
            done += 1
            pct = int(done / total * 100)
            self.progress.emit(pct)
            names.append(nm)
        self.finished.emit(names)

class ParserWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()
        self.thread = None
        self.worker = None
        self._current_path = None

    def _build_ui(self):
        self.btnOpen  = QPushButton("Открыть XML")
        self.lbl      = QLabel("Перетащите файл слева или нажмите Открыть")
        self.pbar     = QProgressBar()
        self.listBox  = QListWidget()
        self.btnSave  = QPushButton("Сохранить лог")
        self.btnSave.setEnabled(False)

        lay = QVBoxLayout(self)
        lay.addWidget(self.btnOpen)
        lay.addWidget(self.lbl)
        lay.addWidget(self.pbar)
        lay.addWidget(self.listBox, 1)
        lay.addWidget(self.btnSave)

        self.btnOpen.clicked.connect(self._on_open)
        self.btnSave.clicked.connect(self._on_save)

    def _on_open(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Открыть XML", "", "XML files (*.xml)"
        )
        if path:
            self.load_file(path)

    def load_file(self, path: str):
        print(f"DEBUG: load_file → {path}")
        self._current_path = path
        self.lbl.setText(f"Парсим: {path}")
        self.pbar.setValue(0)
        self.listBox.clear()
        self.btnSave.setEnabled(False)

        self.thread = QThread(self)
        self.worker = _Worker(path)              # ← храним, чтобы не GC
        self.worker.moveToThread(self.thread)

        self.worker.progress.connect(self.pbar.setValue)
        self.worker.finished.connect(self._on_finished)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def _on_finished(self, names: list[str]):
        print(f"DEBUG: finished → {names}")
        self.lbl.setText(f"Готово. Уникальных: {len(names)}")
        self.listBox.addItems(names)
        self.btnSave.setEnabled(True)

        # ОТРИСОВКА ДИАГРАММ — В GUI-ПОТОКЕ
        parser = GPXMLParser(self._current_path)
        parser.parse()

    def _on_save(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить лог", "chords.txt", "Text (*.txt)"
        )
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            for i in range(self.listBox.count()):
                f.write(self.listBox.item(i).text() + "\n")
        QMessageBox.information(self, "Сохранено")
