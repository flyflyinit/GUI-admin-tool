import psutil
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtWidgets, QtCore
import matplotlib.pyplot as plt


class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=5, dpi=50):
        fig = Figure(figsize=(width, height), dpi=dpi)
        #plt.style.use('Solarize_Light2')
        plt.style.use('seaborn')
        #fig.patch.set_facecolor('black')
        self.Axes = fig.add_subplot()
        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
    def compute_initial_figure(self):
        pass


class MemoryCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.mem_update_figure)
        timer.start(1000)
    def compute_initial_figure(self):
        global memava
        global memused
        global memfree
        global membuff
        global memcached
        global memshared
        global swapused
        global swapfree
        global memtime
        global memcurrenttime
        global Axes

        memused = []
        memfree = []
        memava = []
        membuff = []
        memcached = []
        memshared = []
        swapused = []
        swapfree = []
        memtime = []
        memcurrenttime = 0
        self.Axes.plot(memtime, memava, label='available')
        self.Axes.plot(memtime, memused, label='used')
        self.Axes.plot(memtime, memfree, label='free')
        self.Axes.plot(memtime, membuff, label='buffers')
        self.Axes.plot(memtime, memcached, label='cached')
        self.Axes.plot(memtime, memshared, label='shared')
        self.Axes.plot(memtime, swapused, label='used swap',color='black')
        self.Axes.plot(memtime, swapfree, label='free swap',color='gray')
        self.Axes.set_xlabel("Seconds")
        self.Axes.set_ylabel("Bytes")
        self.Axes.set_title("Memory Usage")
        self.Axes.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        self.Axes.grid(True)
        self.Axes.legend(loc='upper left')

    def mem_update_figure(self):
        global memava
        global memused
        global memfree
        global membuff
        global memcached
        global memshared
        global swapused
        global swapfree
        global memtime
        global memcurrenttime
        global Axes

        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        memava.append(mem[1])
        memused.append(mem[3])
        memfree.append(mem[4])
        membuff.append(mem[7])
        memcached.append(mem[8])
        memshared.append(mem[9])
        swapused.append(swap[1])
        swapfree.append(swap[2])
        memcurrenttime=memcurrenttime+1
        memtime.append(str(memcurrenttime))

        if len(memtime) == 20:
            memava.pop(0)
            memused.pop(0)
            memfree.pop(0)
            membuff.pop(0)
            memcached.pop(0)
            memshared.pop(0)
            swapused.pop(0)
            swapfree.pop(0)
            memtime.pop(0)

        self.Axes.cla()
        self.Axes.plot(memtime, memava, label='available')
        self.Axes.plot(memtime, memused, label='used')
        self.Axes.plot(memtime, memfree, label='free')
        self.Axes.plot(memtime, membuff, label='buffers')
        self.Axes.plot(memtime, memcached, label='cached')
        self.Axes.plot(memtime, memshared, label='shared')
        self.Axes.plot(memtime, swapused, label='used swap',color='black')
        self.Axes.plot(memtime, swapfree, label='free swap',color='gray')
        #self.Axes.get_xaxis().set_visible(False)
        self.Axes.set_xlabel("Seconds")
        self.Axes.set_ylabel("Bytes")
        self.Axes.set_title("Memory Usage")
        self.Axes.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        self.Axes.grid(True)
        self.Axes.legend(loc='upper left')
        self.draw()


