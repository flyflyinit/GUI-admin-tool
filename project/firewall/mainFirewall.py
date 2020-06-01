import qtmodern.styles
import qtmodern.windows
from project.firewall.configFirewall import CreateFwWindow,EditFwWindow,DeleteFwWindow
from project.firewall.firewallScripts import firewallGlobalInfo,setDefaultZone,defaultZone
from project.firewall.tableFirewall import *

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import subprocess

from project.firewall.tableFirewall import listservices, listZoneModified, listports


def getContentFirewall(self):
    self.gridFw = QGridLayout()
    #################### creating and triggerting update for user's table
    createTableFw(self)
    #################### creating buttons under pie plots
    createFwButtons(self)

    self.groupBox = QGroupBox()
    #self.groupBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    #self.groupBox.setAutoFillBackground(True)
    #self.groupBox.setFixedWidth(1150)

    self.containerFw=QVBoxLayout()

    self.containerFw.addLayout(self.gridFw)
    self.containerFw.addLayout(self.hboxbtn)
    self.containerFw.addWidget(self.tableFw)
    self.containerFw.addStretch()

    self.groupBox.setLayout(self.containerFw)
    self.scroll = QScrollArea()
    self.scroll.setFixedWidth(1150)
    #self.scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    self.scroll.setWidget(self.groupBox)
    #self.scroll.setFixedHeight(1000)
    #self.scroll.setAutoFillBackground(True)
    #self.bottomRightLayout.addLayout(self.gridUsers)
    #self.bottomLayout.setCentralWidget(self.scroll)
    self.bottomRightLayout.addWidget(self.scroll)

def createFwButtons(self):
    self.hboxbtn=QHBoxLayout()
    self.addBtn=QPushButton('Add')
    self.editBtn=QPushButton('Edit')
    self.deleteBtn=QPushButton('Delete')
    self.addBtn.setFixedHeight(30)
    self.addBtn.setFixedWidth(120)
    self.editBtn.setFixedHeight(30)
    self.editBtn.setFixedWidth(120)
    self.deleteBtn.setFixedHeight(30)
    self.deleteBtn.setFixedWidth(120)
    self.addBtn.clicked.connect(lambda: createFwWindow(self))
    self.addBtn.setStyleSheet("color: #ecf0f1; background-color: #2ecc71 ; border: 0px solid #2c3e50")
    self.editBtn.clicked.connect(lambda: editFwWindow(self))
    self.editBtn.setStyleSheet("color: #ecf0f1; background-color: #34495e ; border: 0px solid #2c3e50")
    self.deleteBtn.clicked.connect(lambda: deleteFwWindow(self))
    self.deleteBtn.setStyleSheet("color: #ecf0f1; background-color: #e74c3c; border: 0px solid #2c3e50")
    self.hboxbtn.addStretch()
    self.hboxbtn.addWidget(self.addBtn)
    self.hboxbtn.addWidget(self.editBtn)
    self.hboxbtn.addWidget(self.deleteBtn)


def createTableFw(self):
    self.tableFw=QTableWidget()
    self.tableFw.setRowCount(0)
    self.tableFw.setColumnCount(4)

    self.tableFw.setFixedHeight(570)
    self.tableFw.setFixedWidth(1130)

    self.tableFw.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    self.tableFw.setHorizontalHeaderItem(0, QTableWidgetItem("zone"))
    self.tableFw.setHorizontalHeaderItem(1, QTableWidgetItem("Services"))
    self.tableFw.setHorizontalHeaderItem(2, QTableWidgetItem("Ports"))
    self.tableFw.setHorizontalHeaderItem(3, QTableWidgetItem("set-Default"))

    self.tableFw.setEditTriggers(QAbstractItemView.NoEditTriggers)
    showmyfwlist(self)



class SetDefaultZone(QWidget):
    def __init__(self,zone, parent=None):
        super(SetDefaultZone,self).__init__(parent)
        self.zone = zone
        self.hbox = QHBoxLayout()
        self.showmoreBtn=QPushButton('Set')
        self.showmoreBtn.clicked.connect(self.showmoreBtnClicked)
        self.hbox.addWidget(self.showmoreBtn)
        self.hbox.addStretch()
        self.hbox.setContentsMargins(0,0,0,0)
        self.hbox.setSpacing(8)
        self.setLayout(self.hbox)

    def showmoreBtnClicked(self):
        index=str(self.zone)

        try:
            setDefaultZone(index)
        except:
            QMessageBox.critical(self, 'warrning', f'\n can set  {index} the default zone ')
        else:
            QMessageBox.information(self, 'Services', f'\n {index} has been setted the default zone ')


class ServiceTableFw(QWidget):
    def __init__(self,username, parent=None):
        super(ServiceTableFw,self).__init__(parent)
        self.username = username
        self.hbox = QHBoxLayout()
        self.showmoreBtn=QPushButton('more')
        self.showmoreBtn.clicked.connect(self.showmoreBtnClicked)
        self.hbox.addWidget(self.showmoreBtn)
        self.hbox.addStretch()
        self.hbox.setContentsMargins(0,0,0,0)
        self.hbox.setSpacing(8)
        self.setLayout(self.hbox)

    def showmoreBtnClicked(self):
        index=str(self.username)
        output=listservices(index)
        outputString=''
        for i in output:
            outputString+=f'{i} '
        QMessageBox.information(self, 'Services', f'\n Services enabled in {index} Zone are:\n {outputString}')

class PortsTableFw(QWidget):
    def __init__(self,username, parent=None):
        super(PortsTableFw,self).__init__(parent)
        self.username = username
        self.hbox = QHBoxLayout()
        self.showmoreBtn=QPushButton('more')
        self.showmoreBtn.clicked.connect(self.showmoreBtnClicked)
        self.hbox.addWidget(self.showmoreBtn)
        self.hbox.addStretch()
        self.hbox.setContentsMargins(0,0,0,0)
        self.hbox.setSpacing(8)
        self.setLayout(self.hbox)

    def showmoreBtnClicked(self):
        index=str(self.username)
        output = listports(index)
        outputString = ''
        for i in output:
            outputString+= f'{i} '
        QMessageBox.information(self, 'Ports', f'\n Ports added  in {index} Zone are:\n {outputString}')


def showmyfwlist(self):
    list_of_fw=listZoneModified()
    self.dic={}
    self.dic1={}
    self.dic2={}
    self.rowposition = 0

    for i in list_of_fw:
        self.rowPosition = self.tableFw.rowCount()
        self.tableFw.insertRow(self.rowPosition)
        self.tableFw.setItem(self.rowPosition, 0, QTableWidgetItem(i[0]))
        self.dic[i[0]] = SetDefaultZone(i[0])
        self.dic1[i[0]] = ServiceTableFw(i[0])
        self.dic2[i[0]] = PortsTableFw(i[0])
        self.tableFw.setCellWidget(self.rowPosition, 3, self.dic[i[0]])
        self.tableFw.setCellWidget(self.rowPosition, 1, self.dic1[i[0]])
        self.tableFw.setCellWidget(self.rowPosition, 2, self.dic2[i[0]])


def createFwWindow(self):
    self.secondwindow = CreateFwWindow()
    self.sw = qtmodern.windows.ModernWindow(self.secondwindow)
    self.sw.show()

def editFwWindow(self):
    self.secondwindow = EditFwWindow()
    self.sw = qtmodern.windows.ModernWindow(self.secondwindow)
    self.sw.show()

def deleteFwWindow(self):
    self.secondwindow = DeleteFwWindow()
    self.sw = qtmodern.windows.ModernWindow(self.secondwindow)
    self.sw.show()
