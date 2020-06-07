from datetime import datetime
import qtmodern.styles
import qtmodern.windows
from PyQt5 import QtGui, QtCore
from PyQt5 import *
from project.networking.globalInfo import globalInfo
from project.networking.configureNet import *
from project.networking.networkingScripts import currentlyActiveConnectionNow,upConnection,downConnection,AutoConnection
from project.networking.netScript import takeIpFromDHCP
from project.networking.displayIP import DisplayIP
from project.networking.globalInfo import globalInfoTwo
from project.networking.networkingplots import NetSentCanvas, NetRecCanvas

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, Qt
import psutil
import platform
import subprocess


def getContentNetwork(self):
    self.gridNetwork = QGridLayout()
    createGrid(self)
    self.netSent = NetSentCanvas(self,interface="All",width=6, height=3.3, dpi=60)
    self.gridNetwork.addWidget(self.netSent, 1, 0)

    ############################### last bad logins pie plot
    self.netRec = NetRecCanvas(self,interface="All",width=6, height=3.3, dpi=60)
    self.gridNetwork.addWidget(self.netRec, 1, 1)

    #################### creating and triggerting update for user's table
    createTableNet(self)
    # updating table still has some issues
    '''
    try:
        self.timerTableUsers = QtCore.QTimer(self)
        self.timerTableUsers.timeout.connect(lambda: updateTableUsers(self))
        self.timerTableUsers.start(10000)
    except Exception:
        pass
    '''

    #################### creating buttons under pie plots
    createUsersButtons(self)

    self.containerUsers=QVBoxLayout()
    self.containerUsers.setContentsMargins(0,20,0,0)
    self.containerUsers.addLayout(self.gridNetwork)
    self.containerUsers.addLayout(self.hboxbtn)
    self.containerUsers.addWidget(self.tableNet)

    self.bottomRightLayout.addLayout(self.containerUsers)

def createGrid(self):
    ############################### last logins pie plot
    self.hboxxx = QHBoxLayout()
    self.listnet = QComboBox(self)
    self.selectBtn = QPushButton("Select")
    self.selectBtn.clicked.connect(lambda :selectclicked(self))
    self.selectBtn.setStyleSheet("color: #95a5a6; background-color: #303a46 ; border: 0px solid #303a46")
    self.listnet.setStyleSheet("color: #95a5a6; background-color: #303a46 ; border: 0px solid #303a46")
    self.listnet.setFixedHeight(25)
    self.listnet.setFixedWidth(110)
    self.selectBtn.setFixedHeight(25)
    self.selectBtn.setFixedWidth(80)

    a = subprocess.run("curl ifconfig.me",shell=True,stdout=subprocess.PIPE)
    mypubaddr = QLabel(f"My Public IP : {a.stdout.decode('utf-8')}")
    mypubaddr.setContentsMargins(10,0,0,0)
    mypubaddr.setStyleSheet("color: #303a46 ; border: 0px solid #303a46")

    self.hboxxx.addWidget(self.listnet)
    self.hboxxx.addWidget(self.selectBtn)
    self.hboxxx.addWidget(mypubaddr)
    self.hboxxx.addStretch()

    out = psutil.net_io_counters(pernic=True)
    self.listnet.addItem("All")
    self.listnet.setCurrentIndex(0)
    for i in out:
        self.listnet.addItem(str(i))

    self.gridNetwork.addLayout(self.hboxxx, 0, 0)
    #################### creating and triggerting update for list logged in usesrs
    createtcpudpsocketsList(self)
    updatetcpudpsocketsList(self)


def selectclicked(self):
    self.setCursor(Qt.WaitCursor)
    current = self.listnet.currentIndex()
    currenttext = self.listnet.currentText()
    clearLayoutt(self,self.gridNetwork)
    createGrid(self)

    self.listnet.setCurrentIndex(current)

    self.netSent = NetSentCanvas(self,interface=currenttext,width=4.5, height=3, dpi=80)
    self.gridNetwork.addWidget(self.netSent, 1, 0)

    self.netRec = NetRecCanvas(self,interface=currenttext,width=4.5, height=3, dpi=80)
    self.gridNetwork.addWidget(self.netRec, 1, 1)
    self.setCursor(Qt.ArrowCursor)