class CpuCanvas(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.cpu_update_figure)
        timer.start(1000)

    def compute_initial_figure(self):
        global cpuuser
        global cpusystem
        global cpuidle
        global cpuiowait
        global cpuirq
        global cpusoftirq
        global cputimee
        global cpucurrenttime
        global Axes

        cpuuser = []
        cpusystem = []
        cpuiowait = []
        cpuidle = []
        cpuirq = []
        cpusoftirq = []
        cputimee = []
        cpucurrenttime = 0

        self.Axes.plot(cputimee, cpuuser, label='user')
        self.Axes.plot(cputimee, cpusystem, label='system')
        self.Axes.plot(cputimee, cpuidle, label='idle')
        self.Axes.plot(cputimee, cpuiowait, label='iowait')
        self.Axes.plot(cputimee, cpuirq, label='irq')
        self.Axes.plot(cputimee, cpusoftirq, label='softirq')
        self.Axes.set_xlabel("Seconds")
        self.Axes.set_ylabel("Cpu Times")
        self.Axes.set_title("CPU Statistics")
        self.Axes.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        self.Axes.grid(True)
        self.Axes.legend(loc='upper left')

    def cpu_update_figure(self):
        global cpuuser
        global cpusystem
        global cpuidle
        global cpuiowait
        global cpuirq
        global cpusoftirq
        global cputimee
        global cpucurrenttime
        global Axes

        cpu = psutil.cpu_times()
        cpuuser.append(cpu[0])
        cpusystem.append(cpu[2])
        cpuidle.append(cpu[3])
        cpuiowait.append(cpu[4])
        cpuirq.append(cpu[5])
        cpusoftirq.append(cpu[6])
        cpucurrenttime=cpucurrenttime+1
        cputimee.append(str(cpucurrenttime))

        if len(cputimee) == 20:
            cpuuser.pop(0)
            cpusystem.pop(0)
            cpuidle.pop(0)
            cpuiowait.pop(0)
            cpuirq.pop(0)
            cpusoftirq.pop(0)
            cputimee.pop(0)

        self.Axes.cla()
        self.Axes.plot(cputimee, cpuuser, label='user')
        self.Axes.plot(cputimee, cpusystem, label='system')
        self.Axes.plot(cputimee, cpuidle, label='idle')
        self.Axes.plot(cputimee, cpuiowait, label='iowait')
        self.Axes.plot(cputimee, cpuirq, label='irq')
        self.Axes.plot(cputimee, cpusoftirq, label='softirq')
        self.Axes.set_xlabel("Seconds")
        self.Axes.set_ylabel("Cpu Times")
        self.Axes.set_title("CPU Statistics")
        self.Axes.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        self.Axes.grid(True)
        self.Axes.legend(loc='upper left')
        self.draw()


class IoCanvas(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.io_update_figure)
        timer.start(1000)

    def compute_initial_figure(self):
        global ioread
        global iowrite
        global iotime
        global iocurrenttime
        global Axes

        ioread = []
        iowrite = []
        iotime = []
        iocurrenttime = 0
        self.Axes.plot(iotime, ioread, label='read bytes')
        self.Axes.plot(iotime, iowrite, label='write bytes')
        self.Axes.set_xlabel("Seconds")
        self.Axes.set_ylabel("Bytes")
        self.Axes.set_title("Disk IO Usage")
        self.Axes.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        self.Axes.grid(True)
        self.Axes.legend(loc='upper left')

    def io_update_figure(self):
        global ioread
        global iowrite
        global iotime
        global iocurrenttime
        global Axes

        io = psutil.disk_io_counters()
        ioread.append(io[1])
        iowrite.append(io[2])
        iocurrenttime=iocurrenttime+1
        iotime.append(str(iocurrenttime))

        if len(iotime) == 20:
            ioread.pop(0)
            iowrite.pop(0)
            iotime.pop(0)

        self.Axes.cla()
        self.Axes.plot(iotime, ioread, label='read bytes')
        self.Axes.plot(iotime, iowrite, label='write bytes')
        self.Axes.set_xlabel("Seconds")
        self.Axes.set_ylabel("Bytes")
        self.Axes.set_title("Disk IO Usage")
        self.Axes.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        self.Axes.grid(True)
        self.Axes.legend(loc='upper left')
        self.draw()


class IooCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.io_update_figure)
        timer.start(1000)

    def compute_initial_figure(self):
        global ioread
        global iowrite
        global iotime
        global iocurrenttime
        global Axes

        ioread = []
        iowrite = []
        iotime = []
        iocurrenttime = 0

        import numpy as np
        import matplotlib.pyplot as plt

        labels = ['G1', 'G2', 'G3', 'G4', 'G5']
        men_means = [20, 35, 30, 35, 27]
        women_means = [25, 32, 34, 20, 25]
        men_std = [2, 3, 4, 1, 2]
        women_std = [3, 5, 2, 3, 3]
        width = 0.35  # the width of the bars: can also be len(x) sequence

        self.Axes.bar(labels, men_means,width,yerr=men_std, label='read bytes', color='blue')
        self.Axes.bar(labels, women_means,width,yerr=women_std, bottom=men_means, label='read bytes', color='blue')
        self.Axes.set_xlabel("Seconds")
        self.Axes.set_ylabel("Bytes")
        self.Axes.set_title("Disk IO Usage")
        self.Axes.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        self.Axes.grid(True)
        self.Axes.legend()

    def io_update_figure(self):
        global ioread
        global iowrite
        global iotime
        global iocurrenttime
        global Axes

        labels = ['G1', 'G2', 'G3', 'G4', 'G5']
        men_means = [20, 35, 30, 35, 27]
        women_means = [25, 32, 34, 20, 25]
        men_std = [2, 3, 4, 1, 2]
        women_std = [3, 5, 2, 3, 3]
        width = 0.35  # the width of the bars: can also be len(x) sequence


        io = psutil.disk_io_counters()
        ioread.append(io[1])
        iowrite.append(io[2])
        iocurrenttime=iocurrenttime+1
        iotime.append(str(iocurrenttime))

        if len(iotime) == 10:
            ioread.pop(0)
            iowrite.pop(0)
            iotime.pop(0)

        self.Axes.cla()
        self.Axes.bar(labels, men_means,width,yerr=men_std, label='read bytes', color='blue')
        self.Axes.bar(labels, women_means,width,yerr=women_std, bottom=men_means, label='read bytes', color='blue')
        self.Axes.set_xlabel("Seconds")
        self.Axes.set_ylabel("Bytes")
        self.Axes.set_title("Disk IO Usage")
        self.Axes.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        self.Axes.grid(True)
        self.Axes.legend()
        self.draw()


