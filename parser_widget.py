from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget,
    QPushButton, QProgressBar, QFileDialog, QMessageBox
)
from PyQt5.QtCore import QObject, QThread, pyqtSignal

from parser import GPXMLParser

class _Worker(QObject):
    progress = pyqtSignal(int)         # 0..100
    finished = pyqtSignal(list)        # список имён

    def __init__(self, path:str):
        super().__init__()
        self.path = path

    def run(self):
        parser = GPXMLParser(self.path)
        total = parser.total_harmony or 1
        done = 0
        names = []
        for nm in parser.iter_chord_names():
            done += 1
            pct = int(done/total*100)
            self.progress.emit(pct)
            names.append(nm)
        self.finished.emit(names)

class ParserWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._ui()
        self.thread = None

    def _ui(self):
        self.lbl    = QLabel("Перетащите файл…")
        self.pbar   = QProgressBar()
        self.list   = QListWidget()
        self.btnOpen= QPushButton("Открыть XML")
        self.btnSave= QPushButton("Сохранить лог")
        self.btnSave.setEnabled(False)

        v=QVBoxLayout(self)
        v.addWidget(self.btnOpen)
        v.addWidget(self.lbl)
        v.addWidget(self.pbar)
        v.addWidget(self.list,1)
        v.addWidget(self.btnSave)

        self.btnOpen.clicked.connect(self._open)
        self.btnSave.clicked.connect(self._save)

    def _open(self):
        path,_ = QFileDialog.getOpenFileName(self,"Открыть XML","","XML (*.xml)")
        if path:
            self.load_file(path)

    def load_file(self,path:str):
        print("DEBUG: load_file",path)
        self.lbl.setText(f"Парсим: {path}")
        self.pbar.setValue(0)
        self.list.clear()
        self.btnSave.setEnabled(False)

        self.thread = QThread(self)
        worker = _Worker(path)
        worker.moveToThread(self.thread)

        worker.progress.connect(self.pbar.setValue)
        worker.finished.connect(self._done)

        self.thread.started.connect(worker.run)
        worker.finished.connect(self.thread.quit)
        worker.finished.connect(worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def _done(self,names:list):
        print("DEBUG: finished",names)
        self.lbl.setText(f"Готово. Уникальных: {len(names)}")
        self.list.addItems(names)
        self.btnSave.setEnabled(True)
        # а теперь, в главном (GUI) потоке, рисуем все chord’ы
        parser = GPXMLParser(self._current_path)
        parser.parse()

    def _save(self):
        path,_ = QFileDialog.getSaveFileName(self,"Сохранить","chords.txt","Text (*.txt)")
        if not path: return
        with open(path,"w",encoding="utf-8") as f:
            for i in range(self.list.count()):
                f.write(self.list.item(i).text()+"\n")
        QMessageBox.information(self,"OK","Сохранено")
