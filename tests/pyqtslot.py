from PyQt5.QtCore import pyqtSlot

@pyqtSlot(str)
def func(s: str) -> int:
    return 42

func("test")
