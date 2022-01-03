from typing import Any

from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal

def myprint(v: Any, v2: Any = '') -> None:
    # uncomment the next line to debug
    # print(v, v2)
    pass


# Python style properties
class UseProps1(QObject):

    def __init__(self) -> None:
        QObject.__init__(self)
        self._prop1 = 0
        self._prop2 = 0

    ### prop1
    @property
    def prop1(self) -> int:
        myprint('_prop1 getter')
        return self._prop1

    @prop1.setter
    def prop1(self, value: int) -> None:
        myprint('_prop1 setter')
        self._prop1 = value+100 # add + 100 to detect that we are running through the setter and because it's fun

    @prop1.deleter
    def prop1(self) -> None:
        myprint('_prop1 deleter')
        del self._prop1


    ### prop2
    def set_prop2(self, value: int) -> None:
        myprint('_prop2 setter')
        self._prop2 = value+100 # add + 100 to detect that we are running through the setter and because it's fun

    def get_prop2(self) -> int:
        myprint('_prop2 getter')
        return self._prop2

    def del_prop2(self) -> None:
        myprint('_prop2 deleter')
        del self._prop2

    prop2 = property(get_prop2, set_prop2, del_prop2)


### Qt style properties
class UseProps2(QObject):

    def __init__(self) -> None:
        QObject.__init__(self)
        self._prop3 = 0

    def prop3_getter(self) -> int:
        myprint('prop3 getter')
        return self._prop3

    def prop3_setter(self, v: int) -> None:
        myprint('prop3 setter')
        self._prop3 = v + 100  # add + 100 for fun
        self.prop3_sig_changed.emit()

    def prop3_another_getter(self) -> int:
        myprint('prop3 another getter')
        return - self._prop3

    def prop3_another_setter(self, v: int) -> None:
        myprint('prop3 another setter')
        self._prop3 = v + 1000  # add + 100 for fun
        self.prop3_sig_changed.emit()

    def prop3_resetter(self) -> None:
        myprint('prop3 resetter')
        self._prop3 = 0

    def prop3_deleter(self) -> None:
        myprint('prop3 deleter')
        del self._prop3

    def prop3_slot_changed(self) -> None:
        myprint('prop3 changed to ', self._prop3)

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

    # create another property, with just the setter being different
    prop4 = prop3.setter(prop3_another_setter)      # type: ignore[type-var] # I can not figure out how to make this work



class UseProps3(QObject):
    '''Note: using pyqtProperty() just like the function property() in Python is possible but is
    impossible to type-check so far.
    
    '''

    def __init__(self) -> None:
        QObject.__init__(self)
        self._prop4 = 0

    def prop4_slot_changed(self, value: int) -> None:
        myprint('prop4 changed to', value)

    prop4_sig_changed_1arg = pyqtSignal([int])

    ### This is not supported by mypy at the moment. Just giving up
    '''
    @pyqtProperty(int)
    def prop4(self) -> int:
        myprint('prop4 getter')
        return self._prop4

    @prop4.setter
    def prop4(self, v: int) -> None:
        myprint('prop4 setter')
        self._prop4 = v + 100      # add +100 for fun
        self.prop4_sig_changed_1arg.emit(self._prop4)

    @prop4.deleter
    def prop4(self) -> None:
        myprint('prop4 deleter')
        del self._prop4
    '''


myprint('==> Python style properties with UseProps1')
up = UseProps1()
myprint( up.prop1 )
up.prop1 = 2
myprint( up.prop1 )
del up.prop1

myprint( up.prop2 )
up.prop1 = 3
myprint( up.prop2 )
del up.prop2


myprint('==> PyQt style properties with UseProps2')
up2 = UseProps2()
myprint(up2.prop3)
up2.prop3_sig_changed.connect(up2.prop3_slot_changed)
myprint('Setting to 2')
up2.prop3 = 2   # type: ignore[assignment]
myprint(up2.prop3)

# Qt style access
up2.setProperty('prop3', 3)
myprint( up2.property('prop3') )
metaProperty = up2.metaObject().property(up2.metaObject().indexOfProperty('prop3'))
myprint('Qt property available: ', metaProperty.name())

myprint(up2.prop4)
up2.prop4 = 500     # type: ignore[assignment]  # mypy does not understand that prop4 is a property
myprint(up2.prop4)


myprint('Resetting')
up2.prop3_resetter()
myprint(up2.prop3)

myprint(up2.prop3.__doc__)
# final deletion
del up2.prop3

'''
The rest here will not typecheck, so comment it until mypy accepts to define
a property through an alternative method.

myprint('\n==> PyQt/python style properties with UseProps3')
up3 = UseProps3()
myprint(up3.prop4)
up3.prop4_sig_changed_1arg.connect(up3.prop4_slot_changed)
myprint('Setting to 2')
up3.prop4 = 2
myprint(up3.prop4)
up3.setProperty('prop4', 3)
myprint( up3.property('prop4') )

# final deletion
del up3.prop4
'''




