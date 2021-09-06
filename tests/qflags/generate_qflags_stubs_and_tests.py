from typing import List, Tuple, Dict, Union, Any, Optional, cast

import dataclasses
import functools
import json
import os
import subprocess
from enum import Enum

try:
	import libcst as cst
	import libcst.matchers as matchers
except ImportError:
	raise ImportError('You need libcst to run the missing stubs generation\n'
					  'Please run the command:\n\tpython -m pip install libcst')


USAGE = '''Usage 1: {prog} analyse_grep_results <grep result filename>
	Process the <grep result filename> to extract all the qflag location information. Generates
	two output:
	- qflags_modules_analysis.json : a general file describing which qflag are suitable for processing
	- qflags_to_process.json: a list of qflag ready to process with the next command.

Usage 2: {prog} gen_qflag_stub <number>
	Using file qflag_to_process.json, process <number> qflags and modify the PyQt modules.
	The output of this processing is available in qflag_process_result.json
	If <number> is not provided, defaults to 1
'''.format(prog=sys.argv[0])

# the file defining the qflag implementation, to be skipped
QFLAG_SRC='src\\corelib\\global\\qflags.h'

# the template after which we model all generated qflag tests
TEMPLATE_QFLAGS_TESTS = 'qflags_test_template.py'

# the markers inside the above template to identify the parts to replace
MARKER_SPECIFIC_START = '### Specific part'
MARKER_SPECIFIC_END = '### End of specific part'


QTBASE_MODULES = [
	('QtCore', '../../PyQt5-stubs/QtCore.pyi'),
	('QtWidgets', '../../PyQt5-stubs/QtWidgets.pyi'),
	('QtGui', '../../PyQt5-stubs/QtGui.pyi'),
	('QtNetwork', '../../PyQt5-stubs/QtNetwork.pyi'),
	('QtDBus', '../../PyQt5-stubs/QtDBus.pyi'),
	('QtOpenGL', '../../PyQt5-stubs/QtOpenGL.pyi'),
	('QtPrintsupport', '../../PyQt5-stubs/QtPrintsupport.pyi'),
	('QtSql', '../../PyQt5-stubs/QtSql.pyi'),
	('QtTest', '../../PyQt5-stubs/QtTest.pyi'),
	('QtXml', '../../PyQt5-stubs/QtXml.pyi'),
]

def log_progress(s: str) -> None:
	print('>>>>>>>>>>>>>>', s)

@dataclasses.dataclass
class QFlagLocationInfo:

	# qflag and enum name used in the QDECLARE() grep line
	qflag_class: str
	enum_class: str

	# grep line indicating this qflag
	grep_line: str = ''

	# full class name (including nesting classes) generated in a second pass
	qflag_full_class_name: str = ''
	enum_full_class_name: str = ''
	enum_value1: str = ''
	enum_value2: str = ''

	# list of (module_name, module_path) where the qflag has been found
	module_info: Tuple[ Tuple[str, str], ... ] = dataclasses.field(default_factory=tuple)


def json_encode_qflaglocationinfo(flag_loc_info: object) -> Union[object, Dict[str, Any]]:
	'''Encode the QFlagClassLoationInfo into a format suitable for json export (a dict)'''
	if not isinstance(flag_loc_info, QFlagLocationInfo):
		# oups, we don't know how to encode that
		return flag_loc_info

	return dataclasses.asdict(flag_loc_info)


