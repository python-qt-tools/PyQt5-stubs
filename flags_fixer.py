"""Script that will check stub files and add missing flag functions."""
from pathlib import Path
from typing import Optional, Union

import libcst as cst

METHOD_TEMPLATE = (
    "def {method_name}("
    "self, other: typing.Union['{base_type}', '{flag_type}']"
    ") -> '{base_type}': ..."
)
METHODS_TO_ADD = [
    "__and__",
    "__iand__",
    "__or__",
    "__ior__",
    "__xor__",
    "__ixor__",
]


def get_flag_constructor_flag_type(
    c_name: str, original_node: cst.FunctionDef
) -> Optional[tuple[str, str]]:
    """Gets flag types from a given constructor node for a flag container class.

    Expects that the constructor node takes a single argument named 'f' which
    has an annotation that reveals the type of the related individual flag.

    :param c_name: owner class name
    :param original_node: constructor node
    :return: tuple with container flags type and individual flag type
    """
    if len(original_node.params.params) != 2:
        return None

    param = original_node.params.params[-1]
    if (
        param.name.value != "f"
        or not param.annotation
        or not isinstance(param.annotation.annotation, cst.Subscript)
        or not all(
            isinstance(slice_element.slice.value, cst.SimpleString)
            for slice_element in param.annotation.annotation.slice
        )
    ):
        return None

    union_values = tuple(
        slice_element.slice.value.value.strip("'")
        for slice_element in param.annotation.annotation.slice
    )
    if len(union_values) != 2 or not union_values[0].endswith(f".{c_name}"):
        return None

    return (union_values[0], union_values[1])


class TypingTransformer(cst.CSTTransformer):
    """TypingTransformer that visits classes and methods."""

    def __init__(self, _mod_name: str):
        """Initialize self."""
        super().__init__()
        self._last_class: list[cst.ClassDef] = []
        self._last_flag_type: Optional[tuple[str, str]] = None
        self._missing_methods: set[str] = set()

    def visit_ClassDef(self, node: cst.ClassDef) -> Optional[bool]:
        """Visit a class definition.

        Puts a class on top of the stack. Resets class state.
        """
        self._last_class.append(node)
        self._last_flag_type = None
        self._missing_methods = METHODS_TO_ADD[:]
        return True

    def leave_FunctionDef(
        self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
    ) -> Union[
        cst.BaseStatement,
        cst.FlattenSentinel[cst.BaseStatement],
        cst.RemovalSentinel,
    ]:
        """Leave a function definition.

        Does nothing if the function is not a method.
        Removes implemented methods from the list of missing methods.
        Remembers the flag types if the function happens to be a constructor
        for a flag container class.
        """
        if not self._last_class:
            return updated_node

        c_name = self._last_class[-1].name.value
        f_name = original_node.name.value

        if f_name in self._missing_methods:
            self._missing_methods.remove(f_name)

        if f_name == "__init__" and (
            flag_type := get_flag_constructor_flag_type(c_name, original_node)
        ):
            self._last_flag_type = flag_type

        return updated_node

    def leave_ClassDef(
        self, original_node: cst.ClassDef, updated_node: cst.ClassDef
    ) -> Union[
        cst.BaseStatement,
        cst.FlattenSentinel[cst.BaseStatement],
        cst.RemovalSentinel,
    ]:
        """Leave a class definition.

        Removes the class from the top of the stack. If the class was
        determined to be a flags container class and there are any methods left
        to add, adds the methods at the end of the class definition.
        """
        if self._last_flag_type and self._missing_methods:
            print(
                "Fixing",
                self._last_class[-1].name.value,
                self._missing_methods,
            )

            updated_node = updated_node.with_changes(
                body=original_node.body.with_changes(
                    body=[
                        *updated_node.body.body,
                        cst.Newline(),
                        *(
                            cst.parse_statement(
                                METHOD_TEMPLATE.format(
                                    method_name=method_name,
                                    base_type=self._last_flag_type[0],
                                    flag_type=self._last_flag_type[1],
                                )
                            )
                            for method_name in METHODS_TO_ADD
                            if method_name in self._missing_methods
                        ),
                    ]
                )
            )

        self._last_class.pop()
        self._last_flag_type = None
        return updated_node


def main() -> None:
    """Main script routine. Iterate over the stub files and transform them by
    adding missing methods.
    """
    for path in Path("PyQt5-stubs").iterdir():
        if path.name.startswith("QtWebKit") or path.name in [
            "QtX11Extras.pyi",
            "sip.pyi",
            "__init__.pyi",
        ]:
            continue

        print(f"Fixing flags in {path}")

        stub_tree = cst.parse_module(path.read_text(encoding="utf-8"))

        transformer = TypingTransformer(path.name.replace(".pyi", ""))
        modified_tree = stub_tree.visit(transformer)

        path.write_text(modified_tree.code, encoding="utf-8")


if __name__ == "__main__":
    main()
