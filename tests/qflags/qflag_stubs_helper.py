from typing import Optional, List, Tuple
from enum import Enum

try:
    import libcst as cst
    import libcst.matchers as matchers
except ImportError:
    raise ImportError('You need libcst to run the code analysis and transform\n'
                      'Please run the command:\n\tpython -m pip install libcst')

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

    mod_content = open('..\..\pyqt5-stubs\QtCore.pyi').read()
    mod_cst = cst.parse_module(mod_content)
    visitor = QFlagFinder('WindowState', 'WindowStates')
    mod_cst.visit(visitor)

    if (visitor.enum_methods_present, visitor.qflag_method_present) == (MethodPresent.All, MethodPresent.All):
        # TODO: check also for existence of the test file
        return (QFlagCheckResult.CodeAlreadyModified, visitor.error_msg)

    if visitor.error_msg:
        return (QFlagCheckResult.ErrorDuringProcessing, visitor.error_msg)

    assert visitor.enum_methods_present == MethodPresent.Not
    assert visitor.qflag_method_present == MethodPresent.Not

    # perform code modification
    # generate test file


class MethodPresent(Enum):
    Unset = 0
    All = 1
    Not = 2
    Partial = 3


class QFlagFinder(cst.CSTVisitor):

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
                self.error_msg = 'class %s found multiple times' % self.enum_class_name
                return
            self.enum_class_full_name = '.'.join(self.full_name_stack)
            self.enum_class_cst_node = node

            self.check_enum_method_present(node)

        elif node.name.value == self.qflag_class_name:
            # we found it
            if self.qflag_class_full_name != '':
                self.error_msg = 'class %s found multiple times' % self.qflag_class_name
                return
            self.qflag_class_full_name = '.'.join(self.full_name_stack)
            self.qflag_class_cst_node = node

            self.check_qflag_method_present(node)
        return None


    def check_enum_method_present(self, enum_node: cst.ClassDef) -> None:
        '''Check if the class contains method __or__ and __ror__ with one argument and if class
        inherit from int'''
        if len(enum_node.bases) == 0 or enum_node.bases[0].value != 'int':
            self.error_msg += 'Class %s does not inherit from int' % self.enum_class_full_name
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


import unittest
class TestMe(unittest.TestCase):

    def test1(self):
        mod_cst = cst.parse_module('''
class Toto:

    class Titi:
        'bla bla bla'
        
        def toto(self) -> None: ... 
    
        @overload
        def my_titi(self) -> str: ...
        
        
    class QFlagExample:
        def abd(self): ...
        def __or__(self, other): ...
        def __ror__(self, other): ...
    ''')
        visitor = QFlagFinder('Titi')
        mod_cst.visit(visitor)
        self.assertEqual(visitor.enum_class_full_name, 'Toto.Titi')
        print(visitor.enum_class_cst_node)


        visitor = QFlagFinder('QFlagExample')
        mod_cst.visit(visitor)
        self.assertEqual(visitor.enum_class_full_name, 'Toto.QFlagExample')
        print(visitor.enum_class_cst_node)




check_qflag_in_module(None)