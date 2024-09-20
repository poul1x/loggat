from typing import Optional

from PySide6.QtCore import QModelIndex, Signal
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QListView, QWidget

from .hotkeys import HotkeyHelper


class ListView(QListView):
    #
    # This widget is used for cross-platform implementation of the 'activated' signal.
    # Unfortunately, the built-in implementation does not work on MacOS.
    # Therefore, we need to implement handlers for mouse double-click on a row and
    # keyboard shortcuts (<Enter>, <Space>) pressed on the selected row.
    #

    rowActivated = Signal(QModelIndex)

    def _emitRowActivated(self, index: QModelIndex):
        self.rowActivated.emit(index)

    def keyPressEvent(self, event: QKeyEvent):
        helper = HotkeyHelper(event)
        if helper.isEnterPressed() or helper.isSpacePressed():
            indexes = self.selectionModel().selectedIndexes()
            if indexes:
                self._emitRowActivated(indexes[0])

        return super().keyPressEvent(event)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.doubleClicked.connect(self._emitRowActivated)
