try:
    from PyQt5.QtCore import QProcess
    from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QLabel, QHBoxLayout, QSizePolicy, QPushButton
except ImportError as e:
    print(f'package PyQt5 Not Found\n{e}\ntry :\npip3 install --user pyqt5\nOR\ndnf install python3-pyqt5, yum install python3-pyqt5\n')

import subprocess

class embterminal(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.process = QProcess(self)
        self.terminal = QWidget(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.terminal)
        self.process.start(f'urxvt -embed {str(int(self.winId()))}')
        #self.process.start(f'xterm -into {str(int(self.winId()))}')
        #-hold -geometry 298x500
        self.setLayout(layout)

def main(self):
    global i
    i = 1

    self.terminal = {}
    '''
    self.tabs = QTabWidget()
    self.tab1 = embterminal()
    self.tab2 = embterminal()

    self.tabs.addTab(self.tab2, "Tab 2")
    self.tabs.addTab(self.tab1, "Tab 1")

    # Add tabs to widget
    #self.layout.addWidget(self.tabs)
    #self.setLayout(self.layout)

    self.bottomRightLayout.addWidget(self.tabs)
    '''
    subprocess.run("cp terminal/Xresources ~/.Xresources",shell=True)
    subprocess.run("xrdb ~/.Xresources",shell=True)

    self.tabs = QTabWidget(self)
    self.tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    self.tabs.setAutoFillBackground(True)

    addTerminal = QPushButton("Add")
    addTerminal.clicked.connect(lambda :addTerminalClicked(self))
    deleteTerminal = QPushButton("Delete")
    deleteTerminal.clicked.connect(lambda :deleteTerminalClicked(self))
    addTerminal.setStyleSheet("color: #ecf0f1; background-color: #2ecc71 ; border: 0px solid #2c3e50")
    addTerminal.setFixedHeight(30)
    addTerminal.setFixedWidth(50)
    deleteTerminal.setStyleSheet("color: #ecf0f1; background-color: #e74c3c; border: 0px solid #2c3e50")
    deleteTerminal.setFixedHeight(30)
    deleteTerminal.setFixedWidth(50)

    self.terminal[i] = embterminal()
    self.tabs.addTab(self.terminal[i], f"Terminal{str(i)}")

    box = QHBoxLayout()
    box.addStretch()
    box.addWidget(addTerminal)
    box.addWidget(deleteTerminal)

    self.bottomRightLayout.addLayout(box)
    self.bottomRightLayout.addWidget(self.tabs)

def addTerminalClicked(self):
    global i
    i = i + 1
    self.terminal[i] = embterminal()
    self.tabs.addTab(self.terminal[i], f"Terminal{str(i)}")

def deleteTerminalClicked(self):
    self.tabs.removeTab(self.tabs.currentIndex())