"""Tests for QLineEdit."""
from PyQt5.QtWidgets import QLineEdit

# test that QLineEdit.setText() accepts None as parameter
edit = QLineEdit()
edit.setText(None)
edit.setValidator(None)
