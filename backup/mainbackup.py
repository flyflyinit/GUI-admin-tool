import qtmodern.styles
import qtmodern.windows
from PyQt5 import QtCore

from backup.configurebackup import CreateFullBackupWindow,DeleteFullBackupWindow,DeleteIncBackupWindow,MoreFullBackupWindow,RestoreFullBackupWindow,MoreIncBackupWindow,CreateIncBackupWindow,RestoreIncBackupWindow

from PyQt5.QtWidgets import *
import sqlite3



def getContentBackup(self):
    global con
    global cur
    con = sqlite3.connect('backup/backupshistory.db')
    cur = con.cursor()

    self.gridBackup = QGridLayout()
    self.gridBackup.setColumnMinimumWidth(1100,1100)
    self.titlefullbackup=QLabel('Full Backups :  ')
    self.titleincbackup=QLabel('Incremental Backups :  ')

    #################### creating and triggerting update for user's table
    createTableFullBackup(self)
    createTableIncBackup(self)
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
    createFullBackupButtons(self)
    createIncBackupButtons(self)

    self.groupBox = QGroupBox()
    self.containerBackup=QVBoxLayout()

    self.containerBackup.addLayout(self.gridBackup)
    self.containerBackup.addLayout(self.hboxfullbackupbtn)
    self.containerBackup.addWidget(self.tableFullBackup)
    self.containerBackup.addLayout(self.hboxincbackupbtn)
    self.containerBackup.addWidget(self.tableIncBackup)
    self.containerBackup.addStretch()

    self.groupBox.setLayout(self.containerBackup)
    self.scroll = QScrollArea()
    self.scroll.setFixedWidth(1150)
    self.scroll.setWidget(self.groupBox)
    #self.scroll.setFixedHeight(1000)
    self.scroll.setAutoFillBackground(True)
    #self.bottomRightLayout.addLayout(self.gridUsers)
    #self.bottomLayout.setCentralWidget(self.scroll)
    self.bottomRightLayout.addWidget(self.scroll)



def createTableFullBackup(self):
    self.tableFullBackup=QTableWidget()
    self.tableFullBackup.setRowCount(0)
    self.tableFullBackup.setColumnCount(8)

    self.tableFullBackup.setFixedHeight(250)
    self.tableFullBackup.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    '''
    self.tableUsers.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
    self.tableUsers.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.tableUsers.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.tableUsers.resizeColumnsToContents()
    self.tableUsers.setFixedSize(self.tableUsers.horizontalHeader().length()+self.tableUsers.verticalHeader().width(),self.tableUsers.verticalHeader().length() +self.tableUsers.horizontalHeader().height())
    '''
    self.tableFullBackup.setHorizontalHeaderItem(0, QTableWidgetItem("Backup ID"))
    self.tableFullBackup.setHorizontalHeaderItem(1, QTableWidgetItem("Backup Date"))
    self.tableFullBackup.setHorizontalHeaderItem(2, QTableWidgetItem("Backup Name"))
    self.tableFullBackup.setHorizontalHeaderItem(3, QTableWidgetItem("Source Path"))
    self.tableFullBackup.setHorizontalHeaderItem(4, QTableWidgetItem("Destination Path"))
    self.tableFullBackup.setHorizontalHeaderItem(5, QTableWidgetItem("Excluded Items"))
    self.tableFullBackup.setHorizontalHeaderItem(6, QTableWidgetItem("More"))
    self.tableFullBackup.setHorizontalHeaderItem(7, QTableWidgetItem("Select"))
    self.tableFullBackup.setEditTriggers(QAbstractItemView.NoEditTriggers)
    #self.tableUsers.doubleClicked.connect(self.doubleClick)
    showmyfullbackuplist(self)


def updateTableFullBackup(self):
    try:
        self.tableFullBackup.setRowCount(0)
        self.rowposition=0
        showmyfullbackuplist(self)
    except Exception as e:
        return None


