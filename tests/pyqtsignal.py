import typing
from PyQt5 import QtCore


class Class(QtCore.QObject):
    signal = QtCore.pyqtSignal([str])  # type: typing.ClassVar[QtCore.pyqtSignal]

    def __init__(self) -> None:
        super().__init__()

    def my_slot(self) -> None:
        pass

# check that method exists
Class.signal.__get__

instance = Class()
instance.signal.emit
instance.signal.connect
instance.signal.disconnect
instance.signal[str].emit

# use some of them
connection = QtCore.QMetaObject.Connection()

connection = instance.signal.connect(instance.my_slot)
instance.signal.disconnect()
connection = instance.signal.connect(instance.my_slot)
instance.signal.disconnect(connection)