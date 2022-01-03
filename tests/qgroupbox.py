from PyQt5.QtWidgets import QApplication, QGroupBox

app = QApplication(['my_program', '-platform', 'offscreen'])

groupBox = QGroupBox(objectName='some_name')
