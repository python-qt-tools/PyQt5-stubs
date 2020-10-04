from PyQt5.QtCore import pyqtSlot

@pyqtSlot(str)
def func_none(s: str) -> None:
    return

@pyqtSlot(str, result=int)
def func_int(s: str) -> int:
    return 42

func_none("test")
x = func_int("test")  # type: int
