<img src="http://mypy-lang.org/static/mypy_light.svg" alt="mypy logo" width="300px"/>

[![PyPI version](https://badge.fury.io/py/PyQt5-stubs.svg)](https://badge.fury.io/py/PyQt5-stubs)
[![mypy checked](https://camo.githubusercontent.com/34b3a249cd6502d0a521ab2f42c8830b7cfd03fa/687474703a2f2f7777772e6d7970792d6c616e672e6f72672f7374617469632f6d7970795f62616467652e737667)](http://mypy-lang.org/)
[![Build Status](https://github.com/python-qt-tools/PyQt5-stubs/actions/workflows/ci.yml/badge.svg?query=branch%3Amaster)](https://github.com/python-qt-tools/PyQt5-stubs/actions/workflows/ci.yml?query=branch%3Amaster)
[![Downloads](https://pepy.tech/badge/pyqt5-stubs)](https://pepy.tech/project/pyqt5-stubs)
[![Downloads](https://pepy.tech/badge/pyqt5-stubs/week)](https://pepy.tech/project/pyqt5-stubs/week)

# Mypy stubs for the PyQt5 framework

This repository holds the stubs of the PyQt5 framework. The stub files released
within the PyQt5 packages have been modified to allow using them for type-checking via mypy. 
Improvements over the default stubs include:

* Signals are properly typed as signals and not as methods
* QFlags derived classes correctly support all combination operations
* Many methods accepting an optional None have been annotated so
* and more...

This repository can always be improved and the authors will
appreciate any PRs or Issues that help making this stub-repository more reliable.

# Installation

Simply install PyQt5-stubs with pip:

    $ pip install PyQt5-stubs

Or clone the latest version from Github and install it via Python setuptools:

    $ git clone https://github.com/python-qt-tools/PyQt5-stubs
    $ python setup.py install


# Supported Modules

The modules supported by PyQt5-stubs include modules from the PyQt5 package as well as modules from the other
packages released by Riverbank Computing (PyQt3D, PyQtCharts, ...). Here is the full list
of packages and modules:

* package PyQt5:
    * QtBluetooth
    * QtCore
    * QtDBus
    * QtGui
    * QtLocation
    * QtMultimedia
    * QtNetwork
    * QtNfc
    * QtOpenGL
    * QtPositioning
    * QtPrintSupport
    * QtQml
    * QtQuick
    * QtQuickWidgets
    * QtRemoteObjects
    * QtSensors
    * QtSerialPort
    * QtSql
    * QtSvg
    * QtTest
    * QtWebChannel
    * QtWebSockets
    * QtWidgets
    * QtX11Extras
    * QtXml
    * QtXmlPatterns
    * sip
* package PyQt3D:
    * Qt3DAnimation
    * Qt3DCore
    * Qt3DExtras
    * Qt3DInput
    * Qt3DLogic
    * Qt3DRender
* package PyQtChart:
    * QtChart
* package PyQtDataVisualization:
    * QtDataVisualization
* package PyQtNetworkAuth:
    * QtNetworkAuth
* package PyQtPurchasing:
    * QtPurchasing
* package PyQtWebEngine:
    * QtWebEngine
    * QtWebEngineCore
    * QtWebEngineWidgets
* package PyQtWebkit:
    * QtWebKit
    * QtWebKitWidgets
  
# Authors
* Stefan Lehmann
* Kyle Altendorf 
* Bryce Beagle 
* Florian Bruhin
* Philippe Fremy
