from typing import Callable, Dict, Any, List, Optional

import libcst as cst
import libcst.matchers as matchers

stubtest_output = '''
error: PyQt5.QtBluetooth.QBluetoothDeviceInfo.Field.__new__ is inconsistent, stub argument "__x" differs from runtime argument "value"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtBluetooth.QBluetoothDeviceInfo.Field.__new__ is inconsistent, stub argument "__x" has a default value but runtime argument does not
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtBluetooth.QBluetoothDeviceInfo.Field.__new__ is inconsistent, stub argument "__x" should be positional or keyword (remove leading double underscore)
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtBluetooth.QBluetoothDeviceInfo.Field.__new__ is inconsistent, runtime does not have argument "base"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtCore.QAbstractItemModel.CheckIndexOption.__new__ is inconsistent, stub argument "__x" differs from runtime argument "value"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtCore.QAbstractItemModel.CheckIndexOption.__new__ is inconsistent, stub argument "__x" has a default value but runtime argument does not
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtCore.QAbstractItemModel.CheckIndexOption.__new__ is inconsistent, stub argument "__x" should be positional or keyword (remove leading double underscore)
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtCore.QAbstractItemModel.CheckIndexOption.__new__ is inconsistent, runtime does not have argument "base"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtCore.QByteArray.Base64DecodingStatus.__new__ is inconsistent, stub argument "__x" differs from runtime argument "value"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtCore.QByteArray.Base64DecodingStatus.__new__ is inconsistent, stub argument "__x" has a default value but runtime argument does not
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtCore.QByteArray.Base64DecodingStatus.__new__ is inconsistent, stub argument "__x" should be positional or keyword (remove leading double underscore)
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtCore.QByteArray.Base64DecodingStatus.__new__ is inconsistent, runtime does not have argument "base"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtCore.QCborKnownTags.__new__ is inconsistent, stub argument "__x" differs from runtime argument "value"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtCore.QCborKnownTags.__new__ is inconsistent, stub argument "__x" has a default value but runtime argument does not
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtCore.QCborKnownTags.__new__ is inconsistent, stub argument "__x" should be positional or keyword (remove leading double underscore)
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtCore.QCborKnownTags.__new__ is inconsistent, runtime does not have argument "base"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtCore.QCborSimpleType.__new__ is inconsistent, stub argument "__x" differs from runtime argument "value"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtCore.QCborSimpleType.__new__ is inconsistent, stub argument "__x" has a default value but runtime argument does not
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtCore.QCborSimpleType.__new__ is inconsistent, stub argument "__x" should be positional or keyword (remove leading double underscore)
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtCore.QCborSimpleType.__new__ is inconsistent, runtime does not have argument "base"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtCore.QDateTime.YearRange.__new__ is inconsistent, stub argument "__x" differs from runtime argument "value"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtCore.QDateTime.YearRange.__new__ is inconsistent, stub argument "__x" has a default value but runtime argument does not
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtCore.QDateTime.YearRange.__new__ is inconsistent, stub argument "__x" should be positional or keyword (remove leading double underscore)
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtCore.QDateTime.YearRange.__new__ is inconsistent, runtime does not have argument "base"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtCore.Qt.HighDpiScaleFactorRoundingPolicy.__new__ is inconsistent, stub argument "__x" differs from runtime argument "value"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtCore.Qt.HighDpiScaleFactorRoundingPolicy.__new__ is inconsistent, stub argument "__x" has a default value but runtime argument does not
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtCore.Qt.HighDpiScaleFactorRoundingPolicy.__new__ is inconsistent, stub argument "__x" should be positional or keyword (remove leading double underscore)
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtCore.Qt.HighDpiScaleFactorRoundingPolicy.__new__ is inconsistent, runtime does not have argument "base"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtGui.QColorSpace.Primaries.__new__ is inconsistent, stub argument "__x" differs from runtime argument "value"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtGui.QColorSpace.Primaries.__new__ is inconsistent, stub argument "__x" has a default value but runtime argument does not
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtGui.QColorSpace.Primaries.__new__ is inconsistent, stub argument "__x" should be positional or keyword (remove leading double underscore)
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtGui.QColorSpace.Primaries.__new__ is inconsistent, runtime does not have argument "base"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtGui.QColorSpace.TransferFunction.__new__ is inconsistent, stub argument "__x" differs from runtime argument "value"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtGui.QColorSpace.TransferFunction.__new__ is inconsistent, stub argument "__x" has a default value but runtime argument does not
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtGui.QColorSpace.TransferFunction.__new__ is inconsistent, stub argument "__x" should be positional or keyword (remove leading double underscore)
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtGui.QColorSpace.TransferFunction.__new__ is inconsistent, runtime does not have argument "base"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtGui.QTextBlockFormat.MarkerType.__new__ is inconsistent, stub argument "__x" differs from runtime argument "value"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtGui.QTextBlockFormat.MarkerType.__new__ is inconsistent, stub argument "__x" has a default value but runtime argument does not
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtGui.QTextBlockFormat.MarkerType.__new__ is inconsistent, stub argument "__x" should be positional or keyword (remove leading double underscore)
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtGui.QTextBlockFormat.MarkerType.__new__ is inconsistent, runtime does not have argument "base"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNetwork.QOcspCertificateStatus.__new__ is inconsistent, stub argument "__x" differs from runtime argument "value"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNetwork.QOcspCertificateStatus.__new__ is inconsistent, stub argument "__x" has a default value but runtime argument does not
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNetwork.QOcspCertificateStatus.__new__ is inconsistent, stub argument "__x" should be positional or keyword (remove leading double underscore)
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNetwork.QOcspCertificateStatus.__new__ is inconsistent, runtime does not have argument "base"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNetwork.QOcspRevocationReason.__new__ is inconsistent, stub argument "__x" differs from runtime argument "value"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNetwork.QOcspRevocationReason.__new__ is inconsistent, stub argument "__x" has a default value but runtime argument does not
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNetwork.QOcspRevocationReason.__new__ is inconsistent, stub argument "__x" should be positional or keyword (remove leading double underscore)
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNetwork.QOcspRevocationReason.__new__ is inconsistent, runtime does not have argument "base"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNetwork.QSslCertificate.PatternSyntax.__new__ is inconsistent, stub argument "__x" differs from runtime argument "value"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNetwork.QSslCertificate.PatternSyntax.__new__ is inconsistent, stub argument "__x" has a default value but runtime argument does not
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNetwork.QSslCertificate.PatternSyntax.__new__ is inconsistent, stub argument "__x" should be positional or keyword (remove leading double underscore)
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNetwork.QSslCertificate.PatternSyntax.__new__ is inconsistent, runtime does not have argument "base"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNetworkAuth.QAbstractOAuth.ContentType.__new__ is inconsistent, stub argument "__x" differs from runtime argument "value"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNetworkAuth.QAbstractOAuth.ContentType.__new__ is inconsistent, stub argument "__x" has a default value but runtime argument does not
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNetworkAuth.QAbstractOAuth.ContentType.__new__ is inconsistent, stub argument "__x" should be positional or keyword (remove leading double underscore)
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNetworkAuth.QAbstractOAuth.ContentType.__new__ is inconsistent, runtime does not have argument "base"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNetworkAuth.QAbstractOAuth.Error.__new__ is inconsistent, stub argument "__x" differs from runtime argument "value"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNetworkAuth.QAbstractOAuth.Error.__new__ is inconsistent, stub argument "__x" has a default value but runtime argument does not
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNetworkAuth.QAbstractOAuth.Error.__new__ is inconsistent, stub argument "__x" should be positional or keyword (remove leading double underscore)
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNetworkAuth.QAbstractOAuth.Error.__new__ is inconsistent, runtime does not have argument "base"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNetworkAuth.QAbstractOAuth.Stage.__new__ is inconsistent, stub argument "__x" differs from runtime argument "value"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNetworkAuth.QAbstractOAuth.Stage.__new__ is inconsistent, stub argument "__x" has a default value but runtime argument does not
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNetworkAuth.QAbstractOAuth.Stage.__new__ is inconsistent, stub argument "__x" should be positional or keyword (remove leading double underscore)
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNetworkAuth.QAbstractOAuth.Stage.__new__ is inconsistent, runtime does not have argument "base"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNetworkAuth.QAbstractOAuth.Status.__new__ is inconsistent, stub argument "__x" differs from runtime argument "value"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNetworkAuth.QAbstractOAuth.Status.__new__ is inconsistent, stub argument "__x" has a default value but runtime argument does not
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNetworkAuth.QAbstractOAuth.Status.__new__ is inconsistent, stub argument "__x" should be positional or keyword (remove leading double underscore)
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNetworkAuth.QAbstractOAuth.Status.__new__ is inconsistent, runtime does not have argument "base"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNetworkAuth.QOAuth1.SignatureMethod.__new__ is inconsistent, stub argument "__x" differs from runtime argument "value"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNetworkAuth.QOAuth1.SignatureMethod.__new__ is inconsistent, stub argument "__x" has a default value but runtime argument does not
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNetworkAuth.QOAuth1.SignatureMethod.__new__ is inconsistent, stub argument "__x" should be positional or keyword (remove leading double underscore)
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNetworkAuth.QOAuth1.SignatureMethod.__new__ is inconsistent, runtime does not have argument "base"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNetworkAuth.QOAuth1Signature.HttpRequestMethod.__new__ is inconsistent, stub argument "__x" differs from runtime argument "value"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNetworkAuth.QOAuth1Signature.HttpRequestMethod.__new__ is inconsistent, stub argument "__x" has a default value but runtime argument does not
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNetworkAuth.QOAuth1Signature.HttpRequestMethod.__new__ is inconsistent, stub argument "__x" should be positional or keyword (remove leading double underscore)
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNetworkAuth.QOAuth1Signature.HttpRequestMethod.__new__ is inconsistent, runtime does not have argument "base"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNfc.QNearFieldManager.AdapterState.__new__ is inconsistent, stub argument "__x" differs from runtime argument "value"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNfc.QNearFieldManager.AdapterState.__new__ is inconsistent, stub argument "__x" has a default value but runtime argument does not
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNfc.QNearFieldManager.AdapterState.__new__ is inconsistent, stub argument "__x" should be positional or keyword (remove leading double underscore)
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtNfc.QNearFieldManager.AdapterState.__new__ is inconsistent, runtime does not have argument "base"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtTest.QAbstractItemModelTester.FailureReportingMode.__new__ is inconsistent, stub argument "__x" differs from runtime argument "value"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtTest.QAbstractItemModelTester.FailureReportingMode.__new__ is inconsistent, stub argument "__x" has a default value but runtime argument does not
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtTest.QAbstractItemModelTester.FailureReportingMode.__new__ is inconsistent, stub argument "__x" should be positional or keyword (remove leading double underscore)
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtTest.QAbstractItemModelTester.FailureReportingMode.__new__ is inconsistent, runtime does not have argument "base"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtWebEngineCore.QWebEngineUrlScheme.Syntax.__new__ is inconsistent, stub argument "__x" differs from runtime argument "value"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtWebEngineCore.QWebEngineUrlScheme.Syntax.__new__ is inconsistent, stub argument "__x" has a default value but runtime argument does not
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtWebEngineCore.QWebEngineUrlScheme.Syntax.__new__ is inconsistent, stub argument "__x" should be positional or keyword (remove leading double underscore)
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtWebEngineCore.QWebEngineUrlScheme.Syntax.__new__ is inconsistent, runtime does not have argument "base"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtWebEngineWidgets.QWebEnginePage.LifecycleState.__new__ is inconsistent, stub argument "__x" differs from runtime argument "value"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtWebEngineWidgets.QWebEnginePage.LifecycleState.__new__ is inconsistent, stub argument "__x" has a default value but runtime argument does not
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtWebEngineWidgets.QWebEnginePage.LifecycleState.__new__ is inconsistent, stub argument "__x" should be positional or keyword (remove leading double underscore)
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)

error: PyQt5.QtWebEngineWidgets.QWebEnginePage.LifecycleState.__new__ is inconsistent, runtime does not have argument "base"
Stub: at line 181
Overload(def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] =) -> _T`-1, def [_T] (cls: Type[_T`-1], Union[builtins.str, builtins.bytes, builtins.bytearray], base: typing_extensions.SupportsIndex) -> _T`-1)
Inferred signature: def (cls: Type[_T`-1], __x: Union[builtins.str, builtins.bytes, typing.SupportsInt, typing_extensions.SupportsIndex, _typeshed.SupportsTrunc] = ..., base: typing_extensions.SupportsIndex = ...)
Runtime: at line 631 in file D:\program\python38\lib\enum.py
def (cls, value)
'''

