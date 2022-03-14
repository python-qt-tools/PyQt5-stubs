# How to contribute

We welcome contributors.

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
* run `mypy` against the PyQt5 and PyQt5-stubs.
* check the PyQt5-stubs content against the actual PyQt5 modules. We rely on the tool `stubtest.py` (from
  the mypy project). The checks are quite extensive and should spot any missing or non-existing attributes.
  
Some errors reported by `stubtest.py` can not be fixed because they reflect the design of Qt5 or
are a limitation of static typing capabilities. In these case, it is OK to silence them,
see the file `limitations.md` for details.


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

    (env_for_tests) .../PyQt5-stubs/$ # copy the line from tox.ini
    (env_for_tests) .../PyQt5-stubs/$ pip install PyQt5==5.15.6 PyQt3D==5.15.5 PyQtChart==5.15.5 PyQtDataVisualization==5.15.5 PyQtNetworkAuth==5.15.5 PyQtPurchasing==5.15.5 PyQtWebEngine==5.15.5

Install the current directory as PyQt5-stubs:

    (env_for_tests) .../PyQt5-stubs/$ pip install -e .

Also install `pytest` and `mypy` :

    (env_for_tests) .../PyQt5-stubs/$ pip install mypy pytest


### Running the tests

Simply run `pytest`:

    (env_for_tests) .../PyQt5-stubs/$  pytest -v
    ======================================== test session starts ========================================
    platform win32 -- Python 3.8.8, pytest-6.2.2, py-1.10.0, pluggy-0.13.1 -- c:\python38-32\python.exe
    cachedir: .pytest_cache
    tempdir: C:\Users\g582619\AppData\Local\Temp\tests
    rootdir: ...\PyQt5-stubs\PyQt5-stubs, configfile: tox.ini
    plugins: tempdir-2019.10.12
    collected 382 items

    test_stubs.py::test_stubs[pyqtsignal.py] PASSED                                                [  0%]
    test_stubs.py::test_stubs[pyqtslot.py] PASSED                                                  [  0%]
    test_stubs.py::test_stubs[qbytearray.py] PASSED                                                [  0%]
    test_stubs.py::test_stubs[qdialogbuttonbox.py] PASSED                                          [  1%]
    test_stubs.py::test_stubs[qmessagebox.py] PASSED                                               [  1%]
    test_stubs.py::test_stubs[qobject.py] PASSED                                                   [  1%]
    test_stubs.py::test_stubs[qtimer.py] PASSED                                                    [  1%]
    test_stubs.py::test_stubs[qtreewidgetitem.py] PASSED                                           [  2%]
    test_stubs.py::test_stubs[simple.py] PASSED                                                    [  2%]
    test_stubs.py::test_stubs_qflags PASSED                                                        [  2%]
    test_stubs.py::test_files[pyqtsignal.py] PASSED                                                [  2%]
    test_stubs.py::test_files[pyqtslot.py] PASSED                                                  [  3%]
    test_stubs.py::test_files[qbytearray.py] PASSED                                                [  3%]
    test_stubs.py::test_files[qdialogbuttonbox.py] PASSED                                          [  3%]
    test_stubs.py::test_files[qmessagebox.py] PASSED                                               [  3%]
    test_stubs.py::test_files[qobject.py] PASSED                                                   [  4%]
    test_stubs.py::test_files[qtimer.py] PASSED                                                    [  4%]
    test_stubs.py::test_files[qtreewidgetitem.py] PASSED                                           [  4%]
    test_stubs.py::test_files[simple.py] PASSED                                                    [  4%]
    qflags\test_Qt3DCore_ChangeFlags_ChangeFlag.py::test_on_one_flag_class PASSED                  [  5%]
    qflags\test_Qt3DCore_ChangeFlags_ChangeFlag.py::test_on_multi_flag_class PASSED                [  5%]
    qflags\test_Qt3DCore_DeliveryFlags_DeliveryFlag.py::test_on_one_flag_class PASSED              [  5%]
    qflags\test_Qt3DCore_DeliveryFlags_DeliveryFlag.py::test_on_multi_flag_class PASSED            [  6%]
    [...]
    qflags\test_QtWidgets_ViewItemFeatures_ViewItemFeature.py::test_on_one_flag_class PASSED       [ 99%]
    qflags\test_QtWidgets_ViewItemFeatures_ViewItemFeature.py::test_on_multi_flag_class PASSED     [ 99%]
    qflags\test_QtWidgets_WizardOptions_WizardOption.py::test_on_one_flag_class PASSED             [ 99%]
    qflags\test_QtWidgets_WizardOptions_WizardOption.py::test_on_multi_flag_class PASSED           [100%]

    ======================================= 382 passed in 11.72s ========================================



