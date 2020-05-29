import qtmodern.styles
import qtmodern.windows
from PyQt5 import QtGui, QtCore
#from project.services.configServices import CreateServicesWindow, EditServicesWindow, DeleteServicesWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, Qt
import subprocess
from project.services.servicesScripts import stopServices, startServices, listAllServices,isEnable,enableServices,disableServices

def getContentServices(self):
    self.gridServices = QGridLayout()

    #################### creating and triggerting update for services's table
    createTableServices(self)

    #################### creating buttons under pie plots
    #createServicesButtons(self)

    self.groupBox = QGroupBox()
    self.containerServices=QVBoxLayout()

    self.containerServices.addLayout(self.gridServices)
    #self.containerServices.addLayout(self.hboxbtn)
    self.containerServices.addWidget(self.tableServices)
    self.containerServices.addStretch()

    self.groupBox.setLayout(self.containerServices)
    self.scroll = QScrollArea()
    self.scroll.setFixedWidth(1150)
    self.scroll.setWidget(self.groupBox)
    self.scroll.setAutoFillBackground(True)
    self.bottomRightLayout.addWidget(self.scroll)

'''
def createServicesButtons(self):
    self.hboxbtn=QHBoxLayout()
    #self.selectall=QCheckBox('Select All',self)
    self.addBtn=QPushButton('Something Here')
    self.editBtn=QPushButton('Something here')
    self.deleteBtn=QPushButton('Something here')
    self.addBtn.setFixedHeight(30)
    self.addBtn.setFixedWidth(120)
    self.editBtn.setFixedHeight(30)
    self.editBtn.setFixedWidth(120)
    self.deleteBtn.setFixedHeight(30)
    self.deleteBtn.setFixedWidth(120)
    self.addBtn.clicked.connect(lambda: createServicesWindow(self))
    self.addBtn.setStyleSheet("color: #ecf0f1; background-color: #2ecc71 ; border: 0px solid #2c3e50")
    self.editBtn.clicked.connect(lambda: editServicesWindow(self,self.dic2))
    self.editBtn.setStyleSheet("color: #ecf0f1; background-color: #34495e ; border: 0px solid #2c3e50")
    self.deleteBtn.clicked.connect(lambda: deleteServicesWindow(self,self.dic2))
    self.deleteBtn.setStyleSheet("color: #ecf0f1; background-color: #e74c3c; border: 0px solid #2c3e50")
    #self.selectall = SelectAllButton(self.dic2)
    self.hboxbtn.addWidget(self.selectall)
    self.hboxbtn.addStretch()
    self.hboxbtn.addWidget(self.addBtn)
    self.hboxbtn.addWidget(self.editBtn)
    self.hboxbtn.addWidget(self.deleteBtn)
'''

def createTableServices(self):
    self.tableServices=QTableWidget()
    self.tableServices.setRowCount(0)
    self.tableServices.setColumnCount(7)

    self.tableServices.setFixedHeight(600)
    self.tableServices.setFixedWidth(1110)

    self.tableServices.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    self.tableServices.setHorizontalHeaderItem(0, QTableWidgetItem("UNIT Name"))
    self.tableServices.setHorizontalHeaderItem(1, QTableWidgetItem("LOAD"))
    self.tableServices.setHorizontalHeaderItem(2, QTableWidgetItem("ACTIVE"))
    self.tableServices.setHorizontalHeaderItem(3, QTableWidgetItem("SUB"))
    self.tableServices.setHorizontalHeaderItem(4, QTableWidgetItem("DESCRIPTION"))
    self.tableServices.setHorizontalHeaderItem(5, QTableWidgetItem("START-STOP SERVICE"))
    self.tableServices.setHorizontalHeaderItem(6, QTableWidgetItem("ENABLE-DISABLE SERVICE"))
    #self.tableServices.setHorizontalHeaderItem(6, QTableWidgetItem("Select"))
    self.tableServices.setEditTriggers(QAbstractItemView.NoEditTriggers)
    showmyserviceslist(self)

