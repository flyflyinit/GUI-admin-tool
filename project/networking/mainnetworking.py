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
from project.users.usersplots import lastLogins,lastBadLogins

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, Qt
import psutil
import platform
import subprocess



def getContentNetwork(self):
    self.gridUsers = QGridLayout()
    ############################### last logins pie plot
    outt = subprocess.Popen('last --time-format short', stderr=subprocess.PIPE, stdout=subprocess.PIPE,shell=True).communicate()[0].decode('utf-8')
    p = outt.split('\n')
    self.lastLoginsText=QLabel(str(p[-2]))
    self.lastLoginsText.setStyleSheet("color:#2c3e50")
    self.lastlogins = lastLogins(self,width=4.5, height=3, dpi=80)
    self.gridUsers.addWidget(self.lastLoginsText, 0, 0)
    self.gridUsers.addWidget(self.lastlogins, 1, 0)

    ############################### last bad logins pie plot
    outtt = subprocess.Popen('lastb --time-format short', stderr=subprocess.PIPE, stdout=subprocess.PIPE,shell=True).communicate()[0].decode('utf-8')
    pp = outtt.split('\n')
    self.lastBadLoginsText=QLabel(str(pp[-1]))
    self.lastBadLoginsText.setStyleSheet("color:#2c3e50")
    self.lastbadlogins = lastBadLogins(self,width=4.5, height=3, dpi=80)
    self.gridUsers.addWidget(self.lastBadLoginsText, 0, 1)
    self.gridUsers.addWidget(self.lastbadlogins, 1, 1)

    #################### creating and triggerting update for list logged in usesrs
    createLoggedInList(self)
    updateLoggedInList(self)

    #################### creating and triggerting update for user's table
    createTableUsers(self)
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

    self.groupBox = QGroupBox()
    self.containerUsers=QVBoxLayout()

    self.containerUsers.addLayout(self.gridUsers)
    self.containerUsers.addLayout(self.hboxbtn)
    self.containerUsers.addWidget(self.tableUsers)
    self.containerUsers.addStretch()

    self.groupBox.setLayout(self.containerUsers)
    self.scroll = QScrollArea()
    self.scroll.setFixedWidth(1150)
    self.scroll.setWidget(self.groupBox)
    #self.scroll.setFixedHeight(1000)
    self.scroll.setAutoFillBackground(True)
    #self.bottomRightLayout.addLayout(self.gridUsers)
    #self.bottomLayout.setCentralWidget(self.scroll)
    self.bottomRightLayout.addWidget(self.scroll)

def updateTableUsers(self):
    try:
        self.tableUsers.setRowCount(0)
        self.rowposition=0
        showmyuserslist(self)
    except Exception as e:
        return None

def updateLoggedInList(self):
    try:
        self.listLoggedOn.clear()
        o = subprocess.Popen('who -uH', stderr=subprocess.PIPE, stdout=subprocess.PIPE,shell=True).communicate()[0].decode()
        l = o.split('\n')
        for i in l:
            self.listLoggedOn.addItem(i)
    except Exception:
        return None
    QTimer.singleShot(10000, lambda: updateLoggedInList(self))

def createLoggedInList(self):
    self.listLoggedOn=QListWidget()
    self.listLoggedOn.setFixedWidth(380)
    self.listLoggedOn.setStyleSheet("color: #2c3e50; selection-background-color: #e74c3c ;background-color: white ; selection-color: #ecf0f1 ;border: 0px solid #95a5a6")
    o = subprocess.Popen('who -uH', stderr=subprocess.PIPE, stdout=subprocess.PIPE,shell=True).communicate()[0].decode()
    l = o.split('\n')
    for i in l:
        self.listLoggedOn.addItem(i)
    usersLoginsText = QLabel('Logged In Users : ')
    usersLoginsText.setStyleSheet("color:#2c3e50")
    self.gridUsers.addWidget(usersLoginsText, 0, 2)
    self.gridUsers.addWidget(self.listLoggedOn, 1, 2)


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


