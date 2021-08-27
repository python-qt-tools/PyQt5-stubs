from typing import Optional, List
from enum import Enum

try:
    import libcst as cst
    import libcst.matchers as matchers
except ImportError:
    raise ImportError('You need libcst to run the code analysis and transform\n'
                      'Please run the command:\n\tpython -m pip install libcst')

def check_qflag_in_module(flag_info: 'QFlagLocationInfo') -> None:
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
'''
    try:
        import libcst
    except ImportError:
        raise ImportError('You need libcst to run the code analysis and transform\n'
                          'Please run the command:\n\tpython -m pip install libcst')

    mod_content = open('..\..\pyqt5-stubs\QtCore.pyi').read()
    mod_cst = cst.parse_module(mod_content)
    visitor = QFlagFinder('WindowState')
    mod_cst.visit(visitor)
    pass

class MethodPresent(Enum):
    Unset = 0
    All = 1
    Not = 2
    Partial = 3


class QFlagFinder(cst.CSTVisitor):

    def __init__(self, enum_class: str) -> None:
        super().__init__()

        # used internally to generate the full class name
        self.full_name_stack: List[str] = []

        # the class name we are looking for
        self.enum_class_name = enum_class

        # the class full name
        self.enum_class_full_name = ''

        # the node of the class, for further reference
        self.enum_class_cst_node = None

        # when filled, set to one of the MethodPresent values
        self.enum_methods_present = MethodPresent.Unset

        # set when enum_methods_present is set to partial, to add more contect information
        self.error_msg = ''


    def visit_ClassDef(self, node: cst.ClassDef) -> Optional[bool]:
        self.full_name_stack.append( node.name.value )
        if node.name.value == self.enum_class_name:
            # we found it
            if self.enum_class_full_name != '':
                raise ValueError('self.enum_class_full_name alraedy filled, can not setup a new value')
            self.enum_class_full_name = '.'.join(self.full_name_stack)
            self.enum_class_cst_node = node

            self.check_method_present(node)
        return None

    def check_method_present(self, enum_node: cst.ClassDef) -> None:
        '''Check if the class contains method __or__ and __ror__ with one argument'''
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