"""
:author: Stefan Lehmann <stlm@posteo.de>
:license: MIT, see license file or https://opensource.org/licenses/MIT

:created on 2018-10-06 10:55:36
:last modified by:   Stefan Lehmann
:last modified time: 2018-12-08 21:43:54

"""
from distutils.core import setup


setup(
    name="PyQt5-stubs",
    url="https://github.com/stlehmann/PyQt5-stubs",
    author="Stefan Lehmann",
    author_email="stlm@posteo.de",
    version="5.11.3.1",
    package_data={"PyQt5-stubs": ['*.pyi']},
    install_requires=["PyQt5==5.11.3"],
    packages=["PyQt5-stubs"]
)
