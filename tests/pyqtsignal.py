import typing
from PyQt6 import QtCore


class Class(QtCore.QObject):
    signal = QtCore.pyqtSignal([str])  # type: typing.ClassVar[QtCore.pyqtSignal]


Class.signal.__get__

instance = Class()
instance.signal.emit
instance.signal.connect
instance.signal.disconnect
instance.signal[str].emit
