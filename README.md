<img src="http://mypy-lang.org/static/mypy_light.svg" alt="mypy logo" width="300px"/>

[![PyPI version](https://badge.fury.io/py/PyQt5-stubs.svg)](https://badge.fury.io/py/PyQt5-stubs)
[![mypy checked](https://camo.githubusercontent.com/34b3a249cd6502d0a521ab2f42c8830b7cfd03fa/687474703a2f2f7777772e6d7970792d6c616e672e6f72672f7374617469632f6d7970795f62616467652e737667)](http://mypy-lang.org/)
[![Build Status](https://travis-ci.org/stlehmann/PyQt5-stubs.svg?branch=master)](https://travis-ci.org/stlehmann/PyQt5-stubs)

# Mypy stubs for the PyQt5 framework

This repository holds the stubs of the PyQt5 framework. It uses the stub files that are
produced during compilation process of PyQt5. These stub files have been modified by the author
to allow using them for type-checking via Mypy. This repository is far from complete and the author will
appreciate any PRs or Issues that help making this stub-repository more reliable.

# Installation

Simply install PyQt5-stubs with pip:

    $ pip install PyQt5-stubs

Or clone the latest version from Github and install it via Python setuptools:

    $ git clone https://github.com/stlehmann/PyQt5-stubs.git
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
