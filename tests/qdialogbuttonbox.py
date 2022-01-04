from PyQt5 import QtWidgets

a = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Ok  # type: QtWidgets.QDialogButtonBox.StandardButtons
b = QtWidgets.QDialogButtonBox.Ok | 0  # type: int
c = a | 0  # type: QtWidgets.QDialogButtonBox.StandardButtons
d = a | QtWidgets.QDialogButtonBox.Ok  # type: QtWidgets.QDialogButtonBox.StandardButtons
e = a | a  # type: QtWidgets.QDialogButtonBox.StandardButtons
