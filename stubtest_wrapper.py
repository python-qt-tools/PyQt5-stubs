# workaround for https://github.com/python/mypy/issues/14196

import faulthandler
import sys
import typing

import mypy.stubtest


sentinel = object


def noop_generator(*args, **kwargs) -> typing.Iterator[object]:
    return
    yield  # make it a generator as the original is


def maybe_monkey_patch(object_: object, name: str, replacement: object) -> None:
    attribute = getattr(object_, name, sentinel)
    if attribute is sentinel:
        print(f"{name} does not exist on {object_}, skipping monkey patching")
        return

    setattr(object_, name, replacement)
    print(f"{name} on {object_} monkey patched by {replacement}")
    return


def main() -> int:
    maybe_monkey_patch(
        object_=mypy.stubtest,
        name="_verify_final",
        replacement=noop_generator,
    )

    # make sure the messages get out since we're working around a segfault here
    sys.stdout.flush()
    # in case we still get a segfault, try to report it
    faulthandler.enable()

    return mypy.stubtest.main()


sys.exit(main())
