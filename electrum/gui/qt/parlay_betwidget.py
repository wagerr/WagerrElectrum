
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLayout, QPushButton, QSizePolicy, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

class ParlayBetWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.parent = parent
        self.vbox_c = QVBoxLayout()
        self.vbox_c.setSpacing(20)
        self.set_labels()
        self.qlistItem = None

    def btnCloseClicked(self):
        self.parent.betting_main_widget.remove_bet_by_item(self.qlistItem,"parlay")
    
    def set_labels(self):
        self.lblTitle = QLabel("")
        self.lblTitle.setWordWrap(True)
        self.lblTitle.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.eventIdToBetOn = ""
        self.betOutcome = 0

        #require for bet_box odds and potential return calculation.
        self.onChainOddsValue = float(0)
        self.effectiveOddsValue = float(0)

        #Header close button
        self.btnClose = QPushButton("X")
        self.btnClose.setMaximumSize(30,30)
        self.btnClose.clicked.connect(self.btnCloseClicked)

        self.lblPick = QLabel("YOUR PICK:")
        self.lblPick.setAlignment(Qt.AlignHCenter)

        self.lblTeam = QLabel("")
        self.lblTeam.setStyleSheet("color:#BD0000;font-weight: bold;")
        self.lblTeam.setAlignment(Qt.AlignHCenter)

        self.lblHandicap = QLabel("")
        self.lblHandicap.setAlignment(Qt.AlignHCenter)
        self.lblHandicap.setHidden(True)

        self.lblSelectedOddValue = QLabel("1")
        self.lblSelectedOddValue.setMinimumWidth(120)
        self.lblSelectedOddValue.setAlignment(Qt.AlignHCenter)
        self.lblSelectedOddValue.setStyleSheet("background-color: rgb(218, 225, 237);")

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

        self.setLayout(self.vbox_c)