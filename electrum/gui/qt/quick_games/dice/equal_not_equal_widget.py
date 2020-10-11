from PyQt5.QtWidgets import QButtonGroup, QGridLayout, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QSize, Qt
from electrum.gui.qt.amountedit import AmountEdit, BTCAmountEdit
from PyQt5.QtGui import QDoubleValidator
from electrum.bitcoin import COIN
from electrum.util import format_amount
from ..game_util import calculate_potential_return
from electrum.event import Event

MIN_ROLL_AMT  = 25 #WGR
MAX_ROLL_AMT  = 10000 #WGR


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
            button.setStyleSheet("background-color: white; color:red; font-size:22pt; font-weight:bold;")
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
        self.lbl_pr_equal.setStyleSheet("color:black;font-weight:bold;")

        self.lbl_pr_label = QLabel("")
        self.lbl_pr_label.setAlignment(Qt.AlignCenter)
        self.lbl_pr_label.setStyleSheet("color:black;font-weight:bold;")

        self.lbl_pr_notequal = QLabel("")
        self.lbl_pr_notequal.setAlignment(Qt.AlignCenter)
        self.lbl_pr_notequal.setStyleSheet("color:black;font-weight:bold;")
       
        self.roll_control_grid.addWidget(self.lbl_pr_equal,1,1)
        self.roll_control_grid.addWidget(self.lbl_pr_label,1,2)
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
        self.parent.do_roll(self,"dice")
    
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
         
        pr_equal = calculate_potential_return(bb,self.roll_choice,"equal")
        pr_not_equal = calculate_potential_return(bb,self.roll_choice,"notequal")

        if not self.isEffectiveOdds: #calculate onchain odds
            pr_equal = (pr_equal - 1) / 0.99 + 1
            pr_not_equal = (pr_not_equal - 1) / 0.99 + 1

        pr_equal_str = format_amount(pr_equal)
        pr_not_equal_str = format_amount(pr_not_equal)

        self.lbl_pr_equal.setText(pr_equal_str)
        self.lbl_pr_label.setText("<-- Potential Return -->")
        self.lbl_pr_notequal.setText(pr_not_equal_str)
        