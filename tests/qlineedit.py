import os

from PyQt5.QtWidgets import QLineEdit, QApplication

app = QApplication(['my_program', '-platform', 'offscreen'])

le = QLineEdit()
le.setText(None)

