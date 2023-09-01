from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


from dataclasses import dataclass
from typing import List
from enum import Enum


class Columns(int, Enum):
    logLevel = 0
    tagName = 1
    logMessage = 2


class CustomSortProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)

    def filterAcceptsRow(self, sourceRow: int, sourceParent: QModelIndex) -> bool:
        filterRegExp = self.filterRegExp()
        if filterRegExp.isEmpty():
            return True

        sourceModel = self.sourceModel()
        indexBody = sourceModel.index(sourceRow, Columns.logMessage, sourceParent)
        return filterRegExp.indexIn(sourceModel.data(indexBody)) != -1


class LogMessagesPane(QWidget):

    """Displays log messages"""

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.initUserInterface()

    def initUserInterface(self):

        labels = ["Log level", "Tag", "Message"]
        dataModel = QStandardItemModel(0, len(Columns))
        dataModel.setHorizontalHeaderLabels(labels)

        proxyModel = CustomSortProxyModel()
        proxyModel.setSourceModel(dataModel)
        proxyModel.setFilterCaseSensitivity(Qt.CaseInsensitive)

        tableView = QTableView(self)
        tableView.setModel(proxyModel)
        tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        tableView.setSelectionMode(QTableView.SingleSelection)
        tableView.setColumnWidth(Columns.logLevel, 20)
        tableView.setColumnWidth(Columns.tagName, 200)

        hHeader = tableView.horizontalHeader()
        hHeader.setSectionResizeMode(Columns.logMessage, QHeaderView.Stretch)
        hHeader.setDefaultAlignment(Qt.AlignLeft)

        vHeader = tableView.verticalHeader()
        vHeader.setVisible(False)

        # searchField = QLineEdit()
        # searchField.setPlaceholderText("Search in message body")
        # searchField.addAction(QIcon(":search.svg"), QLineEdit.LeadingPosition)
        # searchField.textChanged.connect(proxyModel.setFilterFixedString)

        layout = QVBoxLayout()
        layout.addWidget(tableView)
        # layout.addWidget(searchField)

        self._tableView = tableView
        self._dataModel = dataModel
        self.setLayout(layout)

    def clear(self):
        self._dataModel.clear()

    def appendRow(self, logLevel, tagName, logMessage):
        flags = Qt.ItemIsSelectable | Qt.ItemIsEnabled

        itemLogLevel = QStandardItem(logLevel)
        itemLogLevel.setFlags(flags)

        itemTagName = QStandardItem(tagName)
        itemTagName.setFlags(flags)

        itemLogMessage = QStandardItem(logMessage)
        itemLogMessage.setFlags(flags)

        row = [itemLogLevel, itemTagName, itemLogMessage]
        self._dataModel.appendRow(row)
        self._tableView.scrollToBottom()

    def navigateToItem(self, row, col):
        self.activateWindow()
        self.raise_()
        if 0 <= row < self._dataModel.rowCount() and 0 <= col < self._dataModel.columnCount():
            # self._tableView.selectionModel().select(index, QItemSelectionModel.Select)
            # self._tableView.selectionModel().select(index, QTableView.Rows)
            self._tableView.selectRow(row)
            # self._tableView.scrollTo(index)