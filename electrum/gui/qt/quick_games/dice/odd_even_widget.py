


from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from electrum.gui.qt.amountedit import AmountEdit, BTCAmountEdit
from PyQt5.QtCore import Qt
from electrum.bitcoin import COIN
from PyQt5.QtGui import QDoubleValidator

MIN_ROLL_AMT  = 25 #WGR
MAX_ROLL_AMT  = 10000 #WGR


EFFECTIVE_ODDS = { #effective odds OVER-UNDER
1: "1.99-1.99",
}

ONCHAIN_ODDS = {
1: "2-2"
}

class Odd_Even(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.parent = parent
        #self.setStyleSheet("background-color:#BD0000;")
        self.build_ui()
        self.isEffectiveOdds = self.parent.config.get('iseffectiveodds',True)

    def build_ui(self):
         #roll odd/even
        self.main_grid = QGridLayout()
        self.btn_roll_odd = QPushButton("Roll odd")
        

        self.edit_roll_amount = BTCAmountEdit(self.parent.get_decimal_point)
        self.edit_roll_amount.setMaximumWidth(200)
        self.edit_roll_amount.setPlaceholderText("Roll Amount (Min 25)")
        self.edit_roll_amount.setValidator(QDoubleValidator(self.edit_roll_amount))
        self.edit_roll_amount.textChanged.connect(self.amountChanged)
        
        self.fiat_c = AmountEdit(self.parent.fx.get_currency if self.parent.fx else '')
        if not self.parent.fx or not self.parent.fx.is_enabled():
            self.fiat_c.setVisible(False)

        self.edit_roll_amount.frozen.connect(
            lambda: self.fiat_c.setFrozen(self.edit_roll_amount.isReadOnly()))


        self.btn_roll_even = QPushButton("Roll even")
        
        self.btn_roll_odd.clicked.connect(lambda:self.do_roll("ODD"))
        self.btn_roll_even.clicked.connect(lambda:self.do_roll("EVEN"))

        self.btn_roll_odd.setDisabled(True)
        self.btn_roll_even.setDisabled(True)
       
        self.roll_control_widget = QWidget()

        self.roll_control_vbox = QVBoxLayout(self.roll_control_widget)
        
        self.roll_control_grid = QGridLayout()
        self.roll_control_grid.addWidget(self.btn_roll_odd,0,1)
        self.roll_control_grid.addWidget(self.edit_roll_amount,0,2)
        self.roll_control_grid.addWidget(self.btn_roll_even,0,3)
        self.roll_control_grid.setSpacing(20)

        self.lbl_pr_odd = QLabel("")
        self.lbl_pr_odd.setStyleSheet("color:#CA2626")
        self.lbl_pr_odd.setAlignment(Qt.AlignCenter)
        self.lbl_pr_even = QLabel("")
        self.lbl_pr_even.setStyleSheet("color:#CA2626")
        self.lbl_pr_even.setAlignment(Qt.AlignCenter)

        self.roll_control_grid.addWidget(self.lbl_pr_odd,1,1)
        self.roll_control_grid.addWidget(QWidget(),1,2)
        self.roll_control_grid.addWidget(self.lbl_pr_even,1,3)

        self.roll_control_vbox.addLayout(self.roll_control_grid)
        
        self.roll_control_widget.setFixedWidth(500)
        self.main_grid.addWidget(self.roll_control_widget)
        
        self.setLayout(self.main_grid)

    
    def do_roll(self, side):
        self.side = side
        self.amount = int(self.edit_roll_amount.get_amount())
        self.parent.do_roll(d = self)

    def amountChanged(self):
        rollAmtInWgr = (self.edit_roll_amount.get_amount() or 0) / COIN
        if rollAmtInWgr >= MIN_ROLL_AMT and rollAmtInWgr <= MAX_ROLL_AMT:
           self.btn_roll_odd.setDisabled(False)
           self.btn_roll_even.setDisabled(False)
        else:
           self.btn_roll_odd.setDisabled(True)
           self.btn_roll_even.setDisabled(True)
           

        bb = float(0)
        if not self.edit_roll_amount.text() == "":
            bb = float(self.edit_roll_amount.text())
            
        
        Current_Odd = EFFECTIVE_ODDS if self.isEffectiveOdds else ONCHAIN_ODDS

        even = Current_Odd[1].split("-")[0]
        odd = Current_Odd[1].split("-")[1]

      
        pr_even = str("{0:.2f}".format(bb * float(even))) 
        pr_odd = str("{0:.2f}".format(bb * float(odd)))

        self.lbl_pr_even.setText(pr_even)
        self.lbl_pr_odd.setText(pr_odd)
        