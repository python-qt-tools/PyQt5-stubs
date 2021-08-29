from typing import Optional, List, Tuple
from enum import Enum

try:
    import libcst as cst
    import libcst.matchers as matchers
except ImportError:
    raise ImportError('You need libcst to run the code analysis and transform\n'
                      'Please run the command:\n\tpython -m pip install libcst')

def log_progress(s: str) -> None:
    print('>>>>>>>>>>>>>>', s)

class QFlagCheckResult(Enum):
    CodeModifiedSuccessfully = 0
    CodeAlreadyModified = 1
    ErrorDuringProcessing = 2


def check_qflag_in_module(flag_info: 'QFlagLocationInfo') -> Tuple[QFlagCheckResult, str]:
    '''
    Check that the QFlag enum+class are present in the module and check whether they support
    all the advanced QFlag operations.

    If they do not, add the missing information by performing code transformation and saving the result.

    Returns:
    * QFlag operations already present
    * QFlag operations were missing, now added
    * QFlag operations partially missing, now added.

    Raise ValueError if something goes wrong.

    The QFlag operations are:

    On the enum class, add two methods:
    class KeyboardModifier(int):
    +       def __or__ (self, other: 'Qt.KeyboardModifier') -> 'Qt.KeyboardModifiers': ...  # type: ignore[override]
    +       def __ror__ (self, other: int) -> 'Qt.KeyboardModifiers': ...             # type: ignore[override, misc]

    On the qflag class, add one more argument to __init__()
    -       def __init__(self, f: typing.Union['Qt.KeyboardModifiers', 'Qt.KeyboardModifier']) -> None: ...
    +       def __init__(self, f: typing.Union['Qt.KeyboardModifiers', 'Qt.KeyboardModifier', int]) -> None: ...

    Possibly, remove the __init__() with only int argument if it exists

    Add more methods:
        def __or__ (self, other: typing.Union['Qt.KeyboardModifiers', 'Qt.KeyboardModifier', int]) -> 'Qt.KeyboardModifiers': ...
        def __and__(self, other: typing.Union['Qt.KeyboardModifiers', 'Qt.KeyboardModifier', int]) -> 'Qt.KeyboardModifiers': ...
        def __xor__(self, other: typing.Union['Qt.KeyboardModifiers', 'Qt.KeyboardModifier', int]) -> 'Qt.KeyboardModifiers': ...
        def __ror__ (self, other: 'Qt.KeyboardModifier') -> 'Qt.KeyboardModifiers': ...
        def __rand__(self, other: 'Qt.KeyboardModifier') -> 'Qt.KeyboardModifiers': ...
        def __rxor__(self, other: 'Qt.KeyboardModifier') -> 'Qt.KeyboardModifiers': ...

    Returns a tuple of (result, error_msg):
    * CodeModifiedSuccessfully:
        All modifications to the code of the module have been performed successfully

    * CodeAlreadyModified:
        All modifications to the code were already done, no processing done.

    * ErrorDuringProcessing:
        Some error occured during the processing, such as some modifications were partially done,
        clas not found, class found multiple times, ...

        The detail of the error is provided in the second argument of the return value.
'''
    try:
        import libcst
    except ImportError:
        raise ImportError('You need libcst to run the code analysis and transform\n'
                          'Please run the command:\n\tpython -m pip install libcst')

    log_progress('Opening module %s' % 'QtCore.pyi')
    with open('..\..\pyqt5-stubs\QtCore.pyi') as f:
        mod_content = f.read()

    log_progress('Parsing module %s' % 'QtCore.pyi')
    mod_cst = cst.parse_module(mod_content)

    log_progress('Checking qflags and enumh module %s' % 'QtCore.pyi')
    visitor = QFlagAndEnumFinder('WindowState', 'WindowStates')
    mod_cst.visit(visitor)

    if (visitor.enum_methods_present, visitor.qflag_method_present) == (MethodPresent.All, MethodPresent.All):
        # TODO: check also for existence of the test file
        return (QFlagCheckResult.CodeAlreadyModified, visitor.error_msg)

    if (visitor.enum_methods_present, visitor.qflag_method_present) == (MethodPresent.All, MethodPresent.Not):
        visitor.error_msg += 'Enum methods are present but not QFlag methods\n'

    if (visitor.enum_methods_present, visitor.qflag_method_present) == (MethodPresent.Not, MethodPresent.All):
        visitor.error_msg += 'QFlag methods are present but not Enum methods\n'

    if visitor.error_msg:
        return (QFlagCheckResult.ErrorDuringProcessing, visitor.error_msg)

    assert visitor.enum_methods_present == MethodPresent.Not
    assert visitor.qflag_method_present == MethodPresent.Not

    log_progress('Transforming module %s by adding new methods' % 'QtCore.pyi')
    transformer = QFlagAndEnumUpdater(visitor.enum_class_name, visitor.enum_class_full_name,
                                      visitor.qflag_class_name, visitor.qflag_class_full_name)
    updated_mod_cst = mod_cst.visit(transformer)

    log_progress('Saving updated module %s' % 'QtCore.pyi')
    with open('..\..\pyqt5-stubs\QtCore.pyi', 'w') as f:
        f.write(updated_mod_cst.code)

    # generate test file

    return (QFlagCheckResult.CodeModifiedSuccessfully, '')


