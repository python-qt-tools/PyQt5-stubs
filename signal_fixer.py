"""Script that will check stub files and fix signal annotations."""
import importlib
import os
from types import ModuleType
from typing import List, Optional, Union, cast, Iterable

import libcst as cst

from PyQt5 import QtCore


def is_signal(module: ModuleType, cls_name: str, func_name: str) -> bool:
    """Check if a method of the given Qt class is a signal."""
    cls = getattr(module, cls_name)
    try:
        func = getattr(cls, func_name)
    except AttributeError:
        print(f"Warning! Could not find {cls_name}.{func_name}")
        return False
    return isinstance(func, QtCore.pyqtSignal)


class TypingTransformer(cst.CSTTransformer):
    """TypingTransformer that visits classes and methods."""

    def __init__(self, mod_name: str):
        super().__init__()
        self._last_class: List[cst.ClassDef] = []
        self._fixed_signals: List[str] = []
        self._module: ModuleType = importlib.import_module(f"PyQt5.{mod_name}")

    def visit_ClassDef(self, node: cst.ClassDef) -> Optional[bool]:
        """Put a class on top of the stack when visiting."""
        self._last_class.append(node)
        return True

    def leave_FunctionDef(
        self, original_node: cst.FunctionDef, _: cst.FunctionDef
    ) -> Union[
        cst.BaseStatement,
        cst.FlattenSentinel[cst.BaseStatement],
        cst.RemovalSentinel,
    ]:
        """Leave the method and change signature if a signal."""
        if not self._last_class:
            return original_node
        if len(self._last_class) > 1:
            return original_node

        f_name = original_node.name.value
        if is_signal(self._module, self._last_class[-1].name.value, f_name):
            full_name = f"{self._last_class[-1].name.value}.{f_name}"
            if full_name in self._fixed_signals:
                # Handle the use-case of overloaded signals, that are defined
                # multiple time because of their different signal arguments
                # i.e.: QComboBox.highlighted
                return cst.RemovalSentinel.REMOVE
            self._fixed_signals.append(full_name)
            stmt = f"{f_name}: typing.ClassVar[QtCore.pyqtSignal]"
            node = cst.parse_statement(stmt)
            if original_node.leading_lines:
                # Copy the leading lines and return them with a
                # FlattenSentinel. Just adding a newline char results in an
                # indented EmptyLine which isn't bad but clutters the diff
                # unnecessarily
                empty_nodes = [
                    line.deep_clone() for line in original_node.leading_lines
                ]
                return cst.FlattenSentinel(
                    cast(Iterable[cst.BaseStatement], [*empty_nodes, node])
                )
            return node
        return original_node

    def leave_ClassDef(
        self, original_node: cst.ClassDef, updated_node: cst.ClassDef
    ) -> Union[
        cst.BaseStatement,
        cst.FlattenSentinel[cst.BaseStatement],
        cst.RemovalSentinel,
    ]:
        """Remove a class from the stack and return the updated node."""
        self._last_class.pop()
        return updated_node


if __name__ == "__main__":
    for file in os.listdir("PyQt5-stubs"):
        if file.startswith("QtWebKit") or file in [
            "QtX11Extras.pyi",
            "sip.pyi",
            "__init__.pyi",
        ]:
            continue
        print("Fixing signals in " + file)
        path = os.path.join("PyQt5-stubs", file)
        with open(path, "r", encoding="utf-8") as fhandle:
            stub_tree = cst.parse_module(fhandle.read())

        transformer = TypingTransformer(file.replace(".pyi", ""))
        modified_tree = stub_tree.visit(transformer)

        with open(path, "w", encoding="utf-8") as fhandle:
            fhandle.write(modified_tree.code)
