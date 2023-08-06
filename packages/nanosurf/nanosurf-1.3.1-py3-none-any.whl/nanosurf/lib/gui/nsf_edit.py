# ///
# /// Line Edit for advanced number formatting
# ///
# /// Copyright (C) Nanosurf AG - All Rights Reserved (2021)
# /// Unauthorized copying of this file, via any medium is strictly prohibited
# /// https://www.nanosurf.com
# ///


from PySide2 import QtGui, QtWidgets
from PySide2.QtCore import Qt, Signal

class _LineEditQt(QtWidgets.QLineEdit):

    value_changed_event = Signal(float)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._block_value_change_signal = False
        self.textEdited.connect(self._value_changed())

    # public interface ------------------------------------------

    def set_value(self, new_value: str, notify: bool = True):
        do_notify = notify and (new_value != self.text())
        self.setText(new_value)
        if do_notify:
            self._value_changed()

    def value(self) -> str:
        return self.text()  

    # internal functions --------------------------------------------    

    # def focusInEvent(self, event: QtGui.QFocusEvent) -> None:
    #     """ overwrite handler for widget focus events"""
    #     super().focusInEvent(event)

    def focusOutEvent(self, event: QtGui.QFocusEvent) -> None:
        """  overwrite handler for widget focus events"""
        super().focusOutEvent(event)
        self._value_changed()

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        """ overwrite handler for key events"""
        if self.isReadOnly():
            return
        shift = (event.modifiers() == Qt.ShiftModifier)
        ctrl = (event.modifiers() == Qt.ControlModifier)
        key = event.key()
        if (key == Qt.Key_Return) or (key == Qt.Key_Enter):
            super().keyPressEvent(event)
            self._value_changed()
        else:
            super().keyPressEvent(event)

    def _value_changed(self):
        if not(self._block_value_change_signal):
            self.value_changed_event.emit(self.value())    


class NSFEdit(QtWidgets.QWidget):
    """ Custom Qt Widget to show text in a edit with a descriptive label. """
    value_changed_event = Signal(str)

    def __init__(self, label_str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._setup_widgets(label_str)
        self._edit.value_changed_event.connect(self._on_value_changed)
 
    def set_value(self, text: str, notify: bool = True):
        self._edit.set_value(text)
        if notify:
            self._on_value_changed()        
       
    def set_label(self, label: str):
       self._label.setText(label) 

    def set_read_only(self, set_read_only: bool):
        self._edit.setReadOnly(set_read_only)
        self._edit.setDisabled(set_read_only)
   
    def read_only(self) -> bool:
        return self._edit.isReadOnly()

    def label(self) -> str:
        return self._label.text()

    def value(self) -> str:
        return self._edit.value()  


    # internal ----------------------------------------------------
    
    def _setup_widgets(self, label_str: str):
        layout = QtWidgets.QVBoxLayout()
        self._label = QtWidgets.QLabel()
        self._label.setText(label_str)
        self._label.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        layout.addWidget(self._label, alignment=Qt.AlignBottom)
        self._edit = _LineEditQt()
        self._edit.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        layout.addWidget(self._edit)#, alignment=Qt.AlignTop)
        self.setLayout(layout)

    def _on_value_changed(self):
        self.value_changed_event.emit(self.value())

