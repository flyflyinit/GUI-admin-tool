try:
    from PyQt5 import QtCore, QtWidgets
except ImportError as e:
    print(f'package PyQt5 Not Found\n{e}\ntry :\npip3 install --user pyqt5\nOR\ndnf install python3-pyqt5, yum install python3-pyqt5\n')

try:
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
    import matplotlib.pyplot as plt
except ImportError as e:
    print(f'package matplotlib Not Found\n{e}\ntry :\npip3 install --user matplotlib\n')

try:
    import subprocess
except ImportError as e:
    print(f'package not found\n{e}\n')



begindate = '2000-01-01'
enddate = 'now'

class MyMplCanvas(FigureCanvas):
    def __init__(self,parent=None, width=5, height=5, dpi=50):
        fig = Figure(figsize=(width, height), dpi=dpi)
        plt.style.use('Solarize_Light2')
        self.Axes = fig.add_subplot()
        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
    def compute_initial_figure(self):
        pass


class lastLogins(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        self.lastlogins_update_figure()
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.lastlogins_update_figure)
        timer.start(10000)

    def lastlogins_update_figure(self):
        global begindate
        global enddate

        nameslist = getLastLoginsStats()
        nameslist = nameslist + ['runlevel','reboot']
        count = []
        countnames = []
        explode = ()
        for user in nameslist:
            cmd = f"last -s {begindate} -t {enddate} -w -x --time-format notime | awk " + " {'print $1'} " + f" | grep ^{user}$ | wc -l"
            out = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].decode('utf-8')
            if int(out) != 0:
                countnames.append(str(user))
                count.append(int(out))
                explodelist = list(explode)
                if user == 'root':
                    explodelist.append(0.2)
                    explode = tuple(explodelist)
                else:
                    explodelist.append(0)
                    explode=tuple(explodelist)

        self.Axes.cla()
        self.Axes.pie(count, explode=explode, labels=countnames, autopct='%1.1f%%', shadow=True, startangle=90)
        self.Axes.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        self.Axes.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        self.Axes.grid(True)
        self.Axes.legend()
        self.Axes.legend(loc='upper left')
        self.Axes.set_title('Last Logins')
        self.draw()


class lastBadLogins(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        self.lastbadlogins_update_figure()
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.lastbadlogins_update_figure)
        timer.start(10000)

    def lastbadlogins_update_figure(self):
        global begindate
        global enddate

        nameslist = getLastLoginsStats()
        nameslist.append('unknown')
        count = []
        countnames = []
        explode = ()
        for user in nameslist:
            cmd = f"lastb -s {begindate} -t {enddate} -w -x --time-format notime | awk " + " {'print $1'} " + f" | grep {user} | wc -l"
            outt = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].decode('utf-8')
            if int(outt) != 0:
                countnames.append(str(user))
                count.append(int(outt))
                explodelist = list(explode)
                if user == 'root':
                    explodelist.append(0.2)
                    explode = tuple(explodelist)
                else:
                    explodelist.append(0)
                    explode=tuple(explodelist)

        self.Axes.cla()
        self.Axes.pie(count, explode=explode, labels=countnames, autopct='%1.1f%%', shadow=True, startangle=90)
        self.Axes.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        self.Axes.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        self.Axes.grid(True)
        self.Axes.legend()
        self.Axes.legend(loc='upper left')
        self.Axes.set_title('Last Bad Logins')
        self.draw()


def retrievedatafrompasswdfile():
    list_of_users = []
    with open("/etc/passwd", mode='r') as passwd_content:
        each_line = passwd_content.readlines()
        passwd_content.close()

    for each_user in each_line:
        each_user2 = each_user.split(":")
        list_of_users.append(each_user2)
    return list_of_users

def getLastLoginsStats():
    list_of_users = retrievedatafrompasswdfile()
    nameslist = []
    for i in list_of_users:
        nameslist.append(i[0])
    return nameslist
