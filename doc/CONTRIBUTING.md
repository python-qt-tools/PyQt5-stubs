# How to contribute

We welcome contribuors.

Just keep in ming that this project is maintained by people working in their free time. We are usually
quite reactive, but it may happen that a contribution stays without feedback for a while.
Don't be surprised and if you don't get feedback withing one month, don't hesitate to
signal it in the issue.


## Report issues

You are welcome to report any issues through the GitHub interface. It is even
better if you can provide a Pull Request fixing the problem.


## Pull Requests

Pull Requests are welcome. To be merged, the Pull Request shall be validated by:

1. Passing the Continuous Integration successfully (see next section).
2. Being reviewed by a PyQt5-stubs maintainer

Some suggestions to make a good PR:
* describe clearly the problem you are solving
* if you can add a test, it is even better (see next section)
* please update the CHANGELOG.md with a new entry describing your PR


## Continuous Integration
   
The CI runs automatically on every pull requests and every night on the main branch. It 
runs on all supported Python version on Linux, Windows and MacOs.

The CI is based on `tox`, you can check the `tox.ini` file to see what is actually executed.

The big steps are:
* run our tests with `pytest`. This runs the tests as python scripts and verifies them with mypy.
* check the PyQt5-stubs content against the actual PyQt5 modules. We rely on the tool `stubtest.py` (from
  the mypy project). The checks are quite extensive and should spot any missing or non-existing attributes.
  
Some errors reported by `stubtest.py` can not be fixed because they reflect the design of Qt5 or
are a limitation of static typing capabilities. In these case, it is OK to silence them,
see the file `limitaions.md` for details.


## Running the tests locally

When you improve the stubs, it is convenient to run the tests manually before submitting
a Pull Request and running the CI.

### Setup for tests

You need the following:
* a virtual environment with your local PyQt5-stubs installed
* all PyQt5 packages installed
* pytest and mypy

First, create a dedicated virtual envonment for running the tests and activate it.

    .../PyQt5-stubs/ $ python -m venv env_for_tests
    .../PyQt5-stubs/ $ env_for_tests/Scripts/activate
   
Then install the required packages. The exact PyQt5 packages versions is hidden inside
the `tox.ini` file. Just copy the corresponding line:

    .../PyQt5-stubs/ (env_for_tests) $ # copy the line from tox.ini
    .../PyQt5-stubs/ (env_for_tests) $ pip install PyQt5==5.15.6 PyQt3D==5.15.5 PyQtChart==5.15.5 PyQtDataVisualization==5.15.5 PyQtNetworkAuth==5.15.5 PyQtPurchasing==5.15.5 PyQtWebEngine==5.15.5

Install the local version of PyQt-stubs:

    .../PyQt5-stubs/ (env_for_tests) $ pip install -e .

Also install `pytest` and `mypy` :

    .../PyQt5-stubs/ (env_for_tests) $ pip install mypy pytest


### Running the tests

Go to the directory `tests` and run `pytest`:

    .../PyQt5-stubs/ (env_for_tests) $  cd tests
    .../PyQt5-stubs/tests/ (env_for_tests) $  pytest
    [...]


The different phases of the testing process are driven by the script `test_stub.py`. The steps are:

1. Run mypy on every file of the directory not starting with `test_` . This is the part which generates
   the output `blablabla` XXX
   
2. Run the example python files themselves, to make sure they are correct.
    XXX


### Adding new tests

Each time you find an incorrect stub, it is a good idea to add a dedicated test to show
what is expected from mypy. The steps to do so are:

1. Add a new file under the test directory with a meaningful name (usually, the name of the 
   offending class). Example: `qlineedit.py`
   
2. In the file, write the correct python code which should typecheck correctly. This is usually
    just a few lines of code as you can see from the other examples. If you need to 
    instantiate a widget, you need a `QApplication` instance
    first, which should also run in our GUI-less CI. Passing `['my_program', '-platform', 'offscreen']`
    to the `QApplication` constructor will do the trick. See `qlineedit.py` for an example of how
    to do it.
   
3. Run your example file with Python. There should be no error. Example:

```
.../PyQt5-stubs/tests/ (env_for_tests) $ python qlineedit.py
```


4. Run your example file through mypy. Usually, this is where you are getting the error
   you are reporting. Fix the PyQt5-stubs to fix your error and run it again.

```
.../PyQt5-stubs/tests/ (env_for_tests) $ mypy qlineedit.py
```
   
5. When everything works, you can run the full tests again. It will pickup your example
   automatically:
  
```
.../PyQt5-stubs/tests/ (env_for_tests) $ pytest 
```


6. If you want to run also the checks done by the CI, you may want to run the `stubtest.py` script. Check
   the command-line from `tox.ini` . If you are on a Linux computer, the command-line to run it (from the
   project base directory) is:

```
.../PyQt5-stubs/tests/ (env_for_tests) $ cd ..
.../PyQt5-stubs/ (env_for_tests) $ stubtest --allowlist ./stubtest.allowlist --allowlist ./stubtest.allowlist.to_review --allowlist ./stubtest.allowlist.linux PyQt5
```

This may reveal some quirks, like some method added for convenience but not existing in the PyQt5 package. How
to deal with this is described in the file `limitations.md`.
   
7. Update the `ChangeLog.md` describing your changes.


When you complete all these steps (or even before they are completed), you can submit a Pull Request to the
the project and we will gladly review it.



