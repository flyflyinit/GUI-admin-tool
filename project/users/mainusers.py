try:
    from PyQt5 import QtCore
    from PyQt5.QtCore import QTimer, Qt
    from PyQt5.QtWidgets import QGridLayout, QLabel, QGroupBox, QVBoxLayout, QScrollArea, QListWidget, QHBoxLayout, \
        QPushButton, QTableWidget, QSizePolicy, QTableWidgetItem, QAbstractItemView, QWidget, QCheckBox, QSlider, \
        QMessageBox
except ImportError as e:
    print(f'package PyQt5 Not Found\n{e}\ntry :\npip3 install --user pyqt5\nOR\ndnf install python3-pyqt5, yum install python3-pyqt5\n')

try:
    import qtmodern.styles
    import qtmodern.windows
except ImportError as e:
    print(f'package qtmodern Not Found\n{e}\ntry :\npip3 install --user qtmodern\n')

try:
    import subprocess
    from users.configureusers import CreateUsersWindow, EditUsersWindow, DeleteUsersWindow, MoreUsersWindow
    from users.usersplots import lastLogins, lastBadLogins
except ImportError as e:
    print(f'package not found\n{e}\n')


def getContentUsers(self):
    self.gridUsers = QGridLayout()
    ############################### last logins pie plot
    outt = subprocess.Popen('last --time-format short', stderr=subprocess.PIPE, stdout=subprocess.PIPE,shell=True).communicate()[0].decode('utf-8')
    p = outt.split('\n')
    self.lastLoginsText=QLabel(str(p[-2]))
    self.lastLoginsText.setStyleSheet("color:#2c3e50")
    self.lastlogins = lastLogins(self,width=6, height=3.3, dpi=60)
    self.gridUsers.addWidget(self.lastLoginsText, 0, 0)
    self.gridUsers.addWidget(self.lastlogins, 1, 0)

    ############################### last bad logins pie plot
    outtt = subprocess.Popen('lastb --time-format short', stderr=subprocess.PIPE, stdout=subprocess.PIPE,shell=True).communicate()[0].decode('utf-8')
    pp = outtt.split('\n')
    self.lastBadLoginsText=QLabel(str(pp[-2]))
    self.lastBadLoginsText.setStyleSheet("color:#2c3e50")
    self.lastbadlogins = lastBadLogins(self,width=6, height=3.3, dpi=60)
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
    self.containerUsers=QVBoxLayout()
    self.containerUsers.setContentsMargins(0,20,0,0)
    self.containerUsers.addLayout(self.gridUsers)
    self.containerUsers.addLayout(self.hboxbtn)
    self.containerUsers.addWidget(self.tableUsers)

    self.bottomRightLayout.addLayout(self.containerUsers)

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
    self.tableUsers.setColumnCount(12)

    self.tableUsers.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    self.tableUsers.setAutoFillBackground(True)

    header = self.tableUsers.horizontalHeader()
    header.setStretchLastSection(True)

    '''
    self.tableUsers.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
    self.tableUsers.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.tableUsers.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.tableUsers.resizeColumnsToContents()
    self.tableUsers.setFixedSize(self.tableUsers.horizontalHeader().length()+self.tableUsers.verticalHeader().width(),self.tableUsers.verticalHeader().length() +self.tableUsers.horizontalHeader().height())
    '''
    self.tableUsers.setHorizontalHeaderItem(0, QTableWidgetItem("User Name"))
    self.tableUsers.setHorizontalHeaderItem(1, QTableWidgetItem("User ID"))
    self.tableUsers.setHorizontalHeaderItem(2, QTableWidgetItem("Primary Group"))
    self.tableUsers.setHorizontalHeaderItem(3, QTableWidgetItem("Groups"))
    self.tableUsers.setHorizontalHeaderItem(4, QTableWidgetItem("Comment"))
    self.tableUsers.setHorizontalHeaderItem(5, QTableWidgetItem("Home Directory"))
    self.tableUsers.setHorizontalHeaderItem(6, QTableWidgetItem("Shell"))
    self.tableUsers.setHorizontalHeaderItem(7, QTableWidgetItem("Administrator"))
    self.tableUsers.setHorizontalHeaderItem(8, QTableWidgetItem("Lock"))
    self.tableUsers.setHorizontalHeaderItem(9, QTableWidgetItem("Account Expiration"))
    self.tableUsers.setHorizontalHeaderItem(10, QTableWidgetItem("More"))
    self.tableUsers.setHorizontalHeaderItem(11, QTableWidgetItem("Select"))
    self.tableUsers.setEditTriggers(QAbstractItemView.NoEditTriggers)
    showmyuserslist(self)