def createFullBackupButtons(self):
    self.hboxfullbackupbtn=QHBoxLayout()
    #self.selectall=QCheckBox('Select All',self)
    self.addFullBackupBtn=QPushButton('Add')
    self.restoreFullBackupBtn=QPushButton('Restore')
    self.deleteFullBackupBtn=QPushButton('Delete')
    self.addFullBackupBtn.setFixedHeight(30)
    self.addFullBackupBtn.setFixedWidth(120)
    self.restoreFullBackupBtn.setFixedHeight(30)
    self.restoreFullBackupBtn.setFixedWidth(120)
    self.deleteFullBackupBtn.setFixedHeight(30)
    self.deleteFullBackupBtn.setFixedWidth(120)
    self.addFullBackupBtn.clicked.connect(lambda: createFullBackupWindow(self))
    self.addFullBackupBtn.setStyleSheet("color: #ecf0f1; background-color: #2ecc71 ; border: 0px solid #2c3e50")
    self.restoreFullBackupBtn.clicked.connect(lambda: restoreFullBackupWindow(self,self.fullbackupdic))
    self.restoreFullBackupBtn.setStyleSheet("color: #ecf0f1; background-color: #34495e ; border: 0px solid #2c3e50")
    self.deleteFullBackupBtn.clicked.connect(lambda: deleteFullBackupWindow(self,self.fullbackupdic))
    self.deleteFullBackupBtn.setStyleSheet("color: #ecf0f1; background-color: #e74c3c; border: 0px solid #2c3e50")
    self.selectall = SelectAllFullBackupButton(self.fullbackupdic)
    self.hboxfullbackupbtn.addWidget(self.titlefullbackup)
    self.hboxfullbackupbtn.addWidget(self.selectall)
    self.hboxfullbackupbtn.addStretch()
    self.hboxfullbackupbtn.addWidget(self.restoreFullBackupBtn)
    self.hboxfullbackupbtn.addWidget(self.addFullBackupBtn)
    self.hboxfullbackupbtn.addWidget(self.deleteFullBackupBtn)


class SelectCellInTableFullBackup(QWidget):
    def __init__(self, parent=None):
        super(SelectCellInTableFullBackup,self).__init__(parent)
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


class SelectAllFullBackupButton(QWidget):
    def __init__(self,d, parent=None):
        super(SelectAllFullBackupButton,self).__init__(parent)
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
            for i in self.dd:
                self.dd[i].isSelected = True
                self.dd[i].checkb.setChecked(True)
        else:
            self.selectallIsSelected = False
            for i in self.dd:
                self.dd[i].isSelected = False
                self.dd[i].checkb.setChecked(False)


class moreCellInTableFullBackup(QWidget):
    def __init__(self,id, parent=None):
        super(moreCellInTableFullBackup,self).__init__(parent)
        self.id = id
        self.hbox = QHBoxLayout()
        #self.slider.setStyleSheet("color: #2c3e50; selection-background-color: #e74c3c ;background-color: white ; selection-color: #ecf0f1 ;border: 2px solid #95a5a6")
        self.showmoreBtn=QPushButton('more')
        self.showmoreBtn.clicked.connect(self.showmoreBtnClicked)
        self.hbox.addWidget(self.showmoreBtn)
        self.hbox.addStretch()
        self.hbox.setContentsMargins(0,0,0,0)
        self.hbox.setSpacing(8)
        self.setLayout(self.hbox)

    def showmoreBtnClicked(self):
        self.secondwindow = MoreFullBackupWindow(self.id)
        self.sw = qtmodern.windows.ModernWindow(self.secondwindow)
        self.sw.show()


