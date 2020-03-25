import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.uic.Compiler.qtproxies import QtCore

import user
import network
import firewall
import share
import preferences
import backup



class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(250,250,800, 600)
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

        self.titelInfo = QPushButton('information',self)
        self.titelInfo.move(350, 90)


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

        self.listWidget = QListWidget(self)
        self.listWidget.resize(300,800)


        self.listWidget.move(5,90)
        line='-'*74
        self.listWidget.addItem("            USER    ")
        self.listWidget.addItem("1-Create a user ")
        self.listWidget.addItem("2-Add user to a group ")
        self.listWidget.addItem("3-Remove user ")
        self.listWidget.addItem("4-Create a group ")
        self.listWidget.addItem(line)
        self.listWidget.addItem("            NetWork    ")
        self.listWidget.addItem("1-Show ip informaton ")
        self.listWidget.addItem(line)
        self.listWidget.addItem("            Firewall")
        self.listWidget.addItem("1-Show Default  Zone")
        self.listWidget.addItem(line)
        self.listWidget.addItem("            share")
        self.listWidget.addItem(" 1-Show Default share Subnet ")
        self.listWidget.addItem(line)
        self.listWidget.addItem("            Backup")
        self.listWidget.addItem("1-Show Number Of Backups               ")
        self.listWidget.addItem(line)
        self.listWidget.addItem("            General Preferences")
        self.listWidget.addItem("1-Show name of server  ")
        self.listWidget.addItem("1-Show name of Distrubition ")

        self.listWidget.itemClicked.connect(self.clickingEvent)

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
        self.preferencesconfig=preferences.preferencesConfig()



    def clickingEvent(self):
        try:
         item= self.listWidget.currentItem().text()
         itemNumber=item.split('-')[0]
         itemText=item.split('-')[1]

         print(itemNumber,itemText)
        except IndexError:
            return None

        if itemNumber==1:
            self.infoTitel=QLabel(itemText)
            self.infoTitel.move(400,120)
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

def main():
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec_())

if __name__=='__main__':
    main()
