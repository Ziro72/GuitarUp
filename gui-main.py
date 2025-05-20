import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout
from filedrop_widget import FileDropWidget
from parser_widget import ParserWidget

app = QApplication(sys.argv)
win = QWidget()
lay = QHBoxLayout(win)

drop   = FileDropWidget()
parser = ParserWidget()

drop.fileLoaded.connect(parser.load_file)

lay.addWidget(drop, 1)
lay.addWidget(parser, 2)

win.resize(900, 500)
win.show()
sys.exit(app.exec_())
