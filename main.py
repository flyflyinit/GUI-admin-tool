import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt , QTimer,QModelIndex
from PyQt5.QtGui import QPixmap
from qtpy import QtWidgets, QtCore
import qtmodern.styles
import qtmodern.windows

from system import mainsystem

class networkConfig(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 1500, 1000)
        self.setWindowTitle("Tool Name")
        # self.setWindowIcon(QIcon('icons/admin-tool3.png'))
        self.UI()
        self.show()

    def UI(self):
        self.layouts()
        self.widgets()

    def layouts(self):
        self.mainLayout=QVBoxLayout()
        self.topLayout=QHBoxLayout()
        self.bottomLayout=QHBoxLayout()

        self.bottomLeftLayout=QHBoxLayout()
        self.bottomRightLayout=QVBoxLayout()

        logo = QLabel(self)
        pixmap = QPixmap('icons/admin.png')
        pixmap5 = pixmap.scaled(50, 50)
        logo.setPixmap(pixmap5)

        self.topLayout.addWidget(logo)
        self.topLayout.addStretch()

        self.bottomLayout.addLayout(self.bottomLeftLayout)
        self.bottomLayout.addStretch()
        self.bottomLayout.addLayout(self.bottomRightLayout)
        #self.bottomLayout.addStretch()

        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.bottomLayout)

        self.setLayout(self.mainLayout)
        self.setLayout(self.bottomLayout)
        self.setLayout(self.topLayout)


    def widgets(self):
        self.listWidget = QListWidget(self)
        self.listWidget.setSelectionMode(QAbstractItemView.SingleSelection)

        #self.listWidget.resize(50,50)

        self.item1 = QtWidgets.QListWidgetItem("System Information")
        self.item1.setSizeHint(QtCore.QSize(50, 50))
        self.listWidget.addItem(self.item1)
        self.item2 = QtWidgets.QListWidgetItem("Users Statistics")
        self.item2.setSizeHint(QtCore.QSize(50, 50))
        self.listWidget.addItem(self.item2)
        self.item3 = QtWidgets.QListWidgetItem("Network Statistics")
        self.item3.setSizeHint(QtCore.QSize(50, 50))
        self.listWidget.addItem(self.item3)
        self.item4 = QtWidgets.QListWidgetItem("Firewall")
        self.item4.setSizeHint(QtCore.QSize(50, 50))
        self.listWidget.addItem(self.item4)
        self.listWidget.itemSelectionChanged.connect(self.getContentTrigger)
        self.bottomLeftLayout.addWidget(self.listWidget)

        self.listWidget.setCurrentItem(self.item1)

    def getContentTrigger(self):
        si = self.listWidget.selectedItems()[0]
        if si==self.item1:
            self.clearLayout(self.bottomRightLayout)
            mainsystem.getContentSystem(self)
        elif si==self.item2:
            self.clearLayout(self.bottomRightLayout)
        elif si==self.item3:
            self.clearLayout(self.bottomRightLayout)
        elif si==self.item4:
            self.clearLayout(self.bottomRightLayout)
        else:
            QMessageBox.warning(self,"warning","no section selected, please selecet a section")

    def clearLayout(self,layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clearLayout(child.layout())

def main():
    App = QApplication(sys.argv)
    window = networkConfig()
    qtmodern.styles.light(App)
    mw = qtmodern.windows.ModernWindow(window)
    mw.show()
    sys.exit(App.exec_())

if __name__ == '__main__':
    main()