def identify_qflag_location(fname_grep_result: str,
							qt_modules: List[Tuple[str, str]]
							) -> List[ QFlagLocationInfo ]:
	'''Parses the grep results to extract each qflag, and then look into all Qt modules
	to see where the flag is located.

	Return a list of QFlagLocationInfo indicating in which module the flag has been located.
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
				QFlagLocationInfo(qflag_class, enum_class, grep_line)
			)

	# fill up modules with content
	qt_modules_content = [ (mod_name, mod_stub_path, open(mod_stub_path, encoding='utf8').read())
						   for (mod_name, mod_stub_path) in qt_modules]

	for flag_info in parsed_qflags:
		decl_qflag_class = 'class %s(' % flag_info.qflag_class
		decl_enum_class = 'class %s(' % flag_info.enum_class
		for mod_name, mod_stub_path, mod_content in qt_modules_content:

			if decl_qflag_class in mod_content and decl_enum_class in mod_content:
				# we have found one module
				print('Adding QFlags %s to module %s' % (flag_info.qflag_class, mod_name))
				flag_info.module_info += ((mod_name, mod_stub_path),)

				count_qflag_class = mod_content.count(decl_qflag_class)
				count_enum_class = mod_content.count(decl_enum_class)
				if count_qflag_class > 1 and count_enum_class > 1:
					print('QFlag present more than once, adding it more than once')
					extra_add = min(count_qflag_class, count_enum_class) - 1
					for _ in range(extra_add):
						flag_info.module_info += ((mod_name, mod_stub_path),)

	return parsed_qflags


def group_qflags(qflag_location: List[QFlagLocationInfo] ) -> Dict[str, List[QFlagLocationInfo]]:
	'''Group the QFlags into the following groups (inside a dictionnary):
	* one_flag_one_module: this flag is present once in one module exactly.
	* one_flag_many_modules: this flag is present once or multiple times in one or multiple modules
	* one_flag_no_module: this flag is not present in any modules at all.

	The first group is suitable for automatic processing.
	The second group requires human verification
	The last group reflects the QFlags not exported to PyQt or coming from modules not present in PyQt
	'''
	d = {
		'one_flag_one_module': [
				flag_info for flag_info in qflag_location
								if len(flag_info.module_info) == 1
		],
		'one_flag_many_modules': [
			flag_info for flag_info in qflag_location
			if len(flag_info.module_info) > 1
		],
		'one_flag_no_module': [
			flag_info for flag_info in qflag_location
			if len(flag_info.module_info) == 0
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

	for flag_info in d['one_flag_many_modules']:
		cast(List, result['qflags_to_skip']).append(
			{
				'qflag_class': flag_info['qflag_class'],
				'enum_class': flag_info['enum_class'],
				'skip_reason': 'QFlag present more than once or in multiple modules'
			}
		)

		for flag_info in d['one_flag_no_module']:
			cast(List, result['qflags_to_skip']).append(
				{
					'qflag_class': flag_info['qflag_class'],
					'enum_class':  flag_info['enum_class'],
					'skip_reason':  'QFlag not found',
				}
			)

	for flag_info in d['one_flag_one_module']:
		cast(List, result['qflags_to_process']).append( flag_info )

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

	qflags_to_process = d['qflags_to_process']

	result_json: Dict[str, List[Dict]] = {
		'qflag_already_done': [],
		'qflag_processed_done': [],
		'qflag_process_error': [],
	}

	if os.path.exists(qflag_result_json):
		with open(qflag_result_json, 'r') as f:
			result_json = json.loads(f.read())

	def qflag_already_processed(flag_info: QFlagLocationInfo) -> bool:
		'''Return True if the qflag is already included in one of the result lists
		of result_json'''
		flag_desc = (flag_info.module_info[0][0], flag_info.qflag_class, flag_info.enum_class)
		already_done_set = set( (flag_info_dict['module_info'][0][0],
						 flag_info_dict['qflag_class'],
						 flag_info_dict['enum_class'])
						for flag_info_dict in result_json['qflag_already_done'])
		processed_done_set = set( (flag_info_dict['module_info'][0][0],
								   flag_info_dict['qflag_class'],
								   flag_info_dict['enum_class'])
								  for flag_info_dict in result_json['qflag_processed_done'])
		process_error_set = set( (flag_info_dict['module_info'][0][0],
						 flag_info_dict['qflag_class'],
						 flag_info_dict['enum_class'])
							for flag_info_dict in result_json['qflag_process_error'])
		if flag_desc in already_done_set or flag_desc in processed_done_set or flag_desc in process_error_set:
			return True
		return False

	while len(qflags_to_process) != 0:
		flag_info_dict = qflags_to_process.pop(0)
		flag_info = QFlagLocationInfo(**flag_info_dict)
		# force module_info into a tuple to make it hashable
		flag_info.module_info = tuple((m0, m1) for (m0, m1) in flag_info.module_info)
		if not qflag_already_processed(flag_info):
			break
	else:
		# we have exhausted the list of qflag to process
		return False

	log_progress('Generate stubs for %s and %s in module %s' %
				 (flag_info.qflag_class, flag_info.enum_class, flag_info.module_info[0][0]))

	# check that the qflag is actually in the module
	gen_result, error_msg = generate_missing_stubs(flag_info)
	test_qflag_fname = gen_test_fname(flag_info)

	# Note that flag_info has been modified in-place with additional info:
	# enum_value1, enum_value2, full_enum_class_name, full_qflag_class_name
	if gen_result == QFlagGenResult.CodeModifiedSuccessfully:
		generate_qflag_test_file(flag_info)
		log_progress('Running pytest %s' % test_qflag_fname)
		p = subprocess.run(['pytest', '-v', '--capture=no', test_qflag_fname])
		if p.returncode != 0:
			error_msg += 'pytest failed\n'
			gen_result = QFlagGenResult.ErrorDuringProcessing
		else:
			log_progress('Running mypy %s' % test_qflag_fname)
			p = subprocess.run(['mypy', test_qflag_fname])
			if p.returncode != 0:
				error_msg += 'mypy failed\n'
				gen_result = QFlagGenResult.ErrorDuringProcessing
			else:
				log_progress('validation completed successfully')
				result_json['qflag_processed_done'].append(flag_info_dict)
				log_progress('Staging changes to git')
				subprocess.run(['git', 'add', test_qflag_fname, flag_info.module_info[0][1]])

	if gen_result == QFlagGenResult.CodeAlreadyModified:
		# qflag methods are already there, check that the test filename is here too
		if os.path.exists(test_qflag_fname):
			log_progress('QFlag %s %s already supported by %s' % (flag_info.qflag_class,
																  flag_info.enum_class,
																  flag_info.module_info[0][0]))
			result_json['qflag_already_done'].append(flag_info_dict)
		else:
			error_msg += 'QFlag methods presents but test file %s is missing\n' % test_qflag_fname
			gen_result = QFlagGenResult.ErrorDuringProcessing

	if gen_result == QFlagGenResult.ErrorDuringProcessing:
		log_progress('Error during processing of QFlag %s %s' % (flag_info.qflag_class,
															  flag_info.enum_class))
		flag_info_dict['error'] = flag_info_dict.get('error', '') + error_msg
		result_json['qflag_process_error'].append(flag_info_dict)

	# save our processing result
	with open(qflag_result_json, 'w') as f:
		json.dump(result_json, f, indent=4)

	# return True to indicate that more flags may be processed
	return True



class QFlagGenResult(Enum):
	'''Enum indicating the result of generating the possibly missing stubs on the qflag classes'''
	CodeModifiedSuccessfully = 0
	CodeAlreadyModified = 1
	ErrorDuringProcessing = 2


def generate_missing_stubs(flag_info: 'QFlagLocationInfo') -> Tuple[QFlagGenResult, str]:
	'''
    Check that the QFlag enum+class are present in the module and check whether they support
    all the advanced QFlag operations.

    If they do not, generate the missing methods.

    The flag_info input is also extended with additional information:
    * full qflag class name
    * full enum class name
    * enum value 1
    * enum value 2
    These are needed for generating a proper test file. I don't like in-place modification
    but here, it's the simplest.

	The generation consists of:

    1. On the enum class, add two methods:
		class KeyboardModifier(int):
		+       def __or__ (self, other: 'Qt.KeyboardModifier') -> 'Qt.KeyboardModifiers': ...  # type: ignore[override]
		+       def __ror__ (self, other: int) -> 'Qt.KeyboardModifiers': ...             # type: ignore[override, misc]

    2. On the qflag class, add one more overload of __init__()
		+       @typing.overload
		+       def __init__(self, f: int) -> None: ...

    3. On the qflag class, add more methods:
		+   def __or__ (self, other: typing.Union['Qt.KeyboardModifiers', 'Qt.KeyboardModifier', int]) -> 'Qt.KeyboardModifiers': ...
		+   def __and__(self, other: typing.Union['Qt.KeyboardModifiers', 'Qt.KeyboardModifier', int]) -> 'Qt.KeyboardModifiers': ...
		+   def __xor__(self, other: typing.Union['Qt.KeyboardModifiers', 'Qt.KeyboardModifier', int]) -> 'Qt.KeyboardModifiers': ...
		+   def __ror__ (self, other: 'Qt.KeyboardModifier') -> 'Qt.KeyboardModifiers': ...
		+   def __rand__(self, other: 'Qt.KeyboardModifier') -> 'Qt.KeyboardModifiers': ...
		+   def __rxor__(self, other: 'Qt.KeyboardModifier') -> 'Qt.KeyboardModifiers': ...

    Returns a tuple of (QFlagGenResult, error_msg):
    * CodeModifiedSuccessfully:
        All modifications to the code of the module have been performed successfully.
        Error message is empty.

    * CodeAlreadyModified:
        All modifications to the code were already done, no processing done.
        Error message also indicates this information.

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

	log_progress('Looking for class %s and %s in module %s' % (flag_info.qflag_class, flag_info.enum_class,
															   flag_info.module_info[0][0]))
	visitor = QFlagAndEnumFinder(flag_info.enum_class, flag_info.qflag_class)
	mod_cst.visit(visitor)

	if (visitor.enum_methods_present, visitor.qflag_method_present) == (MethodPresent.All, MethodPresent.All):
		return (QFlagGenResult.CodeAlreadyModified, visitor.error_msg)

	if (visitor.enum_methods_present, visitor.qflag_method_present) == (MethodPresent.All, MethodPresent.Not):
		visitor.error_msg += 'Enum methods are present but not QFlag methods\n'

	if (visitor.enum_methods_present, visitor.qflag_method_present) == (MethodPresent.Not, MethodPresent.All):
		visitor.error_msg += 'QFlag methods are present but not Enum methods\n'

	if visitor.error_msg:
		return (QFlagGenResult.ErrorDuringProcessing, visitor.error_msg)

	assert visitor.enum_methods_present == MethodPresent.Not
	assert visitor.qflag_method_present == MethodPresent.Not

	# storing the enum_values for further usage
	flag_info.enum_full_class_name = visitor.enum_class_full_name
	flag_info.enum_value1 = visitor.enum_value1
	flag_info.enum_value2 = visitor.enum_value2
	flag_info.qflag_full_class_name = visitor.qflag_class_full_name

	log_progress('Updating module %s by adding new methods' % flag_info.module_info[0][0])
	transformer = QFlagAndEnumUpdater(visitor.enum_class_name, visitor.enum_class_full_name,
									  visitor.qflag_class_name, visitor.qflag_class_full_name)
	updated_mod_cst = mod_cst.visit(transformer)

	log_progress('Saving updated module %s' % flag_info.module_info[0][0])
	with open(flag_info.module_info[0][1], 'w') as f:
		f.write(updated_mod_cst.code)

	return (QFlagGenResult.CodeModifiedSuccessfully, '')