def showmyfullbackuplist(self):
    self.fullBackupList = retrievedatafromdbfullbackup()
    self.fullbackupdic={}
    self.fullbackupdic2={}
    self.rowposition = 0
    for i in self.fullBackupList:
        self.rowPosition = self.tableFullBackup.rowCount()
        self.tableFullBackup.insertRow(self.rowPosition)
        self.tableFullBackup.setItem(self.rowPosition, 0, QTableWidgetItem(i[0]))
        self.tableFullBackup.setItem(self.rowPosition, 1, QTableWidgetItem(i[1]))
        self.tableFullBackup.setItem(self.rowPosition, 2, QTableWidgetItem(i[2]))
        self.tableFullBackup.setItem(self.rowPosition, 3, QTableWidgetItem(i[3]))
        self.tableFullBackup.setItem(self.rowPosition, 4, QTableWidgetItem(i[4]))
        self.tableFullBackup.setItem(self.rowPosition, 5, QTableWidgetItem(i[5]))
        self.fullbackupdic[i[0]] = SelectCellInTableFullBackup()
        self.fullbackupdic2[i[0]] = moreCellInTableFullBackup(i[0])
        self.tableFullBackup.setCellWidget(self.rowPosition,6,self.fullbackupdic2[i[0]])
        self.tableFullBackup.setCellWidget(self.rowPosition,7,self.fullbackupdic[i[0]])


def retrievedatafromdbfullbackup():
    global cur
    listfullbackups = []
    query = "SELECT * FROM FullBackups"
    fullbackups = cur.execute(query).fetchall()
    for fullbackup in fullbackups:
        listfullbackups.append([str(fullbackup[0]),str(fullbackup[1]),str(fullbackup[2]),str(fullbackup[3]),str(fullbackup[4]),str(fullbackup[5])])
    return listfullbackups


def createFullBackupWindow(self):
    self.secondwindow = CreateFullBackupWindow()
    self.sw = qtmodern.windows.ModernWindow(self.secondwindow)
    self.sw.show()


def restoreFullBackupWindow(self,d):
    list_fullbackup_to_restore = []
    for i in d:
        if d[i].isSelected == True:
            list_fullbackup_to_restore.append(i)
    if len(list_fullbackup_to_restore) == 0 or len(list_fullbackup_to_restore) > 1:
        QMessageBox.warning(self, 'warning', 'Please select just one full backup')
    else:
        self.secondwindow = RestoreFullBackupWindow(list_fullbackup_to_restore[0])
        self.sw = qtmodern.windows.ModernWindow(self.secondwindow)
        self.sw.show()


def deleteFullBackupWindow(self,d):
    list_fullbackups_to_delete = []
    for i in d:
        if d[i].isSelected == True:
            list_fullbackups_to_delete.append(i)
    if len(list_fullbackups_to_delete) == 0:
        QMessageBox.warning(self, 'warning', 'no selected full backups.\nPlease select at least one full backup')
    else:
        self.secondwindow = DeleteFullBackupWindow(list_fullbackups_to_delete)
        self.sw = qtmodern.windows.ModernWindow(self.secondwindow)
        self.sw.show()


###################################################################


def createTableIncBackup(self):
    self.tableIncBackup=QTreeWidget()
    labels = ['Meta Name','Backup ID','Backup Level','Backup Date','Backup Name','Backup Path','Destination Path','Excluded Items','More','Select']
    self.tableIncBackup.setHeaderLabels(labels)
    self.tableIncBackup.setFixedHeight(250)

    self.tableIncBackup.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    '''
    self.tableIncBackup.setHorizontalHeaderItem(0, QTreeWidgetItem("Backup ID"))
    self.tableIncBackup.setHorizontalHeaderItem(1, QTreeWidgetItem("Backup Date"))
    self.tableIncBackup.setHorizontalHeaderItem(2, QTreeWidgetItem("Backup Name"))
    self.tableIncBackup.setHorizontalHeaderItem(3, QTreeWidgetItem("Source Path"))
    self.tableIncBackup.setHorizontalHeaderItem(4, QTreeWidgetItem("Destination Path"))
    self.tableIncBackup.setHorizontalHeaderItem(5, QTreeWidgetItem("Excluded Items"))
    self.tableIncBackup.setHorizontalHeaderItem(6, QTreeWidgetItem("More"))
    self.tableIncBackup.setHorizontalHeaderItem(7, QTreeWidgetItem("Select"))
    '''
    self.tableIncBackup.setEditTriggers(QAbstractItemView.NoEditTriggers)
    #self.tableUsers.doubleClicked.connect(self.doubleClick)
    showmyincbackuplist(self)


