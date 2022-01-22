"""Python setup script.

:author: Stefan Lehmann <stlm@posteo.de>
:license: MIT, see license file or https://opensource.org/licenses/MIT

:created on 2018-10-06 10:55:36
:last modified by: Stefan Lehmann
:last modified time: 2019-07-23 10:27:04

"""
import io
import os
import re
from setuptools import setup


def read(*names, **kwargs):
    try:
        with io.open(
            os.path.join(os.path.dirname(__file__), *names),
            encoding=kwargs.get("encoding", "utf8")
        ) as fp:
            return fp.read()
    except IOError:
        return ''


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


long_description = read('README.md')


setup(
    name="PyQt5-stubs",
    url="https://github.com/python-qt-tools/PyQt5-stubs",
    author="Stefan Lehmann",
    maintainer="Kyle Altendorf, Bryce Beagle, Florian Bruhin",
    maintainer_email="sda@fstab.net",
    description="PEP561 stub files for the PyQt5 framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=find_version('PyQt5-stubs', '__init__.pyi'),
    python_requires=">= 3.5",
    package_data={"PyQt5-stubs": ['*.pyi']},
    packages=["PyQt5-stubs"],
    extras_require={
        "build": ["docker==4.2.0"],
        "dev": ["mypy", "pytest", "pytest-xvfb"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development"
    ]
)
