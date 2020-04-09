import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class embterminal(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.process = QProcess(self)
        self.terminal = QWidget(self)
        self.terminal.setFixedSize(1100,550)
        layout = QVBoxLayout(self)
        layout.addWidget(self.terminal)
        self.setLayout(layout)

        # Works also with urxvt:
        self.process.start('urxvt',['-embed', str(int(self.winId()))])
        print(self.winId())

def main(self):
    self.sw = embterminal()
    self.bottomRightLayout.addWidget(self.sw)
