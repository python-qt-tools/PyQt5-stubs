from PyQt6 import QtWidgets

a = QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Ok  # type: QtWidgets.QMessageBox.StandardButtons
b = QtWidgets.QMessageBox.Ok | 0  # type: int
c = a | 0  # type: QtWidgets.QMessageBox.StandardButtons
d = a | QtWidgets.QMessageBox.Ok  # type: QtWidgets.QMessageBox.StandardButtons
e = a | a  # type: QtWidgets.QMessageBox.StandardButtons
