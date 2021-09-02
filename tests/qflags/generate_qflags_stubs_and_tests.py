from typing import List, Tuple, Dict, Union, Any, Optional

import dataclasses
import functools
import json
from enum import Enum

try:
	import libcst as cst
	import libcst.matchers as matchers
except ImportError:
	raise ImportError('You need libcst to run the code analysis and transform\n'
					  'Please run the command:\n\tpython -m pip install libcst')


'''How to use this generator script:

1. Grep Qt sources, looking for all QFlag based classes. The command-line to use is:

	qt-src\qt5\qtbase>rg  --type-add "headers:*.h" -t headers Q_DECLARE_FLAGS --no-heading > qt-qflag-grep-result.txt

2. Run the script to identify where each QFlag is located in PyQt.
'''

# the file defining the qflag implementation, to be skipped
QFLAG_SRC='src\\corelib\\global\\qflags.h'

# the template after which we model all generated qflag tests
SOURCE_QFLAGS_TESTS = 'qflags_windowFlags.py'

# the markers inside the above template to identify the parts to replace
MARKER_SPECIFIC_START = '### Specific part'
MARKER_SPECIFIC_END = '### End of specific part'


QTBASE_MODULES = [
	['QtCore', '../../PyQt5-stubs/QtCore.pyi'],
	['QtWidgets', '../../PyQt5-stubs/QtWidgets.pyi'],
	['QtGui', '../../PyQt5-stubs/QtGui.pyi'],
	['QtNetwork', '../../PyQt5-stubs/QtNetwork.pyi'],
	['QtDbus', '../../PyQt5-stubs/QtDbus.pyi'],
	['QtOpengl', '../../PyQt5-stubs/QtOpengl.pyi'],
	['QtPrintsupport', '../../PyQt5-stubs/QtPrintsupport.pyi'],
	['QtSql', '../../PyQt5-stubs/QtSql.pyi'],
	['QtTest', '../../PyQt5-stubs/QtTest.pyi'],
	['QtXml', '../../PyQt5-stubs/QtXml.pyi'],
]

def log_progress(s: str) -> None:
	print('>>>>>>>>>>>>>>', s)

@dataclasses.dataclass
class QFlagLocationInfo:
	grep_line: str
	qflag_class: str
	qflag_enum: str

	# list of (module_name, module_path)
	module_info: List[ Tuple[str, str] ]


def json_encode_qflaglocationinfo(flag_loc_info: object) -> Union[object, Dict[str, Any]]:
	'''Encore the QFlagClassLoationInfo into a format suitable for json export (a dict)'''
	if not isinstance(flag_loc_info, QFlagLocationInfo):
		# oups, we don't know how to encode that
		return flag_loc_info

	return dataclasses.asdict(flag_loc_info)


def identify_qflag_location(fname_grep_result: str,
							qt_modules: List[Tuple[str, str]]
							) -> List[ QFlagLocationInfo ]:
	'''Parses the grep results to extract each qflag, and then look into all Qt modules
	to see where the flag is located.

	Sort the result into 4 cases:
	- qflag present once in only one module: we are sure that these can be safely replaced by a better version
	- qflag present multiple times in one module: probably some extra module parsing might be needed to
	    	understand which version is the qflag which we want to modify
	- qflag present multiple times in multiples modules: we can not infer which module the flag is in
	- qflag not present anywhere: these are probably not exported to PyQt
	'''
	parsed_qflags = []	# type: List[ QFlagLocationInfo ]
	with open(fname_grep_result) as f:
		for l in f.readlines()[:]:
			grep_line = l.strip()
			if len(grep_line) == 0:
				continue
			qflag_fname, qflag_declare_stmt = [s.strip(' \t\n') for s in grep_line.split(':')]
			if qflag_fname == QFLAG_SRC:
				# do not include actual implementation of qflags
				continue
			assert 'Q_DECLARE_FLAGS' in qflag_declare_stmt
			s = qflag_declare_stmt[qflag_declare_stmt.index('(')+1:qflag_declare_stmt.index(')')]
			qflag_class, enum_class = [v.strip(' ') for v in s.split(',')]
			parsed_qflags.append(
				QFlagLocationInfo(grep_line, qflag_class, enum_class, [])
			)

	# fill up modules with content
	qt_modules_content = [ (mod_name, mod_stub_path, open(mod_stub_path, encoding='utf8').read())
						   for (mod_name, mod_stub_path) in qt_modules]

	for qflag_loc_info in parsed_qflags:
		decl_qflag_class = 'class %s(' % qflag_loc_info.qflag_class
		decl_enum_class = 'class %s(' % qflag_loc_info.qflag_enum
		for mod_name, mod_stub_path, mod_content in qt_modules_content:

			if decl_qflag_class in mod_content and decl_enum_class in mod_content:
				# we have found one module
				print('Adding QFlags %s to module %s' % (qflag_loc_info.qflag_class, mod_name))
				qflag_loc_info.module_info.append((mod_name, mod_stub_path))

				count_qflag_class = mod_content.count(decl_qflag_class)
				count_enum_class = mod_content.count(decl_enum_class)
				if count_qflag_class > 1 and count_enum_class > 1:
					print('QFlag present more than once, adding it more than once')
					extra_add = min(count_qflag_class, count_enum_class) - 1
					for _ in range(extra_add):
						qflag_loc_info.module_info.append((mod_name, mod_stub_path))

	return parsed_qflags


