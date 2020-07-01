from PyQt5.QtWidgets import *
import subprocess
from PyQt5 import QtGui, QtCore
from project.networking.networkingScripts import displayNetworkInterface
from project.networking.displayConnections import displayConnection
from project.networking.displayIP import DisplayIP
from project.networking.netScript import disInterfaceConnection, displaySSID
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QDateTimeEdit, QFormLayout, QLabel, QApplication, QWidget, QLineEdit, QHBoxLayout, \
    QPushButton, QRadioButton, QButtonGroup

import datetime

import qtmodern
import systemd.journal
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDateTimeEdit, QFormLayout, QLabel, QApplication, QWidget, QLineEdit, QHBoxLayout, \
    QPushButton, QRadioButton, QButtonGroup
from PyQt5.uic.properties import QtGui


class CreateNetworkWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 50, 600, 400)
        self.setWindowTitle("Add a New Connection")
        self.layouts()
        self.widgets()

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QFormLayout()
        self.middelLayout = QFormLayout()

        self.bottomLayout = QHBoxLayout()

        self.submitBtn = QPushButton("Add")
        self.submitBtn.clicked.connect(self.submitAction)
        self.cancelBtn = QPushButton("Cancel")
        self.cancelBtn.clicked.connect(self.cancelAction)
        self.submitBtn.setFixedHeight(30)
        self.cancelBtn.setFixedHeight(30)
        self.submitBtn.setStyleSheet("color: #ecf0f1; background-color: #27ae60 ; border: 0px solid #27ae60")
        self.cancelBtn.setStyleSheet("color: #ecf0f1; background-color: #e74c3c; border: 0px solid #e74c3c")

        self.bottomLayout.addWidget(self.submitBtn)
        self.bottomLayout.addWidget(self.cancelBtn)
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addStretch()
        self.mainLayout.addLayout(self.bottomLayout)
        self.setLayout(self.mainLayout)

    def widgets(self):
        self.comboInt = QComboBox()
        try:
            subprocess.run(' ls /sys/class/net > /tmp/networkInterfaces.txt', check=True, shell=True)
            deviceFile = open('/tmp/networkInterfaces.txt', 'rt')
            device = deviceFile.read()
            interName = device.splitlines()
            self.comboInt.addItems(interName)

        except:
            print("Can't fetch network interface ")

        self.ssid = QLineEdit()
        self.ssid.setPlaceholderText('Required on wifi type ')
        self.typeCombo = QComboBox()
        self.typeCombo.addItem("ethernet")
        self.typeCombo.addItem("wifi")
        self.newconNameEdit = QLineEdit()
        self.newconNameEdit.setPlaceholderText('Required field')
        self.ipEdit = QLineEdit()
        self.ipEdit.setPlaceholderText('Required field')
        self.gatewayEdit = QLineEdit()
        self.gatewayEdit.setPlaceholderText('Required field')
        self.dnsEdit = QLineEdit()
        self.dnsEdit.setPlaceholderText('Optionnel field')
        self.maskListItem = QComboBox()
        self.maskListItem.addItem(" /24:     255.255.255.0      ")
        self.maskListItem.addItem(" /32:     255.255.255.255     ")
        self.maskListItem.addItem(" /31:     255.255.255.254   ")
        self.maskListItem.addItem(" /30:     255.255.255.252    ")
        self.maskListItem.addItem(" /29:     255.255.255.248    ")
        self.maskListItem.addItem(" /28:     255.255.255.240     ")
        self.maskListItem.addItem(" /27:     255.255.255.224    ")
        self.maskListItem.addItem(" /26:     255.255.255.192   ")
        self.maskListItem.addItem(" /25:     255.255.255.128      ")
        self.maskListItem.addItem(" /23:     255.255.254.0    ")
        self.maskListItem.addItem(" /22:     255.255.252.0       ")
        self.maskListItem.addItem(" /21:     255.255.248.255")
        self.maskListItem.addItem(" /20:     255.255.255.240")

        self.ip_group = QHBoxLayout()
        widget = QWidget(self)
        self.ip_group_button = QButtonGroup(widget)
        self.man = QRadioButton("Manual")
        self.dhcp = QRadioButton("DHCP")
        self.man.setChecked(True)

        self.ip_group_button.addButton(self.man)
        self.ip_group_button.addButton(self.dhcp)
        self.ip_group.addWidget(self.man)
        self.ip_group.addWidget(self.dhcp)

        self.ethernet = QRadioButton("Ethernet")
        self.wifi = QRadioButton("Wifi")
        self.ethernet.setChecked(True)
        self.type_group = QHBoxLayout()
        self.type_group.addWidget(self.ethernet)
        self.type_group.addWidget(self.wifi)

        self.topLayout.addRow(QLabel('General information'), QLabel(''))
        self.topLayout.addRow(QLabel(''), QLabel(''))
        self.topLayout.addRow(QLabel("Enter New Connection's Name:"), self.newconNameEdit)
        self.topLayout.addRow(QLabel("Enter SSID: "), self.ssid)
        self.topLayout.addRow(QLabel("Select interface:"), self.comboInt)
        self.topLayout.addRow(QLabel("Change Connection Type:"), QLabel(""))
        self.topLayout.addRow(self.type_group)
        self.topLayout.addRow(QLabel(''), QLabel(''))

        self.topLayout.addRow(QLabel('IP Method Assing:'), QLabel(''))
        self.topLayout.addRow(QLabel(''), QLabel(''))

        self.topLayout.addRow(self.ip_group)
        self.topLayout.addRow(QLabel(''), QLabel(''))
        self.topLayout.addRow(QLabel('IP information'), QLabel(''))
        self.topLayout.addRow(QLabel(''), QLabel(''))
        self.topLayout.addRow(QLabel("Enter New IP Address"), self.ipEdit)
        self.topLayout.addRow(QLabel("Enter New Subnet Mask"), self.maskListItem)
        self.topLayout.addRow(QLabel("Enter New GATWAY address"), self.gatewayEdit)
        self.topLayout.addRow(QLabel("Enter DNS Address"), self.dnsEdit)
        self.topLayout.addRow(QLabel(''), QLabel(''))
        self.topLayout.addRow(QLabel(''), QLabel(''))

    def submitAction(self):
        newssid = self.ssid.text()
        newName = self.newconNameEdit
        newInter = self.comboInt
        newIp = self.ipEdit.text()
        newMask = self.maskListItem.currentText()
        newMask = newMask.split(':')[0]
        newGatway = self.gatewayEdit.text()
        newDns = self.dnsEdit.text()

        if str(newName.text()) in ' ':
            QMessageBox.warning(self, 'warning', f"Must Enter Connection name\n")
        elif str(newIp) in ' ' and self.man.isChecked():
            QMessageBox.warning(self, 'warning', f"Must Enter Connection Ip\n")
        elif str(newGatway) in ' ' and self.man.isChecked():
            QMessageBox.warning(self, 'warning', f"Must Enter Connection Gateway\n")
        elif str(newGatway) == str(newIp) and self.man.isChecked():
            QMessageBox.warning(self, 'warning', f"Gateway is the same IP address \n")
        elif self.wifi.isChecked() and newssid in '':
            QMessageBox.warning(self, 'warning', " SSID is missing .\n Enter SSID name  \n")
        else:
            if self.man.isChecked():
                dns = False
                if str(newDns) not in ' ':
                    dns = True

                Mask = str(newMask)
                mask = str(Mask[2:])
                ipMask = f'{newIp}/{mask}'
                name = newName.text()

                command = f'nmcli con add con-name {name} ifname {str(newInter.currentText())}'

                if self.wifi.isChecked():
                    command += f' type wifi ssid {str(newssid)}'
                else:
                    command += f' type ethernet'
                command += f' ipv4.address {ipMask} ipv4.gateway {str(newGatway)}'
                if dns == True:
                    command += f' ipv4.dns {newDns} ipv4.method manual'
                else:
                    command += f' ipv4.method manual'

                try:
                    subprocess.run(command, check=True, shell=True)
                except subprocess.CalledProcessError:
                    QMessageBox.warning(self, 'warning', f"error occured during setting this changes\n")
                else:
                    QMessageBox.information(self, 'success', '\n a New Connection Added  Succesfully.')
                    self.close()

            if self.dhcp.isChecked():
                command = f'nmcli con add con-name {str(newName.text())} ifname {str(newInter.currentText())}'
                if self.wifi.isChecked():
                    command += f' type wifi ssid {str(newssid)}'
                else:
                    command += f' type ethernet'
                command += f' ipv4.method auto'

                try:
                    subprocess.run(command, check=True, shell=True)
                except subprocess.CalledProcessError:
                    QMessageBox.warning(self, 'warning', f"error occured during setting this changes\n")
                else:
                    QMessageBox.information(self, 'success', '\n a New Connection Added  Succesfully.')
                    self.close()

    def cancelAction(self):
        self.close()


