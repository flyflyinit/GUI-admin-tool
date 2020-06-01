from PyQt5.QtWidgets import *
from project.firewall.firewallScripts import *
from project.networking.networkingScripts import displayNetworkInterface


class CreateFwWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 50, 300, 400)
        self.setWindowTitle("Configure Firewall Run Time")
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
        self.clearBtn = QPushButton("Clear List")
        self.clearBtn.clicked.connect(self.clearAction)
        self.submitBtn.setFixedHeight(30)
        self.cancelBtn.setFixedHeight(30)
        self.clearBtn.setFixedHeight(30)
        self.submitBtn.setStyleSheet("color: #ecf0f1; background-color: #27ae60 ; border: 0px solid #27ae60")
        self.cancelBtn.setStyleSheet("color: #ecf0f1; background-color: #e74c3c; border: 0px solid #e74c3c")

        self.bottomLayout.addWidget(self.submitBtn)
        self.bottomLayout.addWidget(self.cancelBtn)
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addStretch()


        self.mainLayout.addLayout(self.middelLayout)
        self.mainLayout.addStretch()
        self.mainLayout.addLayout(self.bottomLayout)
        self.mainLayout.addStretch()
        self.mainLayout.addStretch()

        self.setLayout(self.mainLayout)

    def widgets(self):
        self.operation = QListWidget(self)

        self.operation.clicked.connect(self.addOperationsClick)
        self.operation.addItem('Add Interface To Zone')
        self.operation.addItem('Add Service To Default Zone')
        self.operation.addItem('Add Service To A Specific Zone')
        self.operation.addItem('Add Protocol and Port')
        self.topLayout.addRow(QLabel("Please Select Operations To Applay It "), QLabel())
        self.topLayout.addRow(self.operation, QLabel())
        self.middelLayout.addRow(QLabel(""), QLabel(""))


        # after click Widget

    def addOperationsClick(self):
        self.createNewZone = QLineEdit()
        self.createNewZone.setPlaceholderText('Enter name from New Zone ')
        self.clearMiddel()
        self.task = self.operation.currentItem().text()
        itemsA = listZones()
        itemsB = listAllServices()
        self.zones = QComboBox(self)
        self.zones.addItems(itemsA)
        self.servies = QComboBox(self)
        self.servies.addItems(itemsB)
        zone = defaultZone()
        zone = zone[0]
        self.interfaces=QComboBox(self)
        self.interfaces.addItems(displayNetworkInterface())

        self.port=QComboBox(self)
        self.selectProtocol=QComboBox()
        self.selectProtocol.addItem('tcp')
        self.selectProtocol.addItem('udp')
        self.selectPort=QLineEdit()

        if self.task in 'Add Service To A Specific Zone':

            self.middelLayout.addRow(QLabel('Select a Service :'), self.servies)
            self.middelLayout.addRow(QLabel('Select a Zone :'), self.zones)
            self.middelLayout.addRow(QLabel(""), QLabel(""))

        elif self.task in 'Add Interface To Zone':
            self.middelLayout.addRow(QLabel('Select an Interface :'), self.interfaces)
            self.middelLayout.addRow(QLabel('Select a Zone :'), self.zones)

        elif self.task in 'Add Service To Default Zone':

            self.middelLayout.addRow(QLabel('Select a Service :'), self.servies)
            self.middelLayout.addRow(QLabel('Default Zone Is:'), QLabel(f'{zone}'))

        elif self.task in 'Add Protocol and Port':

            self.middelLayout.addRow(QLabel('Select a Service :'), self.selectProtocol)
            self.middelLayout.addRow(QLabel('Select a Port :'), self.selectPort)

    def submitAction(self):

        self.mbox = QMessageBox.question(self, "Warningg!", f"Are you sure to Apply :\n {self.task} ?",QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if self.mbox == QMessageBox.Yes:

            try:
                self.takeAction()

            except :
                QMessageBox.critical(self, 'error', f'error occured during Applaying this \n {self.task} ')

            else:
                QMessageBox.information(self, 'success',f'Task Done Succesfully')


    def clearAction(self):
        pass

    def cancelAction(self):
        self.close()

    def clearMiddel(self):

        for i in reversed(range(self.middelLayout.count())):
                self.middelLayout.itemAt(i).widget().setParent(None)

    def takeAction(self):
        par1 = Par2 =''
        if self.task=='Add Service To A Specific Zone':
            par1 = self.servies.currentText()
            par2 = self.zones.currentText()
            addServiceToSpecificZone(par1, par2)

        elif self.task in 'Add Interface To Zone':
            par1 = self.interfaces.currentText()
            par2 = self.zones.currentText()
            addInterfaceToZone(par1, par2)
        elif self.task in 'Add Service To Default Zone':
            par1 = self.servies.currentText()
            addServiceToDefaultZone(par1)

        elif self.task in 'Add Protocol and Port':
            par1 = self.selectProtocol.currentText()
            par2 = self.selectPort.text()
            addPort(par2,par1)

############################################################################################################################
class EditFwWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200,50,300,400)
        self.setWindowTitle("Configure System Permanent Mode")
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
        self.clearBtn = QPushButton("Clear List")
        self.clearBtn.clicked.connect(self.clearAction)
        self.submitBtn.setFixedHeight(30)
        self.cancelBtn.setFixedHeight(30)
        self.clearBtn.setFixedHeight(30)
        self.submitBtn.setStyleSheet("color: #ecf0f1; background-color: #27ae60 ; border: 0px solid #27ae60")
        self.cancelBtn.setStyleSheet("color: #ecf0f1; background-color: #e74c3c; border: 0px solid #e74c3c")

        self.bottomLayout.addWidget(self.submitBtn)
        self.bottomLayout.addWidget(self.cancelBtn)
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addStretch()

        self.mainLayout.addLayout(self.middelLayout)
        self.mainLayout.addStretch()
        self.mainLayout.addLayout(self.bottomLayout)
        self.mainLayout.addStretch()
        self.mainLayout.addStretch()

        self.setLayout(self.mainLayout)

    def widgets(self):
        self.operation = QListWidget(self)

        self.operation.clicked.connect(self.addOperationsClick)
        self.operation.addItem('Add Permanent a New zone')
        self.operation.addItem('Add Permanent Interface To Zone')
        self.operation.addItem('Add Permanent a Service To Default Zone')
        self.operation.addItem('Add Permanent a Service To A Specific Zone')
        self.operation.addItem('Add Permanent Protocol and Port')
        self.operation.addItem('Remove Permanent a inteface From A Specific Zone')
        self.operation.addItem('Remove Permanent a Zone')
        self.operation.addItem('Remove Permanent a Service From Default Zone')
        self.operation.addItem('Remove Permanent a Service From Specific Zone')
        self.operation.addItem('Remove Permanent a Protocol')
        self.topLayout.addRow(QLabel("Please Select Operations To Applay It "), QLabel())
        self.topLayout.addRow(self.operation, QLabel())
        self.middelLayout.addRow(QLabel(""), QLabel(""))

        # after click Widget

    def addOperationsClick(self):

        self.clearMiddel()
        self.task = self.operation.currentItem().text()

        itemsA = listZones()
        itemsB = listAllServices()
        self.zones = QComboBox(self)
        self.zones.addItems(itemsA)

        self.servies = QComboBox(self)
        self.servies.addItems(itemsB)
        zone = defaultZone()
        zone = zone[0]

        self.interfaces = QComboBox(self)
        self.interfaces.addItems(displayNetworkInterface())

        self.port = QComboBox(self)
        self.createNewZone=QLineEdit()
        self.createNewZone.setPlaceholderText('Enter name from New Zone ')
        self.port = QComboBox(self)
        self.selectProtocol = QComboBox()
        self.selectProtocol.addItem('tcp')
        self.selectProtocol.addItem('udp')
        self.selectPort = QLineEdit()


        #add new zone
        if self.task in 'Add Permanent a New zone':

            self.middelLayout.addRow(QLabel(""), QLabel(""))
            self.middelLayout.addRow(QLabel(''), self.createNewZone)

        elif self.task in 'Add Permanent Interface To Zone':

            self.middelLayout.addRow(QLabel('Select an Interface :'), self.interfaces)
            self.middelLayout.addRow(QLabel('Select a Zone :'), self.zones)
            self.middelLayout.addRow(QLabel(""), QLabel(""))


        elif self.task in 'Add Permanent a Service To Default Zone':

            self.middelLayout.addRow(QLabel('Select a Service :'), self.servies)
            self.middelLayout.addRow(QLabel('Default Zone Is:'), QLabel(f'{zone}'))

        elif self.task in 'Add Permanent a Service To A Specific Zone':

            self.middelLayout.addRow(QLabel('Select a Service :'), self.servies)
            self.middelLayout.addRow(QLabel('Select a Zone :'), self.zones)

        elif self.task in 'Add Permanent Protocol and Port':

            self.middelLayout.addRow(QLabel('Select a Service :'), self.selectProtocol)
            self.middelLayout.addRow(QLabel('Select a Port :'), self.selectPort)


        #Remove
        elif self.task in 'Remove Permanent a inteface From A Specific Zone':

            self.middelLayout.addRow(QLabel('Select an Interface :'), self.interfaces)
            self.middelLayout.addRow(QLabel('Select a Zone :'), self.zones)
            self.middelLayout.addRow(QLabel(""), QLabel(""))

        elif self.task in 'Remove Permanent a Zone':

            self.middelLayout.addRow(QLabel(""), QLabel(""))
            self.middelLayout.addRow(QLabel('Select a Zone :'), self.zones)


        elif self.task in 'Remove Permanent a Service From Default Zone':

            self.middelLayout.addRow(QLabel(""), QLabel(""))

            self.middelLayout.addRow(QLabel('Select a Service :'), self.servies)
            self.middelLayout.addRow(QLabel('Default Zone Is:'), QLabel(f'{zone}'))

        elif self.task in 'Remove Permanent a Service From Specific Zone':
            self.middelLayout.addRow(QLabel(""), QLabel(""))
            self.middelLayout.addRow(QLabel('Select a Service :'), self.servies)
            self.middelLayout.addRow(QLabel('Select a Zone :'), self.zones)


        elif self.task in 'Remove Permanent a Protocol':
            self.middelLayout.addRow(QLabel(""), QLabel(""))
            self.middelLayout.addRow(QLabel('Select a Service :'), self.selectProtocol)
            self.middelLayout.addRow(QLabel('Select a Port :'), self.selectPort)


    def submitAction(self):

        self.mbox = QMessageBox.question(self, "Warningg!", f"Are you sure to Apply :\n {self.task} ?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if self.mbox == QMessageBox.Yes:

            try:
                self.takeAction()
            except:
                QMessageBox.critical(self, 'error', f'error occured during Applaying this \n {self.task} ')

            else:
                QMessageBox.information(self, 'success', f'Task Done Succesfully')

    def clearAction(self):
        pass

    def cancelAction(self):
        self.close()

    def clearMiddel(self):
        for i in reversed(range(self.middelLayout.count())):
            self.middelLayout.itemAt(i).widget().setParent(None)
    def takeAction(self):
        par1=Par2=None

        if self.task in 'Add Permanent a New zone':
            par1 = self.createNewZone.text()
            addPermanentNewZone(par1)

        elif self.task in 'Add Permanent Interface To Zone':
            par1 = self.interfaces.currentText()
            par2 = self.zones.currentText()
            addPermanentInterfaceToZone(par1, par2)


        elif self.task in 'Add Service To Default Zone':
            par1 = self.servies.currentText()
            addPermanentServiceDefaultZone(par1)

        elif self.task in 'Add Permanent a Service To A Specific Zone':
            par1 = self.servies.currentText()
            par2 = self.zones.currentText()
            addPermanentServiceToSpecificZone(par1, par2)

        elif self.task in 'Add Permanent Protocol and Port':
            par1 = self.selectProtocol.currentText()
            par2 = self.selectPort.text()
            addPermanetProtocolPort(par2, par1)

        #Remove

        elif self.task in 'Remove Permanent a inteface From A Specific Zone':
            par1 = self.interfaces.currentText()
            par2 = self.zones.currentText()
            RemoveInterfaceFromZone(par2, par1)

        elif self.task in 'Remove Permanent a Zone':
            par1 = self.zones.currentText()
            RemoveZone(par1)


        elif self.task in 'Remove Permanent a Service From Default Zone':
            par1 = self.servies.currentText()
            removePermanentServiceFromDefaultZone(par1)


        elif self.task in 'Remove Permanent a Service From Specific Zone':
            par1 = self.servies.currentText()
            par2 = self.zones.currentText()
            RemovePermanetServiceFromSpecificZone(par1, par2)

        elif self.task in 'Remove Permanent a Protocol':
            par1 = self.selectProtocol.currentText()
            par2 = self.selectPort.currentText()
            RemovePermanetProtocolPort(par1, par2)


##################################################################################################""
class DeleteFwWindow(QWidget):
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
        self.topLayout.setContentsMargins(20, 20, 20, 20)
        self.bottomLayout = QHBoxLayout()

        self.submitBtn = QPushButton("Submit")
        self.submitBtn.clicked.connect(self.submitAction)
        self.cancelBtn = QPushButton("Cancel")
        self.cancelBtn.clicked.connect(self.cancelAction)
        self.clearBtn = QPushButton("Clear List")
        self.clearBtn.clicked.connect(self.clearAction)
        self.submitBtn.setFixedHeight(30)
        self.cancelBtn.setFixedHeight(30)
        self.clearBtn.setFixedHeight(30)
        self.submitBtn.setStyleSheet("color: #ecf0f1; background-color: #27ae60 ; border: 0px solid #27ae60")
        self.cancelBtn.setStyleSheet("color: #ecf0f1; background-color: #e74c3c; border: 0px solid #e74c3c")

        self.bottomLayout.addWidget(self.submitBtn)
        self.bottomLayout.addWidget(self.cancelBtn)
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addStretch()

        self.mainLayout.addLayout(self.middelLayout)
        self.mainLayout.addStretch()
        self.mainLayout.addLayout(self.bottomLayout)
        self.mainLayout.addStretch()
        self.mainLayout.addStretch()

        self.setLayout(self.mainLayout)

    def widgets(self):
        self.operation = QListWidget(self)

        self.operation.clicked.connect(self.addOperationsClick)
        self.operation.addItem('Remove Interface To Zone')
        self.operation.addItem('Remove a Specific Zone')
        self.operation.addItem('Remove Service To Default Zone')
        self.operation.addItem('Remove a Service From A Specific Zone')
        self.operation.addItem('Remove a protocol and Port')
        self.topLayout.addRow(QLabel("Please Select Operations To Applay It "), QLabel())
        self.topLayout.addRow(self.operation, QLabel())
        self.middelLayout.addRow(QLabel(""), QLabel(""))

        # after click Widget

    def addOperationsClick(self):

        self.clearMiddel()
        self.task = self.operation.currentItem().text()

        itemsA = listZones()
        itemsB = listAllServices()
        self.zones = QComboBox(self)
        self.zones.addItems(itemsA)

        self.servies = QComboBox(self)
        self.servies.addItems(itemsB)
        zone = defaultZone()
        zone = zone[0]

        self.interfaces = QComboBox(self)
        self.interfaces.addItems(displayNetworkInterface())

        self.port = QComboBox(self)
        self.selectProtocol = QComboBox()
        self.selectProtocol.addItem('tcp')
        self.selectProtocol.addItem('udp')
        self.selectPort = QLineEdit()


        if self.task in 'Remove Interface To Zone':

            self.middelLayout.addRow(QLabel('Select an Interface :'), self.interfaces)
            self.middelLayout.addRow(QLabel('Select a Zone :'), self.zones)


        elif self.task in 'Remove a Specific Zone':
            self.middelLayout.addRow(QLabel('Select a Zone :'), self.zones)



        elif self.task in 'Remove Service To Default Zone':

            self.middelLayout.addRow(QLabel('Select a Service :'), self.servies)
            self.middelLayout.addRow(QLabel('Default Zone Is:'), QLabel(f'{zone}'))


        elif self.task in 'Remove a Service From A Specific Zone':

            self.middelLayout.addRow(QLabel('Select a Service :'), self.servies)
            self.middelLayout.addRow(QLabel('Select a Zone :'), self.zones)


        elif self.task in 'Remove a protocol and Port':
            self.middelLayout.addRow(QLabel('Select a Protocol :'), self.selectProtocol)
            self.middelLayout.addRow(QLabel('Select a Port :'), self.selectPort)



    def submitAction(self):

        self.mbox = QMessageBox.question(self, "Warningg!", f"Are you sure to Apply :\n {self.task} ?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if self.mbox == QMessageBox.Yes:

            try:
                self.takeAction()

            except:
                QMessageBox.critical(self, 'error', f'error occured during Applaying this \n {self.task} ')

            else:
                QMessageBox.information(self, 'success', f'Task Done Succesfully')

    def clearAction(self):
        pass

    def cancelAction(self):
        self.close()

    def clearMiddel(self):

        for i in reversed(range(self.middelLayout.count())):
            self.middelLayout.itemAt(i).widget().setParent(None)

    def takeAction(self):
        par1 =par2=None
        if self.task in 'Remove Interface To Zone':

            par1 = self.interfaces.currentText()
            par2 = self.zones.currentText()
            RemoveInterfaceFromZone(par1, par2)

        elif self.task in 'Remove a Specific Zone':
            par1 = self.zones.currentText()
            RemoveZone(par1)
        elif self.task in 'Remove Service To Default Zone':
            par1 = self.servies.currentText()
            removeServiceFromDefaultZone(par1)
        elif self.task in 'Remove a Service From A Specific Zone':
            par1 = self.servies.currentText()
            par2 = self.zones.currentText()
            RemoveServiceToZone(par1, par2)

        elif self.task in 'Remove a protocol and Port':
            par1 = self.selectProtocol.currentText()
            par2 = self.selectPort.text()
            RemoveProtocolPort(par2, par1)
