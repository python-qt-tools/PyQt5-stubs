from typing import Union, TypeVar, Type
import pytest		# type: ignore
from PyQt5 import QtCore, QtWidgets

OneFlagClass = QtCore.Qt.WindowType
MultiFlagClass = QtCore.Qt.WindowFlags

oneFlagRefValue1 = QtCore.Qt.WindowContextHelpButtonHint
oneFlagRefValue2 = QtCore.Qt.WindowMaximizeButtonHint

T = TypeVar('T')
def assert_type_of_value(expected_type: Type[T], value: T) -> None:
	'''Raise an exception if the value is not of type expected_type'''
	assert type(value) == expected_type


#########################################################3
#
#        tests on WindowType
#
#########################################################3

def test_on_one_flag_class() -> None:
	windowType1 = oneFlagRefValue1
	windowType2 = oneFlagRefValue2
	windowTypeTest = windowType1    # type: QtCore.Qt.WindowType
	intValue = 0                    # type: int
	windowFlagsOrTypeTest = windowType1		# type: Union[QtCore.Qt.WindowType, QtCore.Qt.WindowFlags]
	windowTypeOrInt = windowType1	# type: Union[int, QtCore.Qt.WindowType]

	assert_type_of_value(OneFlagClass, windowType1)
	assert_type_of_value(OneFlagClass, windowType2)
	assert_type_of_value(OneFlagClass, windowTypeTest)
	assert_type_of_value(int, intValue)


	# upcast from WindowType to int
	intValue = windowType1

	# conversion also accepted
	intValue = int(windowType1)

	# this is not supported for a good reason
	windowTypeTest = 33		# type: ignore

	# correct way to do it
	windowTypeTest = OneFlagClass(33)
	windowTypeTest = OneFlagClass(windowType1)

	# The rules of WindowType conversion defined in PyQt5 are:
	# 1. | ~= with WindowType return a WindowFlags (which is not compatible to int)
	#   Note that this breaks Liskov principle
	# 2. everything else returns int: & ^ &= ^=
	# 3. operations with int return int.

	assert_type_of_value(MultiFlagClass, windowType1 | windowType2)
	assert_type_of_value(int, ~windowType1)
	assert_type_of_value(int, windowType1 & windowType2)
	assert_type_of_value(int, windowType1 ^ windowType2)

	# right operand
	assert_type_of_value(int, windowType1 | 33)
	assert_type_of_value(int, windowType1 & 33)
	assert_type_of_value(int, windowType1 ^ 33)
	assert_type_of_value(int, windowType1 + 33)
	assert_type_of_value(int, windowType1 - 33)

	# left operand
	assert_type_of_value(MultiFlagClass, 33 | windowType1)
	assert_type_of_value(int, 33 & windowType1)
	assert_type_of_value(int, 33 ^ windowType1)
	assert_type_of_value(int, 33 + windowType1)
	assert_type_of_value(int, 33 - windowType1)

	windowFlagsOrTypeTest = windowType1	# reset type and value
	assert_type_of_value(OneFlagClass, windowFlagsOrTypeTest)
	windowFlagsOrTypeTest |= windowType2
	assert_type_of_value(MultiFlagClass, windowFlagsOrTypeTest)	# nice violation of Liskov here

	windowTypeOrInt = windowType1	# reset type and value
	assert_type_of_value(OneFlagClass, windowTypeOrInt)
	windowTypeOrInt |= 33
	assert_type_of_value(int, windowTypeOrInt)

	windowTypeOrInt = windowType1	# reset type and value
	assert_type_of_value(OneFlagClass, windowTypeOrInt)
	windowTypeOrInt &= 33
	assert_type_of_value(int, windowTypeOrInt)

	windowTypeOrInt = windowType1	# reset type and value
	assert_type_of_value(OneFlagClass, windowTypeOrInt)
	windowTypeOrInt &= windowType2
	assert_type_of_value(int, windowTypeOrInt)

	windowTypeOrInt = windowType1	# reset type and value
	assert_type_of_value(OneFlagClass, windowTypeOrInt)
	windowTypeOrInt ^= 33
	assert_type_of_value(int, windowTypeOrInt)

	windowTypeOrInt = windowType1	# reset type and value
	assert_type_of_value(OneFlagClass, windowTypeOrInt)
	windowTypeOrInt ^= windowType2
	assert_type_of_value(int, windowTypeOrInt)



