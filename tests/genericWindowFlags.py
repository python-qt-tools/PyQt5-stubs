import typing

from PyQt5 import QtCore



class MyIntOneFlag(int):
    def __invert__(self) -> 'MyIntMultipleFlags': ...
    def __or__(self, other: 'MyIntOneFlag') -> 'MyIntMultipleFlags': ...


class MyIntMultipleFlags(int):
    pass


# test on WindowType
windowType1 = MyIntOneFlag()
windowType2 = MyIntOneFlag()

windowTypeTest = windowType1    # type: MyIntOneFlag
windowTypeTest = windowType2

windowFlagsTest = ~windowType1  # type: MyIntMultipleFlags
windowFlagsTest = windowType1  | windowType2
