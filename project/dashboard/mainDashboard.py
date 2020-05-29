try:
    from PyQt5.QtWidgets import QGridLayout, QFormLayout, QLabel, QGroupBox, QScrollArea, QPushButton, QVBoxLayout, \
    QHBoxLayout, QComboBox, QMessageBox
    from PyQt5.QtCore import QTimer
except ImportError as e:
    print(f'package PyQt5 Not Found\n{e}\ntry :\npip3 install --user pyqt5\nOR\ndnf install python3-pyqt5, yum install python3-pyqt5\n')

try:
    import qtmodern.styles
    import qtmodern.windows
except ImportError as e:
    print(f'package qtmodern Not Found\n{e}\ntry :\npip3 install --user qtmodern\n')

try:
    from datetime import datetime
    import psutil
    import platform
    import subprocess
    import getpass
    from dashboard.dashboardplots import All,All2
except ImportError as e:
    print(f'package not found\n{e}\n')



def getContentDashboard(self):
    self.all = All(width=7, height=3.6, dpi=80)
    self.all2 = All2(width=7, height=3.6, dpi=80)
    #self.all.setContentsMargins(50,10,10,10)
    #self.gridSystem.addWidget(self.all, 0, 0)

    systemInformationn(self)

    self.groupBoxx = QGroupBox()

    grid = QGridLayout()
    grid.addWidget(self.all, 0, 0)
    grid.addWidget(self.all2, 0, 1)

    self.containerSystemm=QVBoxLayout()

    self.containerSystemm.addLayout(grid)
    self.containerSystemm.addLayout(self.vbox1)
    self.containerSystemm.addLayout(self.vbox2)
    self.containerSystemm.addStretch()
    self.groupBoxx.setLayout(self.containerSystemm)
    self.scrollSystemm = QScrollArea()
    self.scrollSystemm.setFixedWidth(1150)
    self.groupBoxx.setAutoFillBackground(True)
    #self.scrollSystem.QAbstractScrollArea.sizeAdjustPolicy()
    #self.scrollSystem.setWidgetResizable(True)
    self.scrollSystemm.setWidget(self.groupBoxx)
    #self.scrollSystem.setFixedHeight(1000)
    self.scrollSystemm.setAutoFillBackground(True)
    self.bottomRightLayout.addWidget(self.scrollSystemm)

    updateHostnameUpTimeAndLoadAvgLabell(self)

