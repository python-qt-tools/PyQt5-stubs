import typing
from PyQt5 import QtCore


class Class(QtCore.QObject):
    signal: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal([str])


Class.signal.__get__

instance = Class()
instance.signal.emit
instance.signal.connect
instance.signal.disconnect
instance.signal[str].emit
