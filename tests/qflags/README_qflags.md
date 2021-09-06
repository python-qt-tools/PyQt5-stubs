# QFlag stubs semi-automatic generation process

This directory is dedicated to helping with the generation of stubs related to all QFlags used in PyQt5.

## Overview

The general idea of the generation is:
* Grep Qt sources, looking for all QFlag based classes and store the result in a text file
* Process the grep text file to identify the QFlag names and their module. Generates a qflags_modules_analysis.json
* Using qflags_modules_analysis.json , extract the QFlags where the module is cleary identified and put
  them into a qflags_to_process.json file.
* Process each flag one by one from qflags_to_process.json and output a qflags_process_result.json . For
  each QFlag:
    ** verify with code analysis if the QFlag is indeed present in this module
    ** check if the stubs for all qflags operation are already present. If yes, stops.
    ** if not, add the missing stubs to the module and generate a test file in the form test_<module>_<qflag>.py
    ** run pytest and mypy on the generated test file
    ** if successful, stage the changes to git
    ** if there is any error in the process, stops.


## Details

To run all the above steps, proceed with the following steps.


### Grep the Qt sources

The command-line to use is:

	qt-src\qt5\qtbase>rg  --type-add "headers:*.h" -t headers Q_DECLARE_FLAGS --no-heading > qt-qflag-grep-result.txt


### Analyse the QFlags module location

Run:

    python generate_qflags_stubs_and_tests.py analyse_grep_results qt-qflag-grep-result.txt

You get two files:
    * qflags_modules_analysis.json
    * qflags_to_process.json

With human verification, you can add more QFlags to the qflags_to_process.json file.


### Generate and test the new stubs

Run:
    python generate_qflags_stubs_and_tests.py gen_qflag_stub 5

This will process 5 QFlags from qflags_to_process.json . The result of the processing is:
* the file qflags_process_result.json is updated
* when the generation and test is successful:
    ** the qt module is updated
    ** a new test file is added in the format test_<qtmodule>_<qflag>.py
    ** the new test file and the module are staged in git

Now, you can manually perform the git commit.

## Conclusion

The process is semi-manual at the moment. The tool will process QFlags in batches and let the user perform
the final git commit and push.

Note that more intelligence shall be put in the future to handle QFlags with identical names located in
multiple classes or modules.


