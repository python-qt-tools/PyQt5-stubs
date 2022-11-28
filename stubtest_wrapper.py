# workaround for https://github.com/python/mypy/issues/14196

import sys
import typing

import mypy.stubtest


def noop_generator(*args, **kwargs) -> typing.Iterator[object]:
    return
    yield  # make it a generator as the original is


def maybe_monkey_patch() -> None:
    if not hasattr(mypy.stubtest, "_verify_final"):
        print("mypy.stubtest._verify_final does not exist, skipping monkey patching")
        return

    if not callable(mypy.stubtest._verify_final):
        print("mypy.stubtest._verify_final is not a callable, skipping monkey patching")
        return

    mypy.stubtest._verify_final = noop_generator
    return


def main() -> int:
    maybe_monkey_patch()

    return mypy.stubtest.main()


sys.exit(main())