def group_qflags(qflag_location: List[QFlagLocationInfo] ) -> Dict[str, List[QFlagLocationInfo]]:
	'''Group the QFlags into the following groups:
	* one_flag_one_module: this flag is present once in one module exactly.
	* one_flag_many_modules: this flag is present once or multiple times in one or multiple modules
	* one_flag_no_module: this flag is not present in any modules at all.

	The first group is suitable for automatic processing.
	The second group requires human verification
	The last group reflects the non exported QFlags
	'''
	d = {
		'one_flag_one_module': [
				qflag_loc_info for qflag_loc_info in qflag_location
								if len(qflag_loc_info.module_info) == 1
		],
		'one_flag_many_modules': [
			qflag_loc_info for qflag_loc_info in qflag_location
			if len(qflag_loc_info.module_info) > 1
		],
		'one_flag_no_module': [
			qflag_loc_info for qflag_loc_info in qflag_location
			if len(qflag_loc_info.module_info) == 0
		],
	}

	return d


def extract_qflags_to_process(qflags_modules_analysis_json: str,
							  qflags_to_process_json: str,
							  ) -> None:
	'''Take the json file as input describing qflags and their modules and output a json file of qflags planned to be processed.

	The qflags which are located in a single module will be selected for further processing.
	The others are marked as skipped with a proper reason.
	'''
	with open(qflags_modules_analysis_json) as f:
		d = json.load(f)

	result = {
		'__': 'This file can be adjusted manually by a human prior to being processed by the tool',
		'qflags_to_process': [],
		'qflags_to_skip': [],
	}

	for qflag_info in d['one_flag_many_modules']:
		result['qflags_to_skip'].append(
			{
				'qflag_class': qflag_info['qflag_class'],
				'qflag_enum': qflag_info['qflag_enum'],
				'skipReason': 'QFlag present more than once or in multiple modules'
			}
		)

		for qflag_info in d['one_flag_no_module']:
			result['qflags_to_skip'].append(
				{
					'qflag_class': qflag_info['qflag_class'],
					'qflag_enum':  qflag_info['qflag_enum'],
					'skipReason':  'QFlag not found',
				}
			)

	for qflag_info in d['one_flag_one_module']:
		result['qflags_to_process'].append( qflag_info )

	with open(qflags_to_process_json, 'w') as f:
		json.dump(result, f, indent=4)


def process_qflag(qflag_to_process_json: str, qflag_result_json: str) -> bool:
	'''Read the qflags to process from the json file

	Process one qflag, by either:
	* identifying that this flag is already processed and add the flag to qflags_alraedy_done
	* identifying a reason why this flag can't be processed and adding the flag to qflags_processed_error
	* performing the qflag ajustment process:
		* generate a test file for this qflag usage
		* change the .pyi module for this qflag for supporting all the qflag operations
		* run pytest on the result
		* run mypy on the result
		* run the tox on result
		* add the flag to qflag_processed_done

	Return True when all flags have been processed
	'''
	with open(qflag_to_process_json) as f:
		d = json.load(f)

	result = {
		'qflag_already_done': [],
		'qflag_processed_done': [],
		'qflag_process_error': [],
	}

	if len(d['qflags_to_process']) == 0:
		return True

	try:
		flag_info_dict = d['qflags_to_process'].pop(0)

		# check if qflag has already been processed. If so move to the next one
		# if all qflags have been processed, return True

		flag_info = QFlagLocationInfo(**flag_info_dict)
		print('Processing qflag: %s / %s in module %s ' %
			  (flag_info.qflag_class,
			   flag_info.qflag_enum,
			   flag_info.module_info[0][0] if len(flag_info.module_info) else ''
			   ))

		result, error_msg = check_qflag_in_module(flag_info)

		# if result is failed, add error message and move to next flag
		# if result succeeds:
			# run tox
			# mark the test as done

		# if there are more flags to process, return False
		# if all flags are processed, return True
		return False
	finally:
		with open(qflag_result_json, 'w') as f:
			json.dump(result, f, indent=4)



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
        class not found, class found multiple times, ...

        The detail of the error is provided in the second argument of the return value.
