import os

os.environ['QT_DEBUG_PLUGINS'] = '1'

from PyQt5.QtWidgets import QLineEdit, QApplication
from PyQt5.QtGui import QGuiApplication

app = QApplication(['my_program', '-platform', 'offscreen'])

le = QLineEdit()
le.setText(None)

