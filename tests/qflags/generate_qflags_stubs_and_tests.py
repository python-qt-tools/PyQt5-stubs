from typing import List, Tuple, Dict

import dataclasses
import functools
import json
import pprint, collections

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

@dataclasses.dataclass
class QFlagLocationInfo:
	grep_line: str
	qflag_class: str
	qflag_enum: str

	# list of (module_name, module_path)
	module_info: List[ Tuple[str, str] ]

def json_encode_qflaglocationinfo(flag_loc_info: object) -> object:
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

def extract_qflags_to_process(qflags_modules_analysis_json: str) -> None:
	'''Take the json file as input describing qflags and their location in modules.

	The qflags which are located in a single module will be selected for further processing.

	The others are marked as skipped.
	'''
	return
	qflags_with_one_module_single = [ qflag_info for qflag_info in parsed_qflags
				   if (len(qflag_info[-1]) == 1) and (mod_qflags[qflag_info[-1][0]][qflag_info[1]] == 1) ]
	qflags_with_one_module_multiple = [ qflag_info for qflag_info in parsed_qflags
				  if (len(qflag_info[-1]) == 1) and (mod_qflags[qflag_info[-1][0]][qflag_info[1]] != 1) ]
	qflags_with_no_module = [ qflag_info for qflag_info in parsed_qflags if len(qflag_info[-1]) == 0]
	qflags_with_many_module = [ qflag_info for qflag_info in parsed_qflags if len(qflag_info[-1]) > 1]

	qflags_with_one_module_single.sort(key=lambda v: (v[-1], v[1]))
	qflags_with_one_module_multiple.sort(key=lambda v: (v[-1], v[1]))
	qflags_with_no_module.sort(key=lambda v: (v[-1], v[1]))
	qflags_with_many_module.sort(key=lambda v: (v[-1], v[1]))

	DISP_RESULTS = True
	if DISP_RESULTS:
		print('\nFlags identified with one module, unique in the module')
		last_mod_name = ''
		for qflag_fname, qflag_class, enum_class, qflag_modules in qflags_with_one_module_single:
			mod_name = qflag_modules[0]
			if mod_name != last_mod_name:
				print('\t%s:' % mod_name)
				last_mod_name = mod_name
			print('\t\t"%s" "%s" \t\t%s' % (qflag_class, enum_class, qflag_fname))


		print('\nFlags identified with one module, multiples in the module')
		last_mod_name = ''
		for qflag_fname, qflag_class, enum_class, qflag_modules in qflags_with_one_module_multiple:
			mod_name = qflag_modules[0]
			if mod_name != last_mod_name:
				print('\t%s:' % mod_name)
				last_mod_name = mod_name
			print('\t\t"%s" "%s" \t\t%s' % (qflag_class, enum_class, qflag_fname))


		print('\nqflags without module:')
		for qflag_fname, qflag_class, enum_class, qflag_modules in qflags_with_no_module:
			print('\t\t"%s" "%s" \t\t%s []' % (qflag_class, enum_class, qflag_fname))


		print('\nqflags with many module:')
		for qflag_fname, qflag_class, enum_class, qflag_modules in qflags_with_many_module:
			print('\t\t"%s" "%s" \t\t%s [%s]' % (qflag_class, enum_class, qflag_fname, ' '.join(qflag_modules)))

	return qflags_with_one_module_single

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

if __name__ == '__main__':
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

	qflags_to_process = extract_qflags_to_process(qflags_modules_analysis_json)
	#
