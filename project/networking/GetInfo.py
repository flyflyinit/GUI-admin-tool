from PyQt5.QtWidgets import *
import subprocess

from project.networking.networkingScripts import displayNetworkInterface
from project.networking.displayConnections import displayConnection


class GetInfo(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200,50,600,400)
        self.setWindowTitle("Add New Connection")
        self.UI()

    def UI(self):
        self.layouts()
        self.widgets()
        print("ffffffffffff")

    def layouts(self):
        pass


    def widgets(self):
        pass



############################################################################################################################
class EditNetworkWindow(QWidget):
    def __init__(self,d):
        super().__init__()
        self.setGeometry(200,50,300,400)
        self.setWindowTitle("Configure System")
        for i in d:
            if d[i].isSelected == True:

                print(i+' selected')
        self.layouts()
        self.widgets()

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QFormLayout()
        self.middelLayout = QFormLayout()
        self.middelLayout.setContentsMargins(20,20,20,20)
        self.topLayout.setContentsMargins(20,20,20,20)
        self.bottomLayout=QHBoxLayout()

        self.submitBtn=QPushButton("Submit")
        self.submitBtn.clicked.connect(self.submitAction)
        self.cancelBtn=QPushButton("Cancel")

        self.submitBtn.setFixedHeight(30)
        self.cancelBtn.setFixedHeight(30)
        self.submitBtn.setStyleSheet("color: #ecf0f1; background-color: #27ae60 ; border: 0px solid #27ae60" )
        self.cancelBtn.setStyleSheet("color: #ecf0f1; background-color: #e74c3c; border: 0px solid #e74c3c")

        self.bottomLayout.addWidget(self.submitBtn)
        self.bottomLayout.addWidget(self.cancelBtn)
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.middelLayout)
        self.mainLayout.addStretch()
        self.mainLayout.addLayout(self.bottomLayout)
        self.setLayout(self.mainLayout)

    def widgets(self):
        self.consName = QComboBox(self)
        self.comboInt = QComboBox()
        consNames=displayConnection()
        consNames.pop()
        self.consName.addItems(consNames)

        interName = displayNetworkInterface()
        self.comboInt.addItem('no change')
        self.comboInt.addItems(interName)
        self.newconNameEdit = QLineEdit()

        self.operation= QComboBox()
        #self.operation.currentIndexChanged.connect(self.clickingEvent)
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


        #user entery
        self.newconNameEdit = QLineEdit()
        self.ipEdit = QLineEdit()
        self.gatewayEdit = QLineEdit()
        self.dnsEdit = QLineEdit()
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


        self.topLayout.addRow(QLabel("Please Select Connection  Name To Applay It "), self.consName)
        self.topLayout.addRow(QLabel(''), QLabel(''))

        self.topLayout.addRow(QLabel("Enter New Connection's Name"), self.newconNameEdit)
        self.topLayout.addRow(QLabel("Select interface"),self.comboInt)
        self.topLayout.addRow(QLabel("Enter New IP Address"), self.ipEdit)
        self.topLayout.addRow(QLabel("Enter New Subnet Mask"), self.maskListItem)
        self.topLayout.addRow(QLabel("Change Connection Type"), self.typeCombo)
        self.topLayout.addRow(QLabel("Enter New GATWAY address"), self.gatewayEdit)
        self.topLayout.addRow(QLabel("Change Primary DNS"), self.dnsEdit)


    def submitAction(self):
        appliedCon=self.consName.currentText()
        newName=self.newconNameEdit
        newInter=self.comboInt
        newType=self.typeCombo.currentText()
        newIp=self.ipEdit.text()
        newMask=self.maskListItem.currentText()
        newMask=newMask.split(':')[0]
        newGatway=self.gatewayEdit.text()
        newDns=self.dnsEdit.text()

        command='nmcli con mod '+appliedCon
        command+=' '

        if str(newName.text()) not in ' ':
            command+=' con-name '
            command+=str(newName.text())

        if newInter.currentText() not in 'no change':
            command+=' ifname '
            command+=newInter.currentText()

        if str(newType) not in 'no change':
            command+=' connection.type '
            command+=str(newType)

        if str(newIp) not in ' ' and str(newMask):
            command += ' ipv4.addresses '
            newIp=str(newIp)
            Mask = str(newMask)
            mask = str(Mask[2:])
            ipMask = f'{newIp}/{mask}'
            command+=str(ipMask)


        if str(newGatway) not in ' ':
            command += ' ipv4.gateway '
            command += str(newGatway)

        if str(newDns) not in ' ':
            command += ' ipv4.dns '
            command += str(newDns)


        if command.find('con-name')== -1 and command.find('ifname')== -1 and  command.find('con-name')== -1 and  command.find('connection.type')== -1 and command.find('ipv4.addresses')== -1 and command.find('ipv4.gateway')== -1 and  command.find('ipv4.dns')== -1 :
             QMessageBox.information(self,'No Change','No Additionel changes ')

        else:
            try:
                subprocess.run(command, check=True, shell=True)

            except subprocess.CalledProcessError:
                print(command)
                QMessageBox.warning(self, 'warning', f"error Verify Mask Field or Other Mising Field \n")
            else:
                QMessageBox.information(self, 'success', 'Add a New  Connection Applied  Succesfully.')
                self.close()

    def cancelAction(self):

        self.close()

