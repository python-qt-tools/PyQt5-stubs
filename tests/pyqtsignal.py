import typing
from PyQt5 import QtCore


class Class(QtCore.QObject):
    signal1 = QtCore.pyqtSignal([str])  # type: typing.ClassVar[QtCore.pyqtSignal]
    signal2 = QtCore.pyqtSignal(int)
    signal3 = QtCore.pyqtSignal([str, bool], [float])
    signal4 = QtCore.pyqtSignal(int, name="cool_signal")
    signal5 = QtCore.pyqtSignal(type, revision=2)
    signal6 = QtCore.pyqtSignal(bool, arguments=["bool_arg"])


Class.signal1.__get__

instance = Class()
instance.signal1.emit
instance.signal1.connect
instance.signal1.disconnect
instance.signal1[str].emit
