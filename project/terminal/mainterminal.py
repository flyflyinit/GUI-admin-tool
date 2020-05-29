try:
    from PyQt5.QtCore import QProcess
    from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QLabel,QHBoxLayout
except ImportError as e:
    print(f'package PyQt5 Not Found\n{e}\ntry :\npip3 install --user pyqt5\nOR\ndnf install python3-pyqt5, yum install python3-pyqt5\n')

import subprocess

class embterminal(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.process = QProcess(self)
        self.terminal = QWidget(self)
        self.terminal.setFixedSize(1100,550)
        #self.terminal.setFixedSize(300,300)
        layout = QVBoxLayout(self)
        layout.addWidget(self.terminal)
        self.process.start(f'urxvt -embed {str(int(self.winId()))}')
        #self.process.start(f'xterm -into {str(int(self.winId()))}')
        #-hold -geometry 298x500
        self.setLayout(layout)

def main(self):
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
    self.sw = embterminal()
    self.sw.setContentsMargins(20,20,25,20)

    box = QHBoxLayout()
    box.addWidget(self.sw)
    box.setContentsMargins(0,20,0,0)

    self.bottomRightLayout.addLayout(box)