def clearLayoutt(self,layout):
    try:
        del self.netSent
    except Exception:
        pass
    try:
        del self.netRec
    except Exception:
        pass
    while layout.count():
        child = layout.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            self.clearLayout(child.layout())

def updateTableNet(self):
    try:
        self.tableNet.setRowCount(0)
        self.rowposition=0
        showmyuserslist(self)
    except Exception as e:
        return None

def updatetcpudpsocketsList(self):
    try:
        self.listtcpudpsockets.clear()
        o = subprocess.Popen('ss -ta', stderr=subprocess.PIPE, stdout=subprocess.PIPE,shell=True).communicate()[0].decode()
        l = o.split('\n')
        for i in l:
            i.replace("   ", "")
            self.listtcpudpsockets.addItem(i)
    except Exception:
        return None
    QTimer.singleShot(1000, lambda: updatetcpudpsocketsList(self))

def createtcpudpsocketsList(self):
    self.listtcpudpsockets=QListWidget()
    self.listtcpudpsockets.setFixedWidth(390)
    self.listtcpudpsockets.setStyleSheet("color: #2c3e50; selection-background-color: #e74c3c ;background-color: white ; selection-color: #ecf0f1 ;border: 0px solid #95a5a6")
    o = subprocess.Popen('ss -ta', stderr=subprocess.PIPE, stdout=subprocess.PIPE,shell=True).communicate()[0].decode()
    l = o.split('\n')
    for i in l:
        i.replace("     ", "")
        self.listtcpudpsockets.addItem(i)
    tcpudpsocketsText = QLabel('TCP UDP Sockets : ')
    tcpudpsocketsText.setStyleSheet("color: #303a46;font: bold 14px;")
    self.gridNetwork.addWidget(tcpudpsocketsText, 0, 2)
    self.gridNetwork.addWidget(self.listtcpudpsockets, 1, 2)


def createUsersButtons(self):
    self.hboxbtn=QHBoxLayout()
    #self.selectall=QCheckBox('Select All',self)
    self.addBtn=QPushButton('Add')
    self.editBtn=QPushButton('Edit')
    self.deleteBtn=QPushButton('Delete')
    self.addBtn.setFixedHeight(30)
    self.addBtn.setFixedWidth(120)
    self.editBtn.setFixedHeight(30)
    self.editBtn.setFixedWidth(120)
    self.deleteBtn.setFixedHeight(30)
    self.deleteBtn.setFixedWidth(120)
    self.addBtn.clicked.connect(lambda: createUsersWindow(self))
    self.addBtn.setStyleSheet("color: #ecf0f1; background-color: #2ecc71 ; border: 0px solid #2c3e50")
    self.editBtn.clicked.connect(lambda: editUsersWindow(self,self.dic2))
    self.editBtn.setStyleSheet("color: #ecf0f1; background-color: #34495e ; border: 0px solid #2c3e50")
    self.deleteBtn.clicked.connect(lambda: deleteUsersWindow(self,self.dic2))
    self.deleteBtn.setStyleSheet("color: #ecf0f1; background-color: #e74c3c; border: 0px solid #2c3e50")
    self.selectall = SelectAllButton(self.dic2)

    self.hboxbtn.addWidget(self.selectall)
    self.hboxbtn.addStretch()
    self.hboxbtn.addWidget(self.addBtn)
    self.hboxbtn.addWidget(self.editBtn)
    self.hboxbtn.addWidget(self.deleteBtn)


