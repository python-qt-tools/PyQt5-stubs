from PyQt5 import QtWidgets

QtWidgets.QMessageBox.question(
    None,
    "Confirm",
    "Are you sure?",
    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
)
