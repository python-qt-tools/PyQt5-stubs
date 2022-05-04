from typing import List, Tuple, Dict, Union, Any, Optional, cast

import dataclasses
import functools
import json
import os
import sys
import subprocess
import traceback
from enum import Enum

from PyQt5 import (QtCore, QtWidgets, QtGui, QtNetwork, QtDBus, QtOpenGL,
                   QtPrintSupport, QtSql, QtTest, QtXml,
                    Qt3DAnimation, Qt3DCore, Qt3DExtras, Qt3DInput, Qt3DLogic, Qt3DRender,
                    QtChart,
                    QtBluetooth, QtNfc,
                    QtDataVisualization,
                    QtQuick, QtQml,
                    QtPositioning, QtLocation,
                    QtMultimedia,
                    QtSerialPort,
                    QtDesigner,
                    QtWebEngineWidgets, QtWebEngineCore,
                   )
try:
    import libcst as cst
    import libcst.matchers as matchers
except ImportError:
    raise ImportError('You need libcst to run the missing stubs generation\n'
                      'Please run the command:\n\tpython -m pip install libcst')

MODULE_GROUPS = {
    'qtbase': [
        'QtCore',
        'QtWidgets',
        'QtGui',
        'QtNetwork',
        'QtDBus',
        'QtOpenGL',
        'QtPrintSupport',
        'QtSql',
        'QtTest',
        'QtXml',
    ],
    'qt3d': [
        'Qt3DAnimation',
        'Qt3DCore',
        'Qt3DExtras',
        'Qt3DInput',
        'Qt3DLogic',
        'Qt3DRender',
    ],
    'qtchart': [
        'QtChart',
    ],
    'qtconnectivity': [
        'QtBluetooth',
        'QtNfc',
    ],
    'qtdatavisualization': [
        'QtDataVisualization',
    ],
    'qtquick': [
        'QtQuick',
        'QtQml',
    ],
    'qtlocation': [
        'QtPositioning',
        'QtLocation',
    ],
    'qtmultimedia': [
        'QtMultimedia',
    ],
    'qtserialport': [
        'QtSerialPort',
    ],
}


USAGE = '''Usage 1: {prog} analyse_grep_results <grep result filename> --group <module_group>
    Process the <grep result filename> to extract all the qflag location information. 
    
    Generates two output:
    - qflags_modules_analysis.json : a general file describing which qflag are suitable for processing
    - qflags_to_process.json: a list of qflag ready to process with the next command.
    
    The <module group> is the name of a group of modules to see where to look for for the exact name
    of the qflags. Possible modules groups are:
    - {groups}
    
Usage 2: {prog} gen_qflag_stub (<number>|all) (--auto-commit)
    Using file qflag_to_process.json, process qflags and modify the PyQt modules.
    The output of this processing is available in qflags_process_result.json
    
    If <number> is not provided, defaults to 1. If "all" is provied, all qflags
    are processed.
    
    If --auto-commit is specified, a git commit is performed after each successful QFlag validation

'''.format(prog=sys.argv[0], groups='\n    - '.join(MODULE_GROUPS.keys()))



def log_progress(s: str) -> None:
    print('>>>>>>>>>>>>>>', s)

@dataclasses.dataclass
class QFlagLocationInfo:

    # qflag and enum name used in the QDECLARE() grep line
    qflag_class: str
    enum_class: str

    # sometimes, human help is needed to identify a qflag/enum pair
    human_hint_qflag_full_class_name: str = ''
    human_hint_enum_full_class_name: str = ''

    # one or more grep lines where this qflag name has been found
    grep_line: Tuple[str] = dataclasses.field(default_factory=tuple)

    # full class name (including nesting classes) generated in a second pass
    qflag_full_class_name: str = ''
    enum_full_class_name: str = ''
    enum_value1: str = ''
    enum_value2: str = ''

    # number of occurence in this module
    module_count: int = 0

    # index of occurence in this module
    module_idx: int = -1

    # module name and path
    module_name: str = ''
    module_path: str = ''

    def key(self) -> Tuple[str, str, str]:
        '''Mostly unique description of the QFlagInfo'''
        return (self.module_name, self.qflag_class, self.enum_class)

    # specific behavior of some QFlag classes varies slightly
    # this helps to define the exact behavior
    or_converts_to_multi: bool = True
    or_int_converts_to_multi: bool = False
    int_or_converts_to_multi: bool = True
    supports_one_op_multi: bool = True


def json_encode_qflaglocationinfo(flag_loc_info: object) -> Union[object, Dict[str, Any]]:
    """Encode the QFlagClassLoationInfo into a format suitable for json export (a dict)"""
    if not isinstance(flag_loc_info, QFlagLocationInfo):
        # oups, we don't know how to encode that
        return flag_loc_info

    d = dataclasses.asdict(flag_loc_info)
    # when returning the result of the grep analysis, we want only a specific subset
    # of the datablass fields
    del d["or_converts_to_multi"]
    del d["or_int_converts_to_multi"]
    del d["int_or_converts_to_multi"]
    del d["supports_one_op_multi"]

    return d


