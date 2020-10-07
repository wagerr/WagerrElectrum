


from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from electrum.bitcoin import COIN
from electrum.gui.qt.amountedit import AmountEdit, BTCAmountEdit
from PyQt5.QtGui import QDoubleValidator
from PyQt5 import QtCore
from electrum.event import Event
from electrum import constants

MIN_BET_AMT  = 25 #WGR
MAX_BET_AMT  = 10000 #WGR

class ParlayBetBoxWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.parent = parent

        self.event = Event.getInstance()
        self.event.register_callback(self.on_parlaybet_list_update,["parlay_list_updated"])

        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color:black;color:white")
        
        self.vbox_parlay_betting = QVBoxLayout(self)
        self.h0 = QHBoxLayout()
        self.totalLegs = QLabel("Total Legs: 0")
        self.totalodds = QLabel("Total Odds: 0")
        self.h0.addWidget(self.totalLegs)
        self.h0.addWidget(self.totalodds)
        
        self.editBettingAmount = BTCAmountEdit(self.parent.get_decimal_point)
        self.editBettingAmount.setPlaceholderText("0")
        self.editBettingAmount.setValidator(QDoubleValidator(self.editBettingAmount))
        self.editBettingAmount.textChanged.connect(self.betAmountChanged)

        self.fiat_c = AmountEdit(self.parent.fx.get_currency if self.parent.fx else '')
        if not self.parent.fx or not self.parent.fx.is_enabled():
            self.fiat_c.setVisible(False)

        self.editBettingAmount.frozen.connect(
            lambda: self.fiat_c.setFrozen(self.editBettingAmount.isReadOnly()))

        

        self.h = QHBoxLayout()
        self.h.addWidget(QLabel("BET"))
        self.h.addWidget(self.editBettingAmount)
        
        self.h1 = QHBoxLayout()
        self.h1.addWidget(QLabel("Potential Returns:"))
        self.totalWin = QLabel("0.0000000 {}".format(constants.net.SYMBOL))
        self.h1.addWidget(self.totalWin)

        self.errText = "Incorrect bet amount. Please ensure your bet is between 25-10000 {} inclusive.".format(constants.net.SYMBOL)
        self.lblLimitError = QLabel(self.errText)
        self.lblLimitError.setStyleSheet("font-weight: bold;")
        
        self.lblLimitError.setWordWrap(True)
        self.lblLimitError.setMinimumSize(self.lblLimitError.sizeHint())

        self.btnBet = QPushButton("PLACE BET")
        self.btnBet.setStyleSheet("QPushButton{" 
                                    "background-color:#BD0000"
                                 "}"
                                 "QPushButton:disabled{"
                                    "background-color:grey;"
                                 "}")
                            
        self.btnBet.setDisabled(True)
        self.btnBet.clicked.connect(self.btnBetClicked)

        self.vbox_parlay_betting.addLayout(self.h0)
        self.vbox_parlay_betting.addLayout(self.h)
        self.vbox_parlay_betting.addLayout(self.h1)
        self.vbox_parlay_betting.addWidget(self.lblLimitError)
        self.lblLimitError.setText("")
        self.vbox_parlay_betting.addWidget(self.btnBet)
        
        self.setLayout(self.vbox_parlay_betting)


    def betAmountChanged(self):
        bet_list_parlay = self.parent.betting_main_widget.bet_list_widget_parlay
        betAmtInWgr = (self.editBettingAmount.get_amount() or 0) / COIN
        if betAmtInWgr >= MIN_BET_AMT and betAmtInWgr <= MAX_BET_AMT or  betAmtInWgr == 0:
            self.lblLimitError.setText("")
        else:
            self.lblLimitError.setText(self.errText)
        bb = float(0)
        if not self.editBettingAmount.text() == "":
            bb = float(self.editBettingAmount.text())
        
        self.odds = float(0)
        self.effOddsSum = float(0)
        if bet_list_parlay.count() > 0:
            self.odds = float(1)
            self.effOddsSum = float(1)

        for i in range(0, bet_list_parlay.count()):
            item = bet_list_parlay.item(i)
            itemWidget = bet_list_parlay.itemWidget(item)
            self.odds = round(self.odds * float(itemWidget.lblSelectedOddValue.text()),2)
            
        
        for i in range(0, bet_list_parlay.count()):
            item = bet_list_parlay.item(i)
            itemWidget = bet_list_parlay.itemWidget(item)
            self.effOddsSum = round(self.effOddsSum * float(itemWidget.effectiveOddsValue),2)
        
        self.betValue = bb * float(self.effOddsSum)
        self.totalWin.setText(str("{0:.2f}".format(self.betValue))+ ' ' + self.parent.base_unit())
        self.totalLegs.setText("Total Legs: " + str(bet_list_parlay.count()))
        self.totalodds.setText("Total Odds: " + str(self.odds))
        if bet_list_parlay.count() > 1 and self.lblLimitError.text() == "" and betAmtInWgr > 0 :
           self.btnBet.setDisabled(False)
        else: 
           self.btnBet.setDisabled(True)

    
    def btnBetClicked(self):
        bet_list_parlay = self.parent.betting_main_widget.bet_list_widget_parlay
        betAmtInWgr = (self.editBettingAmount.get_amount() or 0) / COIN
        print("Betting Amount : ", betAmtInWgr)
        if betAmtInWgr >= MIN_BET_AMT and betAmtInWgr <= MAX_BET_AMT:
            self.legs = []
            for i in range(0, bet_list_parlay.count()):
                item = bet_list_parlay.item(i)
                itemWidget = bet_list_parlay.itemWidget(item)
                eventId = itemWidget.eventIdToBetOn
                outcomeType = itemWidget.betOutcome
                self.legs.append({"eventId":eventId,"outcomeType":outcomeType})
            self.parent.do_bet(self,"parlay")
        

    def on_parlaybet_list_update(self, event, *args):
        self.betAmountChanged()

