import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class networkConfig(QWidget):

    def __init__(self):
        super().__init__()
        self.setGeometry(250, 250, 800, 600)
        self.setWindowTitle("Network  Configuration")
        # self.setWindowIcon(QIcon('icons/admin-tool3.png'))
        self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        pass

def main():
    App = QApplication(sys.argv)
    window = networkConfig()
    sys.exit(App.exec_())

