from typing import Union, TypeVar, Type
import pytest

### Specific part
# file generated from qflags_test_template.py for QFlags class "QStyleOptionToolBar.ToolBarFeatures" and flag class "QStyleOptionToolBar.ToolBarFeature"
from PyQt5 import QtWidgets

OneFlagClass = QtWidgets.QStyleOptionToolBar.ToolBarFeature
MultiFlagClass = QtWidgets.QStyleOptionToolBar.ToolBarFeatures

oneFlagRefValue1 = QtWidgets.QStyleOptionToolBar.ToolBarFeature.None_
oneFlagRefValue2 = QtWidgets.QStyleOptionToolBar.ToolBarFeature.Movable

OR_CONVERTS_TO_MULTI = True
OR_INT_CONVERTS_TO_MULTI = False
INT_OR_CONVERTS_TO_MULTI = True
### End of specific part

T = TypeVar('T')
def assert_type_of_value(expected_type: Type[T], value: T) -> None:
	'''Raise an exception if the value is not of type expected_type'''
	assert type(value) == expected_type


def test_on_one_flag_class() -> None:
	oneFlagValue1 = oneFlagRefValue1
	oneFlagValue2 = oneFlagRefValue2
	oneFlagValueTest = oneFlagValue1    # type: OneFlagClass
	intValue = 0                    # type: int
	oneOrMultiFlagValueTest = oneFlagValue1		# type: Union[OneFlagClass, MultiFlagClass]
	oneFlagOrIntValue = oneFlagValue1	# type: Union[int, OneFlagClass]

	assert_type_of_value(OneFlagClass, oneFlagValue1)
	assert_type_of_value(OneFlagClass, oneFlagValue2)
	assert_type_of_value(OneFlagClass, oneFlagValueTest)
	assert_type_of_value(int, intValue)


	# upcast from OneFlagClass to int
	intValue = oneFlagValue1

	# conversion also accepted
	intValue = int(oneFlagValue1)

	# this is not supported type-safely for a good reason
	oneFlagValueTest = 33		# type: ignore

	# correct way to do it
	oneFlagValueTest = OneFlagClass(33)
	oneFlagValueTest = OneFlagClass(oneFlagValue1)

	# The rules of OneFlagClass conversion defined in PyQt5 are:
	# 1. | ~= with OneFlagClass return a MultiFlagClass (which is not compatible to int)
	#   Note that this breaks Liskov principle
	# 2. everything else returns int: & ^ &= ^=
	# 3. operations with int return int.

	if OR_CONVERTS_TO_MULTI:
		assert_type_of_value(MultiFlagClass, oneFlagValue1 | oneFlagValue2)
	else:
		assert_type_of_value(int, oneFlagValue1 | oneFlagValue2)

	assert_type_of_value(int, ~oneFlagValue1)
	assert_type_of_value(int, oneFlagValue1 & oneFlagValue2)
	assert_type_of_value(int, oneFlagValue1 ^ oneFlagValue2)

	# right operand
	if OR_INT_CONVERTS_TO_MULTI:
		assert_type_of_value(MultiFlagClass, oneFlagValue1 | 33)
	else:
		assert_type_of_value(int, oneFlagValue1 | 33)
	assert_type_of_value(int, oneFlagValue1 & 33)
	assert_type_of_value(int, oneFlagValue1 ^ 33)
	assert_type_of_value(int, oneFlagValue1 + 33)
	assert_type_of_value(int, oneFlagValue1 - 33)

	# left operand
	if INT_OR_CONVERTS_TO_MULTI:
		assert_type_of_value(MultiFlagClass, 33 | oneFlagValue1)
	else:
		assert_type_of_value(int, 33 | oneFlagValue1)
	assert_type_of_value(int, 33 & oneFlagValue1)
	assert_type_of_value(int, 33 ^ oneFlagValue1)
	assert_type_of_value(int, 33 + oneFlagValue1)
	assert_type_of_value(int, 33 - oneFlagValue1)

	oneOrMultiFlagValueTest = oneFlagValue1	# reset type and value
	assert_type_of_value(OneFlagClass, oneOrMultiFlagValueTest)
	oneOrMultiFlagValueTest |= oneFlagValue2
	if OR_CONVERTS_TO_MULTI:
		assert_type_of_value(MultiFlagClass, oneOrMultiFlagValueTest)   # nice violation of Liskov principle here
	else:
		assert_type_of_value(int, oneOrMultiFlagValueTest)

	oneFlagOrIntValue = oneFlagValue1	# reset type and value
	assert_type_of_value(OneFlagClass, oneFlagOrIntValue)
	oneFlagOrIntValue |= 33
	if OR_INT_CONVERTS_TO_MULTI:
		assert_type_of_value(MultiFlagClass, oneFlagOrIntValue)
	else:
		assert_type_of_value(int, oneFlagOrIntValue)

	oneFlagOrIntValue = oneFlagValue1	# reset type and value
	assert_type_of_value(OneFlagClass, oneFlagOrIntValue)
	oneFlagOrIntValue &= 33
	assert_type_of_value(int, oneFlagOrIntValue)

	oneFlagOrIntValue = oneFlagValue1	# reset type and value
	assert_type_of_value(OneFlagClass, oneFlagOrIntValue)
	oneFlagOrIntValue &= oneFlagValue2
	assert_type_of_value(int, oneFlagOrIntValue)

	oneFlagOrIntValue = oneFlagValue1	# reset type and value
	assert_type_of_value(OneFlagClass, oneFlagOrIntValue)
	oneFlagOrIntValue ^= 33
	assert_type_of_value(int, oneFlagOrIntValue)

	oneFlagOrIntValue = oneFlagValue1	# reset type and value
	assert_type_of_value(OneFlagClass, oneFlagOrIntValue)
	oneFlagOrIntValue ^= oneFlagValue2
	assert_type_of_value(int, oneFlagOrIntValue)