def createTableUsers(self):
    self.tableUsers=QTableWidget()
    self.tableUsers.setRowCount(0)
    self.tableUsers.setColumnCount(9)

    self.tableUsers.setFixedHeight(500)
    self.tableUsers.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    '''
    self.tableUsers.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
    self.tableUsers.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.tableUsers.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.tableUsers.resizeColumnsToContents()
    self.tableUsers.setFixedSize(self.tableUsers.horizontalHeader().length()+self.tableUsers.verticalHeader().width(),self.tableUsers.verticalHeader().length() +self.tableUsers.horizontalHeader().height())
    '''
    self.tableUsers.setHorizontalHeaderItem(0, QTableWidgetItem("Connection Name"))
    self.tableUsers.setHorizontalHeaderItem(1, QTableWidgetItem("Connection Type"))
    self.tableUsers.setHorizontalHeaderItem(2, QTableWidgetItem("IP Informaion"))
    self.tableUsers.setHorizontalHeaderItem(3, QTableWidgetItem("IP Assing Method"))
    self.tableUsers.setHorizontalHeaderItem(4, QTableWidgetItem("Auto Connect "))
    self.tableUsers.setHorizontalHeaderItem(5, QTableWidgetItem("Up-Down Control"))
    self.tableUsers.setHorizontalHeaderItem(6, QTableWidgetItem("DHCP Control"))
    self.tableUsers.setHorizontalHeaderItem(7, QTableWidgetItem("AutoConnect Control"))
    self.tableUsers.setHorizontalHeaderItem(8, QTableWidgetItem("Select"))
    self.tableUsers.setEditTriggers(QAbstractItemView.NoEditTriggers)
    #self.tableUsers.doubleClicked.connect(self.doubleClick)
    showmyuserslist(self)

def retrievedatafrompasswdfile():

    list_of_units = globalInfoTwo()
    return list_of_units

