from PyQt5.QtCore import QModelIndex

qmi = QModelIndex()
qmi = qmi.siblingAtRow(33)
qmi = qmi.siblingAtColumn(45)

result = True
result = (qmi == qmi)
result = (qmi != qmi)
result = (qmi <= qmi)
result = (qmi >= qmi)
result = (qmi < qmi)
result = (qmi > qmi)
