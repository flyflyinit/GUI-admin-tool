import qtmodern.styles
import qtmodern.windows
from PyQt5 import QtGui
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import *
import subprocess
import json

def getContentLogs(self):
    self.filters = QHBoxLayout()
    self.hboxxx = QHBoxLayout()

    self.a = ['emerg', 'alert', 'crit', 'err', 'warning', 'notice', 'info', 'debug']

    self.sinceC = QVBoxLayout()
    self.since = QDateTimeEdit(QDate.currentDate().addMonths(-1))
    #self.since.setMinimumDate(QDate.currentDate().addDays(-365))
    self.since.setMaximumDate(QDate.currentDate())
    self.since.setDisplayFormat("yyyy.MM.dd")
    self.since.setStyleSheet("color: #95a5a6; background-color: #303a46 ; border: 0px solid #303a46")
    self.since.setFixedHeight(25)
    self.since.setFixedWidth(110)
    self.sinceT = QLabel("Since :")
    self.sinceC.addWidget(self.sinceT)
    self.sinceC.addWidget(self.since)

    self.untilC = QVBoxLayout()
    self.until = QDateTimeEdit(QDate.currentDate())
    #self.until.setMinimumDate(QDate.currentDate().addDays(-365))
    self.until.setMaximumDate(QDate.currentDate())
    self.until.setDisplayFormat("yyyy.MM.dd")
    self.until.setStyleSheet("color: #95a5a6; background-color: #303a46 ; border: 0px solid #303a46")
    self.until.setFixedHeight(25)
    self.until.setFixedWidth(110)
    self.untilT = QLabel("Until :")
    self.untilC.addWidget(self.untilT)
    self.untilC.addWidget(self.until)


    self.prioC = QVBoxLayout()
    self.prio = QComboBox(self)
    self.prio.setStyleSheet("color: #95a5a6; background-color: #303a46 ; border: 0px solid #303a46")
    self.prio.setFixedHeight(25)
    self.prio.setFixedWidth(80)
    self.prio.addItem("All")
    self.prio.addItems(self.a)
    self.prio.setCurrentIndex(0)
    self.prioT = QLabel("Priority :")
    self.prioC.addWidget(self.prioT)
    self.prioC.addWidget(self.prio)

    self.pidC = QVBoxLayout()
    self.pid = QLineEdit(self)
    self.pid.setPlaceholderText('1 ~ 32768')
    self.pid.setText('All')
    self.pid.setStyleSheet("color: #95a5a6; background-color: #303a46 ; border: 0px solid #303a46")
    self.pid.setFixedHeight(25)
    self.pid.setFixedWidth(100)
    self.pidT = QLabel("Process ID :")
    self.pidC.addWidget(self.pidT)
    self.pidC.addWidget(self.pid)

    self.uidC = QVBoxLayout()
    self.uid = QLineEdit(self)
    self.uid.setPlaceholderText('0 ~ 65536')
    self.uid.setText('All')
    self.uid.setStyleSheet("color: #95a5a6; background-color: #303a46 ; border: 0px solid #303a46")
    self.uid.setFixedHeight(25)
    self.uid.setFixedWidth(100)
    self.uidT = QLabel("User ID :")
    self.uidC.addWidget(self.uidT)
    self.uidC.addWidget(self.uid)

    self.gidC = QVBoxLayout()
    self.gid = QLineEdit(self)
    self.gid.setPlaceholderText('0 ~ 65536')
    self.gid.setText('All')
    self.gid.setStyleSheet("color: #95a5a6; background-color: #303a46 ; border: 0px solid #303a46")
    self.gid.setFixedHeight(25)
    self.gid.setFixedWidth(100)
    self.gidT = QLabel("Group ID :")
    self.gidC.addWidget(self.gidT)
    self.gidC.addWidget(self.gid)

    self.unitC = QVBoxLayout()
    self.unit = QComboBox(self)
    self.unit.setStyleSheet("color: #95a5a6; background-color: #303a46 ; border: 0px solid #303a46")
    self.unit.setFixedHeight(25)
    self.unit.setFixedWidth(180)
    self.unit.addItem("All")
    self.unit.setCurrentIndex(0)
    c = subprocess.run('ls -f /lib/systemd/system',shell=True,stdout=subprocess.PIPE)
    c = c.stdout.decode('utf-8').split('\n')
    c = c[2:-1]
    c.sort()
    self.unit.addItems(c)
    self.unitT = QLabel("Unit :")
    self.unitC.addWidget(self.unitT)

    self.selectBtn = QPushButton("Filter")
    self.selectBtn.clicked.connect(lambda :selectclicked(self))
    self.selectBtn.setStyleSheet("color: #95a5a6; background-color: #303a46 ; border: 0px solid #303a46")
    self.selectBtn.setFixedHeight(25)
    self.selectBtn.setFixedWidth(80)

    box = QHBoxLayout()
    box.addWidget(self.unit)
    box.addWidget(self.selectBtn)
    self.unitC.addLayout(box)

    self.hboxxx.addLayout(self.sinceC)
    self.hboxxx.addLayout(self.untilC)
    self.hboxxx.addLayout(self.prioC)
    self.hboxxx.addLayout(self.pidC)
    self.hboxxx.addLayout(self.gidC)
    self.hboxxx.addLayout(self.uidC)
    self.hboxxx.addLayout(self.unitC)
    self.hboxxx.addStretch()
    f = subprocess.run("journalctl --disk-usage | awk {'print $7'}",shell=True,stdout=subprocess.PIPE)
    diskUsage = QLabel(f"journals size: {f.stdout.decode('utf-8')}")
    self.hboxxx.addWidget(diskUsage)
    self.filters.addLayout(self.hboxxx)

    self.tableLogs=QTableWidget()
    createTableLogs(self)
    showmylogslist(self)

    self.containerLogs=QVBoxLayout()
    self.containerLogs.addLayout(self.filters)
    self.containerLogs.addWidget(self.tableLogs)
    self.bottomRightLayout.addLayout(self.containerLogs)

