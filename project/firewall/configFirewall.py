from PyQt5.QtWidgets import *
from project.firewall.firewallScripts import *
from project.networking.networkingScripts import displayNetworkInterface
from project.firewall.tableFirewall import *


class CreateFwWindow(QWidget):
    def __init__(self,par):
        super().__init__()
        self.parZone=par[0]
        self.setGeometry(200, 50, 300, 400)
        self.setWindowTitle("Add on Run Time ")
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
        self.operation.addItem('Add a New Zone')
        self.operation.addItem('Add Interface To Zone')
        self.operation.addItem('Add Service To Default Zone')
        self.operation.addItem('Add Service To A Specific Zone')
        self.operation.addItem('Add Protocol and Port')
        self.topLayout.addRow(QLabel(f"Zone Selected is : {self.parZone} "), QLabel())
        self.topLayout.addRow(QLabel("Please Select Operations To Applay It "), QLabel())
        self.middelLayout.addRow(QLabel(""), QLabel(""))
        self.middelLayout.addRow(QLabel(""), QLabel(""))
        self.topLayout.addRow(QLabel(""), QLabel(""))
        self.topLayout.addRow(QLabel(""), QLabel(""))

        self.topLayout.addRow(self.operation, QLabel())
        self.middelLayout.addRow(QLabel(""), QLabel(""))
        # after click Widget

    def addOperationsClick(self):
        self.createNewZone = QLineEdit()
        self.createNewZone.setPlaceholderText('Enter name from New Zone ')
        self.clearMiddel()
        self.task = self.operation.currentItem().text()
        #itemsA = listZones()
        itemsB = listAllServices()
        self.zones = QComboBox(self)
        #self.zones.addItems(itemsA)
        self.zones.addItem(self.parZone)
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
            self.middelLayout.addRow(QLabel('Selected Zone :'), self.zones)
            self.middelLayout.addRow(QLabel(""), QLabel(""))

        elif self.task in 'Add Interface To Zone':
            self.middelLayout.addRow(QLabel('Select an Interface :'), self.interfaces)
            self.middelLayout.addRow(QLabel('Selected Zone :'), self.zones)

        elif self.task in 'Add Service To Default Zone':

            self.middelLayout.addRow(QLabel('Select a Service :'), self.servies)
            self.middelLayout.addRow(QLabel('Default Zone Is:'), QLabel(f'{zone}'))

        elif self.task in 'Add Protocol and Port':
            self.middelLayout.addRow(QLabel('Selected Zone :'), self.zones)
            self.middelLayout.addRow(QLabel('Select a Service :'), self.selectProtocol)
            self.middelLayout.addRow(QLabel('Select a Port :'), self.selectPort)

        elif self.task in 'Add a New Zone':
            self.middelLayout.addRow(QLabel(""), QLabel(""))
            self.middelLayout.addRow(QLabel(''), self.createNewZone)


        self.middelLayout.addRow(QLabel(""), QLabel(""))
        self.middelLayout.addRow(QLabel(""), QLabel(""))

    def clearMiddel(self):

        for i in reversed(range(self.middelLayout.count())):
                self.middelLayout.itemAt(i).widget().setParent(None)

    def submitAction(self):

        self.mbox = QMessageBox.question(self, "Warningg!", f"Are you sure to Apply :\n {self.task} ?",QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if self.mbox == QMessageBox.Yes:

            try:

                par1 = Par2 = ''
                if self.task == 'Add Service To A Specific Zone':
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

                    try:
                        par1 = self.selectProtocol.currentText()
                        par2 = self.selectPort.text()
                        int(par2)
                    except ValueError:
                        QMessageBox.warning(self, 'error', f'Port numnber must be an Integer')
                        return
                    else:
                        addPort(par2, par1)

                elif self.task in 'Add a New Zone':
                    par1 = self.createNewZone.text()

                    if par1=='':

                        QMessageBox.warning(self, 'error', f'\n You must enter a name ')
                        return
                    else:
                        addPermanentNewZone(par1)

            except :
                QMessageBox.critical(self, 'error', f'error occured during Applaying this \n {self.task} ')
                self.clearMiddel()

            else:
                QMessageBox.information(self, 'success',f'Task Done Succesfully')
                self.clearMiddel()
        elif self.mbox == QMessageBox.No:
            self.clearMiddel()

    def clearAction(self):
        pass

    def cancelAction(self):
        self.close()

    def clearMiddel(self):

        for i in reversed(range(self.middelLayout.count())):
                self.middelLayout.itemAt(i).widget().setParent(None)


############################################################################################################################
class EditFwWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200,50,300,400)
        self.setWindowTitle("Cancel configuration - Permanent Mode configuration ")
        self.layouts()
        self.widgets()
        self.zone=''
        print(self.zone)
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
        self.applayNewCh = QRadioButton("Save The New Changes Permanently ")
        self.cancelNewCh = QRadioButton("Cancel The New Changes")

        self.topLayout.addRow(QLabel(""), QLabel(""))
        self.topLayout.addRow(self.cancelNewCh,QLabel(""))
        self.topLayout.addRow(QLabel(""), QLabel(""))
        self.topLayout.addRow(self.applayNewCh,QLabel(""))


    def clearMiddel(self):
        for i in reversed(range(self.middelLayout.count())):
            self.middelLayout.itemAt(i).widget().setParent(None)


    def submitAction(self):

        if self.cancelNewCh.isChecked() :
            self.mbox = QMessageBox.question(self, "Warningg!", "\n Are You Shure To Cancel The New Configurations ?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if self.mbox == QMessageBox.Yes:
                try:
                    subprocess.run("firewall-cmd --reload ", check=True, shell=True)

                except subprocess.CalledProcessError:
                    QMessageBox.critical(self, 'Error', '\n Error Can not Cancel the New Changes  ')
                else:
                    QMessageBox.information(self, 'success', ' \n Configuration has been  Canceled  Succesfully.')

            elif self.mbox == QMessageBox.No:
                return
            else:
                return

        elif self.applayNewCh.isChecked():
            self.mbox = QMessageBox.question(self, "Warningg!", "\n Are You Shure To Save The New Configurations Permanently ?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if self.mbox == QMessageBox.Yes:
                try:
                    subprocess.run("firewall-cmd --runtime-to-permanent", check=True, shell=True)
                except subprocess.CalledProcessError:
                    QMessageBox.critical(self, 'Error', '\n Error Can not save the New Changes  ')
                else:
                    QMessageBox.information(self, 'success', 'New Configuration are Saved Succesfully.')

            elif self.mbox == QMessageBox.No:
                return
            else:
                return



    def clearAction(self):
        pass

    def cancelAction(self):
        self.close()

    def clearMiddel(self):
        for i in reversed(range(self.middelLayout.count())):
            self.middelLayout.itemAt(i).widget().setParent(None)


##################################################################################################""
class DeleteFwWindow(QWidget):
    def __init__(self,par):
        super().__init__()
        self.parZone=par[0]
        self.setGeometry(200,50,300,400)
        self.setWindowTitle("Delete Run Time")
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
        self.operation.addItem('Remove a Zone')
        self.operation.addItem('Remove Interface To Zone')
        self.operation.addItem('Remove Service To Default Zone')
        self.operation.addItem('Remove a Service From A Specific Zone')
        self.operation.addItem('Remove a protocol and Port')
        self.topLayout.addRow(QLabel(f"Zone Selected is : {self.parZone} "), QLabel())
        self.topLayout.addRow(QLabel("Please Select Operations To Applay It "), QLabel())
        self.middelLayout.addRow(QLabel(""), QLabel(""))
        self.middelLayout.addRow(QLabel(""), QLabel(""))
        self.topLayout.addRow(QLabel(""), QLabel(""))
        self.topLayout.addRow(QLabel(""), QLabel(""))

        self.topLayout.addRow(self.operation, QLabel())
        self.middelLayout.addRow(QLabel(""), QLabel(""))

        # after click Widget

    def addOperationsClick(self):

        self.clearMiddel()
        self.task = self.operation.currentItem().text()

        itemsA = listZones()
        itemsB = listservices(self.parZone)
        self.zones = QComboBox(self)
        self.zones.addItem(self.parZone)

        #add new code


        self.servies = QComboBox(self)
        self.servies.addItems(itemsB)
        zone = defaultZone()
        zone = zone[0]

        self.interfaces = QComboBox(self)
        self.interfaces.addItems(listinterfaces(self.parZone))

        self.port = QComboBox(self)
        self.selectProtocol = QComboBox()
        self.selectProtocol.addItem('tcp')
        self.selectProtocol.addItem('udp')
        self.selectPort = QLineEdit()


        if self.task in 'Remove Interface To Zone':

            self.middelLayout.addRow(QLabel('Select an Interface :'), self.interfaces)
            self.middelLayout.addRow(QLabel('Selected Zone :'), self.zones)


        elif self.task in 'Remove a Zone':
            self.middelLayout.addRow(QLabel('Selected Zone :'), self.zones)



        elif self.task in 'Remove Service To Default Zone':

            self.middelLayout.addRow(QLabel('Select a Service :'), self.servies)
            self.middelLayout.addRow(QLabel('Default Zone Is:'), QLabel(f'{zone}'))


        elif self.task in 'Remove a Service From A Specific Zone':

            self.middelLayout.addRow(QLabel('Select a Service :'), self.servies)
            self.middelLayout.addRow(QLabel('Selected Zone :'), self.zones)


        elif self.task in 'Remove a protocol and Port':
            self.middelLayout.addRow(QLabel('Selected Zone :'), self.zones)
            self.middelLayout.addRow(QLabel('Select a Protocol :'), self.selectProtocol)
            self.middelLayout.addRow(QLabel('Select a Port :'), self.selectPort)

        self.middelLayout.addRow(QLabel(""), QLabel(""))
        self.middelLayout.addRow(QLabel(""), QLabel(""))

    def clearMiddel(self):

        for i in reversed(range(self.middelLayout.count())):
            self.middelLayout.itemAt(i).widget().setParent(None)


    def submitAction(self):

        self.mbox = QMessageBox.question(self, "Warningg!", f"Are you sure to Apply :\n {self.task} ?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if self.mbox == QMessageBox.Yes:

            try:

                par1 = par2 = None

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

                    try:
                        par1 = self.selectProtocol.currentText()
                        par2 = self.selectPort.text()
                        par3 = self.zones.currentText()
                        int(par2)
                    except ValueError:
                        QMessageBox.warning(self, 'error', f'Port numnber must be an Integer')
                        return
                    else:
                        RemoveProtocolPort(par2, par1,par3)


            except:
                QMessageBox.critical(self, 'error', f'error occured during Applaying this \n {self.task} ')
                self.clearMiddel()

            else:
                QMessageBox.information(self, 'success', f'Task Done Succesfully')
                self.clearMiddel()

    def clearAction(self):
        pass

    def cancelAction(self):
        self.close()