class UsageResume(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.resume_update_figure)
        timer.start(500)

    def compute_initial_figure(self):
        global Axes

        people = ('CPU', 'RAM','SWAP','DISK /')
        y_pos = [0, 1,2,3]

        usage = []
        usage.append(psutil.cpu_percent(percpu=False))
        usage.append(psutil.virtual_memory().percent)
        usage.append(psutil.swap_memory().percent)
        usage.append(psutil.disk_usage('/').percent)

        self.Axes.barh(y_pos, usage, align='center')
        self.Axes.set_yticks(y_pos)
        self.Axes.set_yticklabels(people)
        self.Axes.invert_yaxis()
        self.Axes.set_xlabel('Usage 100$')
        self.Axes.set_xlim(0, 100)
        self.Axes.set_title("System Usage")
        self.Axes.grid(True)

    def resume_update_figure(self):
        global Axes

        people = ('CPU', 'RAM','SWAP','DISK /')
        y_pos = [0, 1,2,3]

        usage = []
        usage.append(psutil.cpu_percent(percpu=False))
        usage.append(psutil.virtual_memory().percent)
        usage.append(psutil.swap_memory().percent)
        usage.append(psutil.disk_usage('/').percent)

        self.Axes.cla()
        self.Axes.barh(y_pos, usage, align='center')
        self.Axes.set_yticks(y_pos)
        self.Axes.set_yticklabels(people)
        self.Axes.invert_yaxis()
        self.Axes.set_xlabel('Usage 100%')
        self.Axes.set_xlim(0, 100)
        self.Axes.set_title("System Usage")
        self.Axes.grid(True)
        self.draw()


class PolygonCPUs(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_figure)
        self.timer.start(1000)

    def compute_initial_figure(self):
        global cpu0
        global cpu1
        global cpu2
        global cpu3
        global cpus
        global cputime
        global cpucurrenttime

        cpus = []
        cpu0 = []
        cpu1 = []
        cpu2 = []
        cpu3 = []
        cputime = []
        cpucurrenttime = 0

        cpu = psutil.cpu_percent(percpu=True)
        cpu0.append(cpu[0])
        cpu1.append(cpu[1])
        cpu2.append(cpu[2])
        cpu3.append(cpu[3])
        cpucurrenttime=cpucurrenttime+1
        cputime.append(str(cpucurrenttime))
        cpus.append(psutil.cpu_percent())


        self.Axes.plot(cputime, cpu0,label='cpu0')
        self.Axes.plot(cputime, cpu1,label='cpu1')
        self.Axes.plot(cputime, cpu2,label='cpu2')
        self.Axes.plot(cputime, cpu3,label='cpu3')
        self.Axes.plot(cputime, cpus,label='All CPUs', color='black')
        self.Axes.set_xlim(0, 20)
        self.Axes.set_ylim(0, 100)
        self.Axes.set_xlabel('Seconds')
        self.Axes.set_ylabel('CPUs')
        self.Axes.set_title("CPUs Usage")
        self.Axes.grid(True)
        self.Axes.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        self.Axes.legend(loc='upper left')

    def update_figure(self):
        global cpu0
        global cpu1
        global cpu2
        global cpu3
        global cpus
        global cputime
        global cpucurrenttime

        cpu = psutil.cpu_percent(percpu=True)
        cpu0.append(cpu[0])
        cpu1.append(cpu[1])
        cpu2.append(cpu[2])
        cpu3.append(cpu[3])
        cpucurrenttime=cpucurrenttime+1
        cputime.append(str(cpucurrenttime))
        cpus.append(psutil.cpu_percent())

        if len(cputime) == 20:
            cpu0.pop(0)
            cpu1.pop(0)
            cpu2.pop(0)
            cpu3.pop(0)
            cpus.pop(0)
            cputime.pop(0)

        self.Axes.cla()
        self.Axes.plot(cputime, cpu0,label='cpu0')
        self.Axes.plot(cputime, cpu1,label='cpu1')
        self.Axes.plot(cputime, cpu2,label='cpu2')
        self.Axes.plot(cputime, cpu3,label='cpu3')
        self.Axes.plot(cputime, cpus,label='All CPUs', color='black')
        self.Axes.set_title("CPUs Usage")
        self.Axes.set_xlim(0, 20)
        self.Axes.set_ylim(0, 100)
        self.Axes.set_xlabel('Seconds')
        self.Axes.set_ylabel('CPUs')
        self.Axes.grid(True)
        self.Axes.legend(loc='upper left')
        self.draw()

