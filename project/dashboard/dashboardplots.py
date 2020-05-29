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
    def __init__(self, parent=None, width=5, height=5, dpi=50):
        fig = Figure(figsize=(width, height), dpi=dpi)
        plt.style.use('Solarize_Light2')
        #plt.style.use('fivethirtyeight')
        #fig.patch.set_facecolor('black')
        self.Axes = fig.add_subplot()
        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
    def compute_initial_figure(self):
        pass


class All(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_figure)
        self.timer.start(1000)

    def compute_initial_figure(self):
        global ram
        global swap
        global alltime
        global allcurrenttime

        ram = []
        swap = []
        alltime = []
        allcurrenttime = 0

        ram.append(psutil.virtual_memory().percent)
        swap.append(psutil.swap_memory().percent)
        allcurrenttime=allcurrenttime+1
        alltime.append(str(allcurrenttime))

        self.Axes.plot(alltime, ram,label='Memory')
        self.Axes.plot(alltime, swap,label='Swap')
        self.Axes.set_xlim(0, 100)
        self.Axes.set_ylim(0, 100)
        self.Axes.set_xlabel('Seconds')
        #self.Axes.set_ylabel('Usage')
        #self.Axes.set_title("Usage")
        self.Axes.grid(True)
        self.Axes.get_xaxis().set_visible(False)
        self.Axes.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        self.Axes.legend(loc='upper left')


    def update_figure(self):
        global ram
        global swap
        global alltime
        global allcurrenttime

        ram.append(psutil.virtual_memory().percent)
        swap.append(psutil.swap_memory().percent)
        allcurrenttime=allcurrenttime+1
        alltime.append(str(allcurrenttime))

        if len(alltime) == 100:
            ram.pop(0)
            swap.pop(0)
            alltime.pop(0)

        self.Axes.cla()
        self.Axes.plot(alltime, ram,label='Memory')
        self.Axes.plot(alltime, swap,label='Swap')
        #self.Axes.set_title("Usage")
        self.Axes.set_xlim(0, 100)
        self.Axes.set_ylim(0, 100)
        self.Axes.set_xlabel('Seconds')
        #self.Axes.set_ylabel('Usage')
        self.Axes.grid(True)
        self.Axes.get_xaxis().set_visible(False)
        self.Axes.legend(loc='upper left')
        self.draw()

class All2(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_figure)
        self.timer.start(1000)

    def compute_initial_figure(self):
        global cpu
        global alltime2
        global allcurrenttime2

        cpu = []
        alltime2 = []
        allcurrenttime2 = 0

        cpu.append(psutil.cpu_percent(percpu=False))
        allcurrenttime2=allcurrenttime2+1
        alltime2.append(str(allcurrenttime2))

        self.Axes.plot(alltime2, cpu,label='Cpu')
        self.Axes.set_xlim(0, 100)
        self.Axes.set_ylim(0, 100)
        self.Axes.set_xlabel('Seconds')
        #self.Axes.set_ylabel('Usage')
        #self.Axes.set_title("Usage")
        self.Axes.grid(True)
        self.Axes.get_xaxis().set_visible(False)
        self.Axes.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        self.Axes.legend(loc='upper left')


    def update_figure(self):
        global cpu
        global alltime2
        global allcurrenttime2

        cpu.append(psutil.cpu_percent(percpu=False))
        allcurrenttime2=allcurrenttime2+1
        alltime2.append(str(allcurrenttime2))

        if len(alltime2) == 100:
            cpu.pop(0)
            alltime2.pop(0)

        self.Axes.cla()
        self.Axes.plot(alltime2, cpu,label='Cpu')
        #self.Axes.set_title("Usage")
        self.Axes.set_xlim(0, 100)
        self.Axes.set_ylim(0, 100)
        self.Axes.set_xlabel('Seconds')
        #self.Axes.set_ylabel('Usage')
        self.Axes.grid(True)
        self.Axes.get_xaxis().set_visible(False)
        self.Axes.legend(loc='upper left')
        self.draw()
