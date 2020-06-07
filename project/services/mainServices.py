from PyQt5.QtWidgets import *
import subprocess
from project.services.servicesScripts import stopServices, startServices, listAllServices, isEnable, enableServices, \
    disableServices, isStart


def getContentServices(self):
    self.gridServices = QGridLayout()

    createTableServices(self)

    self.containerServices = QVBoxLayout()

    self.containerServices.addLayout(self.gridServices)
    self.containerServices.addWidget(self.tableServices)

    self.bottomRightLayout.addLayout(self.containerServices)


def createTableServices(self):
    self.tableServices = QTableWidget()
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
    self.tableServices.setEditTriggers(QAbstractItemView.NoEditTriggers)
    showmyserviceslist(self)


class EnableDisableCellInButton(QWidget):
    def __init__(self, unit, parent=None):
        super(EnableDisableCellInButton, self).__init__(parent)
        self.unit = unit
        self.isEnabled = False

        self.hbox = QHBoxLayout()
        self.enableDisableBtn = QPushButton('')
        self.enableDisableBtn.setFixedSize(100, 30)
        self.enableDisableBtn.clicked.connect(self.enableDisableClicked)
        self.hbox.addWidget(self.enableDisableBtn)
        self.hbox.addStretch()
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.hbox.setSpacing(8)
        self.setLayout(self.hbox)

        if isEnable(self.unit) == True:

            self.enableDisableBtn.setStyleSheet("background-color: #2ecc71 ; border: 0px solid #303a46")
            self.enableDisableBtn.setText("enabled")
            self.isEnabled = True



        else:
            self.enableDisableBtn.setStyleSheet("background-color: #e74c3c ; border: 0px solid #303a46")
            self.enableDisableBtn.setText("disabled")
            self.isEnabled = False

    def enableDisableClicked(self):

        if self.isEnabled == False:
            try:
                enableServices(self.unit)
            except subprocess.CalledProcessError as e:
                QMessageBox.critical(self, 'error', f'error cannot Enable {self.unit} ')
                # self.slider.setValue(0)
            else:
                QMessageBox.information(self, 'success', f'{self.unit} has been Enabled succesfully')
                self.enableDisableBtn.setStyleSheet("background-color: #2ecc71 ; border: 0px solid #303a46")
                self.enableDisableBtn.setText("enabled")
                self.isEnabled == True

        elif self.isEnabled == True:

            try:
                disableServices(self.unit)
            except subprocess.CalledProcessError as e:
                QMessageBox.critical(self, 'error', f'error cannot Disable  {self.unit}')
            else:
                QMessageBox.information(self, 'success', f'{self.unit} has been Disabled succesfully')
                self.enableDisableBtn.setStyleSheet("background-color: #e74c3c ; border: 0px solid #303a46")
                self.enableDisableBtn.setText("disabled")
                self.isEnabled = False
        else:
            pass


class StartStopCellInTableButton(QWidget):
    def __init__(self, unit, parent=None):
        super(StartStopCellInTableButton, self).__init__(parent)
        self.isStarted = False
        self.unit = unit
        self.hbox = QHBoxLayout()
        self.startStopBtn = QPushButton('')
        self.startStopBtn.setFixedSize(100, 30)
        self.startStopBtn.clicked.connect(self.startStopClicked)
        self.hbox.addWidget(self.startStopBtn)
        self.hbox.addStretch()
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.hbox.setSpacing(8)
        self.setLayout(self.hbox)

        if isStart(self.unit) == True:

            self.startStopBtn.setStyleSheet("background-color: #2ecc71 ; border: 0px solid #303a46")
            self.startStopBtn.setText("started")
            self.isStarted = True

        else:
            self.startStopBtn.setStyleSheet("background-color: #e74c3c ; border: 0px solid #303a46")
            self.startStopBtn.setText("stopped")
            self.isStarted = False

    def startStopClicked(self):

        if self.isStarted == False:
            try:
                startServices(self.unit)
            except subprocess.CalledProcessError as e:
                QMessageBox.critical(self, 'error', f'error cannot start {self.unit} ')
                self.isStarted = True
            else:
                QMessageBox.information(self, 'success', f'{self.unit} has been started succesfully')
                self.startStopBtn.setStyleSheet("background-color: #2ecc71 ; border: 0px solid #303a46")
                self.startStopBtn.setText("started")

        elif self.isStarted == True:
            try:
                stopServices(self.unit)
            except subprocess.CalledProcessError as e:
                QMessageBox.critical(self, 'error', f'error cannot stop  {self.unit}')
            else:
                QMessageBox.information(self, 'success', f'{self.unit} has been stopped succesfully')
                self.startStopBtn.setStyleSheet("background-color: #e74c3c ; border: 0px solid #303a46")
                self.startStopBtn.setText("stopped")
                self.isStarted = False
        else:
            pass


def showmyserviceslist(self):
    self.servicesList = listAllServices()
    self.dic2 = {}
    self.dic3 = {}
    self.dic4 = {}
    self.rowposition = 0
    for i in self.servicesList:
        if len(i) != 5:
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
        self.tableServices.setCellWidget(self.rowPosition, 6, self.dic3[i[0]])
        self.tableServices.setCellWidget(self.rowPosition, 5, self.dic2[i[0]])