def createTableNet(self):
    self.tableNet=QTableWidget()
    self.tableNet.setRowCount(0)
    self.tableNet.setColumnCount(9)

    self.tableNet.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    self.tableNet.setAutoFillBackground(True)

    header = self.tableNet.horizontalHeader()
    header.setStretchLastSection(True)

    '''
    self.tableUsers.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
    self.tableUsers.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.tableUsers.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.tableUsers.resizeColumnsToContents()
    self.tableUsers.setFixedSize(self.tableUsers.horizontalHeader().length()+self.tableUsers.verticalHeader().width(),self.tableUsers.verticalHeader().length() +self.tableUsers.horizontalHeader().height())
    '''
    self.tableNet.setHorizontalHeaderItem(0, QTableWidgetItem("Connection Name"))
    self.tableNet.setHorizontalHeaderItem(1, QTableWidgetItem("Connection Type"))
    self.tableNet.setHorizontalHeaderItem(2, QTableWidgetItem("IP Informaion"))
    self.tableNet.setHorizontalHeaderItem(3, QTableWidgetItem("IP Assing Method"))
    self.tableNet.setHorizontalHeaderItem(4, QTableWidgetItem("Auto"))
    self.tableNet.setHorizontalHeaderItem(5, QTableWidgetItem("Up-Down"))
    self.tableNet.setHorizontalHeaderItem(6, QTableWidgetItem("DHCP"))
    self.tableNet.setHorizontalHeaderItem(7, QTableWidgetItem("AutoConnect"))
    self.tableNet.setHorizontalHeaderItem(8, QTableWidgetItem("Select"))
    self.tableNet.setEditTriggers(QAbstractItemView.NoEditTriggers)
    #self.tableUsers.doubleClicked.connect(self.doubleClick)
    showmyuserslist(self)

def retrievedatafrompasswdfile():

    list_of_units = globalInfoTwo()
    return list_of_units

############################ NEW CODE  #############################################"""
class SelectCellInTableNet(QWidget):
    def __init__(self, parent=None):
        super(SelectCellInTableNet,self).__init__(parent)
        self.isSelected = False
        self.hbox = QHBoxLayout()
        self.checkb = QCheckBox(self)
        self.checkb.stateChanged.connect(self.checkBoxChangedAction)
        self.hbox.addStretch()
        self.hbox.addWidget(self.checkb)
        self.hbox.addStretch()
        self.hbox.setContentsMargins(0,0,0,0)
        self.hbox.setSpacing(8)
        self.setLayout(self.hbox)
    def checkBoxChangedAction(self, state):
        if (QtCore.Qt.Checked == state):
            self.isSelected = True
        else:
            self.isSelected = False

class SelectAllButton(QWidget):
    def __init__(self,d, parent=None):
        super(SelectAllButton,self).__init__(parent)
        self.dd = d
        self.selectAllIsSelected = False
        self.hbox = QHBoxLayout()
        self.selectall = QCheckBox('Select/Deselect All',self)
        self.selectall.stateChanged.connect(self.selectAllChangedAction)
        self.hbox.addWidget(self.selectall)
        self.hbox.setContentsMargins(0,0,0,0)
        self.hbox.setSpacing(8)
        self.setLayout(self.hbox)

    def selectAllChangedAction(self, state):
        if (QtCore.Qt.Checked == state):
            self.selectallIsSelected = True
            print('TRUE')
            for i in self.dd:
                self.dd[i].isSelected = True
                self.dd[i].checkb.setChecked(True)
        else:
            self.selectallIsSelected = False
            print('FALSE')
            for i in self.dd:
                self.dd[i].isSelected = False
                self.dd[i].checkb.setChecked(False)

####### TABLE  WIDGETS #############################################"

class UpDownCellInTable(QWidget):
    def __init__(self,username,groups, parent=None):
        super(UpDownCellInTable,self).__init__(parent)
        self.groups = groups
        self.username = str(username)
        self.username = self.username.replace(' ', '\\ ')

        self.userIsAdmin = False
        self.hbox = QHBoxLayout()
        self.slider = QSlider(Qt.Horizontal)
        # self.slider.setStyleSheet("color: #2c3e50; selection-background-color: #e74c3c ;background-color: white ; selection-color: #ecf0f1 ;border: 2px solid #95a5a6")
        self.slider.setMaximum(1)
        self.slider.setMinimum(0)
        self.slider.setFixedWidth(40)
        # self.slider.setStyleSheet("color:#2ecc71 ")
        self.slider.setTickInterval(1)  # change ticks interval
        index1=self.username
        index2=currentlyActiveConnectionNow()
        index1=index1.replace(' ','')
        index2=index2.replace(' ','')
        if index1==index2:
            self.userIsAdmin = True
            self.slider.setValue(1)
        else:
            self.userIsAdmin = False
            self.slider.setValue(0)
        self.slider.valueChanged.connect(self.changed)
        self.hbox.addStretch()
        self.hbox.addWidget(self.slider)
        self.hbox.addStretch()
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.hbox.setSpacing(8)
        self.setLayout(self.hbox)

    def changed(self):
        if self.slider.value() == 1:
            self.setAdmin()
        elif self.slider.value() == 0:
            self.setNormalUser()

    def setAdmin(self):
        try:
            upConnection(self.username)
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, 'error', f'error cannot set {self.username}  UP ')
            # self.slider.setValue(0)
        else:
            QMessageBox.information(self, 'success', f'{self.username} turned UP succesfully')
            self.slider.setValue(1)
            self.userIsAdmin = True

    def setNormalUser(self):
        try:

            downConnection(self.username)
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, 'error', f'error cannot set {self.username}  DOWN ')
            # self.slider.setValue(1)
        else:
            QMessageBox.information(self, 'success', f'{self.username} turned DOWN succesfully')
            self.slider.setValue(0)
            self.userIsAdmin = False


