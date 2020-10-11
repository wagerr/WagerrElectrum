from PyQt5 import QtCore
from electrum.event import Event
from PyQt5.QtGui import QMovie
from electrum.util import resource_path
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget
from electrum.gui.qt.util import read_QImage
from threading import Timer
from PyQt5.QtCore import QSize

class DiceHeaderWidget(QWidget):

    msg_roll_dice = QtCore.pyqtSignal(QMovie, QMovie)
    msg_dice_start = QtCore.pyqtSignal(QMovie,QMovie)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.parent = parent
        self.dice_event = Event.getInstance()
        self.parent = parent
        self.dice_block = None    
        self.build_ui()     
        

    def build_ui(self):
        self.header_img = read_QImage('dice_logo.jpg')
        self.lbl_dice1 = QLabel()
        self.lbl_dice2 = QLabel()
        self.lbl_dice_header_img = QLabel()
        self.lbl_dice_header_img.setPixmap(self.header_img)
        self.lbl_dice_header_img.setFixedHeight(200)
        self.header_hbox = QHBoxLayout()
        self.header_hbox.addStretch()
        self.header_hbox.addWidget(self.lbl_dice_header_img)
        self.header_hbox.addWidget(self.lbl_dice1)
        self.header_hbox.addWidget(self.lbl_dice2)
        self.header_hbox.addStretch()
        
        self.dice_event.register_callback(self.roll_dice,["roll_dice"])
        self.dice_event.register_callback(self.dice_start,["tx_brodcasted"])
        self.setLayout(self.header_hbox)

    
    def roll_dice(self, event, result):
        #only play animation once per block, because multiple result in single block is same
        if self.dice_block == result["blockHeight"]:
            return
        
        self.dice_block = result["blockHeight"]
        dice1 = str(result["betInfo"]["firstDice"])
        dice2 = str(result["betInfo"]["secondDice"])

        self.anim_dice1.stop()
        self.anim_dice2.stop()
        
        self.anim_dice1.setFileName(resource_path("gui","animations","dice","dice"+ dice1 + ".gif"))
        self.anim_dice2.setFileName(resource_path("gui","animations","dice","dice"+ dice2 + ".gif"))

        
        def stop_dice1(frame_no):
            if frame_no == self.anim_dice1.frameCount()-2:
                self.anim_dice1.stop()
                self.anim_dice2.stop()
                
        
        self.anim_dice1.frameChanged.connect(stop_dice1)

        self.anim_dice1.setCacheMode(QMovie.CacheAll)
        self.anim_dice2.setCacheMode(QMovie.CacheAll)
        
        self.lbl_dice1.setMovie(self.anim_dice1)
        self.lbl_dice2.setMovie(self.anim_dice2)

        self.anim_dice1.start()
        self.anim_dice2.start()

    def dice_start(self,event, args):
        print("dice_start called")
        if not (args == None) and args["type"] == "dice":
            self.anim_dice1 = QMovie(resource_path("gui","animations","dice","rolling" + ".gif"))
            self.anim_dice2 = QMovie(resource_path("gui","animations","dice","rolling" + ".gif"))
            
            self.lbl_dice_header_img.setVisible(False)
            self.lbl_dice1.setVisible(True)
            self.lbl_dice2.setVisible(True)

            self.lbl_dice1.setMovie(self.anim_dice1)
            self.lbl_dice2.setMovie(self.anim_dice1)
            self.anim_dice1.start()
            self.anim_dice2.start()
           