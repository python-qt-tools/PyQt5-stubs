from typing import assert_type

import pytest
from PyQt5 import QtCore, sip


class ObjectSubclass(QtCore.QObject):
    pass


class FlagsSubclass(QtCore.Qt.Alignment):
    pass


assert isinstance(ObjectSubclass, sip.wrappertype)
assert issubclass(sip.wrappertype, type)
assert_type(FlagsSubclass(), FlagsSubclass)

with pytest.raises(TypeError):
    QtCore.Qt.Alignment().__or__(other=QtCore.Qt.AlignLeft)  # type: ignore[call-arg]

with pytest.raises(TypeError):
    class EnumSubclass(QtCore.Qt.AlignmentFlag):  # type: ignore[misc]
        pass

with pytest.raises(TypeError):
    class LayoutConflict(QtCore.QObject, list[int]):  # type: ignore[misc]
        pass

pointer = sip.voidptr(address=0, size=0, writeable=False)
assert pointer.getsize() == 0
assert pointer.getwriteable() is False
with pytest.raises(TypeError):
    sip.voidptr(addr=0)  # type: ignore[call-arg]
