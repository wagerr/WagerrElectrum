

from PyQt5.QtWidgets import QButtonGroup, QFrame, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
from electrum.gui.qt.util import read_QImage
from PyQt5.QtCore import QSize, Qt
from electrum.gui.qt.amountedit import AmountEdit, BTCAmountEdit
from PyQt5.QtGui import QDoubleValidator
from .equal_not_equal_widget import Equal_NotEqual
from .under_over_widget import Total_Under_Over
from .odd_even_widget import Odd_Even

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
        #header Hbox
        self.header_hbox = QHBoxLayout()
        self.header_img = read_QImage('dice_logo.png')
        self.lbl_img = QLabel()
        self.lbl_img.setPixmap(self.header_img)
        self.lbl_img.resize(50, 50)
        self.lbl_img.setAlignment(Qt.AlignCenter)
        self.header_hbox.addWidget(self.lbl_img)
        self.main_vbox.addLayout(self.header_hbox)

    def build_roll_choice_box(self):

        self.roll_choice_box = QHBoxLayout()
        self.roll_choice_grid = QGridLayout()

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
         
        self.roll_choice_grid.addWidget(self.btn_choice_E_NE,0,4)
        self.roll_choice_grid.addWidget(self.btn_choice_U_O,0,5)
        self.roll_choice_grid.addWidget(self.btn_choice_E_O,0,6)

        self.roll_choice_box.addLayout(self.roll_choice_grid)

        self.line = QFrame();
        self.line.setFrameShape(QFrame.HLine);
        self.line.setFrameShadow(QFrame.Sunken);

        self.lbl_roll_title = QLabel("")
        self.lbl_roll_title.setStyleSheet("font-size:20pt;font-weight:bold")
        self.lbl_roll_title.setAlignment(Qt.AlignCenter)

        self.main_vbox.addLayout(self.roll_choice_box)
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

        