try:
    from PyQt5.QtCore import QProcess
    from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QLabel, QHBoxLayout, QSizePolicy, QPushButton
except ImportError as e:
    print(
        f'package PyQt5 Not Found\n{e}\ntry :\npip3 install --user pyqt5\nOR\ndnf install python3-pyqt5, yum install python3-pyqt5\n')

import subprocess
import os
from pathlib import Path


class embterminal(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.process = QProcess(self)
        self.terminal = QWidget(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.terminal)
        self.process.start(f'urxvt -embed {str(int(self.winId()))}')
        self.setLayout(layout)


def main(self, font="Monospace", size=10, style="Regular"):
    global i
    i = 1

    self.terminal = {}
    font = f"URxvt.font: xft:{font}:style={style}:size={str(size)}"

    cwd = os.getcwd()
    home = str(Path.home())

    subprocess.run(f"cp {cwd}/terminal/Xresources {home}/.Xresources", shell=True)
    with open(f'{home}/.Xresources', mode='a') as file:
        file.write(f'\n\n{font}')
    subprocess.run(f"xrdb {home}/.Xresources", shell=True)

    self.tabs = QTabWidget(self)
    self.tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    self.tabs.setAutoFillBackground(True)

    addTerminal = QPushButton("Add")
    addTerminal.clicked.connect(lambda: addTerminalClicked(self))
    deleteTerminal = QPushButton("Delete")
    deleteTerminal.clicked.connect(lambda: deleteTerminalClicked(self))
    addTerminal.setStyleSheet("color: #ecf0f1; background-color: #2ecc71 ; border: 0px solid #2c3e50")
    addTerminal.setFixedHeight(30)
    addTerminal.setFixedWidth(50)
    deleteTerminal.setStyleSheet("color: #ecf0f1; background-color: #e74c3c; border: 0px solid #2c3e50")
    deleteTerminal.setFixedHeight(30)
    deleteTerminal.setFixedWidth(50)

    increases = QPushButton("+ size")
    increases.clicked.connect(lambda: increaseSize(self, size))
    decreases = QPushButton("- size")
    decreases.clicked.connect(lambda: decreaseeSize(self, size))
    increases.setStyleSheet("color: #ecf0f1; background-color: #303a46 ; border: 0px solid #2c3e50")
    increases.setFixedHeight(30)
    increases.setFixedWidth(50)
    decreases.setStyleSheet("color: #ecf0f1; background-color: #303a46; border: 0px solid #2c3e50")
    decreases.setFixedHeight(30)
    decreases.setFixedWidth(50)

    self.terminal[i] = embterminal()
    self.tabs.addTab(self.terminal[i], f"Terminal{str(i)}")

    box = QHBoxLayout()
    box.addStretch()
    box.addWidget(increases)
    box.addWidget(decreases)
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


def increaseSize(self, size):
    self.clearLayout(self.bottomRightLayout)
    if size <= 100:
        main(self, size=size + 5)
    else:
        main(self, size=size)


def decreaseeSize(self, size):
    self.clearLayout(self.bottomRightLayout)
    if 5 <= size:
        main(self, size=size - 5)
    else:
        main(self, size=size)