#######################################################################################################
'''
class TwoDCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        #fig = plt.figure()
        self.Axes = fig.gca(projection='3d')
        self.compute_initial_figure()
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
    def compute_initial_figure(self):
        pass

class PolygonCPUs(TwoDCanvas):
    def __init__(self, *args, **kwargs):
        TwoDCanvas.__init__(self, *args, **kwargs)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_figure)
        self.timer.start(1000)

    def compute_initial_figure(self):
        global cpu0
        global cpu1
        global cpu2
        global cpu3
        global cputime
        global cpucurrenttime
        global Axes

        cpu0 = []
        cpu1 = []
        cpu2 = []
        cpu3 = []
        cputime = []
        cpucurrenttime = 0

        cpu0.append((0,0))
        cpu1.append((0,0))
        cpu2.append((0,0))
        cpu3.append((0,0))
        cpus = []
        cpus.append(cpu0)
        cpus.append(cpu1)
        cpus.append(cpu2)
        cpus.append(cpu3)

        zs=range(4)
        poly = PolyCollection(cpus, facecolors=['r', 'g', 'b', 'y'], alpha=.6)
        self.Axes.add_collection3d(poly, zs=zs, zdir='y')
        self.Axes.set_xlabel('Seconds')
        self.Axes.set_ylabel('CPUS')
        self.Axes.set_zlabel('Percent 100%')
        self.Axes.set_title("CPUs Usage")
        self.Axes.set_xlim(0,101)
        self.Axes.set_ylim(-1, 4)
        self.Axes.set_zlim(0, 100)
        self.Axes.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        self.Axes.grid(True)
        self.Axes.legend()

    def update_figure(self):
        global cpu0
        global cpu1
        global cpu2
        global cpu3
        global cputime
        global cpucurrenttime
        global Axes

        cpu = psutil.cpu_percent(interval=1, percpu=True)
        cpu0.append((cpucurrenttime,cpu[0]))
        cpu1.append((cpucurrenttime,cpu[1]))
        cpu2.append((cpucurrenttime,cpu[2]))
        cpu3.append((cpucurrenttime,cpu[3]))
        cpucurrenttime=cpucurrenttime+1
        cputime.append(str(cpucurrenttime))

        cpus = []
        cpus.append(cpu0)
        cpus.append(cpu1)
        cpus.append(cpu2)
        cpus.append(cpu3)

        zs=range(4)
        if len(cputime) == 100:
            cpu0.append((cpucurrenttime, 0))
            cpu1.append((cpucurrenttime, 0))
            cpu2.append((cpucurrenttime, 0))
            cpu3.append((cpucurrenttime, 0))
            cpus = []
            cpus.append(cpu0)
            cpus.append(cpu1)
            cpus.append(cpu2)
            cpus.append(cpu3)
            self.timer.stop()

        self.Axes.cla()
        poly = PolyCollection(cpus, facecolors=['r', 'g', 'b', 'y'], alpha=.6)
        self.Axes.add_collection3d(poly, zs=zs, zdir='y')
        self.Axes.set_xlabel('Seconds')
        self.Axes.set_ylabel('CPUS')
        self.Axes.set_zlabel('Percent 100%')
        self.Axes.set_title("CPUs Usage")
        self.Axes.set_xlim(0,101)
        self.Axes.set_ylim(-1, 4)
        self.Axes.set_zlim(0, 100)
        self.Axes.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        self.Axes.grid(True)
        self.Axes.legend()
        self.draw()

'''


