from typing import Optional
from PyQt5.QtWidgets import QProgressDialog, QPushButton

qpd = QProgressDialog()
button1 = None   # type: Optional[QPushButton]
button2 = None
button3 = QPushButton()
qpd.setCancelButton(button1)
qpd.setCancelButton(button2)
qpd.setCancelButton(button3)
