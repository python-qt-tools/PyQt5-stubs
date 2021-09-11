from pathlib import Path
import pytest
from mypy import api


TESTS_DIR = Path(__file__).parent


def gen_tests():
    '''List of all tests files included in the directory tests'''
    for filename in TESTS_DIR.glob('test_*.py'):
        yield filename

def gen_abs_qflags_tests():
    '''List of all tests included in the directory qflags'''
    for filename in (TESTS_DIR/'qflags').glob('test_*.py'):
        yield filename


@pytest.mark.parametrize('filename',
                         list(gen_tests()),
                         ids=[v.parts[-1] for v in gen_tests()]
                         )
def test_stubs(filename: Path) -> None:
    """Run mypy over example files."""
    stdout, stderr, exitcode = api.run([str(filename)])
    if stdout:
        print(stdout)
    if stderr:
        print(stderr)

    assert stdout.startswith("Success: no issues found")
    assert not stderr
    assert exitcode == 0


@pytest.mark.parametrize('filename',
                         list(gen_abs_qflags_tests()),
                         ids=[v.parts[-1] for v in gen_abs_qflags_tests()])
def test_stubs_qflags(filename: Path) -> None:
    """Run mypy over qflags files."""
    stdout, stderr, exitcode = api.run([str(filename)])
    if stdout:
        print(stdout)
    if stderr:
        print(stderr)

    assert stdout.startswith("Success: no issues found")
    assert not stderr
    assert exitcode == 0

# note: no need to run explicitely pytest over qflags, because pytest finds them automatically

@pytest.mark.parametrize('filename',
                         list(gen_tests()),
                         ids=[v.parts[-1] for v in gen_tests()]
                         )
def test_files(filename):
    """Run the test files to make sure they work properly."""
    with open(str(filename), 'r') as f:
        code = f.read()
    exec(compile(code, filename, 'exec'), {})