def test_on_multi_flag_class() -> None:
	windowType1 = oneFlagRefValue1
	windowFlags1 = MultiFlagClass()
	windowFlags2 = MultiFlagClass()
	windowFlagsTest = windowFlags1     # type: MultiFlagClass
	intValue = 0

	assert_type_of_value(OneFlagClass, windowType1)
	assert_type_of_value(MultiFlagClass, windowFlags1)
	assert_type_of_value(MultiFlagClass, windowFlags2)
	assert_type_of_value(MultiFlagClass, windowFlagsTest)
	assert_type_of_value(int, intValue)


	# window flags may be created by combining windowFlags together
	assert_type_of_value(MultiFlagClass,  ~windowFlags1 )
	assert_type_of_value(MultiFlagClass,  windowFlags1 | windowFlags2 )
	assert_type_of_value(MultiFlagClass,  windowFlags1 & windowFlags2 )
	assert_type_of_value(MultiFlagClass,  windowFlags1 ^ windowFlags2 )


	# window flags may be created by combining windowFlags and windowType, left or right
	assert_type_of_value(MultiFlagClass,  windowFlags1 | windowType1 )
	assert_type_of_value(MultiFlagClass,  windowFlags1 & windowType1 )
	assert_type_of_value(MultiFlagClass,  windowFlags1 ^ windowType1 )

	assert_type_of_value(MultiFlagClass,  windowType1 | windowFlags1 )
	assert_type_of_value(MultiFlagClass,  windowType1 & windowFlags1 )
	assert_type_of_value(MultiFlagClass,  windowType1 ^ windowFlags1 )


	# window flags may be created by combining windowFlags and int, right only
	assert_type_of_value(MultiFlagClass, windowFlags1 | 33)
	assert_type_of_value(MultiFlagClass, windowFlags1 & 33)
	assert_type_of_value(MultiFlagClass, windowFlags1 ^ 33)


	# this is rejected by mypy and is slightly annoying: you can not pass a WindowType variable to a method expecting a WindowFlags
	# explicit typing must be used on those methods to accept both WindowType and WindowFlags
	windowFlagsTest = windowType1   # type: ignore

	# correct way to do it
	windowFlagsTest = MultiFlagClass(windowType1)
	assert_type_of_value(MultiFlagClass, windowFlagsTest)

	# this is rejected for the same reason as for windowType.
	intValue = windowFlagsTest      # type: ignore

	# correct way to do it
	intValue = int(windowFlagsTest)
	assert_type_of_value(int, intValue)

	# rejected by mypy rightfully
	windowFlagsTest = 33            # type: ignore

	# correct way to do it
	windowFlagsTest = MultiFlagClass(33)

	# assignments operations with WindowType
	assert_type_of_value(MultiFlagClass, windowFlagsTest)
	windowFlagsTest |= windowType1
	assert_type_of_value(MultiFlagClass, windowFlagsTest)

	assert_type_of_value(MultiFlagClass, windowFlagsTest)
	windowFlagsTest &= windowType1
	assert_type_of_value(MultiFlagClass, windowFlagsTest)

	assert_type_of_value(MultiFlagClass, windowFlagsTest)
	windowFlagsTest ^= windowType1
	assert_type_of_value(MultiFlagClass, windowFlagsTest)

	# assignments operations with int
	assert_type_of_value(MultiFlagClass, windowFlagsTest)
	windowFlagsTest |= 33
	assert_type_of_value(MultiFlagClass, windowFlagsTest)

	assert_type_of_value(MultiFlagClass, windowFlagsTest)
	windowFlagsTest &= 33
	assert_type_of_value(MultiFlagClass, windowFlagsTest)

	assert_type_of_value(MultiFlagClass, windowFlagsTest)
	windowFlagsTest ^= 33
	assert_type_of_value(MultiFlagClass, windowFlagsTest)

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

	def f1() -> None:
		windowFlagsTest = MultiFlagClass()
		windowFlagsTest += windowType1	  # type: ignore[assignment, operator]
	def f2() -> None:
		windowFlagsTest = MultiFlagClass()
		windowFlagsTest += 33	  # type: ignore[assignment, operator]
	def f3() -> None:
		windowFlagsTest = MultiFlagClass()
		windowFlagsTest -= windowType1	  # type: ignore[assignment, operator]
	def f4() -> None:
		windowFlagsTest = MultiFlagClass()
		windowFlagsTest -= 33	  # type: ignore[assignment, operator]

	pytest.raises(TypeError, f1)
	pytest.raises(TypeError, f2)
	pytest.raises(TypeError, f3)
	pytest.raises(TypeError, f4)

