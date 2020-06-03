from PyQt5.QtWidgets import (QVBoxLayout, QGridLayout, QLineEdit, QTreeWidgetItem,
                             QHBoxLayout, QPushButton, QScrollArea, QTextEdit, 
                             QFrame, QShortcut, QMainWindow, QCompleter, QInputDialog,
                             QWidget, QMenu, QSizePolicy, QStatusBar, QListView,
                             QAbstractItemView, QSpacerItem, QSizePolicy, QListWidget,
                             QListWidgetItem)
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont
from PyQt5.QtCore import Qt, QModelIndex, QItemSelectionModel, QSize
from .util import (read_QIcon)
from .eventwidget import EventWidget
from operator import itemgetter
from collections import defaultdict
import re , time

class EventListView(QListView):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setStyleSheet("QListView::item:selected { background-color: #BD0000; } QListView { border:0px;background-color:#151515;color:#fff;font-weight:bold }")
        self.selectedSport = "All Events"
        self.eventQListWidget_scrollbar = self.parent.eventQListWidget.verticalScrollBar()
        
    def remove_expired_betwidget(self, eventId):
        for item in [self.parent.betQListWidget.item(i) for i in range(self.parent.betQListWidget.count())]:
            itemwidget = self.parent.betQListWidget.itemWidget(item)
            if itemwidget.eventIdToBetOn == str(eventId):
                item1 = self.parent.betQListWidget.takeItem(self.parent.betQListWidget.row(item))
                del item1

        

    def filter_events(self,event):
        odds = event["odds"]
        eventtime = event["starting"]
        eventId = event["event_id"]
        moneyline = odds[0]
        m1 = moneyline["mlAway"] + moneyline["mlDraw"] + moneyline["mlHome"]
        event_expired = (eventtime - 720) < time.time()
        if event_expired:
            self.remove_expired_betwidget(eventId)

        return m1 > 0 and (not (eventtime - 720) > time.time())

    def build_eventlist(self,events_data):
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        events_data = list(filter(lambda d1: self.filter_events(d1),events_data))
        counts = defaultdict(int)
        for item in events_data:
            if item["sport"] == "Mixed Martial Arts":
                item["sport"] = "MMA"
            counts[item["sport"]] += 1

        counts["All Events"] = len(events_data)

        sports = ["All Events", "Football", "Baseball", "Basketball", "Hockey", "Soccer",
                    "MMA", "Aussie Rules", "Cricket", "Rugby Union", "Rugby League","Esports"]
        model = QStandardItemModel(self)
        model.setColumnCount(2)
        self.setSpacing(10)
        for s in sports:
            model.appendRow([
                            QStandardItem(read_QIcon(''.join([s,".png"]))," {0} ({1})".format(s,str(counts[s] or "0")))
                            ])
        self.setModel(model)
        self.selectionModel().currentRowChanged.connect(self.item_changed)

    def item_changed(self, idx):
        sport = self.model().itemFromIndex(idx)
        self.selectedSport = re.sub(r'\([^)]*\)', '', sport.text()).strip()
        print("Selected Sport : ", self.selectedSport)
        self.selectionModel().setCurrentIndex(idx, QItemSelectionModel.SelectCurrent)
        self.update()
        self.eventQListWidget_scrollbar.setValue(0)

    def update(self):
        self.eventQListWidget_scroll_position = self.eventQListWidget_scrollbar.value();
        self.parent.eventQListWidget.clear()
        event_data = list(filter(lambda d1: self.filter_events(d1),self.parent.events_data))
        sorted_data=sorted(event_data, key=lambda x: (x['starting']))
        
        if self.selectedSport=="All Events":
             for x in sorted_data:
                 self.cw=EventWidget(self.parent)
                 self.cw.setData(x)
                 eventQListWidgetItem = QListWidgetItem(self.parent.eventQListWidget)
                 eventQListWidgetItem.setSizeHint(self.cw.sizeHint())
                 eventQListWidgetItem.setTextAlignment(Qt.AlignHCenter)
                 self.parent.eventQListWidget.addItem(eventQListWidgetItem)
                 self.parent.eventQListWidget.setItemWidget(eventQListWidgetItem, self.cw)
        else:
            for x in sorted_data:
                if x["sport"]==self.selectedSport:
                    self.cw=EventWidget(self.parent)
                    self.cw.setData(x)
                    eventQListWidgetItem = QListWidgetItem(self.parent.eventQListWidget)
                    eventQListWidgetItem.setSizeHint(self.cw.sizeHint())
                    self.parent.eventQListWidget.addItem(eventQListWidgetItem)
                    self.parent.eventQListWidget.setItemWidget(eventQListWidgetItem, self.cw)
        self.eventQListWidget_scrollbar.setValue(self.eventQListWidget_scroll_position)