class MethodPresent(Enum):
	'''An enum to reflect if a method is already present or not'''
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

		# the name of two values of the enum class
		self.enum_value1 = ''
		self.enum_value2 = ''

		# the node of the class, for debugging purpose

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
				return None
			self.enum_class_full_name = '.'.join(self.full_name_stack)

			self.check_enum_method_present(node)
			self.collect_enum_values(node)

		elif node.name.value == self.qflag_class_name:
			# we found it
			if self.qflag_class_full_name != '':
				self.error_msg = 'class %s found multiple times\n' % self.qflag_class_name
				return None
			self.qflag_class_full_name = '.'.join(self.full_name_stack)

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


	def collect_enum_values(self, enum_node: cst.ClassDef) -> None:
		'''Collect two actual values for the enum and store them into self.enum_value1 and enum_value2
		'''
		# find all lines consisting of an assignment to an ellipsis, like "AlignLeft = ..."
		enum_values = matchers.findall(enum_node.body, matchers.SimpleStatementLine(
			body=[matchers.Assign(value=matchers.Ellipsis())]))
		if len(enum_values) == 0:
			self.error_msg += 'class %s, could not find any enum values\n' % self.enum_class_full_name
			return

		self.enum_value1 = enum_values[0].body[0].targets[0].target.value
		if len(enum_values) > 1:
			self.enum_value2 = enum_values[1].body[0].targets[0].target.value
		else:
			# it works find if both values are the same so don't bother
			self.enum_value2 = self.enum_value1


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


	def leave_ClassDef(self, original_node: cst.ClassDef, updated_node: cst.ClassDef) -> cst.ClassDef:
		if original_node.name.value == self.enum_class:
			return self.transform_enum_class(original_node, updated_node)
		elif original_node.name.value == self.qflag_class:
			return self.transform_qflag_class(original_node, updated_node)
		return updated_node


	def transform_enum_class(self, original_node: cst.ClassDef, updated_node: cst.ClassDef) -> cst.ClassDef:
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

		# now calculate the proper spacing to have aligned comments
		max_code_len = max(len(code) for code, comment in new_methods_filled)
		new_methods_spaced = tuple(
			code + ' '*(4+max_code_len-len(code)) + comment
			for code, comment in new_methods_filled
		)
		new_methods_cst = tuple(cst.parse_statement(s) for s in new_methods_spaced)
		return updated_node.with_changes(body=updated_node.body.with_changes(body=
			 new_methods_cst \
			 + (updated_node.body.body[0].with_changes(leading_lines=
													   updated_node.body.body[0].leading_lines +
													   (cst.EmptyLine(),)),) \
			 + updated_node.body.body[1:] ) )


	def transform_qflag_class(self, original_node: cst.ClassDef, updated_node: cst.ClassDef) -> cst.ClassDef:
		'''
        On the qflag class, add one more overload __init__() and add more methods
        +		@typing.overload
        +       def __init__(self, f: int) -> None: ...
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
def read_qflag_test_template(template_fname: str) -> Tuple[List[str], List[str], List[str]]:
	'''Return the source of the template for generating qflags test.

	Return 3 parts as a list of strings:
	- the first part should be unmodified
	- the second part should be replaced for a specific QFlag class
	- the third part should be unmodified
	'''
	with open(template_fname) as f:
		lines = f.readlines()

	source_part_before, source_part_middle, source_part_after = [], [], []
	fill_middle, fill_after = False, False
	for l in lines:
		if fill_after:
			source_part_after.append(l)
			continue

		if fill_middle:
			if MARKER_SPECIFIC_END in l:
				fill_after = True
				source_part_after.append(l)
				continue

			source_part_middle.append(l)
			continue

		source_part_before.append(l)
		if MARKER_SPECIFIC_START in l:
			fill_middle = True

	return source_part_before, source_part_middle, source_part_after


def gen_test_fname(fli: QFlagLocationInfo) -> str:
	'''Generate the name of the test file which will verify this qflag'''
	return 'test_{fli.module_info[0][0]}_{fli.qflag_class}_{fli.enum_class}.py'.format(fli=fli)


def generate_qflag_test_file(flag_info: QFlagLocationInfo) -> None:
	'''Generate a qflag test file.

	The filename is inferred from flag_info using gen_test_fname()
	'''
	test_qflag_fname = gen_test_fname(flag_info)
	generic_part_before, _replacable_part, generic_part_after = read_qflag_test_template(TEMPLATE_QFLAGS_TESTS)

	with open(test_qflag_fname, 'w') as f:
		f.writelines(generic_part_before)

		# replace the repplacable_part with code dedicated to our qflag
		f.write('''# file generated from {source} for QFlags class "{multiFlagName}" and flag class "{oneFlagName}"