class EditNetworkWindow(QWidget):
    def __init__(self, d):
        super().__init__()
        self.setGeometry(200, 50, 300, 400)
        self.setWindowTitle("Edit a connection ")
        self.index = d
        self.itwas = d
        self.layouts()
        self.widgets()

    def layouts(self):
        groupBox = QGroupBox("")
        self.mainLayout = QVBoxLayout()
        self.topLayout = QFormLayout()
        self.middelLayout = QFormLayout()
        self.middelLayout.setContentsMargins(20, 20, 20, 20)
        self.topLayout.setContentsMargins(20, 20, 20, 20)
        self.bottomLayout = QHBoxLayout()
        self.upperLayout=QVBoxLayout()
        groupBox.setLayout(self.mainLayout)

        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(600)
        scroll.setFixedWidth(500)
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)

        self.submitBtn = QPushButton("Submit")
        self.cancelBtn = QPushButton("Cancel")

        self.submitBtn.clicked.connect(self.submitAction)
        self.cancelBtn.clicked.connect(self.cancelAction)

        self.submitBtn.setFixedHeight(30)
        self.cancelBtn.setFixedHeight(30)
        self.submitBtn.setStyleSheet("color: #ecf0f1; background-color: #27ae60 ; border: 0px solid #27ae60")
        self.cancelBtn.setStyleSheet("color: #ecf0f1; background-color: #e74c3c; border: 0px solid #e74c3c")

        if self.index[2] != 'auto':
            self.bottomLayout.addWidget(self.submitBtn)
            self.bottomLayout.addWidget(self.cancelBtn)
            self.upperLayout.addLayout(self.topLayout)
            self.upperLayout.addLayout(self.middelLayout)
            self.mainLayout.addLayout(self.upperLayout)
            self.mainLayout.addLayout(self.bottomLayout)

        else:
            self.bottomLayout.addWidget(self.submitBtn)
            self.bottomLayout.addWidget(self.cancelBtn)
            self.upperLayout.addLayout(self.topLayout)
            self.mainLayout.addLayout(self.upperLayout)
            self.mainLayout.addLayout(self.bottomLayout)

        self.setLayout(self.mainLayout)

    def widgets(self):
        self.consName = QComboBox(self)
        self.comboInt = QComboBox()
        consNames = self.index[0]
        self.consName.addItem(consNames)

        interName = displayNetworkInterface()
        self.comboInt.addItem('no change')
        self.comboInt.addItems(interName)
        self.newconNameEdit = QLineEdit()

        self.operation = QComboBox()
        self.operation.addItem('Type')
        self.operation.addItem('Change Network name')
        self.operation.addItem('Change Network interface')
        self.operation.addItem('Change IP Address')
        self.operation.addItem('Change Subnet Mask')
        self.operation.addItem('Change Gateway')
        self.operation.addItem('Change DNS')
        self.operation.addItem('Change Mode Addressing')
        self.typeCombo = QComboBox()

        self.typeCombo.addItem("no change")
        self.typeCombo.addItem("ethernet")
        self.typeCombo.addItem("wifi")

        self.newconNameEdit = QLineEdit()
        self.newSSIDEdit = QLineEdit()
        self.ipEdit = QLineEdit()
        self.gatewayEdit = QLineEdit()
        self.dnsEdit = QLineEdit()
        self.dnsEdit2 = QLineEdit()
        self.maskListItem = QComboBox()
        self.maskListItem.addItem("no change")
        self.maskListItem.addItem(" /24:     255.255.255.0      ")
        self.maskListItem.addItem(" /32:     255.255.255.255     ")
        self.maskListItem.addItem(" /31:     255.255.255.254   ")
        self.maskListItem.addItem(" /30:     255.255.255.252    ")
        self.maskListItem.addItem(" /29:     255.255.255.248    ")
        self.maskListItem.addItem(" /28:     255.255.255.240     ")
        self.maskListItem.addItem(" /27:     255.255.255.224    ")
        self.maskListItem.addItem(" /26:     255.255.255.192   ")
        self.maskListItem.addItem(" /25:     255.255.255.128      ")
        self.maskListItem.addItem(" /23:     255.255.254.0    ")
        self.maskListItem.addItem(" /22:     255.255.252.0       ")
        self.maskListItem.addItem(" /21:     255.255.248.255")
        self.maskListItem.addItem(" /20:     255.255.255.240")

        index = str(self.index[0])
        index = index.replace(' ', '\\ ')
        tmpindex = index
        self.ipInfo = DisplayIP(index)
        ipInfoDns = self.ipInfo[2]
        ipInfoDns = ipInfoDns.split(',')
        self.topLayout.addRow(QLabel("Connection for editing is"), self.consName)
        self.topLayout.addRow(QLabel(''), QLabel(''))
        self.topLayout.addRow(QLabel(f'Old infrmation are '), QLabel(''))
        self.topLayout.addRow(QLabel(f'NAME= {self.index[0]}'), QLabel(''))
        if self.index[1] in 'wifi':
            self.topLayout.addRow(QLabel(f'SSID= {displaySSID(tmpindex)}'), QLabel(''))
        self.topLayout.addRow(QLabel(f'TYPE= {self.index[1]}'), QLabel(''))
        self.topLayout.addRow(QLabel(f'IP ASSIGN METHOD= {self.index[2]}'), QLabel(''))
        self.topLayout.addRow(QLabel(f'AUTO CONNECT = {self.index[3]}'), QLabel(''))
        self.topLayout.addRow(QLabel(f'INTERFACE ASSOICIATED  = {disInterfaceConnection(index)}'), QLabel(''))

        self.topLayout.addRow(QLabel(''), QLabel(''))

        self.topLayout.addRow(QLabel('For New inforamtions Editing '), QLabel(''))
        self.topLayout.addRow(QLabel(''), QLabel(''))
        self.topLayout.addRow(QLabel("Enter New Connection's Name"), self.newconNameEdit)
        thereisSSID = False
        if self.index[1] in 'wifi':
            self.topLayout.addRow(QLabel("Enter New SSID Name"), self.newSSIDEdit)
            thereisSSID = True

        self.topLayout.addRow(QLabel("Select interface"), self.comboInt)
        self.middelLayout.addRow(QLabel('IP old Informations'), QLabel(''))

        self.middelLayout.addRow(QLabel(f'IP= {self.ipInfo[0]}'), QLabel(''))
        self.middelLayout.addRow(QLabel(f'GATEWAY= {self.ipInfo[1]}'), QLabel(''))
        self.middelLayout.addRow(QLabel(f'DNS One= {ipInfoDns}'), QLabel(''))
        self.middelLayout.addRow(QLabel(''), QLabel(''))

        self.middelLayout.addRow(QLabel(''), QLabel(''))
        self.middelLayout.addRow(QLabel('New IP inforamtions Editing'), QLabel(''))
        self.middelLayout.addRow(QLabel(''), QLabel(''))
        self.middelLayout.addRow(QLabel("Enter New IP Address"), self.ipEdit)
        self.middelLayout.addRow(QLabel("Enter New Subnet Mask"), self.maskListItem)
        self.middelLayout.addRow(QLabel("Enter New GATWAY address"), self.gatewayEdit)
        self.middelLayout.addRow(QLabel("Add an other  DNS"), self.dnsEdit)
        self.middelLayout.addRow(QLabel(''), QLabel(''))
        self.middelLayout.addRow(QLabel(''), QLabel(''))

    def submitAction(self):
        appliedCon = self.consName.currentText()
        newName = self.newconNameEdit
        newInter = self.comboInt
        newType = self.typeCombo.currentText()
        newIp = self.ipEdit.text()
        newMask = self.maskListItem.currentText()
        newMask = newMask.split(':')[0]
        newGatway = self.gatewayEdit.text()
        newDns = self.dnsEdit.text()
        newSSID = self.newSSIDEdit.text()

        oldMask = self.ipInfo[0]
        oldMask = oldMask.replace(' ', '')
        oldMask = oldMask[-2:]
        command = 'nmcli con mod ' + appliedCon
        command += ' '

        if self.index[2] != 'auto':
            if str(newName.text()) not in ' ':
                command += ' con-name '
                command += str(newName.text())

            if newInter.currentText() not in 'no change':
                command += ' ifname '
                command += newInter.currentText()

            if str(newIp) not in ' ':
                command += ' ipv4.addresses '
                newIp = str(newIp)
                Mask = str(newMask)
                mask = str(Mask[2:])
                mask = mask.replace(' ', '')
                if mask == 'change':
                    mask = oldMask

                ipMask = f'{newIp}/{mask}'
                command += str(ipMask)

            if str(newGatway) not in ' ':
                command += ' ipv4.gateway '
                command += str(newGatway)

            if str(newDns) not in ' ':
                command += ' +ipv4.dns '
                command += str(newDns)

            if str(newSSID) not in '':
                command += '  ssid '
                command += str(newDns)

            if command.find('con-name') == -1 and command.find('ifname') == -1 and command.find(
                    'con-name') == -1 and command.find('ipv4.addresses') == -1 and command.find(
                'ipv4.gateway') == -1 and command.find('ipv4.dns') == -1 and command.find('ssid') == -1:
                QMessageBox.information(self, 'No Change', 'No Additionel changes ')
            else:
                try:
                    subprocess.run(command, check=True, shell=True)

                except subprocess.CalledProcessError:
                    QMessageBox.warning(self, 'warning', f"error Verify the fields \n")
                else:
                    QMessageBox.information(self, 'success', 'Editing Applied  Succesfully.')
                    self.close()
        else:
            if str(newName.text()) not in ' ':
                command += ' con-name '
                command += str(newName.text())
            if newInter.currentText() not in 'no change':
                command += ' ifname '
                command += newInter.currentText()
            if str(newType) not in 'no change':
                command += ' connection.type '
                command += str(newType)
            if str(newSSID) not in '':
                command += '  ssid '
                command += str(newSSID)
            if command.find('con-name') == -1 and command.find('ifname') == -1 and command.find(
                    'con-name') == -1 and command.find('ssid') == -1:
                QMessageBox.information(self, 'No Change', 'No Additionel changes ')
            else:
                try:
                    subprocess.run(command, check=True, shell=True)
                except subprocess.CalledProcessError:
                    QMessageBox.warning(self, 'warning', f"error Verify the fields \n")
                else:
                    QMessageBox.information(self, 'success', 'Editing Applied  Succesfully.')
                    self.close()

    def cancelAction(self):
        self.close()


