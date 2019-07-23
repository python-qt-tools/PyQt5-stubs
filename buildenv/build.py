"""
:author: Stefan Lehmann <stlm@posteo.de>
:license: MIT, see license file or https://opensource.org/licenses/MIT

:created on: 2019-07-22 14:41:45
:last modified by: Stefan Lehmann
:last modified time: 2019-07-23 08:38:42

"""
import sys
import pathlib
from subprocess import call


p = pathlib.Path()
stubs_path = p / "stubs"

# build docker image
call(["docker", "build", "-tpyqt5-buildenv", "."])

# run docker image
call(
    [
        "docker",
        "run",
        "-it",
        "--name=pyqt5-buildenv",
        "-v" + str(stubs_path.resolve()) + ":/root/stubs",
        "pyqt5-buildenv",
    ]
)
