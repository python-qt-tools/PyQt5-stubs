
from PyQt5 import QtWidgets

class MyTreeWidgetItem(QtWidgets.QTreeWidgetItem):

    # add comparison indicator to allow custom sorting of items
    def __lt__(self, other: QtWidgets.QTreeWidgetItem) -> bool:
        return super().__lt__(other)



