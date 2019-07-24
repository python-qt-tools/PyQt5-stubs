
# Errors in PyQt5-Stubs

## #1 Mixed overloads with static and non-static methods

### Example

```python
class QImageReader(sip.simplewrapper):

    # this is a static method
    @typing.overload
    @staticmethod
    def imageFormat(fileName: str) -> QtCore.QByteArray: ...

    # also static
    @typing.overload
    @staticmethod
    def imageFormat(device: QtCore.QIODevice) -> QtCore.QByteArray: ...

    # non-static
    @typing.overload
    def imageFormat(self) -> QImage.Format: ...
```

**mypy error:**

`Overload does not consistently use the "@staticmethod" decorator on all
function signatures.`

### Solution

None, yet. Backup solution is to use #type: ignore to eleminate the mypy error.


```python
class QImageReader(sip.simplewrapper):

    # this is a static method
    @typing.overload  # type: ignore
    @staticmethod
    def imageFormat(fileName: str) -> QtCore.QByteArray: ...

    # also static
    @typing.overload
    @staticmethod
    def imageFormat(device: QtCore.QIODevice) -> QtCore.QByteArray: ...

    # non-static
    @typing.overload
    def imageFormat(self) -> QImage.Format: ...  # type: ignore
```

## #2 Method signature is incompatible with supertype

### Description

The Liskov substitution principle demands derivated classes to not narrow method
arguments and to not widen method return types. This principle is not always respected
by the Qt5 codebase.

### Example

```python
class QPaintDevice(sip.simplewrapper):
    # ...
    def devicePixelRatio(self) -> int: ...
    # ...


class QPixmap(QPaintDevice):
    # ...
    def devicePixelRatio(self) -> float: ...
    # ...
```

**mypy error:**

`Return type "float" of "devicePixelRatio" incompatible with return type "int" in
supertype "QPaintDevice".`

### Solution

Actually it should be avoided to narrow inputs or broaden outputs of derived classes.
As mypy demands to respect the Liskov substitution principle there is no way to prevent
this error from happening. However, due to the given codebase of PyQt5 and Qt5 itself
the only way to avoid this error from occuring is to use # type: ignore.

```python
class QPaintDevice(sip.simplewrapper):
    # ...
    def devicePixelRatio(self) -> int: ...
    # ...


class QPixmap(QPaintDevice):
    # ...
    def devicePixelRatio(self) -> float: ...  # type: ignore
    # ...
```

## #3 Overloaded function signatures with incompatible return types

### Description

### Example

```python

class QMatrix4x4(sip.simplewrapper):

    @typing.overload
    def map(self, point: QtCore.QPoint) -> QtCore.QPoint: ...
    @typing.overload
    def map(self, point: typing.Union[QtCore.QPointF, QtCore.QPoint]) -> QtCore.QPointF: ...

```

**mypy error:**
`Overloaded function signatures 1 and 2 overlap with incompatible return types.`

### Solution

Fix the function signatures that there is a unique return type for each overload.
Removing the Union in the second signature be the right thing to do in the example.

```
class QMatrix4x4(sip.simplewrapper):

    @typing.overload
    def map(self, point: QtCore.QPoint) -> QtCore.QPoint: ...
    @typing.overload
    def map(self, point: QtCore.QPointF) -> QtCore.QPointF: ...
```

### Occurences

* QtGui.QMatrix4x4.map

## #4 Overloaded function signature will never be matched

### Description

### Example

```python
class QPainter(sip.simplewrapper):
    # ...
    def drawImage(self, r: QtCore.QRect, image: QImage) -> None: ...
    @typing.overload
    def drawImage(self, p: typing.Union[QtCore.QPointF, QtCore.QPoint], image: QImage) -> None: ...
    @typing.overload
    def drawImage(self, p: QtCore.QPoint, image: QImage) -> None: ...
    # ...
```

**mypy error:**
`Overloaded function signature 4 will never be matched: signature 3's parameter type(s)
are the same or broader.`

### Solution


Remove the signature. This would be best to be done while generating the PyQt5 stubs.

```python
class QPainter(sip.simplewrapper):
    # ...
    def drawImage(self, r: QtCore.QRect, image: QImage) -> None: ...
    @typing.overload
    def drawImage(self, p: typing.Union[QtCore.QPointF, QtCore.QPoint], image: QImage) -> None: ...
    # @typing.overload
    # def drawImage(self, p: QtCore.QPoint, image: QImage) -> None: ...
    # ...
```
### Occurences

* QtGui.QPainter.drawImage

## #5 Definitions of base classes are incompatible

### Description

### Example

```python
class QPaintDeviceWindow(QWindow, QPaintDevice):
    # ...
```

**mypy error:**
`Definition of "devicePixelRatio" in base class "QWindow" is incompatible with
definition in base class "QPaintDevice".`

### Solution

This error is due to the Qt5 codebase and can not be fixed without breaking the current
codebase. So silencing the error with # type: ignore seems to be the right way to go.
