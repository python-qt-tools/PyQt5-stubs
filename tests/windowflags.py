
from PyQt5 import QtCore

# test on WindowType
windowType1 = QtCore.Qt.WindowContextHelpButtonHint
windowType2 = QtCore.Qt.WindowMaximizeButtonHint

windowTypeTest = windowType1    # type: QtCore.Qt.WindowType
windowTypeTest = windowType2
windowTypeTest = ~windowType1

# test on WindowFlags
windowFlags1 = QtCore.Qt.WindowFlags()
windowFlags2 = QtCore.Qt.WindowFlags()

windowFlagsTest = windowFlags1     # type: QtCore.Qt.WindowFlags

windowFlagsTest = windowType1 & windowType2
windowFlagsTest = windowType1 | windowType2
windowFlagsTest = windowType1 ^ windowType2
windowFlagsTest = windowType1 + windowType2
windowFlagsTest = windowType1 - windowType2

windowFlagsTest = ~windowFlags1

# right operator
windowFlagsTest = windowFlags1 + windowType1
windowFlagsTest = windowFlags1 - windowType1
windowFlagsTest = windowFlags1 | windowType1
windowFlagsTest = windowFlags1 & windowType1
windowFlagsTest = windowFlags1 ^ windowType1

# left operator
windowFlagsTest = windowType1 + windowFlags1
windowFlagsTest = windowType1 - windowFlags1
windowFlagsTest = windowType1 | windowFlags1
windowFlagsTest = windowType1 & windowFlags1
windowFlagsTest = windowType1 ^ windowFlags1


windowFlagsTest = windowFlags1 + windowFlags2
windowFlagsTest = windowFlags1 - windowFlags2
windowFlagsTest = windowFlags1 | windowFlags2
windowFlagsTest = windowFlags1 & windowFlags2
windowFlagsTest = windowFlags1 ^ windowFlags2