def identify_qflag_location(fname_grep_result: str,
                            qt_modules: List[str]
                            ) -> List[ QFlagLocationInfo ]:
    """Parses the grep results to extract each qflag, and then look into all Qt modules
    to see where the flag is located.

    Return a list of QFlagLocationInfo indicating in which module the flag has been located.
    """
    # the file defining the qflag implementation, to be skipped when performing QDECLARE analysis
    QFLAG_SRC = 'src\\corelib\\global\\qflags.h'

    parsed_qflags = {}  # type: Dict[ Tuple[str, str], QFlagLocationInfo ]
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
            if (qflag_class, enum_class) in parsed_qflags:
                # we already have one similar name in our DB
                # just extend the grep line then
                parsed_qflags[(qflag_class, enum_class)].grep_line += (grep_line,)
            else:
                parsed_qflags[(qflag_class, enum_class)] = QFlagLocationInfo(qflag_class, enum_class, grep_line=(grep_line,))

    # fill up modules with content
    qt_modules_content = [ (mod_name, open('../../PyQt5-stubs/%s.pyi' % mod_name, encoding='utf8').read())
                           for mod_name in qt_modules]

    # associate a qflag enum/class with a mapping from module to QFlagLocationInfo
    module_mapping: Dict[ Tuple[str, str], Dict[str, QFlagLocationInfo]] = {}
    flag_not_found = []

    for qflag_key, flag_info in parsed_qflags.items():
        decl_qflag_class = 'class %s(sip.simplewrapper' % flag_info.qflag_class
        decl_qflag_class2 = 'class %s(sip.wrapper' % flag_info.qflag_class
        decl_enum_class = 'class %s(int' % flag_info.enum_class
        module_found = False
        for mod_name, mod_content in qt_modules_content:

            if (decl_qflag_class in mod_content or decl_qflag_class2 in mod_content) \
                    and decl_enum_class in mod_content:
                # we have found one module
                module_found = True
                # print('Adding QFlags %s to module %s' % (flag_info.qflag_class, mod_name))
                if qflag_key not in module_mapping:
                    module_mapping[qflag_key] = {}
                else:
                    pass
                mod_map = module_mapping[qflag_key]

                if mod_name in mod_map:
                    raise ValueError('Not supposed to happen!')

                # register the number of time where this flag happens in this specific module
                mod_map[mod_name] = dataclasses.replace(flag_info)  # this means a fresh copy of flag_info
                mod_map[mod_name].module_count = 1

                count_qflag_class = mod_content.count(decl_qflag_class)
                count_enum_class = mod_content.count(decl_enum_class)
                if count_qflag_class > 1 and count_enum_class > 1:
                    # print('QFlag present more than once, adding it more than once')
                    mod_map[mod_name].module_count += min(count_qflag_class, count_enum_class) - 1

        if not module_found:
            flag_not_found.append(qflag_key)

    # now, we flatten the structure by recreating one QFlagLocationInfo per module location

    all_qflags: List[QFlagLocationInfo] = []
    for mod_map in module_mapping.values():
        for mod_name, flag_info in mod_map.items():
            idx = 0
            while idx < flag_info.module_count:
                all_qflags.append(dataclasses.replace(flag_info, module_idx=idx,
                                                      module_name=mod_name,
                                                      module_path='../../PyQt5-stubs/%s.pyi' % mod_name))
                idx += 1

    for qflag_key in flag_not_found:
        all_qflags.append(parsed_qflags[qflag_key])

    return all_qflags


def group_qflags(qflag_location: List[QFlagLocationInfo],
                 qflags_group_initial: Optional[Dict[str, List[QFlagLocationInfo]]]) -> Dict[str, List[QFlagLocationInfo]]:
    """Group the QFlags into the following groups (inside a dictionnary):
    * flag_and_module_identified: this flag is present once in one module exactly.
    * flag_without_module: this flag is not present in any modules at all.

    The first group is suitable for automatic processing.
    The last group reflects the QFlags not exported to PyQt or coming from modules not present in PyQt
    """
    if not qflags_group_initial:
        qflags_group_initial = {
            'flag_and_module_identified': [],
            'flag_without_module': [],
        }

    qflag_already_present = [
        (loc.module_name, loc.qflag_class, loc.enum_class)
        for loc in qflags_group_initial['flag_and_module_identified']
    ]

    for flag_info in qflag_location:
        qflag_key = flag_info.key()

        if flag_info.module_name != '':
            if qflag_key in qflag_already_present:
                print('QFlag already analysed: ', qflag_key)
                continue

            qflags_group_initial['flag_and_module_identified'].append(flag_info)
        else:
            qflags_group_initial['flag_without_module'].append(flag_info)

    return qflags_group_initial


