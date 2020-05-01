<img src="http://mypy-lang.org/static/mypy_light.svg" alt="mypy logo" width="300px"/>

# Mypy stubs for the PyQt5 framework

This repository holds the stubs of the PyQt5 framework. It uses the stub files that are
produced during compilation process of PyQt5. These stub files have been modified by the author
to allow using them for type-checking via Mypy. This repository is far from complete and the author will
appreciate any PRs or Issues that help making this stub-repository more reliable.


# Building upstream stubs
The Dockerfile in the root of the `upstream` branch is used to build all* of the
stubs for the upstream PyQt5 modules. The Dockerfile consists of multiple build
layers:
* core `PyQt5`
* `PyQt3D`
* `PyQtChart`
* `PyQtDataVisualization`
* `PyQtPurchasing`
* `PyQtWebEngine`
* an output layer. 

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