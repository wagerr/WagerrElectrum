

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QPushButton, QRadioButton, QSizePolicy, QVBoxLayout, QWidget
from PyQt5.QtCore import QSize, Qt
from electrum.gui.qt.amountedit import AmountEdit, BTCAmountEdit
from electrum.gui.qt.single_betwidget import SingleBetWidget
from electrum.gui.qt.parlay_betwidget import ParlayBetWidget
from electrum.gui.qt.parlaybet_box_widget import ParlayBetBoxWidget
from electrum.bitcoin import COIN, is_address, TYPE_ADDRESS
from PyQt5.QtGui import QDoubleValidator
from electrum.event import Event
from collections import defaultdict

class BettingMainWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.parent = parent
        self.current_bet_type = 'single'
        self.mainLayout = QVBoxLayout()
        self.event = Event.getInstance()
        self.parlay_bet_eventId_list = []

        self.event.register_callback(self.bet_done,["tx_brodcasted"])

        self.nav_widget = QWidget()
        self.nav_widget.setStyleSheet(
            "QWidget{"
                "background-color:black;"
            "}"
            "QPushButton {"
                "background-color:#BD0000;"
                "border:1px solid #BD0000;"
			    "padding:0.5em;"
                "color:#ffffff;"
                "border-radius:3px;"
                "font-weight:bold;"
                "text-decoration:none;"
                "outline: 0;"
                
            "}"
            "QPushButton:disabled {"
                "background-color:#ed4c4c;"
            "}"
            "QPushButton:pressed {"
                "background-color:#800a0a;"
            "}")

        
        self.bet_single = QRadioButton("Single")
        self.bet_single.bet_type = "single"
        self.bet_single.setChecked(True)
        self.bet_single.setStyleSheet("QRadioButton {color : #fff  }")
        
        self.bet_parlay = QRadioButton("Parlay")
        self.bet_parlay.setStyleSheet("QRadioButton {color : #fff  }")
        self.bet_parlay.bet_type = "parlay"

        self.bet_single.toggled.connect(self.switch_bet_type)
        self.bet_parlay.toggled.connect(self.switch_bet_type)
        
        self.clear_slip = QPushButton("CLEAR SLIP")
        self.clear_slip.clicked.connect(self.clear_list)
        self.hbox_bet_nav = QHBoxLayout(self.nav_widget)
        self.hbox_bet_nav.addWidget(self.bet_single)
        self.hbox_bet_nav.addWidget(self.bet_parlay)
        self.hbox_bet_nav.addWidget(self.clear_slip)

        

        self.widget_single_bet = QWidget()
        self.vbox_single_bet = QVBoxLayout(self.widget_single_bet)
        self.bet_list_widget_single = QListWidget()
        self.bet_list_widget_single.setStyleSheet(
            "QListWidget::item {"
                "border: 1px solid #BD0000;"
                #"border-top-color: transparent;"
                #"border-bottom-color: transparent;"
                "margin: 5px;"
                "}"
            "QListWidget::item:hover {"
                "background: rgb(250, 218, 221);"
            "}"
            "QListWidget::item:selected:active{"
                "background: rgb(250, 218, 221);"
            "}"
            # "QListWidget::item:selected:!active {"
            #     "background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6b9be8, stop: 1 #6ea1f1);"
            # "}"
        )
        self.vbox_single_bet.addWidget(self.bet_list_widget_single)
        self.widget_parlay_bet = QWidget()
        self.vbox_parlay_bet = QVBoxLayout(self.widget_parlay_bet)
        self.bet_list_widget_parlay = QListWidget()
        self.bet_list_widget_parlay.setStyleSheet(
            "QListWidget::item {"
                "border: 1px solid #BD0000;"
                #"border-top-color: transparent;"
                #"border-bottom-color: transparent;"
                "margin: 5px;"
                "}"
            "QListWidget::item:hover {"
                "background: rgb(250, 218, 221);"
            "}"
            "QListWidget::item:selected:active{"
                "background: rgb(250, 218, 221);"
            "}"
            # "QListWidget::item:selected:!active {"
            #     "background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6b9be8, stop: 1 #6ea1f1);"
            # "}"
        )
        self.vbox_parlay_bet.addWidget(self.bet_list_widget_parlay)
        
        #Parlay bet box 
        self.parlay_bet_box = ParlayBetBoxWidget(self.parent)
        self.vbox_parlay_bet.addWidget(self.parlay_bet_box)
        #End Mutli bet box

        self.widget_parlay_bet.setVisible(False)
        
        self.mainLayout.addWidget(self.nav_widget)
        self.mainLayout.addWidget(self.widget_single_bet)
        self.mainLayout.addWidget(self.widget_parlay_bet)

        self.setLayout(self.mainLayout)
        
        
    def add_bet(self,bet_event):
        if self.current_bet_type == "single":
            self.single_betWidget = SingleBetWidget(self.parent)
            self.single_betWidget.update_labels(bet_event)
            single_bet_list_item = QListWidgetItem(self.bet_list_widget_single)
            single_bet_list_item.setSizeHint(self.single_betWidget.sizeHint())
            self.single_betWidget.qlistItem = single_bet_list_item #for remove item when close button click or bet done
            self.bet_list_widget_single.addItem(single_bet_list_item)
            self.bet_list_widget_single.setItemWidget(single_bet_list_item, self.single_betWidget)
            self.bet_list_widget_single.setMinimumWidth(self.bet_list_widget_single.sizeHintForColumn(0)+20)
            
            
        elif self.current_bet_type == "parlay":
                self.parlay_betWidget = ParlayBetWidget(self.parent)
                self.parlay_betWidget.update_labels(bet_event)

                if bet_event.eventId in self.parlay_bet_eventId_list or len(self.parlay_bet_eventId_list) == 5:
                    return
                else:
                    self.parlay_bet_eventId_list.append(bet_event.eventId)

                parlay_bet_list_item = QListWidgetItem(self.bet_list_widget_parlay)
                parlay_bet_list_item.setSizeHint(self.parlay_betWidget.sizeHint())
                self.parlay_betWidget.qlistItem = parlay_bet_list_item #for remove item when close button click or bet done
                self.bet_list_widget_parlay.addItem(parlay_bet_list_item)
                self.bet_list_widget_parlay.setMinimumWidth(self.bet_list_widget_parlay.sizeHintForColumn(0))
                self.bet_list_widget_parlay.setItemWidget(parlay_bet_list_item, self.parlay_betWidget)
                
                self.event.trigger_callback("parlay_list_updated")
                self.disable_event(bet_event.eventId) #disable event when parlay slip added



    def update_slips_from_events(self):
        for slip_item in [self.bet_list_widget_parlay.item(i) for i in range(self.bet_list_widget_parlay.count())]:
            slip_itemwidget = self.bet_list_widget_parlay.itemWidget(slip_item)
            for event_item in [self.parent.eventQListWidget.item(i) for i in range(self.parent.eventQListWidget.count())]:
                event_itemwidget = self.parent.eventQListWidget.itemWidget(event_item)
                if str(event_itemwidget.eventId) == slip_itemwidget.eventIdToBetOn:
                    event_itemwidget.betOutcome = slip_itemwidget.betOutcome #outcome is same from slip. as we dont click we dont have outcome
                    slip_itemwidget.update_labels(event_itemwidget)
                    self.event.trigger_callback("parlay_list_updated") #update slip data and bet_box calculation too.

        for slip_item in [self.bet_list_widget_single.item(i) for i in range(self.bet_list_widget_single.count())]:
            slip_itemwidget = self.bet_list_widget_single.itemWidget(slip_item)
            for event_item in [self.parent.eventQListWidget.item(i) for i in range(self.parent.eventQListWidget.count())]:
                event_itemwidget = self.parent.eventQListWidget.itemWidget(event_item)
                if str(event_itemwidget.eventId) == slip_itemwidget.eventIdToBetOn:
                    event_itemwidget.betOutcome = slip_itemwidget.betOutcome #outcome is same from slip. as we dont click we dont have outcome
                    slip_itemwidget.update_labels(event_itemwidget)
            

    def switch_bet_type(self):
        bet_type_radio = self.sender()
        if bet_type_radio.isChecked() and bet_type_radio.bet_type == "single":
            self.widget_single_bet.setVisible(True)
            self.widget_parlay_bet.setVisible(False)
            self.current_bet_type = "single"
            self.enable_All_Events() #enable all events when switch to single bet
        else:
            self.widget_single_bet.setVisible(False)
            self.widget_parlay_bet.setVisible(True)
            self.current_bet_type = "parlay"
            self.disable_All_Events() #disable all event when switch to parlay bet
                  
    def clear_list(self):
        if self.current_bet_type == "single":
            self.bet_list_widget_single.clear()
        else: 
            self.bet_list_widget_parlay.clear()
            self.event.trigger_callback("parlay_list_updated")
            self.enable_All_Events() #enable all events when parlay list clear
            self.parlay_bet_eventId_list.clear()

    def clear_both_list(self):
        self.bet_list_widget_single.clear()
        #parlay
        self.bet_list_widget_parlay.clear()
        self.event.trigger_callback("parlay_list_updated")
        self.enable_All_Events() #enable all events when parlay list clear
        self.parlay_bet_eventId_list.clear()

    def remove_bet_by_eventId(self,eventId):
        #remove expired event net slip for parlay
        for item in [self.bet_list_widget_parlay.item(i) for i in range(self.bet_list_widget_parlay.count())]:
            itemwidget = self.bet_list_widget_parlay.itemWidget(item)
            if itemwidget.eventIdToBetOn == str(eventId):
                self.remove_bet_by_item(item,"parlay")
                 
        #remove expired event net slip for single
        for item in [self.bet_list_widget_single.item(i) for i in range(self.bet_list_widget_single.count())]:
            itemwidget = self.bet_list_widget_single.itemWidget(item)
            if itemwidget.eventIdToBetOn == str(eventId):
                self.remove_bet_by_item(item,"single")

    def remove_bet_by_item(self,list_item, bet_type): #single or parlay
        if bet_type == "single":
            item = self.bet_list_widget_single.takeItem(self.bet_list_widget_single.row(list_item))
        elif bet_type == "parlay":
            #remove from eventId list 
            itemwidget = self.bet_list_widget_parlay.itemWidget(list_item)
            self.enable_event(itemwidget.eventIdToBetOn) #enable event when parlay slip removed
            self.parlay_bet_eventId_list.remove(itemwidget.eventIdToBetOn)

            item = self.bet_list_widget_parlay.takeItem(self.bet_list_widget_parlay.row(list_item))
            self.event.trigger_callback("parlay_list_updated")
        
        del item
        self.bet_list_widget_parlay.repaint()
        self.bet_list_widget_single.repaint()

    def enable_All_Events(self): 
        for item in [self.parent.eventQListWidget.item(i) for i in range(self.parent.eventQListWidget.count())]:
                itemwidget = self.parent.eventQListWidget.itemWidget(item)
                if itemwidget and itemwidget.eventId in self.parlay_bet_eventId_list:
                    itemwidget.setDisabled(False) #enable all event related to parlayslip

    def disable_All_Events(self): 
        if self.current_bet_type == 'parlay':
            for item in [self.parent.eventQListWidget.item(i) for i in range(self.parent.eventQListWidget.count())]:
                itemwidget = self.parent.eventQListWidget.itemWidget(item)
                if itemwidget and itemwidget.eventId in self.parlay_bet_eventId_list:
                    itemwidget.setDisabled(True) #disable all event related to parlayslip

    def disable_event(self, event_Id):
        for item in [self.parent.eventQListWidget.item(i) for i in range(self.parent.eventQListWidget.count())]:
                itemwidget = self.parent.eventQListWidget.itemWidget(item)
                if itemwidget.eventId == event_Id:
                    itemwidget.setDisabled(True) #disable single event
        
    def enable_event(self, event_Id):
        for item in [self.parent.eventQListWidget.item(i) for i in range(self.parent.eventQListWidget.count())]:
                itemwidget = self.parent.eventQListWidget.itemWidget(item)
                if itemwidget.eventId == event_Id:
                    itemwidget.setDisabled(False) #enable single event
        
    def bet_done(self,event,args):

        if args == None:
            return 
            
        if args["type"] == "parlay":
           self.bet_list_widget_parlay.clear()
           self.event.trigger_callback("parlay_list_updated")
           self.enable_All_Events() #enable all events when parlay list clear
           self.parlay_bet_eventId_list.clear()
        if args["type"] == "single":
            self.remove_bet_by_item(args["listitem"].qlistItem,"single")
           



               
            

            
                   