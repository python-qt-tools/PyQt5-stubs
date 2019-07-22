"""
:author: Stefan Lehmann <stlm@posteo.de>
:license: MIT, see license file or https://opensource.org/licenses/MIT

:created on: 2019-07-22 14:41:45
:last modified by: Stefan Lehmann
:last modified time: 2019-07-22 15:22:20

"""
import sys
import pathlib
import subprocess as sp


p = pathlib.Path()
stubs_path = p / "stubs"


sp.call(["docker", "build", "-tpyqt5-buildenv", "."])
sp.call(
    [
        "docker",
        "run",
        "-it",
        "--name=pyqt5-buildenv",
        "-v" + str(stubs_path.resolve()) + ":/root/stubs",
        "pyqt5-buildenv",
    ]
)