class TransformToIntEnumInheritance(cst.CSTTransformer):

    def __init__(self, full_class: str):
        super().__init__()
        self.full_name_stack: List[str] = []
        self.target_class = full_class.split('.')

    def visit_ClassDef(self, node: cst.ClassDef) -> Optional[bool]:
        self.full_name_stack.append( node.name.value )
        return None

    def leave_ClassDef(self, original_node: cst.ClassDef, updated_node: cst.ClassDef) -> cst.ClassDef:
        class_found = False

        if self.full_name_stack == self.target_class:
            class_found = True

        self.full_name_stack.pop()

        if not class_found:
            return updated_node

        if len(updated_node.bases) == 1:
            if updated_node.bases[0].value.value == 'IntEnum':
                print('Already fixed!')
                return updated_node

            if updated_node.bases[0].value.value == 'int':
                print('Fixing...')
                return updated_node.with_changes(
                    bases=(updated_node.bases[0].with_changes(
                        value=updated_node.bases[0].value.with_changes(value='IntEnum')),)
                )

        return updated_node




def fix_stub_class_inheritance_to_int_enum(stub_path: str, full_class: str) -> None:
    '''Fix the stub by replacing "SomeClass(int)" to "SomeClass(IntEnum)"'''
    # open stub file
    # run transformer
    # save stubfile
    with open(stub_path, "r", encoding="utf-8") as fhandle:
        stub_tree = cst.parse_module(fhandle.read())

    print('Fixing module %s class %s' % (stub_path, full_class))
    transformer = TransformToIntEnumInheritance(full_class)
    modified_tree = stub_tree.visit(transformer)

    with open(stub_path, "w", encoding="utf-8") as fhandle:
        fhandle.write(modified_tree.code)
    print('Updated: %s' % stub_path)


def main():
    fixes = set([])

    for line in stubtest_output.split('\n'):
        if line.startswith('error: ') \
                and '__new__ is inconsistent,' in line:
            class_info = line.split(' ')[1]
            stub_module = 'PyQt5-stubs/%s.pyi' % class_info.split('.')[1]
            full_class_name = '.'.join(class_info.split('.')[2:-1])
            fixes.add( (stub_module, full_class_name) )

    for stub, full_class in list(fixes):
        fix_stub_class_inheritance_to_int_enum(stub, full_class)


if __name__ == '__main__':
    main()