class AutoConnectCellInTable(QWidget):
    def __init__(self, username, groups, parent=None):
        super(AutoConnectCellInTable, self).__init__(parent)
        self.groups = groups
        self.username = str(username)
        self.username=self.username.replace(' ','\\ ')
        self.userIsAdmin = False
        self.hbox = QHBoxLayout()
        self.slider = QSlider(Qt.Horizontal)
        # self.slider.setStyleSheet("color: #2c3e50; selection-background-color: #e74c3c ;background-color: white ; selection-color: #ecf0f1 ;border: 2px solid #95a5a6")
        self.slider.setMaximum(1)
        self.slider.setMinimum(0)
        self.slider.setFixedWidth(40)
        # self.slider.setStyleSheet("color:#2ecc71 ")
        self.slider.setTickInterval(1)  # change ticks interval

        if 'yes' in self.groups:
            self.userIsAdmin = True
            self.slider.setValue(1)
        else:
            self.userIsAdmin = False
            self.slider.setValue(0)
        self.slider.valueChanged.connect(self.changed)
        self.hbox.addStretch()
        self.hbox.addWidget(self.slider)
        self.hbox.addStretch()
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.hbox.setSpacing(8)
        self.setLayout(self.hbox)

    def changed(self):
        if self.slider.value() == 1:
            self.setAdmin()
        elif self.slider.value() == 0:
            self.setNormalUser()

    def setAdmin(self):
        try:
            AutoConnection(self.username,True)
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, 'error', f'error cannot set {self.username} Auto Connect ')
            # self.slider.setValue(0)
        else:
            QMessageBox.information(self, 'success', f'Auto Connect Setted succesfully')
            self.slider.setValue(1)
            self.userIsAdmin = True

    def setNormalUser(self):
        try:
            AutoConnection(self.username,False)
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, 'error', f'error cannot set  {self.username} Manual Connect ')
            # self.slider.setValue(1)
        else:
            QMessageBox.information(self, 'success', f'Manual Connect Setted succesfully')
            self.slider.setValue(0)
            self.userIsAdmin = False


class DHCPCellInTable(QWidget):
    def __init__(self, username, groups, parent=None):
        super(DHCPCellInTable, self).__init__(parent)
        self.groups = groups
        self.username = username
        self.username = str(username)
        self.username = self.username.replace(' ', '\\ ')
        self.userIsAdmin = False
        self.hbox = QHBoxLayout()
        self.slider = QSlider(Qt.Horizontal)
        # self.slider.setStyleSheet("color: #2c3e50; selection-background-color: #e74c3c ;background-color: white ; selection-color: #ecf0f1 ;border: 2px solid #95a5a6")
        self.slider.setMaximum(1)
        self.slider.setMinimum(0)
        self.slider.setFixedWidth(40)
        # self.slider.setStyleSheet("color:#2ecc71 ")
        self.slider.setTickInterval(1)  # change ticks interval

        if 'auto' in self.groups:
            self.userIsAdmin = True
            self.slider.setValue(1)
        else:
            self.userIsAdmin = False
            self.slider.setValue(0)
        self.slider.valueChanged.connect(self.changed)
        self.hbox.addStretch()
        self.hbox.addWidget(self.slider)
        self.hbox.addStretch()
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.hbox.setSpacing(8)
        self.setLayout(self.hbox)

    def changed(self):
        if self.slider.value() == 1:
            self.setAdmin()
        elif self.slider.value() == 0:
            self.setNormalUser()

    def setAdmin(self):
        try:
            takeIpFromDHCP(self.username,True)

        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, 'error', 'error cannot enable DHCP  ')
            # self.slider.setValue(0)
        else:
            QMessageBox.information(self, 'success', ' DHCP enabled succesfully')
            self.slider.setValue(1)
            self.userIsAdmin = True

    def setNormalUser(self):
        try:
            takeIpFromDHCP(self.username,False)
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, 'error', f'error cannot Stop Manual Configuration ')
            # self.slider.setValue(1)
        else:
            QMessageBox.information(self, 'success', f' Manual configuration Applied on {self.username}  succesfully')
            self.slider.setValue(0)
            self.userIsAdmin = False