class DeleteNetworkWindow(QWidget):
    def __init__(self, d):
        super().__init__()
        self.setGeometry(200, 50, 300, 300)
        self.setWindowTitle("Delete a Connection")
        self.listUsersToDelete = d
        self.index = d

        self.layouts()
        self.widgets()

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QFormLayout()
        self.middelLayout = QFormLayout()
        self.topLayout.setContentsMargins(20, 20, 20, 20)
        self.bottomLayout = QHBoxLayout()

        self.submitBtn = QPushButton("Submit")
        self.submitBtn.clicked.connect(self.submitAction)
        self.cancelBtn = QPushButton("Cancel")
        self.cancelBtn.clicked.connect(self.cancelAction)
        self.submitBtn.setFixedHeight(30)
        self.cancelBtn.setFixedHeight(30)
        self.submitBtn.setStyleSheet("color: #ecf0f1; background-color: #27ae60 ; border: 0px solid #27ae60")
        self.cancelBtn.setStyleSheet("color: #ecf0f1; background-color: #e74c3c; border: 0px solid #e74c3c")

        self.bottomLayout.addWidget(self.submitBtn)
        self.bottomLayout.addWidget(self.cancelBtn)
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addStretch()
        self.mainLayout.addLayout(self.middelLayout)
        self.mainLayout.addStretch()
        self.mainLayout.addLayout(self.bottomLayout)
        self.setLayout(self.mainLayout)

    def widgets(self):
        self.deleteConnections = QComboBox()
        self.selectCon = QPushButton('Select', self)
        self.selectCon.clicked.connect(self.addConToDelToList)
        self.consName = QComboBox(self)
        self.consName.addItems(self.listUsersToDelete)
        self.topLayout.addRow(QLabel("Please Select Connection  Name To Applay It "), self.consName)
        self.topLayout.addRow(self.selectCon, QLabel(''))
        self.middelLayout.addRow(QLabel("Connections To Delete Are"), self.deleteConnections)

    def addConToDelToList(self):
        item = self.consName.currentText()
        self.deleteConnections.addItem(item)

    def submitAction(self):
        try:
            self.progeesBar.setHidden(False)
            self.progeesBar.setMaximum(len(self.listUsersToDelete))
            self.progeesBar.setValue(0)
            self.deleteuser()
        except subprocess.CalledProcessError:
            QMessageBox.warning(self, 'warning', f"error occured during setting this hostname\n")
        else:
            self.submitBtn.setHidden(True)
            self.cancelBtn.setHidden(True)
            self.okBtn.setHidden(False)

    def submitAction(self):

        AllItems = [self.deleteConnections.itemText(i) for i in range(self.deleteConnections.count())]

        myset = set(AllItems)
        command = 'nmcli con delete'
        for i in myset:
            i = i.replace(' ', '\\ ')
            command += f' {str(i)} '

        try:
            print(command)
            subprocess.run(command, check=True, shell=True)

        except subprocess.CalledProcessError:
            QMessageBox.warning(self, 'warning', f"error occured during Deletion Connections \n")
        else:

            QMessageBox.information(self, 'success', f'Deletion  Applied  Succesfully  ')
            self.close()

    def okAction(self):
        self.close()

    def deleteuserThreading(self, username):
        try:
            subprocess.run(f'userdel -r {username}', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True,
                           shell=True)
        except subprocess.CalledProcessError:
            return f"error occured during deleting {username}"
        else:
            return f"{username} deleted succesfully!"

    def clearAction(self):
        pass

    def cancelAction(self):
        self.close()
