from typing import Union

from PyQt5.QtCore import pyqtSlot, QObject

@pyqtSlot(str)
def func_none(s: str) -> None:
    return

@pyqtSlot(str, result=int)
def func_int(s: str) -> int:
    return 42

@pyqtSlot(str, result='int')    # this means int here
def func_str(s: str) -> str:
    return '42'

@pyqtSlot(str, name='toto', revision=33, result=int)
def func_toto(s: str) -> int:
    return 33

n = None
n = func_none("test")

i = 0
i = func_int("test")

s = ''
s = func_str('test')

print( func_toto('123') )

### Other example extracted from pyqtSlot documentation

class Foo(QObject):

    @pyqtSlot()
    def foo_noarg(self) -> None:
        """ C++: void foo() """
        pass

    @pyqtSlot(int, str)
    def foo_int_str(self, arg1: int, arg2: str) -> None:
        """ C++: void foo(int, QString) """
        pass

    @pyqtSlot(int, name='bar')
    def foo_int(self, arg1: int) -> None:
        """ C++: void bar(int) """
        pass

    @pyqtSlot(int, result=int)
    def foo_int2(self, arg1: int) -> int:
        """ C++: int foo(int) """
        pass

    # make sure that the return type is type-checked
    @pyqtSlot(int, result=int)  # type: ignore[arg-type]
    def foo_int_with_return_arg_error(self, arg1: int) -> str:
        """ C++: int foo(int) """
        pass

    # mypy can not typecheck the pyqtSlot() arguments vs method arguments
    @pyqtSlot(int, result=int)
    def foo_int_with_arg_error(self, arg1: str) -> int:
        """ C++: int foo(int) """
        pass

    @pyqtSlot(int, QObject)
    def foo_qobject(self, arg1: QObject) -> None:
        """ C++: int foo(int, QObject *) """
        pass

    @pyqtSlot(int)
    @pyqtSlot('QString')
    def valueChanged(self, value: Union[int, str]) -> None:
        """ Two slots will be defined in the QMetaObject. """
        pass


f = Foo()

n = f.foo_noarg()

n = f.foo_int_str(33, 'abc')

n = f.foo_int(33)

i = f.foo_int2(33)

n = f.foo_qobject(QObject())

n = f.valueChanged(33)
n = f.valueChanged('abc')
