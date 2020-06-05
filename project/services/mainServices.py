import qtmodern.styles
import qtmodern.windows
from PyQt5 import QtGui, QtCore
#from project.services.configServices import CreateServicesWindow, EditServicesWindow, DeleteServicesWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, Qt
import subprocess
from project.services.servicesScripts import stopServices, startServices, listAllServices,isEnable,enableServices,disableServices,isStart

def getContentServices(self):
    self.gridServices = QGridLayout()

    createTableServices(self)
    
    self.containerServices=QVBoxLayout()

    self.containerServices.addLayout(self.gridServices)
    self.containerServices.addWidget(self.tableServices)

    self.bottomRightLayout.addLayout(self.containerServices)

def createTableServices(self):
    self.tableServices=QTableWidget()
    self.tableServices.setRowCount(0)
    self.tableServices.setColumnCount(7)

    self.tableServices.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    self.tableServices.setAutoFillBackground(True)

    header = self.tableServices.horizontalHeader()
    header.setStretchLastSection(True)

    self.tableServices.setHorizontalHeaderItem(0, QTableWidgetItem("UNIT Name"))
    self.tableServices.setHorizontalHeaderItem(1, QTableWidgetItem("LOAD"))
    self.tableServices.setHorizontalHeaderItem(2, QTableWidgetItem("ACTIVE"))
    self.tableServices.setHorizontalHeaderItem(3, QTableWidgetItem("SUB"))
    self.tableServices.setHorizontalHeaderItem(4, QTableWidgetItem("DESCRIPTION"))
    self.tableServices.setHorizontalHeaderItem(5, QTableWidgetItem(" ENABLED OR DISABLED  "))
    self.tableServices.setHorizontalHeaderItem(6, QTableWidgetItem(" STARTED OR STOPED  "))
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


#############################################################    table WIDGETS "####################################################""

class EnableDisableCellInButton(QWidget):
    def __init__(self,unit, parent=None):
        super(EnableDisableCellInButton,self).__init__(parent)
        self.unit = unit
        self.isEnabled=False

        self.hbox = QHBoxLayout()
        self.enableDisableBtn=QPushButton('')
        self.enableDisableBtn.clicked.connect(self.enableDisableClicked)
        self.hbox.addWidget(self.enableDisableBtn)
        self.hbox.addStretch()
        self.hbox.setContentsMargins(0,0,0,0)
        self.hbox.setSpacing(8)
        self.setLayout(self.hbox)

        if isEnable(self.unit) == True:

            self.enableDisableBtn.setStyleSheet("background-color: green")
            self.enableDisableBtn.setText("enabled")
            self.isEnabled = True



        else:
            self.enableDisableBtn.setStyleSheet("background-color: red")
            self.enableDisableBtn.setText("disabled")
            self.isEnabled =False

    def enableDisableClicked(self):

        if self.isEnabled==False:
            try:
                enableServices(self.unit)
            except subprocess.CalledProcessError as e:
                QMessageBox.critical(self, 'error', f'error cannot Enable {self.unit} ')
                # self.slider.setValue(0)
            else:
                QMessageBox.information(self, 'success', f'{self.unit} has been Enabled succesfully')
                self.enableDisableBtn.setStyleSheet("background-color: green")
                self.enableDisableBtn.setText("enabled")
                self.isEnabled==True

        elif self.isEnabled==True:

            try:
                disableServices(self.unit)
            except subprocess.CalledProcessError as e:
                QMessageBox.critical(self, 'error', f'error cannot Disable  {self.unit}')
            else:
                QMessageBox.information(self, 'success', f'{self.unit} has been Disabled succesfully')
                self.enableDisableBtn.setStyleSheet("background-color: red")
                self.enableDisableBtn.setText("disabled")
                self.isEnabled=False
        else:
            pass

class StartStopCellInTableButton(QWidget):
    def __init__(self,unit, parent=None):
        super(StartStopCellInTableButton,self).__init__(parent)
        self.isStarted=False
        self.unit = unit
        self.hbox = QHBoxLayout()
        self.startStopBtn=QPushButton('')
        self.startStopBtn.clicked.connect(self.startStopClicked)
        self.hbox.addWidget(self.startStopBtn)
        self.hbox.addStretch()
        self.hbox.setContentsMargins(0,0,0,0)
        self.hbox.setSpacing(8)
        self.setLayout(self.hbox)

        if isStart(self.unit) == True:

            self.startStopBtn.setStyleSheet("background-color: green")
            self.startStopBtn.setText("started")
            self.isStarted=True

        else:
            self.startStopBtn.setStyleSheet("background-color: red")
            self.startStopBtn.setText("disabled")
            self.isStarted=False

    def startStopClicked(self):

        if self.isStarted==False:

            try:
                startServices(self.unit)
            except subprocess.CalledProcessError as e:
                QMessageBox.critical(self, 'error', f'error cannot start {self.unit} ')
                # self.slider.setValue(0)
                self.isStarted=True
            else:
                QMessageBox.information(self, 'success', f'{self.unit} has been started succesfully')
                self.startStopBtn.setStyleSheet("background-color: green")
                self.startStopBtn.setText("started")


        elif self.isStarted==True:

            try:
                stopServices(self.unit)
            except subprocess.CalledProcessError as e:
                QMessageBox.critical(self, 'error', f'error cannot stop  {self.unit}')
                 # self.slider.setValue(1)
            else:
                QMessageBox.information(self, 'success', f'{self.unit} has been stopped succesfully')
                self.startStopBtn.setStyleSheet("background-color: red")
                self.startStopBtn.setText("stopped")
                self.isStarted=False
        else:
            pass

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
        self.dic3[i[0]] = StartStopCellInTableButton(i[0])
        self.dic2[i[0]] = EnableDisableCellInButton(i[0])
        #self.dic2[i[0]] = SelectCellInTableServices()
        self.tableServices.setCellWidget(self.rowPosition,6,self.dic3[i[0]])
        self.tableServices.setCellWidget(self.rowPosition,5,self.dic2[i[0]])


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