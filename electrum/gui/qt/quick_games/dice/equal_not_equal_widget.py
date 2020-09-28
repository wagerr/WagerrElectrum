from PyQt5.QtWidgets import QButtonGroup, QGridLayout, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QSize, Qt
from electrum.gui.qt.amountedit import AmountEdit, BTCAmountEdit
from PyQt5.QtGui import QDoubleValidator
from electrum.bitcoin import COIN

MIN_ROLL_AMT  = 25 #WGR
MAX_ROLL_AMT  = 10000 #WGR

EFFECTIVE_ODDS = { #effective odds Equal- NotEqual
2: "35.621488-1.028215",
3: "17.815744-1.058212",
4: "11.894752-1.089892",
5: "8.920891-1.123651",
6: "7.137406-1.159687",
7: "5.948812-1.198",
8: "7.137406-1.159687",
9: "8.920891-1.123651",
10: "11.894752-1.089892",
11: "17.815744-1.058212",
12: "35.621488-1.028215"
}

ONCHAIN_ODDS = {
2: "35.9712-1.0285",
3: "17.9856-1.0588",
4: "12.0048-1.0908",
5: "9.0009-1.1249",
6: "7.1994-1.1613",
7: "5.9988-1.2000",
8: "7.1994-1.1613",
9: "9.0009-1.1249",
10: "12.0048-1.0908",
11: "17.9856-1.0588",
12: "35.9712-1.0285"
}



class Equal_NotEqual(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.parent = parent
        #self.setStyleSheet("background-color:#BD0000;")
        self.build_ui()
        self.isEffectiveOdds = self.parent.config.get('iseffectiveodds',True)

    def build_ui(self):
         #roll equal/notequal
        self.roll_choice = 0
        self.main_grid = QGridLayout()
        self.buttonGroup = QButtonGroup()
        
        btnsize = QSize(70,70)
        for i in range(2,13):
            button = QPushButton(str(i))
            button.setCheckable(True)
            button.setStyleSheet("background-color: white; color:red; font-size:30pt; font-weight:bold;")
            button.setFixedSize(btnsize)
            self.buttonGroup.addButton(button)
            self.main_grid.addWidget(button,0,i)
        
        self.buttonGroup.buttonClicked[int].connect(self.roll_selected)

        self.btn_equal_to = QPushButton("Equal to")

        self.edit_roll_amount = BTCAmountEdit(self.parent.get_decimal_point)
        self.edit_roll_amount.setPlaceholderText("Roll Amount (Min 25)")
        self.edit_roll_amount.setValidator(QDoubleValidator(self.edit_roll_amount))
        self.edit_roll_amount.textChanged.connect(self.amountChanged)
        
        self.fiat_c = AmountEdit(self.parent.fx.get_currency if self.parent.fx else '')
        if not self.parent.fx or not self.parent.fx.is_enabled():
            self.fiat_c.setVisible(False)

        self.edit_roll_amount.frozen.connect(
            lambda: self.fiat_c.setFrozen(self.edit_roll_amount.isReadOnly()))

        self.btn_not_equal_to = QPushButton("Not Equal to")
        
        self.btn_equal_to.setDisabled(True)
        self.btn_not_equal_to.setDisabled(True)

        self.btn_equal_to.clicked.connect(lambda:self.do_roll("EQUAL"))
        self.btn_not_equal_to.clicked.connect(lambda:self.do_roll("NOTEQUAL"))

        self.roll_control_widget = QWidget()
        self.roll_control_vbox = QVBoxLayout(self.roll_control_widget)
        
        self.roll_control_grid = QGridLayout()
        self.roll_control_grid.addWidget(self.btn_equal_to,0,1)
        self.roll_control_grid.addWidget(self.edit_roll_amount,0,2)
        self.roll_control_grid.addWidget(self.btn_not_equal_to,0,3)
        self.roll_control_grid.setSpacing(20)

        self.lbl_pr_equal = QLabel("")
        self.lbl_pr_equal.setAlignment(Qt.AlignCenter)
        self.lbl_pr_equal.setStyleSheet("color:#CA2626")
        self.lbl_pr_notequal = QLabel("")
        self.lbl_pr_notequal.setAlignment(Qt.AlignCenter)
        self.lbl_pr_notequal.setStyleSheet("color:#CA2626")
       
        self.roll_control_grid.addWidget(self.lbl_pr_equal,1,1)
        self.roll_control_grid.addWidget(QWidget(),1,2)
        self.roll_control_grid.addWidget(self.lbl_pr_notequal,1,3)
        

        self.roll_control_vbox.addLayout(self.roll_control_grid)
        
        
        self.main_grid.addWidget(self.roll_control_widget,2,5,1,5)
        self.main_grid.setSpacing(10)
        
        self.setLayout(self.main_grid)
    
    def reset_button_group(self):
        checked= self.buttonGroup.checkedButton()
        if checked:
            self.buttonGroup.setExclusive(False)
            checked.setChecked(False);
            self.buttonGroup.setExclusive(True)
        
    def roll_selected(self, id):
        self.roll_choice = abs(id)
        self.amountChanged() ##recalculate PR.
        

    def do_roll(self, side):
        self.side = side
        self.outcome = int(self.roll_choice)
        self.amount = int(self.edit_roll_amount.get_amount())
        self.parent.do_roll(d = self)

    def amountChanged(self):
        rollAmtInWgr = (self.edit_roll_amount.get_amount() or 0) / COIN
        if rollAmtInWgr >= MIN_ROLL_AMT and rollAmtInWgr <= MAX_ROLL_AMT and self.roll_choice != 0:
           self.btn_equal_to.setDisabled(False)
           self.btn_not_equal_to.setDisabled(False)
        else:
           self.btn_equal_to.setDisabled(True)
           self.btn_not_equal_to.setDisabled(True)
           return

        bb = float(0)
        if not self.edit_roll_amount.text() == "":
            bb = float(self.edit_roll_amount.text())
            
        
        Current_Odd = EFFECTIVE_ODDS if self.isEffectiveOdds else ONCHAIN_ODDS

        odds_equal = Current_Odd[self.roll_choice].split("-")[0]
        odds_not_equal = Current_Odd[self.roll_choice].split("-")[1]

      
        pr_equal = str("PR: {0:.2f}".format(bb * float(odds_equal))) 
        pr_not_equal = str("PR: {0:.2f}".format(bb * float(odds_not_equal)))
        self.lbl_pr_equal.setText(pr_equal)
        self.lbl_pr_notequal.setText(pr_not_equal)
        