'''
class SelectCellInTableServices(QWidget):
    def __init__(self, parent=None):
        super(SelectCellInTableServices,self).__init__(parent)
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
'''


#######START-STOP  WIDGET

class StartStopCellInTable(QWidget):
    def __init__(self,username,groups, parent=None):
        super(StartStopCellInTable,self).__init__(parent)
        self.groups = groups
        self.username = username
        self.userIsAdmin = False
        self.hbox = QHBoxLayout()
        self.slider = QSlider(Qt.Horizontal)
        #self.slider.setStyleSheet("color: #2c3e50; selection-background-color: #e74c3c ;background-color: white ; selection-color: #ecf0f1 ;border: 2px solid #95a5a6")
        self.slider.setMaximum(1)
        self.slider.setMinimum(0)
        self.slider.setFixedWidth(40)
        #self.slider.setStyleSheet("color:#2ecc71 ")
        self.slider.setTickInterval(1)  # change ticks interval
        if ' active ' in self.groups:
            self.userIsAdmin = True
            self.text = QLabel("True")
            self.slider.setValue(1)
        else:
            self.userIsAdmin = False
            self.text = QLabel("False")
            self.slider.setValue(0)
        #self.text.setAlignment(Qt.AlignCenter)  # move to the center
        self.slider.valueChanged.connect(self.changed)
        self.hbox.addStretch()
        self.hbox.addWidget(self.slider)
        self.hbox.addWidget(self.text)
        self.hbox.addStretch()
        self.hbox.setContentsMargins(0,0,0,0)
        self.hbox.setSpacing(8)
        self.setLayout(self.hbox)

    def changed(self):
        if self.slider.value() == 1:
            self.mbox = QMessageBox.question(self, "Warningg!", f"Are you sure to start {self.username} ?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if self.mbox == QMessageBox.Yes:
                self.start()
            elif self.mbox == QMessageBox.No:
                pass
            else:
                pass
        elif self.slider.value() == 0:
            self.stop()

    def start(self):
        try:
            startServices(self.username)
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, 'error', f'error cannot start {self.username} ')
            #self.slider.setValue(0)
        else:
            QMessageBox.information(self, 'success', f'{self.username} has been started succesfully')
            self.text.setText("True")
            self.slider.setValue(1)
            self.userIsAdmin = True

    def stop(self):
        try:
            stopServices(self.username)
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, 'error', f'error cannot stop  {self.username}')
            #self.slider.setValue(1)
        else:
            QMessageBox.information(self, 'success', f'{self.username} has been stopped succesfully')
            self.text.setText("False")
            self.slider.setValue(0)
            self.userIsAdmin = False

