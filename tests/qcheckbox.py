"""
:author: Stefan Lehmann <stlm@posteo.de>
:license: MIT, see license file or https://opensource.org/licenses/MIT

:created on 2018-12-08 18:13:28
:last modified by:   Stefan Lehmann
:last modified time: 2018-12-08 18:18:29

"""
from PyQt5.QtWidgets import QApplication, QCheckBox 


app = QApplication([])

# Check signals
checkbox = QCheckBox()
checkbox.stateChanged.connect(lambda: None)
checkbox.pressed.connect(lambda: None)
checkbox.released.connect(lambda: None )
checkbox.toggled.connect(lambda: None )
checkbox.clicked.connect(lambda: None )
