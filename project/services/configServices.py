import sys,os
from PyQt5.QtWidgets import *
import subprocess

'''
class CreateServicesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200,50,300,400)
        self.setWindowTitle("install a new service")
        self.layouts()
        self.widgets()

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QFormLayout()
        self.topLayout.setContentsMargins(20,20,20,20)
        self.bottomLayout=QHBoxLayout()

        self.submitBtn=QPushButton("install")
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
        self.topLayout.addRow(QLabel('enter service name :'),self.edit)

    def submitAction(self):
        service = self.edit.text()
        system='ubuntu'

        if system in 'ubuntu':
            command=f'sudo  apt-get install {service} -y '

        elif system in ' fedora ':
            command=f' yum install {service}'
        else:
            QMessageBox.warning(self,'error',f"this tool does not work with your current distribution \n")


        try:
            #subprocess.run(command,check=True,shell=True)
            #subprocess.run(f'systemctl enable {service} ',check=True,shell=True)
            print(command)

        except subprocess.CalledProcessError :
            QMessageBox.warning(self,'warning',f"error occured during installation this service \n")
        else:
            QMessageBox.information(self,'success',f'{service} installed succesfully.')
            self.close()

    def cancelAction(self):
        self.close()
'''
