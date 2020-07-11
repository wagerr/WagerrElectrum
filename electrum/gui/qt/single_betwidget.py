from PyQt5.QtWidgets import (QVBoxLayout, QGridLayout, QLineEdit, QTreeWidgetItem,
                             QHBoxLayout, QPushButton, QScrollArea, QTextEdit, 
                             QFrame, QShortcut, QMainWindow, QCompleter, QInputDialog,
                             QWidget, QMenu, QSizePolicy, QStatusBar, QListView,
                             QAbstractItemView, QSpacerItem, QSizePolicy, QListWidget,
                             QListWidgetItem, QWidget, QLabel, QLayout)
from PyQt5.QtCore import Qt, QRect, QStringListModel, QModelIndex, QItemSelectionModel,QSize
from PyQt5.QtGui import QFont, QDoubleValidator
from .amountedit import AmountEdit, BTCAmountEdit
from electrum.bitcoin import COIN, is_address, TYPE_ADDRESS

MIN_BET_AMT  = 25 #WGR
MAX_BET_AMT  = 10000 #WGR

class SingleBetWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.parent = parent
        self.vbox_c = QVBoxLayout()
        self.vbox_c.setSpacing(20)
        self.set_labels()
        self.qlistItem = None

    def btnCloseClicked(self):
        self.parent.betting_main_widget.remove_bet_by_item(self.qlistItem, "single")
        
    
    def set_labels(self):
        self.lblTitle = QLabel("")
        self.lblTitle.setWordWrap(True)
        self.lblTitle.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        
        self.eventIdToBetOn = ""
        self.betOutcome = 0

        #Header close button
        self.btnClose = QPushButton("X")
        self.btnClose.setMaximumSize(30,30)
        self.btnClose.clicked.connect(self.btnCloseClicked)

        #Error on Bet Amount Limit
        self.errText = "Incorrect bet amount. Please ensure your bet is between 25-10000 WGR inclusive."
        self.lblLimitError = QLabel(self.errText)
        self.lblLimitError.setStyleSheet("font-weight: bold;")
        
        self.lblLimitError.setWordWrap(True)
        self.lblLimitError.setMinimumSize(self.lblLimitError.sizeHint())
        
        self.lblPotentialReturn = QLabel("Potential Returns:")
        self.lblPotentialReturn.setAlignment(Qt.AlignHCenter)
        
        self.lblPotentialReturnValue = QLabel("0 WGR")
        self.lblPotentialReturnValue.setStyleSheet("color:#BD0000;font-weight: bold;")
        self.lblPotentialReturnValue.setAlignment(Qt.AlignHCenter)

        self.lblPick = QLabel("YOUR PICK:")
        self.lblPick.setAlignment(Qt.AlignHCenter)

        self.lblTeam = QLabel("")
        self.lblTeam.setStyleSheet("color:#BD0000;font-weight: bold;")
        self.lblTeam.setAlignment(Qt.AlignHCenter)
        #font = QFont("Times", 16) 
        #self.lblTeam.setFont(font)

        self.lblHandicap = QLabel("")
        self.lblHandicap.setAlignment(Qt.AlignHCenter)
        self.lblHandicap.setHidden(True)
        
        self.lblSelectedOddValue = QLabel("1")
        self.lblSelectedOddValue.setMinimumWidth(120)
        self.lblSelectedOddValue.setAlignment(Qt.AlignHCenter)
        self.lblSelectedOddValue.setStyleSheet("background-color: rgb(218, 225, 237);")

        self.editBettingAmount = BTCAmountEdit(self.parent.get_decimal_point)
        self.editBettingAmount.setPlaceholderText("0")
        self.editBettingAmount.setValidator(QDoubleValidator(self.editBettingAmount))
        self.editBettingAmount.textChanged.connect(self.betAmountChanged)

        self.fiat_c = AmountEdit(self.parent.fx.get_currency if self.parent.fx else '')
        if not self.parent.fx or not self.parent.fx.is_enabled():
            self.fiat_c.setVisible(False)

        self.editBettingAmount.frozen.connect(
            lambda: self.fiat_c.setFrozen(self.editBettingAmount.isReadOnly()))

        self.btnBet = QPushButton("BET")
        self.btnBet.clicked.connect(self.btnBetClicked)
        
        self.header_widget= QWidget()
        
        self.header_widget.setStyleSheet("QLabel { color:#fff;font-weight: bold; } QPushButton { color: #fff; border:0;} QWidget { background-color:#BD0000;}")
        self.header_hbox = QHBoxLayout()
        self.header_hbox.setSizeConstraint(QLayout.SetMinimumSize);
        self.header_hbox.setSpacing(0)
        self.header_widget.setLayout(self.header_hbox)
        
        self.header_hbox.addWidget(self.lblTitle,alignment=Qt.AlignLeft)
        self.header_hbox.addWidget(self.btnClose,alignment=Qt.AlignRight)
    
        self.vbox_c.addWidget(self.header_widget)
        self.vbox_c.addWidget(self.lblPick, alignment=Qt.AlignCenter)
        self.vbox_c.addWidget(self.lblTeam, alignment=Qt.AlignCenter)
        self.vbox_c.addWidget(self.lblHandicap, alignment=Qt.AlignCenter)
        self.vbox_c.addWidget(self.lblSelectedOddValue,alignment=Qt.AlignCenter)
        
        self.h = QHBoxLayout()
        self.h.addWidget(self.editBettingAmount)
        self.h.addWidget(self.btnBet)
        self.vbox_c.addLayout(self.h, Qt.AlignCenter)

        self.vbox_c.addWidget(self.lblLimitError)
        self.vbox_c.addWidget(self.lblPotentialReturn)
        self.vbox_c.addWidget(self.lblPotentialReturnValue)
        self.lblLimitError.setText("")
        self.setLayout(self.vbox_c)

    def btnBetClicked(self):
        betAmtInWgr = (self.editBettingAmount.get_amount() or 0) / COIN
        print("Betting Amount : ", betAmtInWgr)
        if betAmtInWgr >= MIN_BET_AMT and betAmtInWgr <= MAX_BET_AMT:
            test = self.parent.do_bet(a = self)
            self.parent.betting_main_widget.remove_bet_by_item(self,"single")

            
        
    def betAmountChanged(self):
        betAmtInWgr = (self.editBettingAmount.get_amount() or 0) / COIN
        if betAmtInWgr >= MIN_BET_AMT and betAmtInWgr <= MAX_BET_AMT or  betAmtInWgr == 0:
            self.lblLimitError.setText("")
        else:
            self.lblLimitError.setText(self.errText)
        bb = float(0)
        if self.editBettingAmount.text() == "":
            bb = float(0)
        else:
            bb = float(self.editBettingAmount.text())        
        self.btnBetValue = bb + (((bb * (float(self.lblSelectedOddValue.text()) -1 ))) *.94 )
        self.lblPotentialReturnValue.setText(str("{0:.2f}".format(self.btnBetValue))+ ' ' + self.parent.base_unit())