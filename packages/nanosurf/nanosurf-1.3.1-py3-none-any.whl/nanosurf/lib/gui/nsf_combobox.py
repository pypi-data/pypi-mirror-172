# ///
# /// Line Edit for advanced number formatting
# ///
# /// Copyright (C) Nanosurf AG - All Rights Reserved (2021)
# /// Unauthorized copying of this file, via any medium is strictly prohibited
# /// https://www.nanosurf.com
# ///


from enum import IntEnum
import typing
from PySide2 import QtGui, QtWidgets
from PySide2.QtCore import Qt, Signal

class NSFComboEntry():
    id: int
    name : str

    def __init__(self, id: typing.Union[int, IntEnum], name: str) -> None:
        self.id = int(id)
        self.name = name


class _ComboboxQt(QtWidgets.QComboBox):

    value_changed_event = Signal(float)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._block_value_change_signal = False
        self.currentIndexChanged.connect(self._index_changed)

    # public interface ------------------------------------------

    def set_index(self, new_index: int, notify: bool = True):
        do_notify = notify and (new_index != self.currentIndex())
        self.setCurrentIndex(new_index)
        if do_notify:
            self._index_changed()

    def index(self) -> int:
        return int(self.currentIndex())  

    # internal functions --------------------------------------------    

    def _index_changed(self):
        if not(self._block_value_change_signal):
            self.value_changed_event.emit(self.index())    


class NSFComboBox(QtWidgets.QWidget):
    """ Custom Qt Widget to show text in a edit with a descriptive label. """
    value_changed_event = Signal(str)

    def __init__(self, entries: list[NSFComboEntry] = [], label_str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._setup_widgets(label_str)
        self.comp_entries = entries
        self.define_entries(self.comp_entries)
        self._combo.value_changed_event.connect(self._on_value_changed)

    def define_entries(self, entries: list[NSFComboEntry]):
        self.comp_entries = entries
        self._combo.clear()
        names = [i.name for i in self.comp_entries]
        self._combo.addItems(names)
 
    def set_value(self, id: int, notify: bool = True):
        self._combo.set_index(self._get_index_from_id(id))
        if notify:
            self._on_value_changed()        
       
    def set_label(self, label: str):
       self._label.setText(label) 

    def label(self) -> str:
        return self._label.text()

    def value(self) -> int:
        return self._get_id_from_index(self._combo.index())  

    def current_entry_name(self) -> str:
        return self._combo.currentText()

    def entry_name(self, id : int) -> str:
        return self.comp_entries[self._get_index_from_id(id)].name


    # internal ----------------------------------------------------
    
    def _setup_widgets(self, label_str: str):
        layout = QtWidgets.QVBoxLayout()
        self._label = QtWidgets.QLabel()
        self._label.setText(label_str)
        self._label.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        layout.addWidget(self._label, alignment=Qt.AlignBottom)
        self._combo = _ComboboxQt()
        self._combo.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        layout.addWidget(self._combo)
        self.setLayout(layout)

    def _on_value_changed(self):
        self.value_changed_event.emit(self.value())

    def _get_index_from_id(self, id: int) -> int:
        found_index = -1
        index = 0
        for entry in self.comp_entries:
            if entry.id == id:
                found_index = index
                break
            index += 1
        return found_index

    def _get_id_from_index(self, index: int) -> int:
        return self.comp_entries[index].id

