<img src="http://mypy-lang.org/static/mypy_light.svg" alt="mypy logo" width="300px"/>

[![PyPI version](https://badge.fury.io/py/PyQt5-stubs.svg)](https://badge.fury.io/py/PyQt5-stubs)
[![mypy checked](https://camo.githubusercontent.com/34b3a249cd6502d0a521ab2f42c8830b7cfd03fa/687474703a2f2f7777772e6d7970792d6c616e672e6f72672f7374617469632f6d7970795f62616467652e737667)](http://mypy-lang.org/)
[![Build Status](https://github.com/python-qt-tools/PyQt5-stubs/actions/workflows/ci.yml/badge.svg?query=branch%3Amaster)](https://github.com/python-qt-tools/PyQt5-stubs/actions/workflows/ci.yml?query=branch%3Amaster)
[![Downloads](https://pepy.tech/badge/pyqt5-stubs)](https://pepy.tech/project/pyqt5-stubs)
[![Downloads](https://pepy.tech/badge/pyqt5-stubs/week)](https://pepy.tech/project/pyqt5-stubs/week)

# Mypy stubs for the PyQt5 framework

This repository holds the stubs of the PyQt5 framework. It uses the stub files that are
produced during compilation process of PyQt5. These stub files have been modified by the author
to allow using them for type-checking via Mypy. This repository is far from complete and the author will
appreciate any PRs or Issues that help making this stub-repository more reliable.

# Installation

Simply install PyQt5-stubs with pip:

    $ pip install PyQt5-stubs

Or clone the latest version from Github and install it via Python setuptools:

    $ git clone https://github.com/python-qt-tools/PyQt5-stubs
    $ python setup.py install


# Supported Modules

The following modules are supported by PyQt5-stubs:

* QtCore
* QtWidgets
* QtGui
* QtDBus
* QtNetwork
* QtOpenGL
* QtPrintSupport
* QtSql
* QtTest
* QtXml
* sip

# Building upstream stubs
The Dockerfile is used to build all of the stubs for the upstream PyQt5 modules.
The Dockerfile consists of multiple build layers:
* core: `PyQt5`
* `PyQt3D`
* `PyQtChart`
* `PyQtDataVisualization`
* `PyQtPurchasing`
* `PyQtWebEngine`
* an output layer

Each module build layer deposits its stub files within `/output/` in its
filesystem. The output layer then collects the contents of each into its own 
`/output/` dir for export to the host computer. Build args are provided to 
change the version of each module.

A convenience script, `build_upstream.py`, is provided. It builds the stubs and 
copies them to the host computer. Make sure you install `docker-py` to use it.
It builds `$PWD/Dockerfile` (overridden with `--dockerfile`) and outputs the
stubs to `$PWD/PyQt5-stubs` (overridden with `--output-dir`). 

\* There are a few missing modules: `QtAxContainer`, `QtAndroidExtras`, 
`QtMacExtras`, and `QtWindowsExtras`. The current project understanding is that
they need to be built on the target platform, something a Linux-based docker
image cannot do. The deprecated `Enginio` module is also missing.  