class MethodPresent(Enum):
    Unset = 0
    All = 1
    Not = 2
    Partial = 3


class QFlagAndEnumFinder(cst.CSTVisitor):

    def __init__(self, enum_class: str, qflag_class: str) -> None:
        super().__init__()

        # used internally to generate the full class name
        self.full_name_stack: List[str] = []

        # the class name we are looking for
        self.enum_class_name = enum_class
        self.qflag_class_name = qflag_class

        # the class full name
        self.enum_class_full_name = ''
        self.qflag_class_full_name = ''

        # the node of the class, for debugging purpose
        self.enum_class_cst_node = None
        self.qflag_class_cst_node = None

        # when filled, set to one of the MethodPresent values
        self.enum_methods_present = MethodPresent.Unset
        self.qflag_method_present = MethodPresent.Unset

        # set when enum_methods_present is set to partial, to add more contect information
        self.error_msg = ''


    def visit_ClassDef(self, node: cst.ClassDef) -> Optional[bool]:
        self.full_name_stack.append( node.name.value )
        if node.name.value == self.enum_class_name:
            # we found it
            if self.enum_class_full_name != '':
                self.error_msg = 'class %s found multiple times\n' % self.enum_class_name
                return
            self.enum_class_full_name = '.'.join(self.full_name_stack)
            self.enum_class_cst_node = node

            self.check_enum_method_present(node)

        elif node.name.value == self.qflag_class_name:
            # we found it
            if self.qflag_class_full_name != '':
                self.error_msg = 'class %s found multiple times\n' % self.qflag_class_name
                return
            self.qflag_class_full_name = '.'.join(self.full_name_stack)
            self.qflag_class_cst_node = node

            self.check_qflag_method_present(node)
        return None


    def check_enum_method_present(self, enum_node: cst.ClassDef) -> None:
        '''Check if the class contains method __or__ and __ror__ with one argument and if class
        inherit from int'''
        if len(enum_node.bases) == 0 or enum_node.bases[0].value.value != 'int':
            self.error_msg += 'Class %s does not inherit from int\n' % self.enum_class_full_name
            return
        has_or = matchers.findall(enum_node.body, matchers.FunctionDef(name=matchers.Name('__or__')))
        has_ror = matchers.findall(enum_node.body, matchers.FunctionDef(name=matchers.Name('__ror__')))
        self.enum_methods_present = {
            0: MethodPresent.Not,
            1: MethodPresent.Partial,
            2: MethodPresent.All
        }[len(has_or) + len(has_ror)]

        if self.enum_methods_present == MethodPresent.Partial:
            if has_or:
                args = ('__or__', '__ror__')
            else:
                args = ('__ror__', '__or__')

            self.error_msg += 'class %s, method %s present without method %s\n' % ((self.enum_class_full_name,)+args)


    def check_qflag_method_present(self, qflag_node: cst.ClassDef) -> None:
        '''Check if the class contains method:
        def __or__
        def __and__
        def __xor__
        def __ror__
        def __rand__
        def __rxor__

        with one argument.

        def __init__(self, f: typing.Union['Qt.KeyboardModifiers', 'Qt.KeyboardModifier']) -> None:
        def __init__(self, f: typing.Union['Qt.KeyboardModifiers', 'Qt.KeyboardModifier', int]) -> None:
        '''

        has_method = [
            (m, matchers.findall(qflag_node.body, matchers.FunctionDef(name=matchers.Name(m))))
            for m in ('__or__', '__and__', '__xor__', '__ror__', '__rxor__', '__rand__')
        ]

        if all(has_info[1] for has_info in has_method):
            # all method presents
            self.qflag_method_present = MethodPresent.All
            return

        if all(not has_info[1] for has_info in has_method):
            # all method absent
            self.qflag_method_present = MethodPresent.Not
            return

        self.qflag_method_present = MethodPresent.Partial

        for m_name, m_has in has_method:
            if m_has:
                self.error_msg += 'class %s, method %s present without all others\n' \
                                  % ((self.qflag_class_full_name, m_name))
            else:
                self.error_msg += 'class %s, method %s missing\n' \
                                  % ((self.qflag_class_full_name, m_name))


    def visit_FunctionDef(self, node: cst.FunctionDef) -> Optional[bool]:
        self.full_name_stack.append( node.name.value )
        return None

    def leave_ClassDef(self, node: cst.ClassDef) -> None:
        self.full_name_stack.pop()

    def leave_FunctionDef(self, node: cst.FunctionDef) -> None:
        self.full_name_stack.pop()