The different phases of the testing process are driven by the script `test_stub.py`. The steps are:

1. Run mypy on every file of the directory not starting with `test_` . This is the part which generates
   the output:

```
   test_stubs.py::test_stubs[pyqtsignal.py] PASSED                                                [  0%]
   test_stubs.py::test_stubs[pyqtslot.py] PASSED                                                  [  0%]
   [...]
   test_stubs.py::test_files[qtreewidgetitem.py] PASSED                                           [  4%]
   test_stubs.py::test_files[simple.py] PASSED                                                    [  4%]
```
   
2. Run the example python files themselves, to make sure they are correct. This is
   the longest part of the output:

```
   qflags\test_Qt3DCore_ChangeFlags_ChangeFlag.py::test_on_one_flag_class PASSED                  [  5%]
   qflags\test_Qt3DCore_ChangeFlags_ChangeFlag.py::test_on_multi_flag_class PASSED                [  5%]
   [...]
   qflags\test_QtWidgets_ViewItemFeatures_ViewItemFeature.py::test_on_one_flag_class PASSED       [ 99%]
   qflags\test_QtWidgets_ViewItemFeatures_ViewItemFeature.py::test_on_multi_flag_class PASSED     [ 99%]

   ======================================= 382 passed in 11.72s ========================================
```


### Adding new tests

Each time you find an incorrect stub, it is a good idea to add a dedicated test to show
what is expected from mypy. The steps to take are:

1. Add a new file under the test directory with a meaningful name (usually, the name of the 
   relevant class). Example: `qlineedit.py`
   
2. In the file, write the correct python code which should typecheck correctly. This is usually
    just a few lines of code as you can see from the other examples. A QApplication has already 
    been created as part of the test execution, so you are free to create an QObject or widgets.
   
3. Run your example file with Python. There should be no error and no output. 
   
   Example:

```
   (env_for_tests) .../PyQt5-stubs/tests/$ python qlineedit.py
   (env_for_tests) .../PyQt5-stubs/tests/$
```


4. Run your example file through `mypy`. Usually, this is where you are getting the error
   you are reporting. Fix the PyQt5-stubs to fix your error and run it again.

```
   (env_for_tests) .../PyQt5-stubs/tests/$ mypy qlineedit.py
   Success: no issues found in 1 source file

```
   
5. When everything works, you can run the full tests again. It will pick up your example
   automatically:
  
```
   (env_for_tests) .../PyQt5-stubs/tests/$ pytest  -v
   [...]
   ======================================= 382 passed in 11.72s ========================================
```


6. If you want to run also the checks done by the CI, you may want to run the `stubtest.py` script. Check
   the command-line from `tox.ini` . If you are on a Linux computer, the command-line to run it (from the
   project base directory) is:

```
   (env_for_tests) .../PyQt5-stubs/$ stubtest --allowlist ./stubtest.allowlist --allowlist ./stubtest.allowlist.to_review --allowlist ./stubtest.allowlist.linux PyQt5
   (env_for_tests) .../PyQt5-stubs/$
```

This may reveal some quirks, like some method added for convenience but not existing in the PyQt5 package. How
to deal with this is described in the file `limitations.md`.
   
7. Update the `ChangeLog.md` describing your changes.


When you complete all these steps (or even before they are completed), you can submit a Pull Request to the
project, and we will gladly review it.



