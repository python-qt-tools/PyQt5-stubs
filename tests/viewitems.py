from PyQt5.QtWidgets import QTableWidgetItem, QListWidgetItem, QTreeWidgetItem


qti = QTableWidgetItem('')

# Check all comparison informtaion
result = True
result = (qti == qti)
result = (qti != qti)
result = (qti <= qti)
result = (qti >= qti)
result = (qti < qti)
result = (qti > qti)

try:
    # comparison does not work, there should be also a type error
    result = qti < object() # type: ignore[operator]
except TypeError:
    pass

class MyTableWidgetItem(QTableWidgetItem):

    # add comparison indicator to allow custom sorting of items
    def __lt__(self, other: QTableWidgetItem) -> bool:
        return super().__lt__(other)


qli = QListWidgetItem()
result = True
result = (qli == qli)
result = (qli != qli)
result = (qli <= qli)
result = (qli >= qli)
result = (qli < qli)
result = (qli > qli)

class MyListWidgetItem(QListWidgetItem):

    # add comparison indicator to allow custom sorting of items
    def __lt__(self, other: QListWidgetItem) -> bool:
        return super().__lt__(other)


qtwi = QTreeWidgetItem([])
result = True
result = (qtwi == qtwi)
result = (qtwi != qtwi)
result = (qtwi <= qtwi)
result = (qtwi >= qtwi)
result = (qtwi < qtwi)
result = (qtwi > qtwi)


class MyTreeWidgetItem(QTreeWidgetItem):

    # add comparison indicator to allow custom sorting of items
    def __lt__(self, other: QTreeWidgetItem) -> bool:
        return super().__lt__(other)


