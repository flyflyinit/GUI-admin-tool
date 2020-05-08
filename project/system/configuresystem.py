try:
    from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QLabel, QMessageBox, QPushButton, QHBoxLayout, \
        QVBoxLayout
except ImportError as e:
    print(f'package PyQt5 Not Found\n{e}\ntry :\npip3 install --user pyqt5\nOR\ndnf install python3-pyqt5, yum install python3-pyqt5\n')

try:
    import subprocess
except ImportError as e:
    print(f'package not found\n{e}\n')


class ConfigureSystemWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200,50,300,400)
        self.setWindowTitle("Configure System")
        self.layouts()
        self.widgets()

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QFormLayout()
        self.topLayout.setContentsMargins(20,20,20,20)
        self.bottomLayout=QHBoxLayout()

        self.submitBtn=QPushButton("Submit")
        self.submitBtn.clicked.connect(self.submitAction)
        self.cancelBtn=QPushButton("Cancel")
        self.cancelBtn.clicked.connect(self.cancelAction)
        self.submitBtn.setFixedHeight(30)
        self.cancelBtn.setFixedHeight(30)
        self.submitBtn.setStyleSheet("color: #ecf0f1; background-color: #27ae60 ; border: 0px solid #27ae60" )
        self.cancelBtn.setStyleSheet("color: #ecf0f1; background-color: #e74c3c; border: 0px solid #e74c3c")

        self.bottomLayout.addWidget(self.submitBtn)
        self.bottomLayout.addWidget(self.cancelBtn)
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addStretch()
        self.mainLayout.addLayout(self.bottomLayout)
        self.setLayout(self.mainLayout)

    def widgets(self):
        self.edit = QLineEdit()
        self.edit.setPlaceholderText('enter new hostname')
        self.topLayout.addRow(QLabel('Hostname :'),self.edit)

    def submitAction(self):
        hst = self.edit.text()
        try:
            subprocess.run(f'hostnamectl set-hostname {hst}',check=True,shell=True)
        except subprocess.CalledProcessError :
            QMessageBox.warning(self,'warning',f"error occured during setting this hostname\n")
        else:
            QMessageBox.information(self,'success',f'hostname changed to {hst} succesfully.')
            self.close()

    def cancelAction(self):
        self.close()