class QFlagAndEnumUpdater(cst.CSTTransformer):

    def __init__(self, enum_class: str, enum_full_name: str, qflag_class: str, qflag_full_name: str) -> None:
        super().__init__()

        self.error_msg = ''

        # the class name we are looking for
        self.enum_class = enum_class
        self.qflag_class = qflag_class
        self.enum_full_name = enum_full_name
        self.qflag_full_name = qflag_full_name

        # set when enum_methods_present is set to partial, to add more contect information
        self.error_msg = ''


    def leave_ClassDef(self, original_node: cst.ClassDef, updated_node: cst.ClassDef) -> cst.CSTNode:
        if original_node.name.value == self.enum_class:
            return self.transform_enum_class(original_node, updated_node)
        elif original_node.name.value == self.qflag_class:
            return self.transform_qflag_class(original_node, updated_node)
        return updated_node


    def transform_enum_class(self, original_node: cst.ClassDef, updated_node: cst.ClassDef) -> cst.CSTNode:
        '''Add the two methods __or__ and __ror__ to the class body'''

        # we keep comments separated to align them properly in the final file
        new_methods_parts = (
            ("def __or__ (self, other: '{enum}') -> '{qflag}': ...", "# type: ignore[override]\n"),
            ("def __ror__ (self, other: int) -> '{qflag}': ...", "# type: ignore[override, misc]\n\n")
        )

        # fill the class names
        new_methods_filled = tuple(
            (code.format(enum=self.enum_full_name, qflag=self.qflag_full_name), comment)
            for code, comment in new_methods_parts
        )

        # new calculate the proper spacing to have aligned comments
        max_code_len = max(len(code) for code, comment in new_methods_filled)
        new_methods_spaced = tuple(
            code + ' '*(4+max_code_len-len(code)) + comment
            for code, comment in new_methods_filled
        )
        new_methods_cst = tuple(cst.parse_statement(s) for s in new_methods_spaced)
        return updated_node.with_changes(body=updated_node.body.with_changes(body=
                                     new_methods_cst \
                                     + (updated_node.body.body[0].with_changes(leading_lines=
                                          updated_node.body.body[0].leading_lines + (cst.EmptyLine(),)),) \
                                     + updated_node.body.body[1:] ) )


    def transform_qflag_class(self, original_node: cst.ClassDef, updated_node: cst.ClassDef) -> cst.CSTNode:
        '''
        On the qflag class, add one more argument to __init__()
        -       def __init__(self, f: typing.Union['Qt.KeyboardModifiers', 'Qt.KeyboardModifier']) -> None: ...
        +       def __init__(self, f: typing.Union['Qt.KeyboardModifiers', 'Qt.KeyboardModifier', int]) -> None: ...

        Possibly, remove the __init__() with only int argument if it exists
        '''
        init_methods = matchers.findall(updated_node.body, matchers.FunctionDef(name=matchers.Name('__init__')))
        if len(init_methods) == 1:
            # we do not handle the case where there is only one init function
            # to handle it, we would need to do the following:
            # * add an @typing.overload to the current init function
            # * add a new init function
            #
            # This is not difficult, it's just that I don't think we have such cases
            self.error_msg += 'Only one __init__ method in QFlag class %s, do not know how to transform it\n' % self.qflag_full_name
            return updated_node

        # find the last __init__() method index
        last_init_idx = 0
        nb_init_found = 0
        for i, body_element in enumerate(updated_node.body.body):
            if matchers.matches(body_element, matchers.FunctionDef(name=matchers.Name('__init__'))):
                nb_init_found += 1
                if nb_init_found == len(init_methods):
                    last_init_idx = i
                    break
        assert last_init_idx != 0

        cst_init = cst.parse_statement( '@typing.overload\ndef __init__(self, f: int) -> None: ...' )
        updated_node = updated_node.with_changes(body=updated_node.body.with_changes(body=
                            tuple(updated_node.body.body[:last_init_idx+1]) +
                            (cst_init,) +
                            tuple(updated_node.body.body[last_init_idx+1:])
                            )
        )

        new_methods = (
            "def __or__ (self, other: typing.Union['{qflag}', '{enum}', int]) -> '{qflag}': ...",
            "def __and__(self, other: typing.Union['{qflag}', '{enum}', int]) -> '{qflag}': ...",
            "def __xor__(self, other: typing.Union['{qflag}', '{enum}', int]) -> '{qflag}': ...",
            "def __ror__ (self, other: '{enum}') -> '{qflag}': ...",
            "def __rand__(self, other: '{enum}') -> '{qflag}': ...",
            "def __rxor__(self, other: '{enum}') -> '{qflag}': ...",
        )
        new_methods_cst = tuple(
            cst.parse_statement(s.format(enum=self.enum_full_name, qflag=self.qflag_full_name))
            for s in new_methods
        )
        return updated_node.with_changes(body=updated_node.body.with_changes(body=
                                     tuple(updated_node.body.body) + new_methods_cst ) )





result, error = check_qflag_in_module(None)
print(result, error)