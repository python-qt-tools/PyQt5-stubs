
# from PyQt5 documentation
from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal


# Python style properties
class UseProps1(QObject):

    def __init__(self) -> None:
        QObject.__init__(self)
        self._prop1 = 0
        self._prop2 = 0

    ### prop1
    @property
    def prop1(self) -> int:
        print('_prop1 getter')
        return self._prop1

    @prop1.setter
    def prop1(self, value: int) -> None:
        print('_prop1 setter')
        self._prop1 = value+100 # add + 100 to detect that we are running through the setter and because it's fun

    @prop1.deleter
    def prop1(self) -> None:
        print('_prop1 deleter')
        del self._prop1


    ### prop2
    def set_prop2(self, value: int) -> None:
        print('_prop2 setter')
        self._prop2 = value+100 # add + 100 to detect that we are running through the setter and because it's fun

    def get_prop2(self) -> int:
        print('_prop2 getter')
        return self._prop2

    def del_prop2(self) -> None:
        print('_prop2 deleter')
        del self._prop2

    prop2 = property(get_prop2, set_prop2, del_prop2)


### Qt style properties
class UseProps2(QObject):

    def __init__(self) -> None:
        QObject.__init__(self)
        self._prop3 = 0

    def prop3_getter(self) -> int:
        print('prop3 getter')
        return self._prop3

    def prop3_setter(self, v: int) -> None:
        print('prop3 setter')
        self._prop3 = v + 100  # add + 100 for fun
        self.prop3_sig_changed.emit()

    def prop3_resetter(self) -> None:
        print('prop3 resetter')
        self._prop3 = 0

    def prop3_deleter(self) -> None:
        print('prop3 deleter')
        del self._prop3

    def prop3_slot_changed(self) -> None:
        print('prop3 changed to ', self._prop3)

    prop3_sig_changed = pyqtSignal()

    prop3 = pyqtProperty(
                    int,
                    fget=prop3_getter,
                    fset=prop3_setter,
                    freset=prop3_resetter,
                    fdel=prop3_deleter,
                    doc='return the total using a Qt property',
                    designable=True,
                    scriptable=True,
                    stored=True,
                    user=True,
                    constant=True,
                    final=True,
                    notify=prop3_sig_changed,
                    revision=1
    )



class UseProps3(QObject):

    def __init__(self) -> None:
        QObject.__init__(self)
        self._prop4 = 0

    def prop4_slot_changed(self, value: int) -> None:
        print('prop4 changed to', value)

    prop4_sig_changed_1arg = pyqtSignal([int])
    prop4 = pyqtProperty(int, notify=prop4_sig_changed_1arg)

    @pyqtProperty(int)
    def prop4(self) -> int:
        print('prop4 getter')
        return self._prop4

    @prop4.setter
    def prop4(self, v: int) -> None:
        print('prop4 setter')
        self._prop4 = v + 100      # add +100 for fun
        self.prop4_sig_changed_1arg.emit(self._prop4)

    @prop4.deleter
    def prop4(self) -> None:
        print('prop4 deleter')
        del self._prop4


print('==> Python style properties with UseProps1')
up = UseProps1()
print( up.prop1 )
up.prop1 = 2
print( up.prop1 )
del up.prop1

print( up.prop2 )
up.prop1 = 3
print( up.prop2 )
del up.prop2


print('==> PyQt style properties with UseProps2')
up2 = UseProps2()
print(up2.prop3)
up2.prop3_sig_changed.connect(up2.prop3_slot_changed)
print('Setting to 2')
up2.prop3 = 2
print(up2.prop3)
up2.setProperty('prop3', 3)
print( up2.property('prop3') )

print('Resetting')
up2.prop3_resetter()
print(up2.prop3)

print(up2.prop3.__doc__)
# final deletion
del up2.prop3

print('\n==> PyQt/python style properties with UseProps3')
up3 = UseProps3()
print(up3.prop4)
up3.prop4_sig_changed_1arg.connect(up3.prop4_slot_changed)
print('Setting to 2')
up3.prop4 = 2
print(up3.prop4)
up3.setProperty('prop4', 3)
print( up3.property('prop4') )

# final deletion
del up3.prop4




