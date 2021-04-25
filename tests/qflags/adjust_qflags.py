import pprint

# command-line to generate the file: all_qflags.txt
# qt-src\qt5\qtbase>rg  --type-add "headers:*.h" -t headers Q_DECLARE_FLAGS --no-heading > all-flags.txt
# note add something to make re at word-boundary
DECLARED_QFLAGS_FNAME = 'all-flags.txt'
QFLAG_SRC='src\\corelib\\global\\qflags.h'

MODULES = [
	['QtCore', '../../PyQt5-stubs/QtCore.pyi'],
	['QtWidgets', '../../PyQt5-stubs/QtWidgets.pyi'],
	['QtGui', '../../PyQt5-stubs/QtGui.pyi'],
	['QtNetwork', '../../PyQt5-stubs/QtNetwork.pyi'],

]

def parse_declared_qflags(fname: str) -> None:
	parsed_qflags = []	# type: List[Tuple[str, str, str]] -> fname, qflags, enum
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
	for mod_info in MODULES:
		mod_name, mod_stub_path = mod_info
		mod_info.append(open(mod_stub_path).read())


	for qflag_info in parsed_qflags:
		qflag_fname, qflag_class, enum_class, qflag_modules = qflag_info

		decl_qflag_class = 'class %s(' % qflag_class
		decl_enum_class = 'class %s(' % enum_class
		for mod_name, mod_stub_path, mod_content in MODULES:

			if decl_qflag_class in mod_content and decl_enum_class in mod_content:
				# we have found one module
				print('Adding QFlags %s to module %s' % (qflag_class, mod_name))
				qflag_modules.append(mod_name)


	qflags_with_one_module = [ qflag_info for qflag_info in parsed_qflags if len(qflag_info[-1]) == 1]
	qflags_with_no_module = [ qflag_info for qflag_info in parsed_qflags if len(qflag_info[-1]) == 0]
	qflags_with_many_module = [ qflag_info for qflag_info in parsed_qflags if len(qflag_info[-1]) > 1]

	qflags_with_one_module.sort(key=lambda v: (v[-1], v[1]))
	qflags_with_no_module.sort(key=lambda v: (v[-1], v[1]))
	qflags_with_many_module.sort(key=lambda v: (v[-1], v[1]))

	print('\nFlags idenfied with a module')
	last_mod_name = ''
	for qflag_fname, qflag_class, enum_class, qflag_modules in qflags_with_one_module:
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



# parse all-qflags.txt
#	-> identify QFlag class and enum
#	-> identify attached module
# save the result

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
	parse_declared_qflags(DECLARED_QFLAGS_FNAME)