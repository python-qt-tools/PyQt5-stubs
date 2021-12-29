from PyQt5 import QtCore

# QSize tests
qs1 = QtCore.QSize(1,2)
qs2 = QtCore.QSize(3,4)
qs3 = QtCore.QSize(5,6)

qs3 = qs1 + qs2
assert type(qs3) == QtCore.QSize
qs3 = qs1 - qs2
assert type(qs3) == QtCore.QSize
qs3 += qs1
assert type(qs3) == QtCore.QSize
qs3 -= qs2
assert type(qs3) == QtCore.QSize

qs3 = qs1 * 3
assert type(qs3) == QtCore.QSize
qs3 = qs1 * 3.0
assert type(qs3) == QtCore.QSize

qs3 = 3 * qs1
assert type(qs3) == QtCore.QSize
qs3 = 3.0 * qs1
assert type(qs3) == QtCore.QSize

qs3 = qs1 / 2.0
assert type(qs3) == QtCore.QSize

qs3 *= 3
assert type(qs3) == QtCore.QSize
qs3 *= 3.0
assert type(qs3) == QtCore.QSize

qs3 /= 3.0
assert type(qs3) == QtCore.QSize


# QSizeF tests
qsf1 = QtCore.QSizeF(1.0,2.0)
qsf2 = QtCore.QSizeF(3.0,4.0)
qsf3 = QtCore.QSizeF(5.0,6.0)

qsf3 = qsf1 + qsf2
assert type(qsf3) == QtCore.QSizeF
qsf3 = qsf1 - qsf2
assert type(qsf3) == QtCore.QSizeF
qsf3 += qsf1
assert type(qsf3) == QtCore.QSizeF
qsf3 -= qsf2
assert type(qsf3) == QtCore.QSizeF

qsf3 = qsf1 * 3
assert type(qsf3) == QtCore.QSizeF
qsf3 = qsf1 * 3.0
assert type(qsf3) == QtCore.QSizeF

qsf3 = 3 * qsf1
assert type(qsf3) == QtCore.QSizeF
qsf3 = 3.0 * qsf1
assert type(qsf3) == QtCore.QSizeF

qsf3 = qsf1 / 2.0
assert type(qsf3) == QtCore.QSizeF

qsf3 *= 3
assert type(qsf3) == QtCore.QSizeF
qsf3 *= 3.0
assert type(qsf3) == QtCore.QSizeF

qsf3 /= 3.0
assert type(qsf3) == QtCore.QSizeF
