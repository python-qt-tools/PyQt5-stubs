"""Test for handling of signals.

In the upstream PyQt stubs, signals are normal methods.
"""

from PyQt6.QtCore import QTimer

timer = QTimer()
timer.timeout.connect(lambda: None)
