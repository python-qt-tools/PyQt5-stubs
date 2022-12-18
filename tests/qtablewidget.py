from typing import Optional
from PyQt5.QtWidgets import QTableWidget, QWidget

table = QTableWidget()
cell: Optional[QWidget] = table.cellWidget(0, 0)
