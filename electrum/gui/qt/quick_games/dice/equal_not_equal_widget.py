from PyQt5.QtWidgets import QButtonGroup, QGridLayout, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QSize, Qt
from electrum.gui.qt.amountedit import AmountEdit, BTCAmountEdit
from PyQt5.QtGui import QDoubleValidator
from electrum.bitcoin import COIN

MIN_ROLL_AMT  = 25 #WGR
MAX_ROLL_AMT  = 10000 #WGR

EFFECTIVE_ODDS = { #effective odds Equal- NotEqual
2: "35.6214-1.0283",
3: "17.8157-1.0582",
4: "11.8947-1.0899",
5: "8.9208-1.1237",
6: "7.1374-1.1596",
7: "5.9488-1.198",
8: "7.1374-1.1596",
9: "8.9208-1.1237",
10: "11.894-1.0899",
11: "17.8157-1.0582",
12: "35.6214-1.0283"
}

ONCHAIN_ODDS = {

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

        self.lbl_potential_return = QLabel("")
        self.lbl_potential_return.setStyleSheet("color:#CA2626")
        self.lbl_potential_return.setAlignment(Qt.AlignCenter)
        self.lbl_potential_return.setWordWrap(True)
        
        self.roll_control_widget = QWidget()
        self.roll_control_vbox = QVBoxLayout(self.roll_control_widget)
        
        self.roll_control_hbox = QHBoxLayout()
        self.roll_control_hbox.addWidget(self.btn_equal_to)
        self.roll_control_hbox.addWidget(self.edit_roll_amount)
        self.roll_control_hbox.addWidget(self.btn_not_equal_to)
        self.roll_control_hbox.setSpacing(20)

        self.roll_control_vbox.addLayout(self.roll_control_hbox)
        self.roll_control_vbox.addWidget(self.lbl_potential_return)
        
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
        print(str(id))

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

      
        pr_equal = str("(Equal) {0:.2f}".format(bb * float(odds_equal))) 
        pr_not_equal = str("(Not Equal) {0:.2f}".format(bb * float(odds_not_equal)))
        self.lbl_potential_return.setText("Poterntial Return: " + pr_equal + ' ' + self.parent.base_unit() + ' / ' + pr_not_equal + ' ' + self.parent.base_unit())