def retrievedatafrompasswdfile():
    list_of_users = []
    with open("/etc/passwd", mode='r') as passwd_content:
        each_line = passwd_content.readlines()
        passwd_content.close()

    for each_user in each_line:
        each_user2 = each_user.split(":")
        list_of_users.append(each_user2)

    list_of_users_adapted = []
    for i in list_of_users:
        if int(i[2]) >= 1000:
            A = i[6]
            c = f"id {i[0]} | awk "+"{'print $2'}"
            b = subprocess.Popen(c,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()[0].decode('utf-8').split('=',1)[1]
            c2 = f"id {i[0]} | awk "+"{'print $3'}"
            b2 = subprocess.Popen(c2,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()[0].decode('utf-8').split('=',1)[1]
            c3 = f"chage -l {i[0]} | grep 'Account' "
            b3 = subprocess.Popen(c3, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].decode('utf-8').split(":",1)[1].strip(" ")
            list_of_users_adapted.append([i[0],i[2],b[:-1:],b2[:-1:],i[4],i[5],A[:-1:],b3[:-1:]])
    return list_of_users_adapted


class SelectCellInTableUsers(QWidget):
    def __init__(self, parent=None):
        super(SelectCellInTableUsers,self).__init__(parent)
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

class AdministratorCellInTableUsers(QWidget):
    def __init__(self,username,groups, parent=None):
        super(AdministratorCellInTableUsers,self).__init__(parent)
        self.groups = groups
        self.username = username
        self.userIsAdmin = False
        self.hbox = QHBoxLayout()
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMaximum(1)
        self.slider.setMinimum(0)
        self.slider.setFixedWidth(40)
        self.slider.setTickInterval(1)  # change ticks interval
        if '(wheel)' in self.groups:
            self.userIsAdmin = True
            self.slider.setValue(1)
        else:
            self.userIsAdmin = False
            self.slider.setValue(0)
        self.slider.valueChanged.connect(self.changed)
        self.hbox.addStretch()
        self.hbox.addWidget(self.slider)
        self.hbox.addStretch()
        self.hbox.setContentsMargins(0,0,0,0)
        self.hbox.setSpacing(8)
        self.setLayout(self.hbox)

    def changed(self):
        if self.slider.value() == 1:
            self.setAdmin()
        elif self.slider.value() == 0:
            self.setNormalUser()

    def setAdmin(self):
        try:
            subprocess.run(f'usermod -aG wheel {self.username}',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,shell=True,check=True)
        except subprocess.CalledProcessError as e :
            QMessageBox.critical(self,'error',f'error occured during setting this username {self.username} an adminstrator')
            self.slider.setValue(0)
        else:
            QMessageBox.information(self,'success',f'{self.username} has been setted an administrator succesfully')
            self.slider.setValue(1)
            self.userIsAdmin = True

    def setNormalUser(self):
        try:
            subprocess.run(f'gpasswd -d {self.username} wheel',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,shell=True,check=True)
        except subprocess.CalledProcessError as e :
            QMessageBox.critical(self,'error',f'error occured during setting this username {self.username} a normal user')
            self.slider.setValue(1)
        else:
            QMessageBox.information(self,'success',f'{self.username} has been setted a normal user succesfully')
            self.slider.setValue(0)
            self.userIsAdmin = False

class LockCellInTableUsers(QWidget):
    def __init__(self,username, parent=None):
        super(LockCellInTableUsers,self).__init__(parent)
        self.username = username
        self.userIsLocked = False
        self.doesntHavePassword = False
        self.hbox = QHBoxLayout()
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMaximum(1)
        self.slider.setMinimum(0)
        self.slider.setFixedWidth(40)
        self.slider.setTickInterval(1)  # change ticks interval

        c = f"cat /etc/shadow | grep {self.username}:"
        b = subprocess.Popen(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].decode('utf-8').split(':', 1)[1]
        if '!' == b[1]:
            self.doesntHavePassword = True

        if '!' == b[0]:
            self.userIsLocked = True
            self.slider.setValue(1)
        else:
            self.userIsLocked = False
            self.slider.setValue(0)
        self.slider.valueChanged.connect(self.changed)
        self.hbox.addStretch()
        self.hbox.addWidget(self.slider)
        self.hbox.addStretch()
        self.hbox.setContentsMargins(0,0,0,0)
        self.hbox.setSpacing(8)
        self.setLayout(self.hbox)

    def changed(self):
        if self.slider.value() == 1:
            if self.doesntHavePassword == True :
                QMessageBox.warning(self, 'error', "you can't unlock a user doesn't have a password")
                #self.slider.setValue(1)
            else:
                self.setLocked()
        elif self.slider.value() == 0:
            self.setUnlocked()

    def setLocked(self):
        try:
            subprocess.run(f'usermod -L {self.username}',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,shell=True,check=True)
        except subprocess.CalledProcessError as e :
            QMessageBox.critical(self,'error',f'error occured during locking this user {self.username}')
            self.slider.setValue(0)
        else:
            QMessageBox.information(self,'success',f'{self.username} has been locked succesfully')
            self.slider.setValue(1)
            self.userIsLocked = True

    def setUnlocked(self):
        try:
            subprocess.run(f'usermod -U {self.username}',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,shell=True,check=True)
        except subprocess.CalledProcessError as e :
            QMessageBox.critical(self,'error',f'error occured during unlocking this user {self.username}')
            self.slider.setValue(1)
        else:
            QMessageBox.information(self,'success',f'{self.username} has been unlocked succesfully')
            self.slider.setValue(0)
            self.userIsLocked = False

class moreCellInTableUsers(QWidget):
    def __init__(self,username, parent=None):
        super(moreCellInTableUsers,self).__init__(parent)
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
        try:
            c = f"chage -l {self.username} "
            b = subprocess.Popen(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].decode('utf-8')
        except subprocess.CalledProcessError as e :
            QMessageBox.critical(self,'error',f'error occured\n{e}')
        else:
            self.secondwindow = MoreUsersWindow(b,self.username)
            self.sw = qtmodern.windows.ModernWindow(self.secondwindow)
            self.sw.show()

def showmyuserslist(self):
    self.usersList = retrievedatafrompasswdfile()
    self.dic={}
    self.dic2={}
    self.dic3={}
    self.dic4={}
    self.rowposition = 0
    for i in self.usersList:
        self.rowPosition = self.tableUsers.rowCount()
        self.tableUsers.insertRow(self.rowPosition)
        self.tableUsers.setItem(self.rowPosition, 0, QTableWidgetItem(i[0]))
        self.tableUsers.setItem(self.rowPosition, 1, QTableWidgetItem(i[1]))
        self.tableUsers.setItem(self.rowPosition, 2, QTableWidgetItem(i[2]))
        self.tableUsers.setItem(self.rowPosition, 3, QTableWidgetItem(i[3]))
        self.tableUsers.setItem(self.rowPosition, 4, QTableWidgetItem(i[4]))
        self.tableUsers.setItem(self.rowPosition, 5, QTableWidgetItem(i[5]))
        self.tableUsers.setItem(self.rowPosition, 6, QTableWidgetItem(i[6]))
        self.dic[i[0]] = AdministratorCellInTableUsers(i[0],i[3])
        self.dic4[i[0]] = LockCellInTableUsers(i[0])
        self.dic2[i[0]] = SelectCellInTableUsers()
        self.dic3[i[0]] = moreCellInTableUsers(i[0])
        self.tableUsers.setCellWidget(self.rowPosition,7,self.dic[i[0]])
        self.tableUsers.setCellWidget(self.rowPosition,8,self.dic4[i[0]])
        self.tableUsers.setItem(self.rowPosition, 9, QTableWidgetItem(i[7]))
        self.tableUsers.setCellWidget(self.rowPosition,10,self.dic3[i[0]])
        self.tableUsers.setCellWidget(self.rowPosition,11,self.dic2[i[0]])

def createUsersWindow(self):
    self.secondwindow = CreateUsersWindow()
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
                self.secondwindow = EditUsersWindow(user)
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
        self.secondwindow = DeleteUsersWindow(list_users_to_delete)
        self.sw = qtmodern.windows.ModernWindow(self.secondwindow)
        self.sw.show()
