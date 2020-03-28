import sys
import qtmodern.styles
import qtmodern.windows
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.uic.Compiler.qtproxies import QtCore, QtWidgets

import subprocess

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import user
import network
import firewall
import share
import system
import backup



class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0,0,1500, 1000)
        self.setWindowTitle("ADMIN-TOOL")
        #self.setWindowIcon(QIcon('icons/admin-tool3.png'))
        #self.setFixedSize(self.size())


        self.UI()
        self.show()


    def UI(self):
        self.createMenu()
        self.toolBar()
        self.widgets()
        self.initialWidget()

    def initialWidget(self):
        pass

    def createMenu(self):

        #CREATEING MENU
        menubar=self.menuBar()
        file=menubar.addMenu("File")
        edite=menubar.addMenu("Edit")
        code=menubar.addMenu("Preferences")
        help_menu=menubar.addMenu("help")

        #CREATING SUB MENU
        new=QAction("New Project",self)
        new.setShortcut("Ctrl+O")
        file.addAction(new)

        open=QAction("Open",self)
        file.addAction(open)

        exit=QAction("Exit",self)
        #exit.setIcon(QIcon("icons/exit"))
        exit.triggered.connect(self.exitFunc)
        file.addAction(exit)

        #ADDING MENU TO TOP LAYOUT

    def toolBar(self):

        self.tb=self.addToolBar("tool bar")
        self.tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        # ICONS

        self.userTB=QAction(QIcon('icons/icon_user2.png'),"User Management",self)
        self.tb.addAction(self.userTB)
        self.userTB.triggered.connect(self.userSection)
         #self.tb.addSeparator()

        self.networkingTB=QAction(QIcon('icons/networking2.png'),"Networking",self)
        self.tb.addAction(self.networkingTB)
        self.networkingTB.triggered.connect(self.networkSection)

        self.firewallTB = QAction(QIcon('icons/firewall.png'), "Firewall", self)
        self.tb.addAction(self.firewallTB )
        self.firewallTB.triggered.connect(self.firewallSection)

        self.backupTB = QAction(QIcon('icons/backup1.png'), "Backup Management", self)
        self.tb.addAction(self.backupTB)
        self.backupTB.triggered.connect(self.backupSection)

        self.shareTB = QAction(QIcon('icons/share2.png'), "Share", self)
        self.tb.addAction(self.shareTB)
        self.shareTB.triggered.connect(self.shareSection)

        self.preferencesTB = QAction(QIcon('icons/preferences1.png'), "Preferences", self)
        self.tb.addAction(self.preferencesTB)
        self.preferencesTB.triggered.connect(self.preferencesSection)


        #TAB ACTION TIGRED
        #self.tb.actionTriggered.connect(self.toolFunction)


    def widgets(self):
        line='-'*74
        self.listWidget = QListWidget(self)
        self.listWidget.resize(200,800)
        self.listWidget.move(5,85)

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

    def getContentTrigger(self):
        syss = System()
        si = self.listWidget.selectedItems()[0]
        if si==self.item1:
            syss.getContentSystem()
            print("syss")
        elif si==self.item2:
            self.getContentUser()
            print("useee")
        elif si==self.item3:
            self.getContentNetwork()
        elif si==self.item4:
            self.getContentFirewall()
        else:
            QMessageBox.warning(self,"warning","no section selected, please selecet a section")








    def getContentUser(self):
        pass
    def getContentNetwork(self):
        pass
    def getContentFirewall(self):
        pass



    def userSection(self):
        self.userconfig=user.UserConfig()

    def networkSection(self):
        self.networkconfig=network.networkConfig()

    def firewallSection(self):
        self.firewallconfig=firewall.firewallConfig()

    def backupSection(self):
        self.backupconfig=backup.backupConfig()

    def shareSection(self):
        self.shareconfig=share.shareConfig()

    def preferencesSection(self):
        self.preferencesconfig=system.preferencesConfig()



    def clickingEvent(self):
        print("clickiiiiiiing")

    def exitFunc(self):
        mbox=QMessageBox.information(self,"Warrings","Are you sure to exit ",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
        if mbox==QMessageBox.Yes:
            sys.exit()
    def btnFunction(self,btn):
        if(btn.text()=='New'):
            print("You cliked new button ")
        elif(btn.text()=='Open'):
            print("You cliked open ")
        else:
            print("You cliked exit button  ")


class System(QWidget):
    def __init__(self):
        self.getContentSystem()

    def getContentSystem(self):
        self.mainLayout=QHBoxLayout()
        #self.mainLayout.move(50,85)

        self.topLayout=QGridLayout()
        self.topLayout.addWidget(QPushButton("click"),0,0)
        self.topLayout.addWidget(QPushButton("click"),0,1)
        self.topLayout.addWidget(QPushButton("click"),0,2)

        self.bottomLayout=QHBoxLayout()
        self.bottomLayout.addWidget(QLabel("Some Shit here dfgkhdbsjg shbdg"))
        self.bottomLayout.addWidget(QLabel("Some Shit here dfgkhdbsjg shbdgdsfkghsd dfskgjdfsg"))
        self.bottomLayout.addWidget(QPushButton("djhbdsj"))

        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.bottomLayout)
        self.setLayout(self.mainLayout)
        self.show()

        hostname = str(subprocess.Popen("hostname",shell=True,stdout=subprocess.PIPE).communicate()[0].decode("utf-8"))
        hostname = str(subprocess.Popen("hostname",shell=True,stdout=subprocess.PIPE).communicate()[0].decode("utf-8"))
        hostname = str(subprocess.Popen("hostname",shell=True,stdout=subprocess.PIPE).communicate()[0].decode("utf-8"))
        hostname = str(subprocess.Popen("hostname",shell=True,stdout=subprocess.PIPE).communicate()[0].decode("utf-8"))




def main():
    App = QApplication(sys.argv)
    window = Window()
    qtmodern.styles.light(App)
    mw = qtmodern.windows.ModernWindow(window)
    mw.show()
    sys.exit(App.exec_())

if __name__=='__main__':
    main()