'''
	log_progress('Opening module %s' % flag_info.module_info[0][0])
	with open(flag_info.module_info[0][1]) as f:
		mod_content = f.read()

	log_progress('Parsing module %s' % flag_info.module_info[0][0])
	mod_cst = cst.parse_module(mod_content)

	log_progress('Looking for class %s and %s in module %s' % (flag_info.qflag_class, flag_info.qflag_enum,
															   flag_info.module_info[0][0]))
	visitor = QFlagAndEnumFinder(flag_info.qflag_enum, flag_info.qflag_class)
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

	log_progress('Transforming module %s by adding new methods' % flag_info.module_info[0][0])
	transformer = QFlagAndEnumUpdater(visitor.enum_class_name, visitor.enum_class_full_name,
									  visitor.qflag_class_name, visitor.qflag_class_full_name)
	updated_mod_cst = mod_cst.visit(transformer)

	log_progress('Saving updated module %s' % flag_info.module_info[0][0])
	with open(flag_info.module_info[0][1], 'w') as f:
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





@functools.lru_cache(maxsize=1)
def read_qflag_test_template() -> Tuple[List[str], List[str], List[str]]:
	'''Return the source of template for generating qflags test.

	Return 3 parts:
	- the first part should be unmodified
	- the second part should be replaced for a specific QFlag class
	- the third part should be unmodified
	'''
	with open(SOURCE_QFLAGS_TESTS) as f:
		lines = f.readlines()

	sourcePart1, sourcePart2, sourcePart3 = [], [], []
	fillPart2, fillPart3 = False, False
	for l in lines:
		if fillPart3:
			sourcePart3.append(l)
			continue

		if fillPart2:
			if MARKER_SPECIFIC_END in l:
				fillPart3 = True
				sourcePart3.append(l)
				continue

			sourcePart2.append(l)
			continue

		sourcePart1.append(l)
		if MARKER_SPECIFIC_START in l:
			fillPart2 = True

	return sourcePart1, sourcePart2, sourcePart3


def generate_one_qflag_file(qflag_fname: str, multiFlagName: str, oneFlagName: str, oneFlagValue1: str, oneFlagValue2: str) -> None:
	sourcePart1, sourcePart2, sourcePart3 = read_qflag_test_template()

	with open(qflag_fname, 'w') as f:
		f.writelines(sourcePart1)
		f.write('''# file generated from {source} for QFlags class "{multiFlagName}" and flag class "{oneFlagName}"

OneFlagClass = {oneFlagName}
MultiFlagClass = {multiFlagName}

oneFlagRefValue1 = {oneFlagValue1}
oneFlagRefValue2 = {oneFlagValue2}
'''.format(source=SOURCE_QFLAGS_TESTS, multiFlagName=multiFlagName, oneFlagName=oneFlagName,
		   oneFlagValue1=oneFlagValue1, oneFlagValue2=oneFlagValue2
		   ))
		f.writelines(sourcePart3)
	print('File %s generated' % qflag_fname)



# TODO:

# for each module/flag
# - generate a test file is not already present
# - run test file. If it fails, skip this flag
# - find where the class is located in the module
# - check if class is in raw form (not QFlag based yet) or already patched
# - if not patched
# 	- modify the code of the module with better implementation
# - generate a test file is not already present
# - run test file and mypy for the qflag class
# - if successful execution, commit it
# - if unsuccessful execution, revert the changes on the module
# repeat...
#
# analyse the result

def generate_qflags_to_process():
	'''Run the generation process from the grep output parsing to the generation of json file listing the flags to process'''
	qt_qflag_grep_result_fname = 'qt-qflag-grep-result.txt'
	location_qflags = identify_qflag_location(qt_qflag_grep_result_fname, QTBASE_MODULES)
	print('%d qflags extracted from grep file' % len(location_qflags))
	qflags_groups = group_qflags(location_qflags)
	print('%d qflags ready to be processed' % len(qflags_groups['one_flag_one_module']))

	qflags_modules_analysis_json = 'qflags_modules_analysis.json'
	# put our intermediate classification into a json file for human review
	with open(qflags_modules_analysis_json, 'w') as f:
		json.dump(qflags_groups, f, indent=4, default=json_encode_qflaglocationinfo)
	print('QFlag analysis saved to: %s' % qflags_modules_analysis_json)

	qflags_to_process_json = 'qflags_to_process.json'
	extract_qflags_to_process(qflags_modules_analysis_json, qflags_to_process_json)


if __name__ == '__main__':
	# generate_qflags_to_process()

	qflags_to_process_json = 'qflags_to_process.json'
	# here we have the opportunity for human modification of the json file

	qflag_result_json = 'qflag_process_result.json'

	# process_qflag(qflags_to_process_json, qflag_result_json)

	flag_info = QFlagLocationInfo(qflag_enum='WindowState',
								  qflag_class='WindowStates',
								  module_info=[ ('QtCore.pyi', r'..\..\pyqt5-stubs\QtCore.pyi')],
								  grep_line='')
	result, error_msg = check_qflag_in_module(flag_info)

