import qtmodern.styles
import qtmodern.windows
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
import subprocess
import json
import select

def getContentLogs(self):
    self.filters = QHBoxLayout()


    createTableLogs(self)
    
    self.containerLogs=QVBoxLayout()

    self.containerLogs.addLayout(self.filters)
    self.containerLogs.addWidget(self.tableLogs)

    self.bottomRightLayout.addLayout(self.containerLogs)

def createTableLogs(self):
    self.tableLogs=QTableWidget()
    self.tableLogs.setRowCount(0)
    self.tableLogs.setColumnCount(9)

    self.tableLogs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    self.tableLogs.setAutoFillBackground(True)

    header = self.tableLogs.horizontalHeader()
    header.setStretchLastSection(True)

    self.tableLogs.setHorizontalHeaderItem(0, QTableWidgetItem("Time"))
    self.tableLogs.setHorizontalHeaderItem(1, QTableWidgetItem("Priority"))
    self.tableLogs.setHorizontalHeaderItem(2, QTableWidgetItem("Hostname"))
    self.tableLogs.setHorizontalHeaderItem(3, QTableWidgetItem("PID"))
    self.tableLogs.setHorizontalHeaderItem(4, QTableWidgetItem("GID"))
    self.tableLogs.setHorizontalHeaderItem(5, QTableWidgetItem("UID"))
    self.tableLogs.setHorizontalHeaderItem(6, QTableWidgetItem("Unit"))
    self.tableLogs.setHorizontalHeaderItem(7, QTableWidgetItem("Command"))
    self.tableLogs.setHorizontalHeaderItem(8, QTableWidgetItem("Message"))
    self.tableLogs.setEditTriggers(QAbstractItemView.NoEditTriggers)
    showmyserviceslist(self)


def showmyserviceslist(self,since='',until='',priority='',pid='',gid='',unit=''):
    self.rowposition = 0

    args = f"journalctl -r {since} {until} {priority} {pid} {gid} {unit} -o json"
    f = subprocess.Popen(args, stdout=subprocess.PIPE,shell=True)
    i = 0
    while True:
        i = i + 1
        try:
            line = f.stdout.readline()
            if not line or i >= 5000:
                break
            if isinstance(line, bytes):
                line = line.decode('utf-8')
            journal_json = json.loads('[' + line.strip() + ']')
            self.rowPosition = self.tableLogs.rowCount()
            self.tableLogs.insertRow(self.rowPosition)
            try:
                self.tableLogs.setItem(self.rowPosition, 0, QTableWidgetItem(journal_json[0]['SYSLOG_TIMESTAMP']))
            except:
                self.tableLogs.setItem(self.rowPosition, 0, QTableWidgetItem(journal_json[0]['__REALTIME_TIMESTAMP']))
            try:
                self.tableLogs.setItem(self.rowPosition, 1, QTableWidgetItem(journal_json[0]['PRIORITY']))
            except:
                pass
            try:
                self.tableLogs.setItem(self.rowPosition, 2, QTableWidgetItem(journal_json[0]['_HOSTNAME']))
            except:
                pass
            try:
                self.tableLogs.setItem(self.rowPosition, 3, QTableWidgetItem(journal_json[0]['_PID']))
            except:
                pass
            try:
                self.tableLogs.setItem(self.rowPosition, 4, QTableWidgetItem(journal_json[0]['_GID']))
            except:
                pass
            try:
                self.tableLogs.setItem(self.rowPosition, 5, QTableWidgetItem(journal_json[0]['_UID']))
            except:
                pass
            try:
                self.tableLogs.setItem(self.rowPosition, 6, QTableWidgetItem(journal_json[0]['_SYSTEMD_UNIT']))
            except:
                pass
            try:
                self.tableLogs.setItem(self.rowPosition, 7, QTableWidgetItem(journal_json[0]['_CMDLINE']))
            except:
                pass
            try:
                self.tableLogs.setItem(self.rowPosition, 8, QTableWidgetItem(journal_json[0]['MESSAGE']))
            except:
                pass
        except Exception as e:
            print(e)


def createLogsWindow(self):
    pass
    '''
    self.secondwindow = CreateLogsWindow()
    self.sw = qtmodern.windows.ModernWindow(self.secondwindow)
    self.sw.show()
    '''

def editLogsWindow(self,d):
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
                self.secondwindow = EditLogsWindow(user)
                self.sw = qtmodern.windows.ModernWindow(self.secondwindow)
                self.sw.show()
            else:
                continue
    '''

def deleteLogsWindow(self,d):
    pass
    '''
    list_users_to_delete = []
    for i in d:
        if d[i].isSelected == True:
            list_users_to_delete.append(i)
    if len(list_users_to_delete) == 0:
        QMessageBox.warning(self, 'warning', 'no selected users.\nPlease select at least one user')
    else:
        self.secondwindow = DeleteLogsWindow(list_users_to_delete)
        self.sw = qtmodern.windows.ModernWindow(self.secondwindow)
        self.sw.show()
    '''