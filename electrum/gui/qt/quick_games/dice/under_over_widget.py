from PyQt5.QtWidgets import QButtonGroup, QGridLayout, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QSize, Qt
from electrum.gui.qt.amountedit import AmountEdit, BTCAmountEdit
from PyQt5.QtGui import QDoubleValidator
from electrum.bitcoin import COIN
from electrum.util import format_amount
from electrum.gui.qt.quick_games.game_util import calculate_potential_return

MIN_ROLL_AMT  = 25 #WGR
MAX_ROLL_AMT  = 10000 #WGR


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
            button.setStyleSheet("background-color: white; color:red; font-size:22pt; font-weight:bold;")
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
        self.lbl_pr_under.setStyleSheet("color:black;font-weight:bold;")
        self.lbl_pr_under.setAlignment(Qt.AlignCenter)

        self.lbl_pr_label = QLabel("")
        self.lbl_pr_label.setAlignment(Qt.AlignCenter)
        self.lbl_pr_label.setStyleSheet("color:black;font-weight:bold;")

        self.lbl_pr_over = QLabel("")
        self.lbl_pr_over.setStyleSheet("color:black;font-weight:bold;")
        self.lbl_pr_over.setAlignment(Qt.AlignCenter)
        
        self.roll_control_grid.addWidget(self.lbl_pr_under,1,1)
        self.roll_control_grid.addWidget(self.lbl_pr_label,1,2)
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
        self.roll_choice = abs(id)
        self.amountChanged() #recalculate PR.

    def do_roll(self, side):
        self.side = side
        self.outcome = int(self.roll_choice)
        self.amount = int(self.edit_roll_amount.get_amount())
        self.parent.do_roll(self,"dice")

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
            
        
        pr_under = calculate_potential_return(bb,self.roll_choice,"totalunder")
        pr_over = calculate_potential_return(bb,self.roll_choice,"totalover")

        if not self.isEffectiveOdds: #calculate onchain odds
            pr_under = (pr_under - 1) / 0.99 + 1
            pr_over = (pr_over - 1) / 0.99 + 1

        pr_under_str = format_amount(pr_under)
        pr_over_str = format_amount(pr_over)

        self.lbl_pr_over.setText(pr_over_str)
        self.lbl_pr_label.setText("<-- Potential Return -->")
        self.lbl_pr_under.setText(pr_under_str)