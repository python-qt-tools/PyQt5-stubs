import typing
from PyQt5 import QtCore

some_bytearray = QtCore.QByteArray(3, 'a')
some_bytes = bytes(some_bytearray)	# type: bytes


