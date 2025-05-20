from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, pyqtSignal
import os


class FileDropWidget(QLabel):
    """Простая зона drag&drop – отдаёт путь xml-файла."""
    fileLoaded = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__("↘  Перетащите MusicXML / GP-XML сюда ↙", parent)
        self.setAlignment(Qt.AlignCenter)
        self.setAcceptDrops(True)
        self.setStyleSheet(
            "border:2px dashed #888;padding:40px;font-size:16px;"
        )

    # --- DnD events ----------------------------------------------------
    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    dragMoveEvent = dragEnterEvent  # поведение одинаковое

    def dropEvent(self, e):
        if not e.mimeData().hasUrls():
            return
        path = e.mimeData().urls()[0].toLocalFile()
        if os.path.isfile(path) and path.lower().endswith(".xml"):
            self.setText(os.path.basename(path))
            self.fileLoaded.emit(path)