class IPCellInTableNet(QWidget):
    def __init__(self,username, parent=None):
        super(IPCellInTableNet,self).__init__(parent)
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
        index=index.replace(' ','\\ ')
        print(index)
        output=DisplayIP(index)
        QMessageBox.information(self, 'IP', f'IP={output[0]} \n GATWAY={output[1]} \n DNS={output[2]}')


##########################################################################

def showmyuserslist(self):
    self.usersList = retrievedatafrompasswdfile()
    self.dic={}
    self.dic2={}
    self.dic3={}
    self.dic4={}
    self.dic5={}
    self.dic6={}
    self.rowposition = 0
    for i in self.usersList:
        self.rowPosition = self.tableNet.rowCount()
        self.tableNet.insertRow(self.rowPosition)
        try:
            self.tableNet.setItem(self.rowPosition, 0, QTableWidgetItem(i[0]))
        except:
            pass
        try:
            self.tableNet.setItem(self.rowPosition, 1, QTableWidgetItem(i[1]))
        except:
            pass
        try:
            self.dic6[i[0]] = IPCellInTableNet(i[0])
        except:
            pass
        try:
            self.tableNet.setCellWidget(self.rowPosition,2,self.dic6[i[0]])
        except:
            pass
        try:
            self.tableNet.setItem(self.rowPosition, 3, QTableWidgetItem(i[2]))
        except:
            pass
        try:
            self.tableNet.setItem(self.rowPosition, 4, QTableWidgetItem(i[3]))
        except:
            pass
        try:
            self.dic3[i[0]] = UpDownCellInTable(i[0],i[2])
        except:
            pass
        try:
            self.tableNet.setCellWidget(self.rowPosition,5,self.dic3[i[0]])
        except:
            pass
        try:
            self.dic2[i[0]] = SelectCellInTableNet()
        except:
            pass
        try:
            self.tableNet.setCellWidget(self.rowPosition,8,self.dic2[i[0]])
        except:
            pass
        try:
            self.dic4[i[0]] = DHCPCellInTable(i[0],i[2])
        except:
            pass
        try:
            self.tableNet.setCellWidget(self.rowPosition,6,self.dic4[i[0]])
        except:
            pass
        try:
            self.dic5[i[0]] = AutoConnectCellInTable(i[0],i[3])
        except:
            pass
        try:
            self.tableNet.setCellWidget(self.rowPosition,7,self.dic5[i[0]])
        except:
            pass

def createUsersWindow(self):
    self.secondwindow = CreateNetworkWindow()
    self.sw = qtmodern.windows.ModernWindow(self.secondwindow)
    self.sw.show()

def editUsersWindow(self,d):
    list_users_to_edit = []
    for i in d:
        if d[i].isSelected == True:
            list_users_to_edit.append(i)
    if len(list_users_to_edit) == 0 or len(list_users_to_edit) > 1:
        QMessageBox.warning(self, 'warning', 'Please select just one connection')
    else:
        for user in self.usersList :
            if user[0] == list_users_to_edit[0]:
                self.secondwindow = EditNetworkWindow(user)
                self.sw = qtmodern.windows.ModernWindow(self.secondwindow)
                self.sw.show()
            else:
                continue

def deleteUsersWindow(self,d):
    list_users_to_delete = []
    for i in d:
        if d[i].isSelected == True:
            list_users_to_delete.append(i)
    if len(list_users_to_delete) == 0:
        QMessageBox.warning(self, 'warning', 'no selected connection.\nPlease select at least one connection')
    else:
        self.secondwindow = DeleteNetworkWindow(list_users_to_delete)
        self.sw = qtmodern.windows.ModernWindow(self.secondwindow)
        self.sw.show()

