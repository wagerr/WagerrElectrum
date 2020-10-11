

from PyQt5.QtWidgets import QApplication, QButtonGroup, QFrame, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QSize, Qt
from electrum.gui.qt.amountedit import AmountEdit, BTCAmountEdit
from PyQt5.QtGui import QDoubleValidator, QMovie
from .equal_not_equal_widget import Equal_NotEqual
from .under_over_widget import Total_Under_Over
from .odd_even_widget import Odd_Even
from .dice_header_widget import DiceHeaderWidget

MIN_ROLL_AMT  = 25 #WGR
MAX_ROLL_AMT  = 10000 #WGR

class DiceGameWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.parent = parent
        #self.setStyleSheet("background-color:#BD0000;")
        self.build_ui()
        

    
    def build_ui(self):
        self.main_vbox = QVBoxLayout()
        
        self.build_header_box()
        self.build_roll_choice_box()
        self.build_roll_Equal_NEqual()
        self.build_roll_under_over()
        self.build_roll_even_odd()
        self.build_dice_history_list()

        self.main_vbox.addStretch()
        self.setLayout(self.main_vbox)

    def build_header_box(self):
        header_widget = DiceHeaderWidget(self)
        self.main_vbox.addWidget(header_widget)
        
    def build_roll_choice_box(self):

        self.btn_choice_E_NE = QPushButton("Equal/Not Equal")
        self.btn_choice_U_O = QPushButton("Under/Over")
        self.btn_choice_E_O = QPushButton("Even/Odd")

        self.btn_choice_E_NE.clicked.connect(lambda: self.flip_roll_control_visibility("E_NE"))
        self.btn_choice_U_O.clicked.connect(lambda: self.flip_roll_control_visibility("U_O"))
        self.btn_choice_E_O.clicked.connect(lambda: self.flip_roll_control_visibility("E_O"))

        self.btn_choice_E_NE.setStyleSheet("background-color:#CA2626;color:white")
        self.btn_choice_U_O.setStyleSheet("background-color:#CA2626;color:white")
        self.btn_choice_E_O.setStyleSheet("background-color:#CA2626;color:white")

        self.btn_choice_E_NE.setFixedHeight(50)
        self.btn_choice_U_O.setFixedHeight(50)
        self.btn_choice_E_O.setFixedHeight(50)
        
        self.roll_choice_grid = QGridLayout()
        self.roll_choice_grid.addWidget(self.btn_choice_E_NE,0,0)
        self.roll_choice_grid.addWidget(self.btn_choice_U_O,0,1)
        self.roll_choice_grid.addWidget(self.btn_choice_E_O,0,2)
        
        self.line = QFrame();
        self.line.setFrameShape(QFrame.HLine);
        self.line.setFrameShadow(QFrame.Sunken);

        self.lbl_roll_title = QLabel("")
        self.lbl_roll_title.setStyleSheet("font-size:20pt;font-weight:bold;color:#CA2626")
        self.lbl_roll_title.setAlignment(Qt.AlignCenter)

        self.main_vbox.addLayout(self.roll_choice_grid)
        self.main_vbox.addWidget(self.line)
        self.main_vbox.addWidget(self.lbl_roll_title)

    def build_roll_Equal_NEqual(self):
         self.roll_equal_not_equal = Equal_NotEqual(self.parent)
         self.main_vbox.addWidget(self.roll_equal_not_equal)
         self.roll_equal_not_equal.setVisible(False)
       
    def build_roll_under_over(self):
        self.roll_under_over = Total_Under_Over(self.parent)
        self.main_vbox.addWidget(self.roll_under_over)
        self.roll_under_over.setVisible(False)
       
    def build_roll_even_odd(self):
        self.roll_odd_even = Odd_Even(self.parent)
        self.main_vbox.addWidget(self.roll_odd_even)
        self.roll_odd_even.setVisible(False)
       
        

    def flip_roll_control_visibility(self, choice):
        self.current_roll_type = choice
        if choice == "E_NE":
            
            self.roll_equal_not_equal.setVisible(True)
            self.lbl_roll_title.setText("Roll Equal/Not Equal")
            
            self.roll_under_over.setVisible(False)
            self.roll_odd_even.setVisible(False)
        elif choice == "U_O":
            self.roll_under_over.setVisible(True)
            self.lbl_roll_title.setText("Roll Under/Over")

            self.roll_equal_not_equal.setVisible(False)
            self.roll_odd_even.setVisible(False)
        elif choice == "E_O":
            self.roll_odd_even.setVisible(True)
            self.lbl_roll_title.setText("Roll Even/Odd")

            self.roll_equal_not_equal.setVisible(False)
            self.roll_under_over.setVisible(False)
        self.reset_roll_buttonGroup()

    def reset_roll_buttonGroup(self):
        self.roll_equal_not_equal.reset_button_group()
        self.roll_under_over.reset_button_group()
    
    def build_dice_history_list(self):
        dice_history_list = self.parent.create_dice_history_grid()
        self.main_vbox.addWidget(dice_history_list)
        self.main_vbox.setStretchFactor(dice_history_list, 1000)
