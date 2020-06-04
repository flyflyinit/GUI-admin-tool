import qtmodern.styles
import qtmodern.windows
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import *
import subprocess
import json
import select

def getContentLogs(self):
    self.filters = QHBoxLayout()
    self.hboxxx = QHBoxLayout()

    #self.time = QComboBox(self)

    self.since = QDateTimeEdit(QDate.currentDate().addMonths(-1))
    #self.since.setMinimumDate(QDate.currentDate().addDays(-365))
    self.since.setMaximumDate(QDate.currentDate())
    self.since.setDisplayFormat("yyyy.MM.dd")
    self.since.setStyleSheet("color: #95a5a6; background-color: #303a46 ; border: 0px solid #303a46")
    self.since.setFixedHeight(25)
    self.since.setFixedWidth(110)

    self.until = QDateTimeEdit(QDate.currentDate())
    #self.until.setMinimumDate(QDate.currentDate().addDays(-365))
    self.until.setMaximumDate(QDate.currentDate())
    self.until.setDisplayFormat("yyyy.MM.dd")
    self.until.setStyleSheet("color: #95a5a6; background-color: #303a46 ; border: 0px solid #303a46")
    self.until.setFixedHeight(25)
    self.until.setFixedWidth(110)


    self.prio = QComboBox(self)
    self.prio.setStyleSheet("color: #95a5a6; background-color: #303a46 ; border: 0px solid #303a46")
    self.prio.setFixedHeight(25)
    self.prio.setFixedWidth(80)
    self.prio.addItem("All")
    self.prio.addItems(['emerg','alert','crit','err','warning','notice','info','debug'])
    self.prio.setCurrentIndex(0)

    self.pid = QLineEdit(self)
    self.pid.setPlaceholderText('PID 1 ~ 32768')
    self.pid.setText('All')
    self.pid.setStyleSheet("color: #95a5a6; background-color: #303a46 ; border: 0px solid #303a46")
    self.pid.setFixedHeight(25)
    self.pid.setFixedWidth(100)

    self.uid = QLineEdit(self)
    self.uid.setPlaceholderText('UID 0 ~ 65536')
    self.uid.setText('All')
    self.uid.setStyleSheet("color: #95a5a6; background-color: #303a46 ; border: 0px solid #303a46")
    self.uid.setFixedHeight(25)
    self.uid.setFixedWidth(100)

    self.gid = QLineEdit(self)
    self.gid.setPlaceholderText('GID 0 ~ 65536')
    self.gid.setText('All')
    self.gid.setStyleSheet("color: #95a5a6; background-color: #303a46 ; border: 0px solid #303a46")
    self.gid.setFixedHeight(25)
    self.gid.setFixedWidth(100)

    self.unit = QComboBox(self)
    self.unit.setStyleSheet("color: #95a5a6; background-color: #303a46 ; border: 0px solid #303a46")
    self.unit.setFixedHeight(25)
    self.unit.setFixedWidth(180)
    self.unit.addItem("All")
    self.unit.setCurrentIndex(0)
    c = subprocess.run('ls -f /lib/systemd/system',shell=True,stdout=subprocess.PIPE)
    c = c.stdout.decode('utf-8').split('\n')
    self.unit.addItems(c[2:-1])

    self.selectBtn = QPushButton("Select")
    self.selectBtn.clicked.connect(lambda :selectclicked(self))
    self.selectBtn.setStyleSheet("color: #95a5a6; background-color: #303a46 ; border: 0px solid #303a46")
    self.selectBtn.setFixedHeight(25)
    self.selectBtn.setFixedWidth(80)

    self.hboxxx.addWidget(self.since)
    self.hboxxx.addWidget(self.until)
    self.hboxxx.addWidget(self.prio)
    self.hboxxx.addWidget(self.pid)
    self.hboxxx.addWidget(self.uid)
    self.hboxxx.addWidget(self.gid)
    self.hboxxx.addWidget(self.unit)
    self.hboxxx.addWidget(self.selectBtn)
    self.hboxxx.addStretch()
    self.filters.addLayout(self.hboxxx)

    createTableLogs(self)
    
    self.containerLogs=QVBoxLayout()
    self.containerLogs.addLayout(self.filters)
    self.containerLogs.addWidget(self.tableLogs)
    self.bottomRightLayout.addLayout(self.containerLogs)

def selectclicked(self):
    current = self.listnet.currentIndex()
    currenttext = self.listnet.currentText()
    while self.tableLogs.rowCount() > 0:
        self.tableLogs.removeRow(0)

    createTableLogs(self)

    self.listnet.setCurrentIndex(current)
    self.containerLogs.addWidget(self.tableLogs)


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
    showmylogslist(self)


def showmylogslist(self,since='',until='',priority='',pid='',gid='',unit=''):
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
