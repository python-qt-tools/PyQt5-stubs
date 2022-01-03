from PyQt5.QtWidgets import QApplication, QScrollArea

app = QApplication(['my_program', '-platform', 'offscreen'])

scrollArea = QScrollArea(widgetResizable=True)
