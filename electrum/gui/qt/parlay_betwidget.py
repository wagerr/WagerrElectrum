
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLayout, QPushButton, QSizePolicy, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

class ParlayBetWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.parent = parent
        self.vbox_c = QVBoxLayout()
        self.vbox_c.setSpacing(20)
        self.build_ui()
        self.qlistItem = None

    def btnCloseClicked(self):
        self.parent.betting_main_widget.remove_bet_by_item(self.qlistItem,"parlay")
    
    def build_ui(self):
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
        self.btnClose.setMaximumSize(50,50)
        self.btnClose.setStyleSheet("font-weight: bold;")
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


    def update_labels(self,bet_event):
                self.lblTitle.setText(bet_event.lblHomeTeam.text() + " vs " + bet_event.lblAwayTeam.text())  
                self.eventIdToBetOn = bet_event.eventId
                self.betOutcome = bet_event.betOutcome
                
                if bet_event.betOutcome == 1:
                    self.lblTeam.setText(bet_event.lblHomeTeam.text())
                    self.lblSelectedOddValue.setText(bet_event.btnMoneyLineHome.text())
                    self.onChainOddsValue = bet_event._moneyLineHomeOddsOC
                    self.effectiveOddsValue = bet_event._moneyLineHomeOddsE
                if bet_event.betOutcome == 2:
                    self.lblTeam.setText(bet_event.lblAwayTeam.text())
                    self.lblSelectedOddValue.setText(bet_event.btnMoneyLineAway.text())
                    self.onChainOddsValue = bet_event._moneyLineAwayOddsOC
                    self.effectiveOddsValue = bet_event._moneyLineAwayOddsE
                if bet_event.betOutcome == 3:
                    self.lblTeam.setText(bet_event.lblDraw.text())
                    self.lblSelectedOddValue.setText(bet_event.btnMoneyLineDraw.text())
                    self.onChainOddsValue = bet_event._moneyLineDrawOddsOC
                    self.effectiveOddsValue = bet_event._moneyLineDrawOddsE
                if bet_event.betOutcome == 4:
                    self.lblTeam.setText(bet_event.lblHomeTeam.text())
                    self.lblHandicap.setHidden(False)
                    self.lblHandicap.setText("Handicap "+ bet_event.spreadPointsHome)
                    self.lblSelectedOddValue.setText(bet_event.spreadHomeOdds)
                    self.onChainOddsValue = bet_event._spreadHomeOddsOC
                    self.effectiveOddsValue = bet_event._spreadHomeOddsE
                if bet_event.betOutcome == 5:
                    self.lblTeam.setText(bet_event.lblAwayTeam.text())
                    self.lblHandicap.setHidden(False)
                    self.lblHandicap.setText("Handicap "+ bet_event.spreadPointsAway)
                    self.lblSelectedOddValue.setText(bet_event.spreadAwayOdds)
                    self.onChainOddsValue = bet_event._spreadAwayOddsOC
                    self.effectiveOddsValue = bet_event._spreadAwayOddsE
                if bet_event.betOutcome == 6:
                    self.lblTeam.setText("Over " + bet_event.totalPoints)
                    self.lblSelectedOddValue.setText(bet_event.totalsOverOdds)
                    self.onChainOddsValue = bet_event._totalsOverOddsOC
                    self.effectiveOddsValue = bet_event._totalsOverOddsE
                if bet_event.betOutcome == 7:
                    self.lblTeam.setText("Under " + bet_event.totalPoints)
                    self.lblSelectedOddValue.setText(bet_event.totalsUnderOdds)
                    self.onChainOddsValue = bet_event._totalsUnderOddsOC
                    self.effectiveOddsValue = bet_event._totalsUnderOddsE