def updateHostnameUpTimeAndLoadAvgLabell(self):
    with open("/proc/uptime", "r") as f:
        uptime = f.read().split(" ")[0].strip()
    uptime = int(float(uptime))
    uptime_hours = uptime // 3600
    uptime_minutes = (uptime % 3600) // 60
    loadavg = str(psutil.getloadavg())
    time = subprocess.Popen("date | awk {'print $5'}", shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()[0].decode('utf-8').replace("\n", "")
    date = subprocess.Popen("date --iso-8601", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].decode('utf-8').replace("\n", "")
    try:
        self.laa.setText(loadavg)
        self.utt.setText(str(uptime_hours) + ":" + str(uptime_minutes) + " hours")
        self.hss.setText(str(platform.node()))
        self.dateandtime.setText(f"{date}, {time}")
    except Exception:
        return None
    QTimer.singleShot(3000, lambda: updateHostnameUpTimeAndLoadAvgLabell(self))


def systemInformationn(self):
    shutdownreboot = QHBoxLayout()
    self.shre = QComboBox()
    self.shre.setFixedHeight(30)
    self.shre.setFixedWidth(120)
    self.shre.setStyleSheet("color: #95a5a6; background-color: #303a46 ; border: 0px solid #303a46")
    self.shre.addItems(["shutdown","shutdown now","restart","suspend","hibernate"])
    ok = QPushButton("ok")
    ok.clicked.connect(lambda: shutdownrebootAction(self))
    shutdownreboot.addStretch()
    shutdownreboot.addWidget(self.shre)
    shutdownreboot.addWidget(ok)
    ok.setFixedHeight(30)
    ok.setFixedWidth(30)
    #ok.clicked.connect(lambda: configureSystemInformationWindow(self))
    ok.setStyleSheet("color: #95a5a6; background-color: #303a46 ; border: 0px solid #303a46")

    with open("/proc/uptime", "r") as f:
        uptime = f.read().split(" ")[0].strip()
    uptime = int(float(uptime))
    uptime_hours = uptime // 3600
    uptime_minutes = (uptime % 3600) // 60

    loadavg = str(psutil.getloadavg())

    self.hss=QLabel(platform.node())
    #self.hs.setStyleSheet("color: #303a46 ;border: 2px solid #303a46")
    self.hss.setStyleSheet("color: #303a46;font: bold 14px;")

    self.utt = QLabel(str(uptime_hours) + ":" + str(uptime_minutes) + " hours")
    self.utt.setStyleSheet("color: #303a46;font: bold 14px;")

    self.vbox1 = QVBoxLayout()
    self.vbox1.setContentsMargins(50, 50, 50, 0)
    user = QLabel("User : ")
    user.setStyleSheet("color: #303a46;font: bold 25px;")
    username = getpass.getuser()
    usrname = QLabel(username)
    usrname.setStyleSheet("color: #303a46;font: bold 25px;")
    hhbox=QHBoxLayout()
    hhbox.addWidget(user)
    hhbox.addWidget(usrname)
    hhbox.addStretch()
    self.vbox1.addLayout(hhbox)

    self.vbox2 = QVBoxLayout()
    self.vbox2.setContentsMargins(50, 0, 50, 50)

    hbox1 =QHBoxLayout()
    hs = QLabel('Hostname :')
    #hbox1.addStretch()
    hbox1.addWidget(hs)
    hbox1.setContentsMargins(0, 0, 0, 10)
    hbox1.addWidget(self.hss)
    hbox1.addStretch()
    hbox1.addLayout(shutdownreboot)

    line = QLabel('______________________________________________________________________________________________________________________________________________________')
    line.setStyleSheet("color: #95a5a6;font: bold 14px;")
    line.setContentsMargins(0, 0, 0, 10)

    hbox2 =QHBoxLayout()
    pl = QLabel('Platform :')
    plt = QLabel(platform.platform())
    plt.setStyleSheet("color: #303a46;font: bold 14px;")

    #hbox2.addStretch()
    hbox2.addWidget(pl)
    hbox2.addWidget(plt)
    hbox2.addStretch()

    hbox3 =QHBoxLayout()
    ut = QLabel('Uptime :')
    #hbox3.addStretch()
    hbox3.addWidget(ut)
    hbox3.addWidget(self.utt)
    hbox3.addStretch()

    hbox4 =QHBoxLayout()
    loa = QLabel('Load Average :')
    self.laa = QLabel(loadavg)
    self.laa.setStyleSheet("color: #303a46;font: bold 14px;")
    #hbox4.addStretch()
    hbox4.addWidget(loa)
    hbox4.addWidget(self.laa)
    hbox4.addStretch()

    hbox5 =QHBoxLayout()
    dateandtime = QLabel('System Time :')
    time = subprocess.Popen("date | awk {'print $5'}", shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()[0].decode('utf-8').replace("\n", "")
    date = subprocess.Popen("date --iso-8601", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].decode('utf-8').replace("\n", "")
    self.dateandtime = QLabel(f"{date}, {time}")
    self.dateandtime.setStyleSheet("color: #303a46;font: bold 14px;")
    hbox5.addWidget(dateandtime)
    hbox5.addWidget(self.dateandtime)
    hbox5.addStretch()

    self.vbox2.addLayout(hbox1)
    self.vbox2.addWidget(line)
    self.vbox2.addLayout(hbox2)
    self.vbox2.addLayout(hbox3)
    self.vbox2.addLayout(hbox4)
    self.vbox2.addLayout(hbox5)


def shutdownrebootAction(self):
    mbox = QMessageBox.question(self,"Warningg!", "Are You Sure?",QMessageBox.Yes | QMessageBox.No , QMessageBox.No)
    if mbox == QMessageBox.Yes:
        if "shutdown" == self.shre.currentText():
            try:
                c = subprocess.run('shutdown',stderr=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
                QMessageBox.information(self,"Shutting Down",f"{str(c.stderr.decode('utf-8').split(',')[0])}")
            except subprocess.CalledProcessError as e:
                QMessageBox.critical(self, 'error',f'error occured during -shutdown- opperation\n{e}')
        elif "shutdown now" == self.shre.currentText():
            try:
                subprocess.run('shutdown now',stderr=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
            except subprocess.CalledProcessError as e:
                QMessageBox.critical(self, 'error',f'error occured during -shutdown now- opperation\n{e}')
        else :
            try:
                subprocess.run(f'systemctl {self.shre.currentText()}',stderr=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
            except subprocess.CalledProcessError as e:
                QMessageBox.critical(self, 'error',f'error occured during {self.shre.currentText()} opperation\n{e}')

    elif mbox == QMessageBox.No:
        pass
