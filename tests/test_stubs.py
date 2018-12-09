import os.path
import pytest
from subprocess import Popen, PIPE
from mypy import api


TESTS_DIR = os.path.dirname(__file__)


def gen_tests():
    for filename in os.listdir(TESTS_DIR):
        if filename.endswith('.py') and not filename.startswith('test_'):
            yield filename


def test_package():
    breakpoint()
    p = Popen(["mypy", "-p", "PyQt5-stubs"], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()

    assert not stdout
    assert not stderr

@pytest.mark.parametrize('filename', list(gen_tests()))
def test_stubs(filename):
    """Run mypy over example files."""
    path = os.path.join(TESTS_DIR, filename)
    stdout, stderr, exitcode = api.run([path])
    if stdout:
        print(stdout)

    assert not stdout
    assert not stderr
    assert exitcode == 0


@pytest.mark.parametrize('filename', list(gen_tests()))
def test_files(filename):
    """Run the test files to make sure they work properly."""
    path = os.path.join(TESTS_DIR, filename)
    with open(path, 'r') as f:
        code = f.read()
    exec(compile(code, filename, 'exec'))