##################################################################################################""
class DeleteNetworkWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200,50,300,400)
        self.setWindowTitle("Configure System")
        self.layouts()
        self.widgets()

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QFormLayout()
        self.middelLayout = QFormLayout()
        self.topLayout.setContentsMargins(20,20,20,20)
        self.bottomLayout=QHBoxLayout()

        self.submitBtn=QPushButton("Submit")
        self.submitBtn.clicked.connect(self.submitAction)
        self.cancelBtn=QPushButton("Cancel")
        self.cancelBtn.clicked.connect(self.cancelAction)
        self.clearBtn = QPushButton("Clear List")
        self.clearBtn.clicked.connect(self.clearAction)
        self.submitBtn.setFixedHeight(30)
        self.cancelBtn.setFixedHeight(30)
        self.clearBtn.setFixedHeight(30)
        self.submitBtn.setStyleSheet("color: #ecf0f1; background-color: #27ae60 ; border: 0px solid #27ae60" )
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
        self.deleteConnections=QComboBox()
        self.selectCon=QPushButton('Select',self)
        self.selectCon.clicked.connect(self.addConToDelToList)
        self.consName = QComboBox(self)


        # fetch connections

        try:
            subprocess.run("nmcli con sh | awk '{print $1}' > /tmp/connections.txt", check=True, shell=True)
            deviceFile = open('/tmp/connections.txt', 'rt')
            device = deviceFile.read()
            conName = device.splitlines()
            conName.pop(0)
            self.consName.addItems(conName)
        except:
            print("Can't fetch connections ")

        self.topLayout.addRow(QLabel("Please Select Connection  Name To Applay It "), self.consName)
        self.topLayout.addRow(self.selectCon, QLabel(''))
        self.middelLayout.addRow(QLabel("Connections To Delete Are"), self.deleteConnections)

    def  addConToDelToList(self):

        item=self.consName.currentText()
        self.deleteConnections.addItem(item)

    def submitAction(self):

        AllItems = [self.deleteConnections.itemText(i) for i in range(self.deleteConnections.count())]
        myset=set(AllItems)
        command= 'nmcli con delete'
        for i in myset:
            command+=f' {str(i)} '

        try:
            subprocess.run(command, check=True, shell=True)

        except subprocess.CalledProcessError:
            QMessageBox.warning(self, 'warning', f"error occured during Deletion Connections \n")
        else:

            QMessageBox.information(self, 'success', f'Deletion  Applied  Succesfully  ')
            self.close()

    def clearAction(self):
        pass

    def cancelAction(self):
            self.close()

