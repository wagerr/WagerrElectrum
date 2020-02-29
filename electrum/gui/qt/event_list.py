from PyQt5.QtWidgets import (QVBoxLayout, QGridLayout, QLineEdit, QTreeWidgetItem,
                             QHBoxLayout, QPushButton, QScrollArea, QTextEdit, 
                             QFrame, QShortcut, QMainWindow, QCompleter, QInputDialog,
                             QWidget, QMenu, QSizePolicy, QStatusBar, QListView,
                             QAbstractItemView, QSpacerItem, QSizePolicy, QListWidget,
                             QListWidgetItem)
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont
from PyQt5.QtCore import Qt, QModelIndex, QItemSelectionModel, QSize

from .eventwidget import EventWidget

class EventListView(QListView):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        self.selectedSport = "All Events"
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

        sports = ["All Events", "Football", "Baseball", "Basketball", "Hockey", "Soccer",
                    "MMA", "Aussie Rules", "Cricket", "Rugby Union", "Rugby League"]
        model = QStandardItemModel(self)
        self.setSpacing(10)
        for s in sports:
            model.appendRow(QStandardItem(s))
        self.setModel(model)
        self.selectionModel().currentRowChanged.connect(self.item_changed)

    def item_changed(self, idx):
        sport = self.model().itemFromIndex(idx)
        self.selectedSport = sport.text()
        print("Selected Sport : ", sport.text())
        self.selectionModel().setCurrentIndex(idx, QItemSelectionModel.SelectCurrent)
        self.update()

    def update(self):
        self.parent.eventQListWidget.clear()
        data=self.parent.events_data
        if self.selectedSport=="All Events":
             for x in data:
                 self.cw=EventWidget(self.parent)
                 self.cw.setData(x)
                 self.cw.setFixedHeight(150)
                 eventQListWidgetItem = QListWidgetItem(self.parent.eventQListWidget)
                 eventQListWidgetItem.setSizeHint(self.cw.sizeHint())
                 eventQListWidgetItem.setTextAlignment(Qt.AlignHCenter)
                 self.parent.eventQListWidget.addItem(eventQListWidgetItem)
                 self.parent.eventQListWidget.setItemWidget(eventQListWidgetItem, self.cw)
        else:
            for x in data:
                if x["sport"]==self.selectedSport:
                    self.cw=EventWidget(self.parent)
                    self.cw.setData(x)
                    self.cw.setFixedHeight(150)
                    eventQListWidgetItem = QListWidgetItem(self.parent.eventQListWidget)
                    eventQListWidgetItem.setSizeHint(self.cw.sizeHint())
                    self.parent.eventQListWidget.addItem(eventQListWidgetItem)
                    self.parent.eventQListWidget.setItemWidget(eventQListWidgetItem, self.cw)
            
        self.parent.grid_betting.addWidget(self.parent.eventQListWidget,0,1)