def createIncBackupButtons(self):
    self.hboxincbackupbtn=QHBoxLayout()
    #self.selectall=QCheckBox('Select All',self)
    self.addIncBackupBtn=QPushButton('Add')
    self.restoreIncBackupBtn=QPushButton('Restore')
    self.deleteIncBackupBtn=QPushButton('Delete')
    self.addIncBackupBtn.setFixedHeight(30)
    self.addIncBackupBtn.setFixedWidth(120)
    self.restoreIncBackupBtn.setFixedHeight(30)
    self.restoreIncBackupBtn.setFixedWidth(120)
    self.deleteIncBackupBtn.setFixedHeight(30)
    self.deleteIncBackupBtn.setFixedWidth(120)
    self.addIncBackupBtn.clicked.connect(lambda: createIncBackupWindow(self))
    self.addIncBackupBtn.setStyleSheet("color: #ecf0f1; background-color: #2ecc71 ; border: 0px solid #2c3e50")
    self.restoreIncBackupBtn.clicked.connect(lambda: restoreIncBackupWindow(self))
    self.restoreIncBackupBtn.setStyleSheet("color: #ecf0f1; background-color: #34495e ; border: 0px solid #2c3e50")
    self.deleteIncBackupBtn.clicked.connect(lambda: deleteIncBackupWindow(self,self.incbackupdic))
    self.deleteIncBackupBtn.setStyleSheet("color: #ecf0f1; background-color: #e74c3c; border: 0px solid #2c3e50")
    self.selectallinc = SelectAllIncBackupButton(self.incbackupdic)
    self.hboxincbackupbtn.addWidget(self.titleincbackup)
    self.hboxincbackupbtn.addWidget(self.selectallinc)
    self.hboxincbackupbtn.addStretch()
    self.hboxincbackupbtn.addWidget(self.restoreIncBackupBtn)
    self.hboxincbackupbtn.addWidget(self.addIncBackupBtn)
    self.hboxincbackupbtn.addWidget(self.deleteIncBackupBtn)



class SelectCellInTableIncBackup(QWidget):
    def __init__(self, parent=None):
        super(SelectCellInTableIncBackup,self).__init__(parent)
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


class SelectAllIncBackupButton(QWidget):
    def __init__(self,d, parent=None):
        super(SelectAllIncBackupButton,self).__init__(parent)
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
            for i in self.dd:
                self.dd[i].isSelected = True
                self.dd[i].checkb.setChecked(True)
        else:
            self.selectallIsSelected = False
            for i in self.dd:
                self.dd[i].isSelected = False
                self.dd[i].checkb.setChecked(False)





class moreCellInTableIncBackup(QWidget):
    def __init__(self,id, parent=None):
        super(moreCellInTableIncBackup,self).__init__(parent)
        self.id = id
        self.hbox = QHBoxLayout()
        #self.slider.setStyleSheet("color: #2c3e50; selection-background-color: #e74c3c ;background-color: white ; selection-color: #ecf0f1 ;border: 2px solid #95a5a6")
        self.showmoreBtn=QPushButton('more')
        self.showmoreBtn.clicked.connect(self.showmoreBtnClicked)
        self.hbox.addWidget(self.showmoreBtn)
        self.hbox.addStretch()
        self.hbox.setContentsMargins(0,0,0,0)
        self.hbox.setSpacing(8)
        self.setLayout(self.hbox)

    def showmoreBtnClicked(self):
        self.secondwindow = MoreIncBackupWindow(self.id)
        self.sw = qtmodern.windows.ModernWindow(self.secondwindow)
        self.sw.show()


