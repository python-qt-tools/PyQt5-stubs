from typing import Literal, assert_type

import pytest
from PyQt5 import QtCore, QtWidgets, sip


def get_value(obj: QtCore.QObject) -> int:
    return 0


def set_value(obj: QtCore.QObject, value: int) -> None:
    pass


def reset_value(obj: QtCore.QObject) -> None:
    pass


prop = QtCore.pyqtProperty(int)
prop.read(get_value)
prop.write(set_value)
prop.reset(reset_value)
prop.getter(get_value)
prop.setter(set_value)
prop.deleter(reset_value)

with pytest.raises(TypeError):
    prop.read(func=get_value)  # type: ignore[call-arg]
with pytest.raises(TypeError):
    prop.write(func=set_value)  # type: ignore[call-arg]
with pytest.raises(TypeError):
    prop.reset(func=reset_value)  # type: ignore[call-arg]
with pytest.raises(TypeError):
    prop.getter(func=get_value)  # type: ignore[call-arg]
with pytest.raises(TypeError):
    prop.setter(func=set_value)  # type: ignore[call-arg]
with pytest.raises(TypeError):
    prop.deleter(func=reset_value)  # type: ignore[call-arg]

ptr = sip.voidptr(0)
ptr.setsize(0)
ptr.setwriteable(False)
assert ptr.getsize() == 0
assert ptr.getwriteable() is False
with pytest.raises(TypeError):
    ptr.setsize(size=0)  # type: ignore[call-arg]
with pytest.raises(TypeError):
    ptr.setwriteable(bool=False)  # type: ignore[call-arg]

obj = QtCore.QObject()
sip.dump(obj)
with pytest.raises(TypeError):
    sip.dump(obj=obj)  # type: ignore[call-arg]
with pytest.raises(TypeError):
    sip.dump(obj, obj)  # type: ignore[call-arg]

assert_type(QtCore.QCborKnownTags.DateTimeString, Literal[QtCore.QCborKnownTags.DateTimeString])
assert_type(
    QtWidgets.QActionGroup.ExclusionPolicy.Exclusive,
    Literal[QtWidgets.QActionGroup.ExclusionPolicy.Exclusive],
)
