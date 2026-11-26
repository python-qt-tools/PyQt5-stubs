from typing import assert_type

import pytest
from PyQt5.QtCore import QPoint, QPointF, QSize, QSizeF


point = QPoint(2, 3)
point_f = QPointF(2, 3)
size = QSize(2, 3)
size_f = QSizeF(2, 3)

assert_type(2 * point, QPoint)
assert_type(2 * point_f, QPointF)
assert 2 * point == QPoint(4, 6)
assert 2 * point_f == QPointF(4, 6)

assert_type(point.__radd__(QPoint(5, 7)), QPoint)
assert_type(point.__rsub__(QPoint(5, 7)), QPoint)
assert point.__radd__(QPoint(5, 7)) == QPoint(7, 10)
assert point.__rsub__(QPoint(5, 7)) == QPoint(3, 4)

assert_type(point_f.__radd__(QPointF(5, 7)), QPointF)
assert_type(point_f.__rsub__(QPointF(5, 7)), QPointF)
assert point_f.__radd__(QPointF(5, 7)) == QPointF(7, 10)
assert point_f.__rsub__(QPointF(5, 7)) == QPointF(3, 4)

assert_type(size.__radd__(QSize(5, 7)), QSize)
assert_type(size.__rsub__(QSize(5, 7)), QSize)
assert size.__radd__(QSize(5, 7)) == QSize(7, 10)
assert size.__rsub__(QSize(5, 7)) == QSize(3, 4)

assert_type(size_f.__radd__(QSizeF(5, 7)), QSizeF)
assert_type(size_f.__rsub__(QSizeF(5, 7)), QSizeF)
assert size_f.__radd__(QSizeF(5, 7)) == QSizeF(7, 10)
assert size_f.__rsub__(QSizeF(5, 7)) == QSizeF(3, 4)

with pytest.raises(TypeError):
    2 / point  # type: ignore[operator]
with pytest.raises(TypeError):
    2 / point_f  # type: ignore[operator]
with pytest.raises(TypeError):
    2 / size  # type: ignore[operator]
with pytest.raises(TypeError):
    2 / size_f  # type: ignore[operator]
