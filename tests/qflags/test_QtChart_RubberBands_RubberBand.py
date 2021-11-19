# mypy: no-warn-unreachable

import sys
from typing import Union
if sys.version_info[:2] >= (3,8):
	from typing import Literal
else:
	from typing_extensions import Literal
import pytest

### Specific part
# file generated from qflags_test_template.py for QFlags class "QChartView.RubberBands" and flag class "QChartView.RubberBand"
from PyQt5 import QtChart

OneFlagClass = QtChart.QChartView.RubberBand
MultiFlagClass = QtChart.QChartView.RubberBands

oneFlagRefValue1 = QtChart.QChartView.RubberBand.NoRubberBand
oneFlagRefValue2 = QtChart.QChartView.RubberBand.VerticalRubberBand

OR_CONVERTS_TO_MULTI: Literal[False] = False
OR_INT_CONVERTS_TO_MULTI: Literal[False] = False
INT_OR_CONVERTS_TO_MULTI: Literal[False] = False
SUPPORTS_ONE_OP_MULTI: Literal[True] = True
### End of specific part

def assert_type_of_value_int(value: int) -> None:
	'''Raise an exception if the value is not of type expected_type'''
	assert isinstance(value, int)

def assert_type_of_value_oneFlag(value: OneFlagClass) -> None:
	'''Raise an exception if the value is not of type expected_type'''
	assert type(value) == OneFlagClass

def assert_type_of_value_multiFlag(value: MultiFlagClass) -> None:
	'''Raise an exception if the value is not of type expected_type'''
	assert type(value) == MultiFlagClass



def test_on_one_flag_class() -> None:
	oneFlagValue1 = oneFlagRefValue1
	oneFlagValue2 = oneFlagRefValue2
	oneFlagValueTest = oneFlagValue1    # type: OneFlagClass
	intValue = 0                    # type: int
	oneOrMultiFlagValueTest = oneFlagValue1		# type: Union[OneFlagClass, MultiFlagClass]
	oneFlagOrIntValue = oneFlagValue1	# type: Union[int, OneFlagClass]

	# upcast from OneFlagClass to int
	intValue = oneFlagValue1

	# conversion also accepted
	intValue = int(oneFlagValue1)

	# this is not supported type-safely for a good reason
	oneFlagValueTest = 1		# type: ignore

	# correct way to do it
	oneFlagValueTest = OneFlagClass(1)
	oneFlagValueTest = OneFlagClass(oneFlagValue1)

	# The rules of OneFlagClass conversion defined in PyQt5 are:
	# 1. | ~= with OneFlagClass return a MultiFlagClass (which is not compatible to int)
	#   Note that this breaks Liskov principle
	# 2. everything else returns int: & ^ &= ^=
	# 3. operations with int return int.

	if OR_CONVERTS_TO_MULTI:
		assert_type_of_value_multiFlag(oneFlagValue1 | oneFlagValue2)
	else:
		assert_type_of_value_int(oneFlagValue1 | oneFlagValue2)

	assert_type_of_value_int(~oneFlagValue1)
	assert_type_of_value_int(oneFlagValue1 & oneFlagValue2)
	assert_type_of_value_int(oneFlagValue1 ^ oneFlagValue2)

	# right operand
	if OR_INT_CONVERTS_TO_MULTI:
		assert_type_of_value_multiFlag(oneFlagValue1 | 1)
	else:
		assert_type_of_value_int(oneFlagValue1 | 1)
	assert_type_of_value_int(oneFlagValue1 & 1)
	assert_type_of_value_int(oneFlagValue1 ^ 1)
	assert_type_of_value_int(oneFlagValue1 + 1)
	assert_type_of_value_int(oneFlagValue1 - 1)

	# left operand
	if INT_OR_CONVERTS_TO_MULTI:
		assert_type_of_value_multiFlag(1 | oneFlagValue1)
	else:
		assert_type_of_value_int(1 | oneFlagValue1)
	assert_type_of_value_int(1 & oneFlagValue1)
	assert_type_of_value_int(1 ^ oneFlagValue1)
	assert_type_of_value_int(1 + oneFlagValue1)
	assert_type_of_value_int(1 - oneFlagValue1)

	if OR_CONVERTS_TO_MULTI:
		oneOrMultiFlagValueTest = oneFlagValue1  # reset type and value
		assert_type_of_value_oneFlag(oneOrMultiFlagValueTest)
		oneOrMultiFlagValueTest |= oneFlagValue2
		assert_type_of_value_multiFlag(oneOrMultiFlagValueTest)   # nice violation of Liskov principle here
	else:
		oneFlagOrIntValue = oneFlagValue1  # reset type and value
		assert_type_of_value_oneFlag(oneFlagOrIntValue)
		oneFlagOrIntValue |= oneFlagValue2
		assert_type_of_value_int(oneFlagOrIntValue)

	if OR_INT_CONVERTS_TO_MULTI:
		oneOrMultiFlagValueTest = oneFlagValue1  # reset type and value
		assert_type_of_value_oneFlag(oneOrMultiFlagValueTest)
		oneOrMultiFlagValueTest |= 1
		assert_type_of_value_multiFlag(oneOrMultiFlagValueTest)
	else:
		oneFlagOrIntValue = oneFlagValue1  # reset type and value
		assert_type_of_value_oneFlag(oneFlagOrIntValue)
		oneFlagOrIntValue |= 1
		assert_type_of_value_int(oneFlagOrIntValue)

	oneFlagOrIntValue = oneFlagValue1	# reset type and value
	assert_type_of_value_oneFlag(oneFlagOrIntValue)
	oneFlagOrIntValue &= 1
	assert_type_of_value_int(oneFlagOrIntValue)

	oneFlagOrIntValue = oneFlagValue1	# reset type and value
	assert_type_of_value_oneFlag(oneFlagOrIntValue)
	oneFlagOrIntValue &= oneFlagValue2
	assert_type_of_value_int(oneFlagOrIntValue)

	oneFlagOrIntValue = oneFlagValue1	# reset type and value
	assert_type_of_value_oneFlag(oneFlagOrIntValue)
	oneFlagOrIntValue ^= 1
	assert_type_of_value_int(oneFlagOrIntValue)

	oneFlagOrIntValue = oneFlagValue1	# reset type and value
	assert_type_of_value_oneFlag(oneFlagOrIntValue)
	oneFlagOrIntValue ^= oneFlagValue2
	assert_type_of_value_int(oneFlagOrIntValue)



