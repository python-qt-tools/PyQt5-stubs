from typing import Tuple, List

SOURCE = 'windowFlags.py'
MARKER_SPECIFIC_START = '### Specific part'
MARKER_SPECIFIC_END = '### End of specific part'

# Content is:
# - name of the file to generate
# - name of the QFlags<> class
# - name of the individual flag class (inheriting from int)
# - one individual flag value
# - a second individual flag value
FLAGS_FILES = [
    ('qflags_alignmentflags.py', 'QtCore.Qt.Alignment', 'QtCore.Qt.AlignmentFlag', 'QtCore.Qt.AlignLeft', 'QtCore.Qt.AlignRight'),

]

# global values for simplicity of the code
sourcePart1, sourcePart2, sourcePart3 = [], [], []  # type: Tuple[List[str], List[str], List[str]]

def generate_qflags_files() -> None:
    global sourcePart1, sourcePart2, sourcePart3
    with open(SOURCE) as f:
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

    for qflag_info in FLAGS_FILES:
        generate_one_qflag_file(*qflag_info)


def generate_one_qflag_file(qflag_fname: str, multiFlagName: str, oneFlagName: str, oneFlagValue1: str, oneFlagValue2: str) -> None:
    with open(qflag_fname, 'w') as f:
        f.writelines(sourcePart1)
        f.write('''# file generated from {source} for QFlags class "{multiFlagName}" and flag class "{oneFlagName}"

OneFlagClass = {oneFlagName}
MultiFlagClass = {multiFlagName}

oneFlagRefValue1 = {oneFlagValue1}
oneFlagRefValue2 = {oneFlagValue2}
'''.format(source=SOURCE, multiFlagName=multiFlagName, oneFlagName=oneFlagName,
            oneFlagValue1=oneFlagValue1, oneFlagValue2=oneFlagValue2
    ))
        f.writelines(sourcePart3)
    print('File %s generated' % qflag_fname)


if __name__ == '__main__':
    generate_qflags_files()