def showmyincbackuplist(self):
    global cur
    self.incBackupList = retrievedatafromdbincbackup()
    self.incbackupdic={}
    self.incbackupdic2={}
    for i in self.incBackupList:
        query = "SELECT * FROM IncrementalBackups WHERE metaname=?"
        incbackups = cur.execute(query,(i,)).fetchall()
        item1 = QTreeWidgetItem(self.tableIncBackup, [i])
        for incbackup in incbackups:
            #self.treeWidget.setItemWidget(self.childItems[0], 0, self.childButton_1)

            tmplist=['',str(incbackup[0]),str(incbackup[2]),str(incbackup[3]),str(incbackup[4]),str(incbackup[5]),str(incbackup[6]),str(incbackup[7])]
            subitem1 = QTreeWidgetItem(item1,tmplist)

            self.incbackupdic2[incbackup[0]] = moreCellInTableIncBackup(incbackup[0])
            self.tableIncBackup.setItemWidget(subitem1, 8, self.incbackupdic2[incbackup[0]])

            self.incbackupdic[incbackup[0]] = SelectCellInTableIncBackup()
            self.tableIncBackup.setItemWidget(subitem1, 9, self.incbackupdic[incbackup[0]])


        #self.incbackupdic[i[0]] = SelectCellInTableIncBackup()

        #item1 = QTreeWidgetItem(self.tableIncBackup, [i[0], i[1],i[2],i[3],i[4],i[5]])
        #self.btn = QPushButton('cccc')
        #self.tableIncBackup.addTopLevelItem(self.btn)

        #item1.setCheckState(0, QtCore.Qt.Checked)


        '''
        self.topLevelItem = QTreeWidgetItem()

        # Creating top level and child widgets
        self.topLevelButton = QLabel(i)
        self.childButton_1 = QPushButton("Child 1")
        self.childButton_2 = QPushButton("Child 2")
        self.childButton_3 = QPushButton("Child 3")
        self.childItems = []
        for i in range(3):
            self.childItems.append(QTreeWidgetItem())
            self.topLevelItem.addChild(self.childItems[i])

        self.tableIncBackup.addTopLevelItem(self.topLevelItem)
        self.tableIncBackup.setItemWidget(self.topLevelItem, 0, self.topLevelButton)

        # Replacing the child items with widgets
        self.tableIncBackup.setItemWidget(self.childItems[0], 0, self.childButton_1)
        self.tableIncBackup.setItemWidget(self.childItems[1], 0, self.childButton_2)
        self.tableIncBackup.setItemWidget(self.childItems[2], 0, self.childButton_3)

        #self.incbackupdic2[i[0]] = moreCellInTableIncBackup(i[0])
        #self.tableIncBackup.setCellWidget(self.rowPosition,6,self.incbackupdic2[i[0]])
        #self.tableIncBackup.setCellWidget(self.rowPosition,7,self.incbackupdic[i[0]])
        '''


def retrievedatafromdbincbackup():
    global cur
    listincbackups = []
    query = "SELECT DISTINCT metaname FROM IncrementalBackups ORDER BY ROWID ASC"
    incbackups = cur.execute(query).fetchall()
    for incbackup in incbackups:
        #listincbackups.append([str(incbackup[1]),[str(incbackup[0]),str(incbackup[2]),str(incbackup[3]),str(incbackup[4]),str(incbackup[5]),str(incbackup[6]),str(incbackup[7])]])
        listincbackups.append(str(incbackup[0]))
    return listincbackups


def createIncBackupWindow(self):
    incBackupList = retrievedatafromdbincbackup()
    self.secondwindow = CreateIncBackupWindow(incBackupList)
    self.sw = qtmodern.windows.ModernWindow(self.secondwindow)
    self.sw.show()


def restoreIncBackupWindow(self):
    incBackupList = retrievedatafromdbincbackup()
    self.secondwindow = RestoreIncBackupWindow(incBackupList)
    self.sw = qtmodern.windows.ModernWindow(self.secondwindow)
    self.sw.show()


def deleteIncBackupWindow(self,d):
    list_incbackups_to_delete = []
    for i in d:
        if d[i].isSelected == True:
            list_incbackups_to_delete.append(str(i))
    if len(list_incbackups_to_delete) == 0:
        QMessageBox.warning(self, 'warning', 'no selected incremental backups.\nPlease select at least one incremental backup')
    else:
        self.secondwindow = DeleteIncBackupWindow(list_incbackups_to_delete)
        self.sw = qtmodern.windows.ModernWindow(self.secondwindow)
        self.sw.show()