def selectclicked(self):

    currentSince = '--since='+self.since.date().toString(Qt.ISODate)
    currentUntil = '--until='+self.until.date().toString(Qt.ISODate)
    currentPID = self.pid.text()
    currentGID = self.gid.text()
    currentUID = self.uid.text()
    currentPrio = self.prio.currentText()
    currentUnit = self.unit.currentText()

    while self.tableLogs.rowCount() > 0:
        self.tableLogs.removeRow(0)

    createTableLogs(self)

    if currentPID == 'All':
        currentPID = ''
    else:
        currentPID = '_PID='+currentPID
    if currentGID == 'All':
        currentGID = ''
    else:
        currentGID = '_GID='+currentGID
    if currentUID == 'All':
        currentUID = ''
    else:
        currentUID = '_UID='+currentUID
    if currentPrio == 'All':
        currentPrio = ''
    else:
        currentPrio = 'PRIORITY='+str(self.a.index(currentPrio))
    if currentUnit == 'All':
        currentUnit = ''
    else:
        currentUnit = '_SYSTEMD_UNIT='+currentUnit

    showmylogslist(self,since=currentSince,until=currentUntil,priority=currentPrio,pid=currentPID,gid=currentGID,uid=currentUID,unit=currentUnit)
    self.containerLogs.addWidget(self.tableLogs)


def createTableLogs(self):
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


def showmylogslist(self,since='',until='',priority='',pid='',gid='',uid='',unit=''):
    self.rowposition = 0

    args = f"journalctl -r {since} {until} {priority} {pid} {gid} {uid} {unit} -o json"
    print(args)
    f = subprocess.Popen(args, stdout=subprocess.PIPE,shell=True)
    i = 0
    self.dic = {}

    while True:
        i = i + 1
        try:
            line = f.stdout.readline()
            if not line or i >= 1000:
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
                self.tableLogs.setItem(self.rowPosition, 1, QTableWidgetItem(str(self.a[int(journal_json[0]['PRIORITY'])])))
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
                self.dic[i] = moreCellInTableLogs(journal_json[0]['MESSAGE'])
                self.tableLogs.setCellWidget(self.rowPosition, 8, self.dic[i])
            except:
                pass

            if journal_json[0]['PRIORITY'] in ['0','1','2','3']:
                self.tableLogs.item(self.rowPosition, 1).setBackground(QtGui.QColor(234, 0, 0))
            if journal_json[0]['PRIORITY'] == '4':
                self.tableLogs.item(self.rowPosition, 1).setBackground(QtGui.QColor(254, 177, 0))

        except Exception as e:
            print(e)


class moreCellInTableLogs(QWidget):
    def __init__(self,message, parent=None):
        super(moreCellInTableLogs,self).__init__(parent)
        self.message = message
        self.hbox = QHBoxLayout()
        self.showmoreBtn=QPushButton('message')
        self.showmoreBtn.clicked.connect(self.showmoreBtnClicked)
        self.hbox.addWidget(self.showmoreBtn)
        self.hbox.addWidget(QLabel(self.message))
        self.hbox.addStretch()
        self.hbox.setContentsMargins(0,0,0,0)
        self.hbox.setSpacing(8)
        self.setLayout(self.hbox)

    def showmoreBtnClicked(self):
        self.secondwindow = MoreMessageWindow(self.message)
        self.sw = qtmodern.windows.ModernWindow(self.secondwindow)
        self.sw.show()


class MoreMessageWindow(QWidget):
    def __init__(self,message):
        super().__init__()
        self.setGeometry(200,50,300,300)
        self.setWindowTitle('Message')
        self.message = message
        self.layouts()

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout=QHBoxLayout()

        top = QHBoxLayout()
        text = QLabel(str(self.message))
        groupBox = QGroupBox()
        text.setContentsMargins(30, 30, 30, 30)  # left ,#top ,#right , #bottom
        top.addWidget(text)

        groupBox.setLayout(top)
        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)

        self.okBtn=QPushButton("Ok")
        self.okBtn.clicked.connect(self.okAction)
        self.okBtn.setFixedHeight(30)
        self.okBtn.setStyleSheet("color: #ecf0f1; background-color: #27ae60 ; border: 0px" )

        self.topLayout.addWidget(scroll)
        self.bottomLayout.addWidget(self.okBtn)
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addStretch()
        self.mainLayout.addLayout(self.bottomLayout)
        self.setLayout(self.mainLayout)

    def okAction(self):
        self.close()