def extract_qflags_to_process(qflags_modules_analysis_json: str,
                              qflags_to_process_json: str,
                              module_group: str,
                              ) -> None:
    """Take the json file as input describing qflags and their modules and output a json file of qflags planned to be processed.

    The qflags which are located in a single module will be selected for further processing.
    The others are marked as skipped with a proper reason.
    """
    with open(qflags_modules_analysis_json) as f:
        d = json.load(f)

    if os.path.exists(qflags_to_process_json):
        with open(qflags_to_process_json) as f:
            result = json.load(f)
    else:
        result = {
            '__': 'This file can be adjusted manually by a human prior to being processed by the tool',
            'qflags_to_process': [],
            'qflags_to_skip': [],
        }

    skip_already_present = set( (d['qflag_class'], d['enum_class'])
        for d in result['qflags_to_skip']
    )
    for flag_info in d['flag_without_module']:
        key = (flag_info['qflag_class'], flag_info['enum_class'])
        if key in skip_already_present:
            continue
        cast(List, result['qflags_to_skip']).append(
            {
                'qflag_class': flag_info['qflag_class'],
                'enum_class':  flag_info['enum_class'],
                'skip_reason':  'QFlag not found in module group %s' % module_group,
            }
        )

    already_present = set((flag_info_d['module_name'], flag_info_d['qflag_class'], flag_info_d['enum_class'])
                          for flag_info_d in result['qflags_to_process'])

    for flag_info_d in d['flag_and_module_identified']:
        key = (flag_info_d['module_name'], flag_info_d['qflag_class'], flag_info_d['enum_class'])
        if key in already_present:
            print('QFlag to process already present: ', key )
            continue
        cast(List, result['qflags_to_process']).append( flag_info_d )

    with open(qflags_to_process_json, 'w') as f:
        json.dump(result, f, indent=4)