class EnableDisableCellInTable(QWidget):
    def __init__(self,username,groups, parent=None):
        super(EnableDisableCellInTable,self).__init__(parent)
        self.groups = groups
        self.username = username
        self.userIsAdmin = False
        self.hbox = QHBoxLayout()
        self.slider = QSlider(Qt.Horizontal)
        #self.slider.setStyleSheet("color: #2c3e50; selection-background-color: #e74c3c ;background-color: white ; selection-color: #ecf0f1 ;border: 2px solid #95a5a6")
        self.slider.setMaximum(1)
        self.slider.setMinimum(0)
        self.slider.setFixedWidth(40)
        #self.slider.setStyleSheet("color:#2ecc71 ")
        self.slider.setTickInterval(1)  # change ticks interval
        if isEnable(self.username)==True :
            self.userIsAdmin = True
            self.text = QLabel("True")
            self.slider.setValue(1)
        else:
            self.userIsAdmin = False
            self.text = QLabel("False")
            self.slider.setValue(0)
        #self.text.setAlignment(Qt.AlignCenter)  # move to the center
        self.slider.valueChanged.connect(self.changed)
        self.hbox.addStretch()
        self.hbox.addWidget(self.slider)
        self.hbox.addWidget(self.text)
        self.hbox.addStretch()
        self.hbox.setContentsMargins(0,0,0,0)
        self.hbox.setSpacing(8)
        self.setLayout(self.hbox)

    def changed(self):
        if self.slider.value() == 1:
            self.mbox = QMessageBox.question(self, "Warningg!", f"Are you sure to Enable {self.username} ?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if self.mbox == QMessageBox.Yes:
                self.start()
            elif self.mbox == QMessageBox.No:
                pass
            else:
                pass
        elif self.slider.value() == 0:
            self.stop()

    def start(self):
        try:
            enableServices(self.username)
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, 'error', f'error cannot Enable {self.username} ')
            #self.slider.setValue(0)
        else:
            QMessageBox.information(self, 'success', f'{self.username} has been Enabled succesfully')
            self.text.setText("True")
            self.slider.setValue(1)
            self.userIsAdmin = True

    def stop(self):
        try:
            disableServices(self.username)
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, 'error', f'error cannot Disable  {self.username}')
            #self.slider.setValue(1)
        else:
            QMessageBox.information(self, 'success', f'{self.username} has been Disabled succesfully')
            self.text.setText("False")
            self.slider.setValue(0)
            self.userIsAdmin = False

def showmyserviceslist(self):
    self.servicesList = listAllServices()
    self.dic2={}
    self.dic3={}
    self.dic4={}
    self.rowposition = 0
    for i in self.servicesList:
        if len(i) != 5  :
            continue
        self.rowPosition = self.tableServices.rowCount()
        self.tableServices.insertRow(self.rowPosition)
        self.tableServices.setItem(self.rowPosition, 0, QTableWidgetItem(i[0]))
        self.tableServices.setItem(self.rowPosition, 1, QTableWidgetItem(i[1]))
        self.tableServices.setItem(self.rowPosition, 2, QTableWidgetItem(i[2]))
        self.tableServices.setItem(self.rowPosition, 3, QTableWidgetItem(i[3]))
        self.tableServices.setItem(self.rowPosition, 4, QTableWidgetItem(i[4]))
        self.dic3[i[0]] = StartStopCellInTable(i[0],i[2])
        self.dic2[i[0]] = EnableDisableCellInTable(i[0],i[2])
        #self.dic2[i[0]] = SelectCellInTableServices()
        self.tableServices.setCellWidget(self.rowPosition,5,self.dic3[i[0]])
        self.tableServices.setCellWidget(self.rowPosition,6,self.dic2[i[0]])


def createServicesWindow(self):
    pass
    '''
    self.secondwindow = CreateServicesWindow()
    self.sw = qtmodern.windows.ModernWindow(self.secondwindow)
    self.sw.show()
    '''

def editServicesWindow(self,d):
    pass
    '''
    list_users_to_edit = []
    for i in d:
        if d[i].isSelected == True:
            list_users_to_edit.append(i)
    if len(list_users_to_edit) == 0 or len(list_users_to_edit) > 1:
        QMessageBox.warning(self, 'warning', 'Please select just one user')
    else:
        for user in self.usersList :
            if user[0] == list_users_to_edit[0]:
                self.secondwindow = EditServicesWindow(user)
                self.sw = qtmodern.windows.ModernWindow(self.secondwindow)
                self.sw.show()
            else:
                continue
    '''

def deleteServicesWindow(self,d):
    pass
    '''
    list_users_to_delete = []
    for i in d:
        if d[i].isSelected == True:
            list_users_to_delete.append(i)
    if len(list_users_to_delete) == 0:
        QMessageBox.warning(self, 'warning', 'no selected users.\nPlease select at least one user')
    else:
        self.secondwindow = DeleteServicesWindow(list_users_to_delete)
        self.sw = qtmodern.windows.ModernWindow(self.secondwindow)
        self.sw.show()
    '''