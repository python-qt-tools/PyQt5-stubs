"""Tests for QLineEdit."""
from PyQt5.QtWidgets import QApplication, QLineEdit

# test that QLineEdit.setText() accepts None as parameter
edit = QLineEdit()
edit.setText(None)
