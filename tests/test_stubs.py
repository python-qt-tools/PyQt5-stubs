import os.path
import pytest
from mypy import api
from PyQt5.QtWidgets import QApplication


TESTS_DIR = os.path.dirname(__file__)


@pytest.fixture(name="qapplication", scope="session")
def qapplication_fixture():
    application = QApplication.instance()
    if application is None:
        application = QApplication(["-platform", "minimal"])

    return application


def gen_tests():
    for filename in os.listdir(TESTS_DIR):
        if filename.endswith('.py') and not filename.startswith('test_'):
            yield filename


@pytest.mark.parametrize('filename', list(gen_tests()))
def test_stubs(filename):
    """Run mypy over example files."""
    path = os.path.join(TESTS_DIR, filename)
    stdout, stderr, exitcode = api.run([path])
    if stdout:
        print(stdout)

    assert stdout.startswith("Success: no issues found")
    assert not stderr
    assert exitcode == 0


@pytest.mark.parametrize('filename', list(gen_tests()))
def test_files(filename, qapplication):
    """Run the test files to make sure they work properly."""
    path = os.path.join(TESTS_DIR, filename)
    with open(path, 'r') as f:
        code = f.read()
    exec(compile(code, filename, 'exec'), {})
