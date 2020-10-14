from PyQt5 import QtWidgets

QtWidgets.QMessageBox.question(
    None,
    "Confirm",
    "Are you sure?",
    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
)

a: QtWidgets.QMessageBox.StandardButtons = QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Ok
b: int = QtWidgets.QMessageBox.Ok | 0