from PyQt5 import {qtmodule}

OneFlagClass = {qtmodule}.{oneFlagName}
MultiFlagClass = {qtmodule}.{multiFlagName}

oneFlagRefValue1 = {qtmodule}.{oneFlagName}.{oneFlagValue1}
oneFlagRefValue2 = {qtmodule}.{oneFlagName}.{oneFlagValue2}
'''.format(source=TEMPLATE_QFLAGS_TESTS,
		   multiFlagName=flag_info.qflag_full_class_name,
		   oneFlagName=flag_info.enum_full_class_name,
		   oneFlagValue1=flag_info.enum_value1,
		   oneFlagValue2=flag_info.enum_value2,
		   qtmodule=flag_info.module_info[0][0]
		   ))
		f.writelines(generic_part_after)
	log_progress('Test file generated: %s' % test_qflag_fname)


def generate_qflags_to_process(qt_qflag_grep_result_fname):
	'''Run the generation process from the grep output parsing to the generation of json file listing the flags to process'''
	location_qflags = identify_qflag_location(qt_qflag_grep_result_fname, QTBASE_MODULES)
	log_progress('%d qflags extracted from grep file' % len(location_qflags))
	qflags_groups = group_qflags(location_qflags)
	log_progress('%d qflags ready to be processed' % len(qflags_groups['one_flag_one_module']))

	qflags_modules_analysis_json = 'qflags_modules_analysis.json'
	# put our intermediate classification into a json file for human review
	with open(qflags_modules_analysis_json, 'w') as f:
		json.dump(qflags_groups, f, indent=4, default=json_encode_qflaglocationinfo)
	log_progress('QFlag analysis saved to: %s' % qflags_modules_analysis_json)

	qflags_to_process_json = 'qflags_to_process.json'
	extract_qflags_to_process(qflags_modules_analysis_json, qflags_to_process_json)
	log_progress('qflag file ready to process: %s' % qflags_to_process_json)

if __name__ == '__main__':

	if len(sys.argv) <= 1:
		print(USAGE)
		sys.exit(1)

	if sys.argv[1] == 'gen_qflag_stub':
		nb = 1
		if len(sys.argv) > 2:
			nb = int(sys.argv[2])

		qflags_to_process_json = 'qflags_to_process.json'
		qflag_result_json = 'qflag_process_result.json'
		more_available = True
		while nb > 0 and more_available:
			nb -= 1
			more_available = process_qflag(qflags_to_process_json, qflag_result_json)

	elif sys.argv[1] == 'analyse_grep_results':
		if len(sys.argv) <= 2:
			print('Error, you must provide the filename of the grep results\n')
			print(USAGE)
			sys.exit(1)

		grep_fname = sys.argv[2]
		generate_qflags_to_process(grep_fname)

	else:
		print('Error, invalid command line arguments\n')
		print(USAGE)
		sys.exit(1)