def process_qflag(qflag_to_process_json: str, qflag_result_json: str, auto_commit: bool) -> int:
    """Read the qflags to process from the json file

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

    * auto_commit: if True, a git commit is performed after each successful QFlag validation

    Return number of remaining flags to process (0 when everything done)
    """

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
        """Return True if the qflag is already included in one of the result lists
        of result_json"""
        flag_desc = (flag_info.module_name, flag_info.module_idx,
                     flag_info.qflag_class, flag_info.enum_class)
        already_done_set = set( (flag_info_dict['module_name'],
                                 flag_info_dict['module_idx'],
                         flag_info_dict['qflag_class'],
                         flag_info_dict['enum_class'])
                        for flag_info_dict in result_json['qflag_already_done'])
        processed_done_set = set( (flag_info_dict['module_name'],
                                   flag_info_dict['module_idx'],
                                   flag_info_dict['qflag_class'],
                                   flag_info_dict['enum_class'])
                                  for flag_info_dict in result_json['qflag_processed_done'])
        process_error_set = set( (flag_info_dict['module_name'],
                                  flag_info_dict['module_idx'],
                                  flag_info_dict['qflag_class'],
                         flag_info_dict['enum_class'])
                            for flag_info_dict in result_json['qflag_process_error'])
        if flag_desc in already_done_set or flag_desc in processed_done_set or flag_desc in process_error_set:
            return True
        return False

    while len(qflags_to_process) != 0:
        flag_info_dict = qflags_to_process.pop(0)
        flag_info = QFlagLocationInfo(**flag_info_dict)
        flag_info.grep_line = tuple(flag_info.grep_line)    # to make it hashable
        if not qflag_already_processed(flag_info):
            break
    else:
        # we have exhausted the list of qflag to process
        return 0

    log_progress('Processing %s and %s in module %s, index %d' %
             (flag_info.qflag_class, flag_info.enum_class, flag_info.module_name, flag_info.module_idx))

    # check that the qflag is actually in the module
    gen_result, error_msg, old_mod_content = generate_missing_stubs(flag_info)
    flag_info_dict = dataclasses.asdict(flag_info)
    test_qflag_fname = gen_test_fname(flag_info)

    # Note that flag_info has been modified in-place with additional info:
    # enum_value1, enum_value2, full_enum_class_name, full_qflag_class_name
    if gen_result == QFlagGenResult.CodeModifiedSuccessfully:
        generate_qflag_test_file(flag_info)
        log_progress('Running pytest %s' % test_qflag_fname)
        p = subprocess.run(['pytest', '-v', '--capture=no', test_qflag_fname])
        if p.returncode != 0:
            error_msg += 'pytest failed:\n'
            # Re-run the same command to capture the output in the error message
            # in the first run, the stdout/stderr was simply displayed and not captured
            # here, we want to capture it and not display it
            p = subprocess.run(['pytest', '-v', '--capture=no', test_qflag_fname],
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf8')
            error_msg += p.stdout
            gen_result = QFlagGenResult.ErrorDuringProcessing
            log_progress('Restoring module content')
            with open(flag_info.module_path, 'w') as f:
                f.write(old_mod_content)
            os.unlink(test_qflag_fname)
        else:
            log_progress('Running mypy %s' % test_qflag_fname)
            p = subprocess.run(['mypy', test_qflag_fname])
            if p.returncode != 0:
                error_msg += 'mypy failed\n'
                # Re-run the same command to capture the output in the error message
                # in the first run, the stdout/stderr was simply displayed and not captured
                # here, we want to capture it and not display it
                p = subprocess.run(['mypy', test_qflag_fname],
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf8')
                error_msg += p.stdout
                gen_result = QFlagGenResult.ErrorDuringProcessing
                log_progress('Restoring module content')
                with open(flag_info.module_path, 'w') as f:
                    f.write(old_mod_content)
                os.unlink(test_qflag_fname)
            else:
                log_progress('validation completed successfully')
                result_json['qflag_processed_done'].append(flag_info_dict)

                if auto_commit:
                    log_progress('Performing git commit')
                    subprocess.run(['git', 'add', test_qflag_fname, flag_info.module_path])
                    subprocess.run(['git', 'commit', '-m', 'QFlag operations for %s, %s in module %s' %
                          (flag_info.qflag_full_class_name, flag_info.enum_full_class_name, flag_info.module_name)])

    if gen_result == QFlagGenResult.CodeAlreadyModified:
        # qflag methods are already there, check that the test filename is here too
        if os.path.exists(test_qflag_fname):
            log_progress('QFlag %s %s already supported by %s' % (flag_info.qflag_class,
                                                                  flag_info.enum_class,
                                                                  flag_info.module_name))
            result_json['qflag_already_done'].append(flag_info_dict)
        else:
            error_msg += 'QFlag methods presents but test file %s is missing\n' % test_qflag_fname
            gen_result = QFlagGenResult.ErrorDuringProcessing

    if gen_result == QFlagGenResult.ErrorDuringProcessing:
        log_progress('Error during processing of QFlag %s %s' % (flag_info.qflag_class,
                                                              flag_info.enum_class))
        print(error_msg)
        flag_info_dict['error'] = error_msg.splitlines()
        result_json['qflag_process_error'].append(flag_info_dict)

    # save our processing result
    with open(qflag_result_json, 'w') as f:
        json.dump(result_json, f, indent=4)

    # return True to indicate that more flags may be processed
    log_progress('.')
    return len(qflags_to_process)

local_cst_module_cache: Dict[str, Tuple[str, cst.Module]] = {}

def retrieve_cst_parsed_module(mod_name: str, mod_content: str) -> cst.Module:
    '''Return the cst parsed module and cache the result for each module name'''
    if mod_name in local_cst_module_cache:
        cached_mod_content, cached_parsed_module = local_cst_module_cache[mod_name]
        if cached_mod_content == mod_content:
            log_progress('Returning cached %s parse results' % mod_name)
            return cached_parsed_module
        else:
            log_progress('Updating cache for module %s' % mod_name)
    else:
        log_progress('Parsing module %s and adding it to cache' % mod_name)

    parsed_module = cst.parse_module(mod_content)
    local_cst_module_cache[mod_name] = (mod_content, parsed_module)
    return parsed_module


class QFlagGenResult(Enum):
    """Enum indicating the result of generating the possibly missing stubs on the qflag classes"""
    CodeModifiedSuccessfully = 0
    CodeAlreadyModified = 1
    ErrorDuringProcessing = 2


def generate_missing_stubs(flag_info: 'QFlagLocationInfo') -> Tuple[QFlagGenResult, str, str]:
    """
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

    Returns a tuple of (QFlagGenResult, error_msg, mod_content):
    * CodeModifiedSuccessfully:
        All modifications to the code of the module have been performed successfully.
        Error message is empty.
        mod_content contains the full text of the module. If when performing verifications on this
        change, it turns out that the change is not valid, you can restore the module to its
        previous content using mod_content

    * CodeAlreadyModified:
        All modifications to the code were already done, no processing done.
        Error message also indicates this information.
        mod_content is empty (not useful)

    * ErrorDuringProcessing:
        Some error occured during the processing, such as some modifications were partially done,
        class not found, class found multiple times, ...

        The detail of the error is provided in the second argument of the return value.
        mod_content is empty (not useful)
"""
    log_progress('Opening module %s' % flag_info.module_name)
    with open(flag_info.module_path) as f:
        mod_content = f.read()

    mod_cst = retrieve_cst_parsed_module(flag_info.module_name, mod_content)

    log_progress('Looking for class %s and %s in module %s, index %d' %
                 (flag_info.qflag_class, flag_info.enum_class, flag_info.module_name, flag_info.module_idx))
    if len(flag_info.human_hint_enum_full_class_name) and len(flag_info.human_hint_qflag_full_class_name):
        log_progress('Using hints: %s and %s' % (flag_info.human_hint_enum_full_class_name, flag_info.human_hint_qflag_full_class_name))
    visitor = QFlagAndEnumFinder(flag_info.enum_class, flag_info.qflag_class,
                                 flag_info.module_count, flag_info.module_idx,
                                 flag_info.human_hint_enum_full_class_name,
                                 flag_info.human_hint_qflag_full_class_name,
                                 )
    mod_cst.visit(visitor)

    # storing the enum_values + full class name for further usage
    flag_info.enum_full_class_name = visitor.enum_class_full_name
    flag_info.enum_value1 = visitor.enum_value1
    flag_info.enum_value2 = visitor.enum_value2
    flag_info.qflag_full_class_name = visitor.qflag_class_full_name

    if visitor.enum_class_full_name == '':
        return (QFlagGenResult.ErrorDuringProcessing, 'Could not locate class %s' % visitor.enum_class_name, '')

    if visitor.qflag_class_full_name == '':
        return (QFlagGenResult.ErrorDuringProcessing, 'Could not locate class %s' % visitor.qflag_class_name, '')

    # evaluate exact behavior of QFlag
    try:
        flag_info.or_converts_to_multi = not eval('''type({qtmodule}.{oneFlagName}.{value1} | {qtmodule}.{oneFlagName}.{value2}) == int'''.format(
            value1=flag_info.enum_value1, value2=flag_info.enum_value2,
            qtmodule=flag_info.module_name,
            oneFlagName=flag_info.enum_full_class_name))
    except Exception as exc:
        return (QFlagGenResult.ErrorDuringProcessing, traceback.format_exc(), '')

    flag_info.or_int_converts_to_multi = not eval('''type({qtmodule}.{oneFlagName}.{value1} | 33) == int'''.format(
        value1=flag_info.enum_value1, qtmodule = flag_info.module_name, oneFlagName = flag_info.enum_full_class_name))
    flag_info.int_or_converts_to_multi = not eval('''type(33 | {qtmodule}.{oneFlagName}.{value1}) == int'''.format(
        value1=flag_info.enum_value1, qtmodule = flag_info.module_name, oneFlagName = flag_info.enum_full_class_name))

    try:
        flag_info.supports_one_op_multi = True
        eval('''{qtmodule}.{oneFlagName}.{enumValue} | {qtmodule}.{multiFlagName}()'''.format(
            oneFlagName=flag_info.enum_full_class_name,
        enumValue=flag_info.enum_value1,
            multiFlagName=flag_info.qflag_full_class_name,
            qtmodule=flag_info.module_name
        ))
    except TypeError:
        flag_info.supports_one_op_multi = False

    if (visitor.enum_methods_present, visitor.qflag_method_present) == (MethodPresent.All, MethodPresent.All):
        return (QFlagGenResult.CodeAlreadyModified, visitor.error_msg, '')

    if (visitor.enum_methods_present, visitor.qflag_method_present) == (MethodPresent.All, MethodPresent.Not):
        visitor.error_msg += 'Enum methods are present but not QFlag methods\n'

    if (visitor.enum_methods_present, visitor.qflag_method_present) == (MethodPresent.Not, MethodPresent.All):
        # this is ok if enum does not need any special method
        if (flag_info.or_converts_to_multi
           or flag_info.int_or_converts_to_multi
           or flag_info.or_int_converts_to_multi):
            # this means __or__ or __ror__ must be present, we have an error
            visitor.error_msg += 'QFlag methods are present but not Enum methods\n'
        else:
            # it's ok
            return (QFlagGenResult.CodeAlreadyModified, visitor.error_msg, '')

    if visitor.error_msg:
        return (QFlagGenResult.ErrorDuringProcessing, visitor.error_msg, '')

    log_progress('Found %s and %s' % (flag_info.qflag_full_class_name, flag_info.enum_full_class_name))

    print('enum behavior:')
    print('- or_converts_to_multi: ', flag_info.or_converts_to_multi)
    print('- or_int_converts_to_multi: ', flag_info.or_int_converts_to_multi)
    print('- int_or_converts_to_multi: ', flag_info.int_or_converts_to_multi)
    print('- supports_one_op_multi: ', flag_info.supports_one_op_multi)

    log_progress('Updating module %s by adding new methods' % flag_info.module_name)
    transformer = QFlagAndEnumUpdater(visitor.enum_class_name, visitor.enum_class_full_name,
                                      visitor.qflag_class_name, visitor.qflag_class_full_name, flag_info.module_idx,
                                      flag_info.human_hint_enum_full_class_name,
                                      flag_info.human_hint_qflag_full_class_name,
                                      flag_info.or_converts_to_multi,
                                      flag_info.or_int_converts_to_multi,
                                      flag_info.int_or_converts_to_multi)
    updated_mod_cst = mod_cst.visit(transformer)

    if transformer.error_msg:
        return (QFlagGenResult.ErrorDuringProcessing, visitor.error_msg, '')

    log_progress('Saving updated module %s' % flag_info.module_name)
    with open(flag_info.module_path, 'w') as f:
        f.write(updated_mod_cst.code)

    return (QFlagGenResult.CodeModifiedSuccessfully, '', mod_content)


class MethodPresent(Enum):
    """An enum to reflect if a method is already present or not"""
    Unset = 0
    All = 1
    Not = 2
    Partial = 3


class QFlagAndEnumFinder(cst.CSTVisitor):

    def __init__(self, enum_class: str, qflag_class: str,
                 module_count: int, module_idx: int,
                 human_hint_enum_full_class_name: str = '',
                 human_hint_qflag_full_class_name: str = '',
                 ) -> None:
        super().__init__()

        # used internally to generate the full class name
        self.full_name_stack: List[str] = []

        # the class name we are looking for
        self.enum_class_name = enum_class
        self.qflag_class_name = qflag_class

        # human help for finding the class
        if human_hint_enum_full_class_name:
            self.human_hint_enum_full_class_name = human_hint_enum_full_class_name.split('.')
        else:
            self.human_hint_enum_full_class_name = ''

        if human_hint_qflag_full_class_name:
            self.human_hint_qflag_full_class_name = human_hint_qflag_full_class_name.split('.')
        else:
            self.human_hint_qflag_full_class_name = human_hint_qflag_full_class_name

        # the number of expected occurences in this module of this flag
        self.module_count = module_count

        # the index of the flag in the module which we are looking for
        # useful if there are multiple same name flags
        self.module_idx = module_idx

        # our internal index for finding this class
        self.visit_enum_idx = -1
        self.visit_qflag_idx = -1

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
            self.visit_enum_idx += 1
            found_enum_class = False
            if self.human_hint_enum_full_class_name:
                if self.human_hint_enum_full_class_name == self.full_name_stack:
                    found_enum_class = True
            else:
                if self.visit_enum_idx > self.module_count:
                    self.error_msg = 'class %s found too many times: %d\n' % (self.enum_class_name, self.visit_enum_idx)
                    return None

                if self.visit_enum_idx == self.module_idx:
                    # we found the index we are looking for
                    found_enum_class = True

            if found_enum_class:
                if self.check_enum_method_present(node):
                    self.enum_class_full_name = '.'.join(self.full_name_stack)
                    self.collect_enum_values(node)
                return None

        elif node.name.value == self.qflag_class_name:
            self.visit_qflag_idx += 1
            found_qflag_class = False
            if self.human_hint_qflag_full_class_name:
                if self.human_hint_qflag_full_class_name == self.full_name_stack:
                    found_qflag_class = True
            else:
                if self.visit_qflag_idx > self.module_count:
                    self.error_msg = 'class %s found too times: %d\n' % (self.qflag_class_name, self.visit_qflag_idx)
                    return None

                if self.visit_qflag_idx == self.module_idx:
                    # we found the index we are looking for
                    found_qflag_class = True

            if found_qflag_class:
                if self.check_qflag_method_present(node):
                    self.qflag_class_full_name = '.'.join(self.full_name_stack)
                return None

        return None


    def check_enum_method_present(self, enum_node: cst.ClassDef) -> bool:
        """Check if the class contains method __or__ and __ror__ with one argument and if class
        inherit from int"""
        if len(enum_node.bases) == 0 or enum_node.bases[0].value.value != 'int':
            # class does not inherit from int, not the one we are looking for
            return False
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

        return True


    def collect_enum_values(self, enum_node: cst.ClassDef) -> None:
        """Collect two actual values for the enum and store them into self.enum_value1 and enum_value2
        """
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


    def check_qflag_method_present(self, qflag_node: cst.ClassDef) -> bool:
        """Check if the class contains method:
        def __or__
        def __and__
        def __xor__
        def __ror__
        def __rand__
        def __rxor__

        with one argument.

        def __init__(self, f: typing.Union['Qt.KeyboardModifiers', 'Qt.KeyboardModifier']) -> None:
        def __init__(self, f: typing.Union['Qt.KeyboardModifiers', 'Qt.KeyboardModifier', int]) -> None:
        """
        if (len(qflag_node.bases) == 0
           or not (matchers.matches(qflag_node.bases[0],
                                         matchers.Arg(value=matchers.Attribute(value=matchers.Name('sip'),
                                                                               attr=matchers.Name('simplewrapper')
                                                                               )
                                                      )
                                         )
                   or matchers.matches(qflag_node.bases[0],
                                matchers.Arg(value=matchers.Attribute(value=matchers.Name('sip'),
                                                                      attr=matchers.Name('wrapper')
                                                                      )
                                             )
                                )
                )
            ):
            # 'Class does not inherit from sip.simplewrapper' or sip.wrapper
            return False

        has_method = [
            (m, matchers.findall(qflag_node.body, matchers.FunctionDef(name=matchers.Name(m))))
            for m in ('__or__', '__and__', '__xor__', '__ror__', '__rxor__', '__rand__')
        ]

        if all(has_info[1] for has_info in has_method):
            # all method presents
            self.qflag_method_present = MethodPresent.All
            return True

        if all(not has_info[1] for has_info in has_method):
            # all method absent
            self.qflag_method_present = MethodPresent.Not
            return True

        self.qflag_method_present = MethodPresent.Partial

        for m_name, m_has in has_method:
            if m_has:
                self.error_msg += 'class %s, method %s present without all others\n' \
                                  % ((self.qflag_class_full_name, m_name))
            else:
                self.error_msg += 'class %s, method %s missing\n' \
                                  % ((self.qflag_class_full_name, m_name))
        return True


    def visit_FunctionDef(self, node: cst.FunctionDef) -> Optional[bool]:
        self.full_name_stack.append( node.name.value )
        return None

    def leave_ClassDef(self, node: cst.ClassDef) -> None:
        self.full_name_stack.pop()

    def leave_FunctionDef(self, node: cst.FunctionDef) -> None:
        self.full_name_stack.pop()


class QFlagAndEnumUpdater(cst.CSTTransformer):

    def __init__(self, enum_class: str, enum_full_name: str, qflag_class: str, qflag_full_name: str,
                 module_idx: int,
                 human_hint_enum_full_class_name: str,
                 human_hint_qflag_full_class_name: str,
                 or_converts_to_multi: bool,
                 or_int_converts_to_multi: bool,
                 int_or_converts_to_multi: bool) -> None:
        super().__init__()

        # used internally to generate the full class name
        self.full_name_stack: List[str] = []

        self.error_msg = ''

        # the class name we are looking for
        self.enum_class = enum_class
        self.qflag_class = qflag_class
        self.enum_full_name = enum_full_name
        self.qflag_full_name = qflag_full_name

        # human help for finding the class
        self.human_hint_enum_full_class_name = ''
        if human_hint_enum_full_class_name:
            self.human_hint_enum_full_class_name = human_hint_enum_full_class_name.split('.')
        self.human_hint_qflag_full_class_name = ''
        if human_hint_qflag_full_class_name:
            self.human_hint_qflag_full_class_name = human_hint_qflag_full_class_name.split('.')

        # the index in this module of the  class we are looking for
        self.module_idx = module_idx

        # our current count of visit
        self.visit_enum_idx = -1
        self.visit_qflag_idx = -1

        self.or_converts_to_multi = or_converts_to_multi
        self.or_int_converts_to_multi = or_int_converts_to_multi
        self.int_or_converts_to_multi = int_or_converts_to_multi

        # set when enum_methods_present is set to partial, to add more contect information
        self.error_msg = ''

    def visit_ClassDef(self, node: cst.ClassDef) -> Optional[bool]:
        self.full_name_stack.append( node.name.value )
        return None

    def visit_FunctionDef(self, node: cst.FunctionDef) -> Optional[bool]:
        self.full_name_stack.append( node.name.value )
        return None

    def leave_FunctionDef(self, node: cst.FunctionDef, updated_node: cst.FunctionDef) -> cst.FunctionDef:
        self.full_name_stack.pop()
        return updated_node

    def leave_ClassDef(self, original_node: cst.ClassDef, updated_node: cst.ClassDef) -> cst.ClassDef:
        found_enum_class = False
        found_qflag_class = False

        if self.human_hint_enum_full_class_name:
            if self.human_hint_enum_full_class_name == self.full_name_stack:
                found_enum_class = True
        else:
            if original_node.name.value == self.enum_class:
                self.visit_enum_idx += 1
                if self.visit_enum_idx == self.module_idx:
                    found_enum_class = True

        if self.human_hint_qflag_full_class_name:
            if self.human_hint_qflag_full_class_name == self.full_name_stack:
                found_qflag_class = True
        else:
            if original_node.name.value == self.qflag_class:
                self.visit_qflag_idx += 1
                if self.visit_qflag_idx == self.module_idx:
                    found_qflag_class = True

        self.full_name_stack.pop()

        if found_enum_class:
            return self.transform_enum_class(original_node, updated_node)

        if found_qflag_class:
            return self.transform_qflag_class(original_node, updated_node)

        return updated_node


    def transform_enum_class(self, original_node: cst.ClassDef, updated_node: cst.ClassDef) -> cst.ClassDef:
        """Add the two methods __or__ and __ror__ to the class body"""

        # we keep comments separated to align them properly in the final file
        or_behavior = (self.or_converts_to_multi, self.or_int_converts_to_multi, self.int_or_converts_to_multi)
        if or_behavior == (True, False, True):
            new_methods_parts = (
                ("def __or__ (self, other: '{enum}') -> '{qflag}': ...", "# type: ignore[override]\n"),
                ("def __ror__ (self, other: int) -> '{qflag}': ...", "# type: ignore[override, misc]\n\n")
            )
        elif or_behavior == (True, True, True):
            new_methods_parts = (
                ("def __or__ (self, other: typing.Union[int, '{enum}']) -> '{qflag}': ...", "# type: ignore[override]\n"),
                ("def __ror__ (self, other: int) -> '{qflag}': ...", "# type: ignore[override, misc]\n\n")
            )
        elif or_behavior == (False, False, False):
            # no changes needed
            return updated_node
        else:
            raise ValueError('Unsupported or behavior:', or_behavior)


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
        """
        On the qflag class, add one more overload __init__() and add more methods
        +       @typing.overload
        +       def __init__(self, f: int) -> None: ...
        """
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

        if last_init_idx == 0:
            self.error_msg += 'No __init__ method found in class %s' % self.qflag_full_name
            return updated_node


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
    """Return the source of the template for generating qflags test.

    Return 3 parts as a list of strings:
    - the first part should be unmodified
    - the second part should be replaced for a specific QFlag class
    - the third part should be unmodified
    """

    # the markers inside the above template to identify the parts to replace
    MARKER_SPECIFIC_START = '### Specific part'
    MARKER_SPECIFIC_END = '### End of specific part'

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
    """Generate the name of the test file which will verify this qflag"""
    return 'test_{fli.module_name}_{fli.qflag_class}_{fli.enum_class}.py'.format(fli=fli)


def generate_qflag_test_file(flag_info: QFlagLocationInfo) -> None:
    """Generate a qflag test file.

    The filename is inferred from flag_info using gen_test_fname()
    """

    # the template after which we model all generated qflag tests
    TEMPLATE_QFLAGS_TESTS = 'qflags_test_template.py'

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

OR_CONVERTS_TO_MULTI: Literal[{or_converts_to_multi}] = {or_converts_to_multi}
OR_INT_CONVERTS_TO_MULTI: Literal[{or_int_converts_to_multi}] = {or_int_converts_to_multi}
INT_OR_CONVERTS_TO_MULTI: Literal[{int_or_converts_to_multi}] = {int_or_converts_to_multi}
SUPPORTS_ONE_OP_MULTI: Literal[{supports_one_op_multi}] = {supports_one_op_multi}
'''.format(source=TEMPLATE_QFLAGS_TESTS,
           multiFlagName=flag_info.qflag_full_class_name,
           oneFlagName=flag_info.enum_full_class_name,
           oneFlagValue1=flag_info.enum_value1,
           oneFlagValue2=flag_info.enum_value2,
           qtmodule=flag_info.module_name,
           or_converts_to_multi=flag_info.or_converts_to_multi,
           or_int_converts_to_multi=flag_info.or_int_converts_to_multi,
           int_or_converts_to_multi=flag_info.int_or_converts_to_multi,
           supports_one_op_multi=flag_info.supports_one_op_multi
           ))
        f.writelines(generic_part_after)
    log_progress('Test file generated: %s' % test_qflag_fname)


def generate_qflags_to_process(qt_qflag_grep_result_fname: str, module_group: str) -> None:
    """Run the generation process from the grep output parsing to the generation of json file listing the flags to process"""
    location_qflags = identify_qflag_location(qt_qflag_grep_result_fname, MODULE_GROUPS[module_group])
    log_progress('%d qflags extracted from grep file' % len(location_qflags))

    qflags_modules_analysis_json = 'qflags_modules_analysis.json'
    # put our intermediate classification into a json file for human review
    if os.path.exists(qflags_modules_analysis_json):
        with open(qflags_modules_analysis_json) as f:
            d = json.load(f)
            qflag_groups_initial = {
                'flag_and_module_identified': [QFlagLocationInfo(**v) for v in d['flag_and_module_identified']],
                'flag_without_module': [QFlagLocationInfo(**v) for v in d['flag_without_module']]
            }
    else:
        qflag_groups_initial = None


    initial_len = len(qflag_groups_initial['flag_and_module_identified'])
    qflags_groups = group_qflags(location_qflags, qflag_groups_initial)
    new_len = len(qflag_groups_initial['flag_and_module_identified'])
    log_progress('%d qflags ready to be processed' % (new_len - initial_len))

    with open(qflags_modules_analysis_json, 'w') as f:
        json.dump(qflags_groups, f, indent=4, default=json_encode_qflaglocationinfo)
    log_progress('QFlag analysis saved to: %s' % qflags_modules_analysis_json)

    qflags_to_process_json = 'qflags_to_process.json'
    extract_qflags_to_process(qflags_modules_analysis_json, qflags_to_process_json, module_group)
    log_progress('qflag file ready to process: %s' % qflags_to_process_json)


def regen_test_files(qflag_process_results: str) -> None:
    with open(qflag_process_results) as f:
        results_content = f.read()
    results = json.loads(results_content)

    flags_to_process =  results['qflag_processed_done'] + results['qflag_already_done']
    log_progress('%d test files to regenerate' % len(flags_to_process))
    for flag_info_dict in flags_to_process:
        flag_info = QFlagLocationInfo(**flag_info_dict)
        test_qflag_fname = gen_test_fname(flag_info)
        print('Updating', test_qflag_fname)
        generate_qflag_test_file(flag_info)



if __name__ == '__main__':

    if len(sys.argv) <= 1:
        print(USAGE)
        sys.exit(1)

    auto_commit = False
    if '--auto-commit' in sys.argv:
        auto_commit = True


    if sys.argv[1] == 'gen_qflag_stub':
        nb = 1
        process_all = False
        if len(sys.argv) > 2:
            if sys.argv[2] == 'all':
                process_all = True
            else:
                nb = int(sys.argv[2])

        qflags_to_process_json = 'qflags_to_process.json'
        qflag_result_json = 'qflags_process_result.json'
        more_available = -1
        while (nb > 0 or process_all) and (more_available == -1 or more_available > 0):
            nb -= 1
            more_available = process_qflag(qflags_to_process_json, qflag_result_json, auto_commit)
            if more_available:
                log_progress('Still %d flags to process' % more_available)
        log_progress('All qflags are processed.')

    elif sys.argv[1] == 'analyse_grep_results':
        if len(sys.argv) <= 4 or sys.argv[3] != '--group':
            print('Error, you must provide the filename of the grep results and the group of modules to use\n')
            print(USAGE)
            sys.exit(1)

        grep_fname = sys.argv[2]
        module_group = sys.argv[4]
        if not module_group in MODULE_GROUPS:
            print('Unknown module group: %s' % module_group)
            print('Possible choices are:\n-', '\n- '.join(MODULE_GROUPS.keys()))
            sys.exit(0)

        generate_qflags_to_process(grep_fname, module_group)


    elif sys.argv[1] == 'regen_test_files':

        if len(sys.argv) <= 2:
            print('Error, you must provide the filename of the qflag-process-results\n')
            print(USAGE)
            sys.exit(1)

        qflag_process_results = sys.argv[2]
        regen_test_files(qflag_process_results)

    else:
        print('Error, invalid command line arguments\n')
        print(USAGE)
        sys.exit(1)


