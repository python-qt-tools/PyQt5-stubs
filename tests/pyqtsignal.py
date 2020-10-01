import typing
from PyQt5 import QtCore


class Class(QtCore.QObject):
    signal: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal()


instance = Class()
instance.signal.emit
