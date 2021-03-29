from typing import Union
import pytest	# type: ignore[import]
from PyQt5 import QtCore, QtWidgets

#########################################################3
#
#        The original problem
#
#########################################################3

def test_original_problem() -> None:
	app = QtWidgets.QApplication([])

	w = QtWidgets.QWidget()
	w.setWindowFlags(w.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)


#########################################################3
#
#        tests on WindowType
#
#########################################################3

def assert_type_windowType(value: QtCore.Qt.WindowType) -> None:
	'''This validates both with mypy and regular python the actual type of the value'''
	assert type(value) == QtCore.Qt.WindowType


def assert_type_int(value: int) -> None:
	assert type(value) == int


def assert_type_windowFlags(value: QtCore.Qt.WindowFlags) -> None:
	'''This validates both with mypy and regular python the actual type of the value'''
	assert type(value) == QtCore.Qt.WindowFlags


def test_on_windowtype() -> None:
	windowType1 = QtCore.Qt.WindowContextHelpButtonHint
	windowType2 = QtCore.Qt.WindowMaximizeButtonHint
	windowTypeTest = windowType1    # type: QtCore.Qt.WindowType
	intValue = 0                    # type: int
	windowFlagsTest = QtCore.Qt.WindowFlags()
	windowFlagsOrTypeTest = windowType1		# type: Union[QtCore.Qt.WindowType, QtCore.Qt.WindowFlags]
	windowTypeOrInt = windowType1	# type: Union[int, QtCore.Qt.WindowType]

	assert_type_windowType(windowType1)
	assert_type_windowType(windowType2)
	assert_type_windowType(windowTypeTest)
	assert_type_windowFlags(windowFlagsTest)
	assert_type_int(intValue)

	# upcast from WindowType to int
	intValue = windowType1

	# conversion also accepted
	intValue = int(windowType1)

	# this is not supported for a good reason
	windowTypeTest = 33		# type: ignore

	# correct way to do it
	windowTypeTest = QtCore.Qt.WindowType(33)

	# The rules of WindowType conversion defined in PyQt5 are:
	# 1. | ~= with WindowType return a WindowFlags (which is not compatible to int)
	#   Note that this breaks Liskov principle
	# 2. everything else returns int: & ^ &= ^=
	# 3. operations with int return int.

	assert_type_windowFlags(windowType1 | windowType2)
	assert_type_int(~windowType1)
	assert_type_int(windowType1 & windowType2)
	assert_type_int(windowType1 ^ windowType2)

	# right operand
	assert_type_int(windowType1 | 33)
	assert_type_int(windowType1 & 33)
	assert_type_int(windowType1 ^ 33)
	assert_type_int(windowType1 + 33)
	assert_type_int(windowType1 - 33)

	# left operand
	assert_type_windowFlags(33 | windowType1)
	assert_type_int(33 & windowType1)
	assert_type_int(33 ^ windowType1)
	assert_type_int(33 + windowType1)
	assert_type_int(33 - windowType1)

	windowFlagsOrTypeTest = windowType1	# reset type and value
	assert_type_windowType(windowFlagsOrTypeTest)
	windowFlagsOrTypeTest |= windowType2
	assert_type_windowFlags(windowFlagsOrTypeTest)	# nice violation of Liskov here

	windowTypeOrInt = windowType1	# reset type and value
	assert_type_windowType(windowTypeOrInt)
	windowTypeOrInt |= 33
	assert_type_int(windowTypeOrInt)

	windowTypeOrInt = windowType1	# reset type and value
	assert_type_windowType(windowTypeOrInt)
	windowTypeOrInt &= 33
	assert_type_int(windowTypeOrInt)

	windowTypeOrInt = windowType1	# reset type and value
	assert_type_windowType(windowTypeOrInt)
	windowTypeOrInt &= windowType2
	assert_type_int(windowTypeOrInt)

	windowTypeOrInt = windowType1	# reset type and value
	assert_type_windowType(windowTypeOrInt)
	windowTypeOrInt ^= 33
	assert_type_int(windowTypeOrInt)

	windowTypeOrInt = windowType1	# reset type and value
	assert_type_windowType(windowTypeOrInt)
	windowTypeOrInt ^= windowType2
	assert_type_int(windowTypeOrInt)



