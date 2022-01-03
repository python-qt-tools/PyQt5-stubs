# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [unreleased]

### Added
* [#179](https://github.com/python-qt-tools/PyQt5-stubs/pull/179) update to PyQt5 5.15.6
* [#176](https://github.com/python-qt-tools/PyQt5-stubs/pull/176) update to PyQt5 5.15.5
* [#175](https://github.com/python-qt-tools/PyQt5-stubs/pull/175) catch up PyQtNetworkAuth with the 5.15.4 release
* [#149](https://github.com/python-qt-tools/PyQt5-stubs/pull/149) update to PyQt5 5.15.4
* [#138](https://github.com/python-qt-tools/PyQt5-stubs/pull/138) update to PyQt5 5.15.3
* [#145](https://github.com/python-qt-tools/PyQt5-stubs/pull/145) Support all implemented arithmetic operations between Qt.WindowType and Qt.WindowFlags and int
* [#144](https://github.com/python-qt-tools/PyQt5-stubs/pull/144) add `QTreeWidgetItem.__lt__()` to allow sorting of items in a QTreeWidget
* [#143](https://github.com/python-qt-tools/PyQt5-stubs/pull/143) make `bytes(QByteArray())` valid by incorrectly adding `.__bytes__()` until a proper solution is developed upstream
* [#152](https://github.com/python-qt-tools/PyQt5-stubs/pull/152) add `.__or__()` for `QDialogButtonBox.StandardButton` and `QDialogButtonBox.StandardButtons`
* [#156](https://github.com/python-qt-tools/PyQt5-stubs/pull/156) add operators to `QSize` and `QSizeF`
* [#153](https://github.com/python-qt-tools/PyQt5-stubs/pull/153) Support all implemented arithmetic operations for QFlags 
  based classes in modules QtCore, QtWidgets, QtGui, QtNetwork, QtDBus, QtOpenGL, QtPrintsupport, QtSql, QtTest, QtXml
* [#162](https://github.com/python-qt-tools/PyQt5-stubs/pull/162) fixes all method not declared as signals
* [#184](https://github.com/python-qt-tools/PyQt5-stubs/pull/184) Fix missing module variable
   detected by latest mypy 0.930
* [#183](https://github.com/python-qt-tools/PyQt5-stubs/pull/183) Add missing operations on QSize
* [#148](https://github.com/python-qt-tools/PyQt5-stubs/pull/148) add `widgetResizable` parameter to `QScrollArea.__init__()`


## 5.15.2.0

### Added
* [#125](https://github.com/python-qt-tools/PyQt5-stubs/pull/125) on `QtWidgets.QMessageBox`, enumerators are also attributes of their enumerations
* [#99](https://github.com/python-qt-tools/PyQt5-stubs/pull/99) enable mypy's strict mode
* [#92](https://github.com/python-qt-tools/PyQt5-stubs/pull/92) add `Sequence` methods and `.__setitem__()` to `sip.array`
* [#94](https://github.com/python-qt-tools/PyQt5-stubs/pull/94) add several operators to `QIODevice.OpenMode` and `QIODevice.OpenModeFlag`
* [#93](https://github.com/python-qt-tools/PyQt5-stubs/pull/93) test against 3.5, 3.6, 3.7, 3.8, and 3.9
* [#71](https://github.com/python-qt-tools/PyQt5-stubs/pull/71) update to PyQt5 5.15.1
* [#56](https://github.com/python-qt-tools/PyQt5-stubs/pull/56) adds `pyqtBoundSignal.__getitem__()` allowing for indexing
* [#51](https://github.com/python-qt-tools/PyQt5-stubs/pull/51) adds `pyqtBoundSignal.signal` hinted as `str`

### Changed
* [#129](https://github.com/python-qt-tools/PyQt5-stubs/pull/129) fixes `QThread` and `QNetworkAccessManager` signals
* [#109](https://github.com/python-qt-tools/PyQt5-stubs/pull/109) `.__or__()` for `QMessageBox.StandardButton` and `QMessageBox.StandardButtons`
* [#126](https://github.com/python-qt-tools/PyQt5-stubs/pull/126) fix `QCoreApplication.instance()` return type to be optional
* [#102](https://github.com/python-qt-tools/PyQt5-stubs/pull/102) fix `pyqtSlot` parameter typing and overloads
* [#104](https://github.com/python-qt-tools/PyQt5-stubs/pull/104) `sip.voidptr` handles integer values and sequences and takes `self`
* [#103](https://github.com/python-qt-tools/PyQt5-stubs/pull/103) `pyqtBoundSignal.disconnect()`'s `slot` parameter is optional
* [#100](https://github.com/python-qt-tools/PyQt5-stubs/pull/100) fill generic parameter as `sip.array[int]` for QtDataVisualization textures
* [#92](https://github.com/python-qt-tools/PyQt5-stubs/pull/92) remove self from `qDefaultSurfaceFormat()` and `qIdForNode()`
* [#83](https://github.com/python-qt-tools/PyQt5-stubs/pull/83) fixes `sip.array` to be generic
* [#79](https://github.com/python-qt-tools/PyQt5-stubs/pull/79) fixes extra class layer in several modules
* [#57](https://github.com/python-qt-tools/PyQt5-stubs/pull/57) fixes `PYQT_SLOT` to allow callables returning any object
* [#56](https://github.com/python-qt-tools/PyQt5-stubs/pull/56) fixes `pyqtSignal` as a descriptor and moves `.emit()`, `.connect()`, and `.disconnect()` to `pyqtBoundSignal`
* [#54](https://github.com/python-qt-tools/PyQt5-stubs/pull/54) fixes `pyqtSignal.connect()` and `pyqtSignal.disconnect()` to support `QMetaObject.Connection`
* [#59](https://github.com/python-qt-tools/PyQt5-stubs/pull/59) fixes `QGuiApplication.lastWindowClosed` to be a signal
* [#58](https://github.com/python-qt-tools/PyQt5-stubs/pull/50) improves `QObject.findChild` and `QObject.findChildren`
* [#50](https://github.com/python-qt-tools/PyQt5-stubs/pull/50) fixes `QAbstractItemModelTester.FailureReportingMode` attributes
* [#46](https://github.com/python-qt-tools/PyQt5-stubs/pull/46) fixes `QCoreApplication` and `QObject` signals
* [#48](https://github.com/python-qt-tools/PyQt5-stubs/pull/48) fixes some signals for `QClipBoard`, `QWindows`, `QQuickView`, `QQmlApplicationEngine` and `QQmlEngine`
* [#49](https://github.com/python-qt-tools/PyQt5-stubs/pull/49) fixes `QAbstractItemView.setModel()` to accept `None`

### Removed

## 5.14.2.2

### Added

### Changed
* [#43](https://github.com/python-qt-tools/PyQt5-stubs/pull/43) Update stubs to PyQt5 5.14.2

### Removed

## 5.14.2.1

### Added
* [#39](https://github.com/python-qt-tools/PyQt5-stubs/pull/39) Add this changelog file
* [#36](https://github.com/python-qt-tools/PyQt5-stubs/pull/36),
[#41](https://github.com/python-qt-tools/PyQt5-stubs/pull/41)
New build script for upstream stubs includes extra packages like `QtWebEngine` and `Qt3D`

### Changed
* [#38](https://github.com/python-qt-tools/PyQt5-stubs/pull/38) Changed license to GPLv3 to be compilient with PyQt5 license

### Removed
