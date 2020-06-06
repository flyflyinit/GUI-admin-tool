try:
    import psutil
except ImportError as e:
    print(f'package not found\n{e}\n')

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


class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, interface='a',width=5, height=5, dpi=50):
        fig = Figure(figsize=(width, height), dpi=dpi)
        plt.style.use('Solarize_Light2')
        #plt.style.use('seaborn')
        #fig.patch.set_facecolor('black')
        self.Axes = fig.add_subplot()
        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
    def compute_initial_figure(self):
        pass


class NetSentCanvas(MyMplCanvas):
    def __init__(self,*args, **kwargs):
        for key, value in kwargs.items():
            #print ("%s == %s" %(key, value))
            if key == 'interface':
                self.interface = value

        MyMplCanvas.__init__(self, *args, **kwargs)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.netsent_update_figure)
        self.timer.start(1000)

    def compute_initial_figure(self):
        global netsent
        global netsenttimee
        global netsentcurrenttime
        global Axes
        global netsentval

        netsent = []
        netsenttimee = []
        netsentcurrenttime = 0

        if self.interface == "All" :
            netsentval = psutil.net_io_counters(pernic=False, nowrap=False)[0]
        else:
            netsentval = psutil.net_io_counters(pernic=True, nowrap=False)[self.interface][0]

        self.Axes.plot(netsenttimee, netsent, label='sent')
        self.Axes.set_xlabel("Seconds")
        self.Axes.set_ylabel("Bytes")
        self.Axes.set_title("Network Sent")
        self.Axes.set_xlim(0, 100)
        self.Axes.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        self.Axes.grid(True)
        self.Axes.get_xaxis().set_visible(False)
        self.Axes.legend(loc='upper left')

    def netsent_update_figure(self):
        global netsent
        global netsenttimee
        global netsentcurrenttime
        global Axes
        global netsentval

        netsentvalpre = netsentval
        if self.interface == "All" :
            netsentval = psutil.net_io_counters(pernic=False, nowrap=False)[0]
        else:
            netsentval = psutil.net_io_counters(pernic=True, nowrap=False)[self.interface][0]

        netsent.append(netsentval - netsentvalpre)

        netsentcurrenttime=netsentcurrenttime+1
        netsenttimee.append(str(netsentcurrenttime))

        if len(netsenttimee) == 100:
            netsent.pop(0)
            netsenttimee.pop(0)

        self.Axes.cla()
        self.Axes.plot(netsenttimee, netsent, label='sent')
        self.Axes.set_xlabel("Seconds")
        self.Axes.set_ylabel("Bytes")
        self.Axes.set_title("Network Sent")
        self.Axes.set_xlim(0, 100)
        self.Axes.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        self.Axes.grid(True)
        self.Axes.get_xaxis().set_visible(False)
        self.Axes.legend(loc='upper left')
        self.draw()

class NetRecCanvas(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            #print ("%s == %s" %(key, value))
            if key == 'interface':
                self.interface = value
        MyMplCanvas.__init__(self, *args, **kwargs)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.netrec_update_figure)
        self.timer.start(1000)

    def compute_initial_figure(self):
        global netrec
        global netrectimee
        global netreccurrenttime
        global Axes
        global netrecval

        netrec = []
        netrectimee = []
        netreccurrenttime = 0

        if self.interface == "All":
            netrecval = psutil.net_io_counters(pernic=False, nowrap=False)[1]
        else:
            netrecval = psutil.net_io_counters(pernic=True, nowrap=False)[self.interface][1]

        self.Axes.plot(netrectimee, netrec, label='recieved')
        self.Axes.set_xlabel("Seconds")
        self.Axes.set_ylabel("Bytes")
        self.Axes.set_title("Network Recieved")
        self.Axes.set_xlim(0, 100)
        self.Axes.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        self.Axes.grid(True)
        self.Axes.get_xaxis().set_visible(False)
        self.Axes.legend(loc='upper left')

    def netrec_update_figure(self):
        global netrec
        global netrectimee
        global netreccurrenttime
        global Axes
        global netrecval

        netrecvalpre = netrecval
        if self.interface == "All":
            netrecval = psutil.net_io_counters(pernic=False, nowrap=False)[1]
        else:
            netrecval = psutil.net_io_counters(pernic=True, nowrap=False)[self.interface][1]

        netrec.append(netrecval - netrecvalpre)
        netreccurrenttime=netreccurrenttime+1
        netrectimee.append(str(netreccurrenttime))

        if len(netrectimee) == 100:
            netrec.pop(0)
            netrectimee.pop(0)

        self.Axes.cla()
        self.Axes.plot(netrectimee, netrec, label='recieved')
        self.Axes.set_xlabel("Seconds")
        self.Axes.set_ylabel("Bytes")
        self.Axes.set_title("Network Recieved")
        self.Axes.set_xlim(0, 100)
        self.Axes.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        self.Axes.grid(True)
        self.Axes.get_xaxis().set_visible(False)
        self.Axes.legend(loc='upper left')
        self.draw()


