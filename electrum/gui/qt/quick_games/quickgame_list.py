
from PyQt5.QtWidgets import QAbstractItemView, QListView
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from electrum.gui.qt.util import read_QIcon
from electrum.gui.qt.quick_games.dice.dicegame_main_widget import DiceGameWidget



class QuickGameListView(QListView):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent
        self.setStyleSheet("QListView::item:selected { background-color: #BD0000; } QListView { border:0px;background-color:#151515;color:#fff;font-weight:bold }")
        self.build_chaingame_list()
        

    def build_chaingame_list(self):
        sports = [ "Dice"]
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        model = QStandardItemModel(self)
        model.setColumnCount(2)
        self.setSpacing(10)
        for s in sports:
            model.appendRow([
                            QStandardItem(read_QIcon(''.join([s,".png"]))," {0}".format(s))
                            ])
        self.setModel(model)
        self.setMinimumWidth(self.sizeHintForColumn(0)+10)
        