#########################################################3
#
#        tests on WindowFlags
#
#########################################################3

def test_on_window_flags() -> None:
	windowType1 = QtCore.Qt.WindowContextHelpButtonHint
	windowFlags1 = QtCore.Qt.WindowFlags()
	windowFlags2 = QtCore.Qt.WindowFlags()
	windowFlagsTest = windowFlags1     # type: QtCore.Qt.WindowFlags
	intValue = 0

	assert_type_windowType(windowType1)
	assert_type_windowFlags(windowFlags1)
	assert_type_windowFlags(windowFlags2)
	assert_type_windowFlags(windowFlagsTest)
	assert_type_int(intValue)


	# window flags may be created by combining windowFlags together
	assert_type_windowFlags( ~windowFlags1 )
	assert_type_windowFlags( windowFlags1 | windowFlags2 )
	assert_type_windowFlags( windowFlags1 & windowFlags2 )
	assert_type_windowFlags( windowFlags1 ^ windowFlags2 )


	# window flags may be created by combining windowFlags and windowType, left or right
	assert_type_windowFlags( windowFlags1 | windowType1 )
	assert_type_windowFlags( windowFlags1 & windowType1 )
	assert_type_windowFlags( windowFlags1 ^ windowType1 )

	assert_type_windowFlags( windowType1 | windowFlags1 )
	assert_type_windowFlags( windowType1 & windowFlags1 )
	assert_type_windowFlags( windowType1 ^ windowFlags1 )


	# window flags may be created by combining windowFlags and int, right only
	assert_type_windowFlags(windowFlags1 | 33)
	assert_type_windowFlags(windowFlags1 & 33)
	assert_type_windowFlags(windowFlags1 ^ 33)


	# this is rejected by mypy and is slightly annoying: you can not pass a WindowType variable to a method expecting a WindowFlags
	# explicit typing must be used on those methods to accept both WindowType and WindowFlags
	windowFlagsTest = windowType1   # type: ignore

	# correct way to do it
	windowFlagsTest = QtCore.Qt.WindowFlags(windowType1)
	assert_type_windowFlags(windowFlagsTest)

	# this is rejected for the same reason as for windowType.
	intValue = windowFlagsTest      # type: ignore

	# correct way to do it
	intValue = int(windowFlagsTest)
	assert_type_int(intValue)

	# rejected by mypy rightfully
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

	pytest.raises(TypeError, lambda: 33 | windowFlags1 )	# type: ignore[operator]
	pytest.raises(TypeError, lambda: 33 & windowFlags1 )	# type: ignore[operator]
	pytest.raises(TypeError, lambda: 33 ^ windowFlags1 )	# type: ignore[operator]

	pytest.raises(TypeError, lambda: windowFlags1 + windowFlags2 )	# type: ignore[operator]
	pytest.raises(TypeError, lambda: windowFlags1 - windowFlags2 )	# type: ignore[operator]
	pytest.raises(TypeError, lambda: windowFlags1 + windowType1)	# type: ignore[operator]
	pytest.raises(TypeError, lambda: windowFlags1 - windowType1)	# type: ignore[operator]
	pytest.raises(TypeError, lambda: windowFlags1 + 33)				# type: ignore[operator]
	pytest.raises(TypeError, lambda: windowFlags1 - 33)				# type: ignore[operator]
	pytest.raises(TypeError, lambda: windowType1 + windowFlags1)	# type: ignore[operator]
	pytest.raises(TypeError, lambda: windowType1 - windowFlags1)	# type: ignore[operator]
	pytest.raises(TypeError, lambda: 33 + windowFlags1)				# type: ignore[operator]
	pytest.raises(TypeError, lambda: 33 - windowFlags1)				# type: ignore[operator]

