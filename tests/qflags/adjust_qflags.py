from typing import List, Tuple

import functools
import pprint, collections

# command-line to generate the file: all_qflags.txt
# qt-src\qt5\qtbase>rg  --type-add "headers:*.h" -t headers Q_DECLARE_FLAGS --no-heading > all-flags.txt
# note add something to make re at word-boundary
DECLARED_QFLAGS_FNAME = 'all-flags.txt'
QFLAG_SRC='src\\corelib\\global\\qflags.h'
SOURCE_QFLAGS_TESTS = 'qflags_windowFlags.py'
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

def parse_declared_qflags(fname: str) -> List[Tuple[str, str, str, List[str]]]:
	'''Parses the list of modules from QTBASE_MODULES and look for the qflags declated in QFLAG_SRC

	Sort the result into 4 cases:
	- qflag present once in only one module: we are sure that these can be safely replaced by a better version
	- qflag present multiple times in one module: probably some extra module parsing might be needed to
	    	understand which version is the qflag which we want to modify
	- qflag present multiple times in multiples modules: we can not infer which module the flag is in
	- qflag not present anywhere: these are probably not exported to PyQt
	'''
	parsed_qflags = []	# type: List[Tuple[str, str, str, List[str]]] # -> fname, qflags, enum
	with open(fname) as f:
		for l in f.readlines()[:]:
			if len(l.strip()) == 0:
				continue
			qflag_fname, qflag_declare_stmt = [s.strip(' \t\n') for s in l.split(':')]
			if qflag_fname == QFLAG_SRC:
				# do not include actual implementation of qflags
				continue
			assert 'Q_DECLARE_FLAGS' in qflag_declare_stmt
			print(qflag_declare_stmt)
			s = qflag_declare_stmt[qflag_declare_stmt.index('(')+1:qflag_declare_stmt.index(')')]
			qflag_class, enum_class = [v.strip(' ') for v in s.split(',')]
			parsed_qflags.append((qflag_fname, qflag_class, enum_class, []))
			# print(qflag_fname)
			# print('->', qflag_class, enum_class)

	# fill up modules with content
	for mod_info in QTBASE_MODULES:
		mod_name, mod_stub_path = mod_info
		mod_info.append(open(mod_stub_path).read())

	mod_qflags = collections.defaultdict(lambda: collections.defaultdict(int))

	for qflag_info in parsed_qflags:
		qflag_fname, qflag_class, enum_class, qflag_modules = qflag_info

		decl_qflag_class = 'class %s(' % qflag_class
		decl_enum_class = 'class %s(' % enum_class
		for mod_name, mod_stub_path, mod_content in QTBASE_MODULES:

			if decl_qflag_class in mod_content and decl_enum_class in mod_content:
				# we have found one module
				print('Adding QFlags %s to module %s' % (qflag_class, mod_name))
				qflag_modules.append(mod_name)
				mod_qflags[mod_name][qflag_class] += 1


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
	qflags_with_module = parse_declared_qflags(DECLARED_QFLAGS_FNAME)
	for qflag_fname, qflag_class, enum_class, qflag_modules in qflags_with_module:
		# generate_test_file(qflag_class, enum_class, qflag_fname)
		pass
