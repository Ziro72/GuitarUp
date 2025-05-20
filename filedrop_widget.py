from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, pyqtSignal
import os

class FileDropWidget(QLabel):
    """Зона drag&drop: испускает fileLoaded(path) при сбросе .xml."""
    fileLoaded = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__("↘ Перетащите XML сюда ↙", parent)
        self.setAlignment(Qt.AlignCenter)
        self.setAcceptDrops(True)
        self.setStyleSheet("border:2px dashed #888;padding:40px;font-size:16px;")

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    dragMoveEvent = dragEnterEvent

    def dropEvent(self, e):
        urls = e.mimeData().urls()
        if not urls:
            return
        path = urls[0].toLocalFile()
        if os.path.isfile(path) and path.lower().endswith(".xml"):
            print(f"DEBUG: dropEvent → {path}")
            self.setText(os.path.basename(path))
            self.fileLoaded.emit(path)
        e.acceptProposedAction()
