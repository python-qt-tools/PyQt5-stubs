
# from PyQt5 documentation
from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal

class Total(QObject):

    def __init__(self) -> None:
        QObject.__init__(self)
        self._total = 0

    # @pyqtProperty(int)
    @property
    def total(self) -> int:
        print('total getter')
        return self._total

    @total.setter
    def total(self, value: int) -> None:
        print('total setter')
        self._total = value+100 # add + 100 to detect that we are running through the setter and because it's fun


class Total2(QObject):

    def __init__(self) -> None:
        QObject.__init__(self)
        self._total2 = 0

    def total2_getter(self) -> int:
        print('total2 getter')
        return self._total2

    def total2_setter(self, v: int) -> None:
        print('total2 setter')
        self._total2 = v + 100  # add + 100 for fun
        self.total2_sig_changed.emit()

    def total2_resetter(self) -> None:
        print('total2 resetter')
        self._total2 = 0

    def total2_deleter(self) -> None:
        print('total2 deleter')
        del self._total2

    def total2_slot_changed(self) -> None:
        print('total2 changed')

    total2_sig_changed = pyqtSignal()

    total2 = pyqtProperty(
                    int,
                    fget=total2_getter,
                    fset=total2_setter,
                    freset=total2_resetter,
                    fdel=total2_deleter,
                    doc='return the total using a Qt property',
                    designable=True,
                    scriptable=True,
                    stored=True,
                    user=True,
                    constant=True,
                    final=True,
                    notify=total2_sig_changed,
                    revision=1
    )

class Total3(QObject):

    def __init__(self) -> None:
        QObject.__init__(self)
        self._total3 = 0

    def total3_slot_changed(self, value: int) -> None:
        print('total3 changed to', value)

    total3_sig_changed_1arg = pyqtSignal([int])
    total3 = pyqtProperty(int, notify=total3_sig_changed_1arg)

    @pyqtProperty(int)
    def total3(self) -> int:
        print('total3 getter')
        return self._total3

    @total3.getter
    def total3(self) -> int:
        print('total3 getter')
        return self._total3

    @total3.setter
    def total3(self, v: int) -> None:
        print('total3 setter')
        self._total3 = v + 100      # add +100 for fun

    @total3.deleter
    def total3(self) -> None:
        print('total3 deleter')
        del self._total3


print('==> Total')
t = Total()
print(t.total)
t.total = 1
print(t.total)

print('\n==> Total2')
t2 = Total2()
t2.total2_sig_changed.connect(t2.total2_slot_changed)
t2.total2 = 2
print(t2.total2)
t2.total2_resetter()
print(t2.total2)
print(t2.total2.__doc__)
# final deletion
del t2.total2

print('\n==> Total3')
t3 = Total3()
print(t3.total3)
t3.total3_sig_changed_1arg.connect(t3.total3_slot_changed)
t3.total3 = 3      # not working...
del t3.total3



