from PyQt5.QtWidgets import QButtonGroup, QGridLayout, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QSize, Qt
from electrum.gui.qt.amountedit import AmountEdit, BTCAmountEdit
from PyQt5.QtGui import QDoubleValidator
from electrum.bitcoin import COIN

MIN_ROLL_AMT  = 25 #WGR
MAX_ROLL_AMT  = 10000 #WGR


EFFECTIVE_ODDS = { #effective odds OVER-UNDER
2.5: "1.028215-35.621488",
3.5: "1.089892-11.894752",
4.5: "1.198-5.948812",
5.5: "1.380754-3.573703",
6.5: "1.707157-2.385802",
7.5: "2.385802-1.707157",
8.5: "3.573703-1.380754",
9.5: "5.948812-1.198",
10.5: "11.894752-1.089892",
11.5: "35.621488-1.028215"
}

ONCHAIN_ODDS = {
2.5: "1.0285-35.9712",
3.5: "1.0908-12.0048",
4.5: "1.2000-5.9988",
5.5: "1.3846-3.5997",
6.5: "1.7143-2.3998",
7.5: "2.3998-1.7143",
8.5: "3.5997-1.3846",
9.5: "5.9988-1.2000",
10.5: "12.0048-1.0908",
11.5: "35.9712-1.0285"
}

class Total_Under_Over(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.parent = parent
        #self.setStyleSheet("background-color:#BD0000;")
        self.build_ui()
        self.isEffectiveOdds = self.parent.config.get('iseffectiveodds',True)

    def build_ui(self):
         #roll under/over
        self.roll_choice = 0
        self.main_grid = QGridLayout()
        self.buttonGroup = QButtonGroup()
        btnsize = QSize(70,70)
        for i in range(2,12):
            button = QPushButton(str(i+ 0.5))
            button.setCheckable(True)
            button.setStyleSheet("background-color: white; color:red; font-size:30pt; font-weight:bold;")
            button.setFixedSize(btnsize)
            self.buttonGroup.addButton(button)
            self.main_grid.addWidget(button,0,i)
        
        self.buttonGroup.buttonClicked[int].connect(self.roll_selected)

        self.btn_roll_under = QPushButton("Roll under")

        self.edit_roll_amount = BTCAmountEdit(self.parent.get_decimal_point)
        self.edit_roll_amount.setPlaceholderText("Roll Amount (Min 25)")
        self.edit_roll_amount.setValidator(QDoubleValidator(self.edit_roll_amount))
        self.edit_roll_amount.textChanged.connect(self.amountChanged)
        
        self.fiat_c = AmountEdit(self.parent.fx.get_currency if self.parent.fx else '')
        if not self.parent.fx or not self.parent.fx.is_enabled():
            self.fiat_c.setVisible(False)

        self.edit_roll_amount.frozen.connect(
            lambda: self.fiat_c.setFrozen(self.edit_roll_amount.isReadOnly()))

        self.btn_roll_over = QPushButton("Roll over")
        
        self.btn_roll_over.clicked.connect(lambda:self.do_roll("TOTALOVER"))
        self.btn_roll_under.clicked.connect(lambda:self.do_roll("TOTALUNDER"))

        self.btn_roll_over.setDisabled(True)
        self.btn_roll_under.setDisabled(True)

        self.roll_control_widget = QWidget()
        self.roll_control_vbox = QVBoxLayout(self.roll_control_widget)

        self.roll_control_grid = QGridLayout()
        self.roll_control_grid.addWidget(self.btn_roll_under,0,1)
        self.roll_control_grid.addWidget(self.edit_roll_amount,0,2)
        self.roll_control_grid.addWidget(self.btn_roll_over,0,3)
        self.roll_control_grid.setSpacing(20)

        self.lbl_pr_under = QLabel("")
        self.lbl_pr_under.setStyleSheet("color:#CA2626")
        self.lbl_pr_under.setAlignment(Qt.AlignCenter)
        self.lbl_pr_over = QLabel("")
        self.lbl_pr_over.setStyleSheet("color:#CA2626")
        self.lbl_pr_over.setAlignment(Qt.AlignCenter)
        
        self.roll_control_grid.addWidget(self.lbl_pr_under,1,1)
        self.roll_control_grid.addWidget(QWidget(),1,2)
        self.roll_control_grid.addWidget(self.lbl_pr_over,1,3)

        self.roll_control_vbox.addLayout(self.roll_control_grid)

        self.main_grid.addWidget(self.roll_control_widget,2,4,1,5)
        self.main_grid.setSpacing(10)
        
        self.setLayout(self.main_grid)
    
    def reset_button_group(self):
        checked= self.buttonGroup.checkedButton()
        if checked:
            self.buttonGroup.setExclusive(False)
            checked.setChecked(False);
            self.buttonGroup.setExclusive(True)

    def roll_selected(self, id):
        self.roll_choice = abs(id) + 0.5
        self.amountChanged() #recalculate PR.

    def do_roll(self, side):
        self.side = side
        self.outcome = int(self.roll_choice)
        self.amount = int(self.edit_roll_amount.get_amount())
        self.parent.do_roll(d = self)

    def amountChanged(self):
        rollAmtInWgr = (self.edit_roll_amount.get_amount() or 0) / COIN
        if rollAmtInWgr >= MIN_ROLL_AMT and rollAmtInWgr <= MAX_ROLL_AMT and self.roll_choice != 0:
           self.btn_roll_over.setDisabled(False)
           self.btn_roll_under.setDisabled(False)
        else:
           self.btn_roll_over.setDisabled(True)
           self.btn_roll_under.setDisabled(True)
           return

        bb = float(0)
        if not self.edit_roll_amount.text() == "":
            bb = float(self.edit_roll_amount.text())
            
        
        Current_Odd = EFFECTIVE_ODDS if self.isEffectiveOdds else ONCHAIN_ODDS

        odds_over = Current_Odd[self.roll_choice].split("-")[0]
        odds_under = Current_Odd[self.roll_choice].split("-")[1]

      
        pr_over = str("PR: {0:.2f}".format(bb * float(odds_over))) 
        pr_under = str("PR: {0:.2f}".format(bb * float(odds_under)))
        
        self.lbl_pr_over.setText(pr_over)
        self.lbl_pr_under.setText(pr_under)