def test_on_multi_flag_class() -> None:
	oneFlagValue1 = oneFlagRefValue1
	multiFlagValue1 = MultiFlagClass()
	multiFlagValue2 = MultiFlagClass()
	multiFlagValueTest = multiFlagValue1     # type: MultiFlagClass
	intValue = 0

	assert_type_of_value(OneFlagClass, oneFlagValue1)
	assert_type_of_value(MultiFlagClass, multiFlagValue1)
	assert_type_of_value(MultiFlagClass, multiFlagValue2)
	assert_type_of_value(MultiFlagClass, multiFlagValueTest)
	assert_type_of_value(int, intValue)


	# MultiFlagClass may be created by combining MultiFlagClass together
	assert_type_of_value(MultiFlagClass,  ~multiFlagValue1 )
	assert_type_of_value(MultiFlagClass,  multiFlagValue1 | multiFlagValue2 )
	assert_type_of_value(MultiFlagClass,  multiFlagValue1 & multiFlagValue2 )
	assert_type_of_value(MultiFlagClass,  multiFlagValue1 ^ multiFlagValue2 )


	# MultiFlagClass may be created by combining MultiFlagClass and OneFlagClass, left or right
	assert_type_of_value(MultiFlagClass,  multiFlagValue1 | oneFlagValue1 )
	assert_type_of_value(MultiFlagClass,  multiFlagValue1 & oneFlagValue1 )
	assert_type_of_value(MultiFlagClass,  multiFlagValue1 ^ oneFlagValue1 )

	assert_type_of_value(MultiFlagClass,  oneFlagValue1 | multiFlagValue1 )
	assert_type_of_value(MultiFlagClass,  oneFlagValue1 & multiFlagValue1 )
	assert_type_of_value(MultiFlagClass,  oneFlagValue1 ^ multiFlagValue1 )


	# MultClassFlag may be created by combining MultiFlagClass and int, right only
	assert_type_of_value(MultiFlagClass, multiFlagValue1 | 33)
	assert_type_of_value(MultiFlagClass, multiFlagValue1 & 33)
	assert_type_of_value(MultiFlagClass, multiFlagValue1 ^ 33)


	# this is rejected by mypy and is slightly annoying: you can not pass a OneFlagClass variable to a method expecting a MultiFlagClass
	# explicit typing must be used on those methods to accept both OneFlagClass and MultiFlagClass
	multiFlagValueTest = oneFlagValue1   # type: ignore

	# correct way to do it
	multiFlagValueTest = MultiFlagClass(oneFlagValue1)
	assert_type_of_value(MultiFlagClass, multiFlagValueTest)

	# this is rejected for the same reason as for OneFlagClass.
	intValue = multiFlagValueTest      # type: ignore

	# correct way to do it
	intValue = int(multiFlagValueTest)
	assert_type_of_value(int, intValue)

	# rejected by mypy rightfully
	multiFlagValueTest = 33            # type: ignore

	# correct way to do it
	multiFlagValueTest = MultiFlagClass(33)

	# assignments operations with OneFlagClass
	assert_type_of_value(MultiFlagClass, multiFlagValueTest)
	multiFlagValueTest |= oneFlagValue1
	assert_type_of_value(MultiFlagClass, multiFlagValueTest)

	assert_type_of_value(MultiFlagClass, multiFlagValueTest)
	multiFlagValueTest &= oneFlagValue1
	assert_type_of_value(MultiFlagClass, multiFlagValueTest)

	assert_type_of_value(MultiFlagClass, multiFlagValueTest)
	multiFlagValueTest ^= oneFlagValue1
	assert_type_of_value(MultiFlagClass, multiFlagValueTest)

	# assignments operations with int
	assert_type_of_value(MultiFlagClass, multiFlagValueTest)
	multiFlagValueTest |= 33
	assert_type_of_value(MultiFlagClass, multiFlagValueTest)

	assert_type_of_value(MultiFlagClass, multiFlagValueTest)
	multiFlagValueTest &= 33
	assert_type_of_value(MultiFlagClass, multiFlagValueTest)

	assert_type_of_value(MultiFlagClass, multiFlagValueTest)
	multiFlagValueTest ^= 33
	assert_type_of_value(MultiFlagClass, multiFlagValueTest)

	#########################################################3
	#
	#        Exploring errors
	#
	#########################################################3

	# This checks the following:
	# + and - operations are not supported on MultiFlagClass
	# combining int with MultiFlagClass does not work

	pytest.raises(TypeError, lambda: 33 | multiFlagValue1 )	# type: ignore[operator]
	pytest.raises(TypeError, lambda: 33 & multiFlagValue1 )	# type: ignore[operator]
	pytest.raises(TypeError, lambda: 33 ^ multiFlagValue1 )	# type: ignore[operator]

	pytest.raises(TypeError, lambda: multiFlagValue1 + multiFlagValue2 )	# type: ignore[operator]
	pytest.raises(TypeError, lambda: multiFlagValue1 - multiFlagValue2 )	# type: ignore[operator]
	pytest.raises(TypeError, lambda: multiFlagValue1 + oneFlagValue1)	# type: ignore[operator]
	pytest.raises(TypeError, lambda: multiFlagValue1 - oneFlagValue1)	# type: ignore[operator]
	pytest.raises(TypeError, lambda: multiFlagValue1 + 33)				# type: ignore[operator]
	pytest.raises(TypeError, lambda: multiFlagValue1 - 33)				# type: ignore[operator]
	pytest.raises(TypeError, lambda: oneFlagValue1 + multiFlagValue1)	# type: ignore[operator]
	pytest.raises(TypeError, lambda: oneFlagValue1 - multiFlagValue1)	# type: ignore[operator]
	pytest.raises(TypeError, lambda: 33 + multiFlagValue1)				# type: ignore[operator]
	pytest.raises(TypeError, lambda: 33 - multiFlagValue1)				# type: ignore[operator]

	def f1() -> None:
		multiFlagValueTest = MultiFlagClass()
		multiFlagValueTest += oneFlagValue1	  # type: ignore[assignment, operator]
	def f2() -> None:
		multiFlagValueTest = MultiFlagClass()
		multiFlagValueTest += 33	  # type: ignore[assignment, operator]
	def f3() -> None:
		multiFlagValueTest = MultiFlagClass()
		multiFlagValueTest -= oneFlagValue1	  # type: ignore[assignment, operator]
	def f4() -> None:
		multiFlagValueTest = MultiFlagClass()
		multiFlagValueTest -= 33	  # type: ignore[assignment, operator]

	pytest.raises(TypeError, f1)
	pytest.raises(TypeError, f2)
	pytest.raises(TypeError, f3)
	pytest.raises(TypeError, f4)

