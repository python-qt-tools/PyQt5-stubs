from typing import Optional

from PyQt5.QtCore import QCoreApplication

# let the default type propagate to app
app = QCoreApplication.instance()

# ensure that QCoreApplication.instance() may also return None
app = None