############################ NEW CODE  #############################################"""
class SelectCellInTableUsers(QWidget):
    def __init__(self, parent=None):
        super(SelectCellInTableUsers,self).__init__(parent)
        self.isSelected = False
        self.hbox = QHBoxLayout()
        self.checkb = QCheckBox(self)
        self.checkb.stateChanged.connect(self.checkBoxChangedAction)
        #self.slider.setStyleSheet("color: #2c3e50; selection-background-color: #e74c3c ;background-color: white ; selection-color: #ecf0f1 ;border: 2px solid #95a5a6")
        #self.text.setAlignment(Qt.AlignCenter)  # move to the center
        #self.checkb.stateChanged.connect(self.changed())
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
        #self.slider.setStyleSheet("color: #2c3e50; selection-background-color: #e74c3c ;background-color: white ; selection-color: #ecf0f1 ;border: 2px solid #95a5a6")
        #self.text.setAlignment(Qt.AlignCenter)  # move to the center
        #self.checkb.stateChanged.connect(self.changed())
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
            self.text = QLabel("True")
            self.slider.setValue(1)
        else:
            self.userIsAdmin = False
            self.text = QLabel("False")
            self.slider.setValue(0)
        # self.text.setAlignment(Qt.AlignCenter)  # move to the center
        self.slider.valueChanged.connect(self.changed)
        self.hbox.addStretch()
        self.hbox.addWidget(self.slider)
        self.hbox.addWidget(self.text)
        self.hbox.addStretch()
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.hbox.setSpacing(8)
        self.setLayout(self.hbox)

    def changed(self):
        if self.slider.value() == 1:
            self.mbox = QMessageBox.question(self, "Warningg!", f"Are you sure to make {self.username} UP ?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if self.mbox == QMessageBox.Yes:
                self.setAdmin()
            elif self.mbox == QMessageBox.No:
                pass
            else:
                pass
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
            self.text.setText("True")
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
            self.text.setText("False")
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
            self.text = QLabel("True")
            self.slider.setValue(1)
        else:
            self.userIsAdmin = False
            self.text = QLabel("False")
            self.slider.setValue(0)
        # self.text.setAlignment(Qt.AlignCenter)  # move to the center
        self.slider.valueChanged.connect(self.changed)
        self.hbox.addStretch()
        self.hbox.addWidget(self.slider)
        self.hbox.addWidget(self.text)
        self.hbox.addStretch()
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.hbox.setSpacing(8)
        self.setLayout(self.hbox)

    def changed(self):
        if self.slider.value() == 1:
            self.mbox = QMessageBox.question(self, "Warningg!", f"Are you sure to make {self.username} Auto Connect ?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if self.mbox == QMessageBox.Yes:
                self.setAdmin()
            elif self.mbox == QMessageBox.No:
                pass
            else:
                pass
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
            self.text.setText("True")
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
            self.text.setText("False")
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
            self.text = QLabel("True")
            self.slider.setValue(1)
        else:
            self.userIsAdmin = False
            self.text = QLabel("False")
            self.slider.setValue(0)
        # self.text.setAlignment(Qt.AlignCenter)  # move to the center
        self.slider.valueChanged.connect(self.changed)
        self.hbox.addStretch()
        self.hbox.addWidget(self.slider)
        self.hbox.addWidget(self.text)
        self.hbox.addStretch()
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.hbox.setSpacing(8)
        self.setLayout(self.hbox)

    def changed(self):
        if self.slider.value() == 1:
            self.mbox = QMessageBox.question(self, "Warningg!", f"Are you sure to make {self.username} take IP information From DHCP ?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if self.mbox == QMessageBox.Yes:
                self.setAdmin()
            elif self.mbox == QMessageBox.No:
                pass
            else:
                pass
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
            self.text.setText("True")
            self.slider.setValue(1)
            self.userIsAdmin = True


    def setNormalUser(self):
        try:
            takeIpFromDHCP(self.username,False)
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, 'error', f'error cannot set {self.username}  DOWN ')
            # self.slider.setValue(1)
        else:
            QMessageBox.information(self, 'success', f'{self.username} turned DOWN succesfully')
            self.text.setText("False")
            self.slider.setValue(0)
            self.userIsAdmin = False


class IPCellInTableUsers(QWidget):
    def __init__(self,username, parent=None):
        super(IPCellInTableUsers,self).__init__(parent)
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
        self.rowPosition = self.tableUsers.rowCount()
        self.tableUsers.insertRow(self.rowPosition)
        self.tableUsers.setItem(self.rowPosition, 0, QTableWidgetItem(i[0]))
        self.tableUsers.setItem(self.rowPosition, 1, QTableWidgetItem(i[1]))
        self.tableUsers.setItem(self.rowPosition, 3, QTableWidgetItem(i[2]))
        self.tableUsers.setItem(self.rowPosition, 4, QTableWidgetItem(i[3]))
        self.dic3[i[0]] = UpDownCellInTable(i[0],i[2])
        self.dic2[i[0]] = SelectCellInTableUsers()
        #new
        self.dic4[i[0]] = DHCPCellInTable(i[0],i[2])
        self.dic5[i[0]] = AutoConnectCellInTable(i[0],i[3])
        self.dic6[i[0]] = IPCellInTableUsers(i[0])
        self.tableUsers.setCellWidget(self.rowPosition,5,self.dic3[i[0]])
        self.tableUsers.setCellWidget(self.rowPosition,8,self.dic2[i[0]])
        self.tableUsers.setCellWidget(self.rowPosition,6,self.dic4[i[0]])
        self.tableUsers.setCellWidget(self.rowPosition,7,self.dic5[i[0]])
        self.tableUsers.setCellWidget(self.rowPosition,2,self.dic6[i[0]])


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
        QMessageBox.warning(self, 'warning', 'Please select just one user')
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
        QMessageBox.warning(self, 'warning', 'no selected users.\nPlease select at least one user')
    else:
        self.secondwindow = DeleteNetworkWindow(list_users_to_delete)
        self.sw = qtmodern.windows.ModernWindow(self.secondwindow)
        self.sw.show()

