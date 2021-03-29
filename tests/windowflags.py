from PyQt5 import QtCore, QtWidgets

#########################################################3
#
#        The original problem
#
#########################################################3
app = QtWidgets.QApplication([])

w = QtWidgets.QWidget()
w.setWindowFlags(w.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

#########################################################3
#
#        tests on WindowType
#
#########################################################3

windowType1 = QtCore.Qt.WindowContextHelpButtonHint
windowType2 = QtCore.Qt.WindowMaximizeButtonHint

windowTypeTest = windowType1    # type: QtCore.Qt.WindowType
intValue = 0                    # type: int

# this is rejected by mypy and is ok, we want to force precise typing on such flags and avoid using generic int
intValue = windowType1          # type: ignore

# if you really need the int value, you can use this.
intValue = int(windowType1)

# this is not supported for a good reason
windowTypeTest = 33	# type: ignore

# correct way to do it
windowTypeTest = QtCore.Qt.WindowType(33)

#########################################################3
#
#        tests on WindowFlags
#
#########################################################3

windowFlags1 = QtCore.Qt.WindowFlags()
windowFlags2 = QtCore.Qt.WindowFlags()

windowFlagsTest = windowFlags1     # type: QtCore.Qt.WindowFlags


# window flags may be created by combining windowFlags together
windowFlagsTest = ~windowFlags1
windowFlagsTest = windowFlags1 | windowFlags2
windowFlagsTest = windowFlags1 & windowFlags2
windowFlagsTest = windowFlags1 ^ windowFlags2

# window flags may be created by combining windowType together
windowFlagsTest = ~windowType1
windowFlagsTest = windowType1 & windowType2
windowFlagsTest = windowType1 | windowType2
windowFlagsTest = windowType1 ^ windowType2
windowFlagsTest = windowType1 + windowType2
windowFlagsTest = windowType1 - windowType2

# window flags may also be created by combining windowType and int, left or right
windowFlagsTest = windowType1 & 33
windowFlagsTest = windowType1 | 33
windowFlagsTest = windowType1 ^ 33
windowFlagsTest = windowType1 + 33
windowFlagsTest = windowType1 - 33
windowFlagsTest =  33 & windowType1
windowFlagsTest =  33 | windowType1
windowFlagsTest =  33 ^ windowType1
windowFlagsTest =  33 + windowType1
windowFlagsTest =  33 - windowType1

# window flags may be created by combining windowFlags and windowType, left or right
windowFlagsTest = windowFlags1 | windowType1
windowFlagsTest = windowFlags1 & windowType1
windowFlagsTest = windowFlags1 ^ windowType1
windowFlagsTest = windowType1 | windowFlags1
windowFlagsTest = windowType1 & windowFlags1
windowFlagsTest = windowType1 ^ windowFlags1


# window flags may be created by combining windowFlags and int, right only
windowFlagsTest = windowFlags1 | 33
windowFlagsTest = windowFlags1 & 33
windowFlagsTest = windowFlags1 ^ 33


# this is rejected and is slightly annoying: you can not pass a WindowType variable to a method expecting a WindowFlags
# explicit typing must be used on those methods to accept both WindowType and WindowFlags
windowFlagsTest = windowType1   # type: ignore

# correct way to do it
windowFlagsTest = QtCore.Qt.WindowFlags(windowType1)

# this is rejected for the same reason as for windowType. We want windowFlags to be stay precise typing
intValue = windowFlagsTest      # type: ignore

# correct way to do it
intValue = int(windowFlagsTest)

# rejected because all other operations on WindowFlags would then fail, because int
# does not support as many operations as WindowFlags
windowFlagsTest = 33            # type: ignore

# correct way to do it
windowFlagsTest = QtCore.Qt.WindowFlags(33)


#########################################################3
#
#        Exploring errors
#
#########################################################3

# This checks the following:
# + and - operations are not supported on windowFlags
# combining int with windowFlags does not work

try:
    windowFlagsTest = windowFlags1 + windowFlags2		# type: ignore
    assert False
except TypeError:
    pass

try:
	windowFlagsTest = windowFlags1 - windowFlags2		# type: ignore
	assert False
except TypeError:
	pass

try:
	windowFlagsTest = windowFlags1 + windowType1		# type: ignore
	assert False
except TypeError:
	pass

try:
	windowFlagsTest = windowFlags1 - windowType1		# type: ignore
	assert False
except TypeError:
	pass

try:
	windowFlagsTest = windowType1 + windowFlags1		# type: ignore
	assert False
except TypeError:
	pass

try:
	windowFlagsTest = windowType1 - windowFlags1		# type: ignore
	assert False
except TypeError:
	pass

try:
	windowFlagsTest = windowFlags1 + 33		# type: ignore
	assert False
except TypeError:
	pass

try:
	windowFlagsTest = windowFlags1 - 33		# type: ignore
	assert False
except TypeError:
	pass

try:
	windowFlagsTest = 33 + windowFlags1		# type: ignore
	assert False
except TypeError:
	pass

try:
	windowFlagsTest = 33 - windowFlags1		# type: ignore
	assert False
except TypeError:
	pass

try:
	windowFlagsTest = 33 | windowFlags1		# type: ignore
	assert False
except TypeError:
	pass

try:
	windowFlagsTest = 33 & windowFlags1		# type: ignore
	assert False
except TypeError:
	pass

try:
	windowFlagsTest = 33 ^ windowFlags1		# type: ignore
	assert False
except TypeError:
	pass