def test_on_multi_flag_class() -> None:
	oneFlagValue1 = oneFlagRefValue1
	multiFlagValue1 = MultiFlagClass()
	multiFlagValue2 = MultiFlagClass()
	multiFlagValueTest = multiFlagValue1     # type: MultiFlagClass
	intValue = 0

	assert_type_of_value_oneFlag(oneFlagValue1)
	assert_type_of_value_multiFlag(multiFlagValue1)
	assert_type_of_value_multiFlag(multiFlagValue2)
	assert_type_of_value_multiFlag(multiFlagValueTest)
	assert_type_of_value_int(intValue)


	# MultiFlagClass may be created by combining MultiFlagClass together
	assert_type_of_value_multiFlag( ~multiFlagValue1 )
	assert_type_of_value_multiFlag( multiFlagValue1 | multiFlagValue2 )
	assert_type_of_value_multiFlag( multiFlagValue1 & multiFlagValue2 )
	assert_type_of_value_multiFlag( multiFlagValue1 ^ multiFlagValue2 )


	# MultiFlagClass may be created by combining MultiFlagClass and OneFlagClass, left or right
	assert_type_of_value_multiFlag( multiFlagValue1 | oneFlagValue1 )
	assert_type_of_value_multiFlag( multiFlagValue1 & oneFlagValue1 )
	assert_type_of_value_multiFlag( multiFlagValue1 ^ oneFlagValue1 )

	if SUPPORTS_ONE_OP_MULTI:
		assert_type_of_value_multiFlag( oneFlagValue1 | multiFlagValue1 )
		assert_type_of_value_multiFlag( oneFlagValue1 & multiFlagValue1 )
		assert_type_of_value_multiFlag( oneFlagValue1 ^ multiFlagValue1 )


	# MultClassFlag may be created by combining MultiFlagClass and int, right only
	assert_type_of_value_multiFlag(multiFlagValue1 | 1)
	assert_type_of_value_multiFlag(multiFlagValue1 & 1)
	assert_type_of_value_multiFlag(multiFlagValue1 ^ 1)


	# this is rejected by mypy and is slightly annoying: you can not pass a OneFlagClass variable to a method expecting a MultiFlagClass
	# explicit typing must be used on those methods to accept both OneFlagClass and MultiFlagClass
	multiFlagValueTest = oneFlagValue1   # type: ignore

	# correct way to do it
	multiFlagValueTest = MultiFlagClass(oneFlagValue1)
	assert_type_of_value_multiFlag(multiFlagValueTest)

	# this is rejected for the same reason as for OneFlagClass.
	intValue = multiFlagValueTest      # type: ignore

	# correct way to do it
	intValue = int(multiFlagValueTest)
	assert_type_of_value_int(intValue)

	# rejected by mypy rightfully
	multiFlagValueTest = 1            # type: ignore

	# correct way to do it
	multiFlagValueTest = MultiFlagClass(1)

	# assignments operations with OneFlagClass
	assert_type_of_value_multiFlag(multiFlagValueTest)
	multiFlagValueTest |= oneFlagValue1
	assert_type_of_value_multiFlag(multiFlagValueTest)

	assert_type_of_value_multiFlag(multiFlagValueTest)
	multiFlagValueTest &= oneFlagValue1
	assert_type_of_value_multiFlag(multiFlagValueTest)

	assert_type_of_value_multiFlag(multiFlagValueTest)
	multiFlagValueTest ^= oneFlagValue1
	assert_type_of_value_multiFlag(multiFlagValueTest)

	# assignments operations with int
	assert_type_of_value_multiFlag(multiFlagValueTest)
	multiFlagValueTest |= 1
	assert_type_of_value_multiFlag(multiFlagValueTest)

	assert_type_of_value_multiFlag(multiFlagValueTest)
	multiFlagValueTest &= 1
	assert_type_of_value_multiFlag(multiFlagValueTest)

	assert_type_of_value_multiFlag(multiFlagValueTest)
	multiFlagValueTest ^= 1
	assert_type_of_value_multiFlag(multiFlagValueTest)

	#########################################################1
	#
	#        Exploring errors
	#
	#########################################################1

	if not SUPPORTS_ONE_OP_MULTI:
		pytest.raises(TypeError, lambda: oneFlagValue1 | multiFlagValue1)  # type: ignore[operator]
		pytest.raises(TypeError, lambda: oneFlagValue1 & multiFlagValue1)  # type: ignore[operator]
		pytest.raises(TypeError, lambda: oneFlagValue1 ^ multiFlagValue1)  # type: ignore[operator]

	pytest.raises(TypeError, lambda: 1 | multiFlagValue1 )	# type: ignore[operator]
	pytest.raises(TypeError, lambda: 1 & multiFlagValue1 )	# type: ignore[operator]
	pytest.raises(TypeError, lambda: 1 ^ multiFlagValue1 )	# type: ignore[operator]

	# This checks the following:
	# + and - operations are not supported on MultiFlagClass
	# combining int with MultiFlagClass does not work
	pytest.raises(TypeError, lambda: multiFlagValue1 + multiFlagValue2 )	# type: ignore[operator]
	pytest.raises(TypeError, lambda: multiFlagValue1 - multiFlagValue2 )	# type: ignore[operator]
	pytest.raises(TypeError, lambda: multiFlagValue1 + oneFlagValue1)	# type: ignore[operator]
	pytest.raises(TypeError, lambda: multiFlagValue1 - oneFlagValue1)	# type: ignore[operator]
	pytest.raises(TypeError, lambda: multiFlagValue1 + 1)				# type: ignore[operator]
	pytest.raises(TypeError, lambda: multiFlagValue1 - 1)				# type: ignore[operator]
	pytest.raises(TypeError, lambda: oneFlagValue1 + multiFlagValue1)	# type: ignore[operator]
	pytest.raises(TypeError, lambda: oneFlagValue1 - multiFlagValue1)	# type: ignore[operator]
	pytest.raises(TypeError, lambda: 1 + multiFlagValue1)				# type: ignore[operator]
	pytest.raises(TypeError, lambda: 1 - multiFlagValue1)				# type: ignore[operator]

	def f1() -> None:
		multiFlagValueTest = MultiFlagClass()
		multiFlagValueTest += oneFlagValue1	  # type: ignore[assignment, operator]
	def f2() -> None:
		multiFlagValueTest = MultiFlagClass()
		multiFlagValueTest += 1	  # type: ignore[assignment, operator]
	def f3() -> None:
		multiFlagValueTest = MultiFlagClass()
		multiFlagValueTest -= oneFlagValue1	  # type: ignore[assignment, operator]
	def f4() -> None:
		multiFlagValueTest = MultiFlagClass()
		multiFlagValueTest -= 1	  # type: ignore[assignment, operator]

	pytest.raises(TypeError, f1)
	pytest.raises(TypeError, f2)
	pytest.raises(TypeError, f3)
	pytest.raises(TypeError, f4)

