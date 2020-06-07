try:
    import psutil
except ImportError as e:
    print(f'package not found\n{e}\n')

try:
    from PyQt5 import QtCore, QtWidgets
except ImportError as e:
    print(
        f'package PyQt5 Not Found\n{e}\ntry :\npip3 install --user pyqt5\nOR\ndnf install python3-pyqt5, yum install python3-pyqt5\n')

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
        self.Axes = fig.add_subplot()
        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class MemoryCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        self.mem_update_figure()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.mem_update_figure)
        self.timer.start(1000)

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
        self.Axes.plot(memtime, swapused, label='used swap', color='black')
        self.Axes.plot(memtime, swapfree, label='free swap', color='gray')
        self.Axes.set_xlabel("Seconds")
        self.Axes.set_ylabel("Bytes")
        self.Axes.set_title("Memory Usage")
        self.Axes.set_xlim(0, 60)
        self.Axes.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        self.Axes.grid(True)
        self.Axes.get_xaxis().set_visible(False)
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
        memcurrenttime = memcurrenttime + 1
        memtime.append(str(memcurrenttime))

        if len(memtime) == 60:
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
        self.Axes.plot(memtime, swapused, label='used swap', color='black')
        self.Axes.plot(memtime, swapfree, label='free swap', color='gray')
        self.Axes.set_xlabel("Seconds")
        self.Axes.set_ylabel("Bytes")
        self.Axes.set_title("Memory Usage")
        self.Axes.set_xlim(0, 60)
        self.Axes.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        self.Axes.grid(True)
        self.Axes.legend(loc='upper left')
        self.draw()


class CpuCanvas(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        self.cpu_update_figure()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.cpu_update_figure)
        self.timer.start(1000)

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
        self.Axes.set_xlim(0, 60)
        self.Axes.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        self.Axes.grid(True)
        self.Axes.get_xaxis().set_visible(False)
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
        cpucurrenttime = cpucurrenttime + 1
        cputimee.append(str(cpucurrenttime))

        if len(cputimee) == 60:
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
        self.Axes.set_xlim(0, 60)
        self.Axes.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        self.Axes.grid(True)
        self.Axes.get_xaxis().set_visible(False)
        self.Axes.legend(loc='upper left')
        self.draw()


class ReadCanvas(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        self.read_update_figure()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.read_update_figure)
        self.timer.start(1000)

    def compute_initial_figure(self):
        global read
        global rtime
        global rcurrenttime
        global Axes
        global readval

        readval = psutil.disk_io_counters()[2]
        read = []
        rtime = []
        rcurrenttime = 0

        self.Axes.plot(rtime, read, label='read bytes')
        self.Axes.set_xlabel("Seconds")
        self.Axes.set_ylabel("Bytes")
        self.Axes.set_title("Disk Read")
        self.Axes.set_xlim(0, 60)
        self.Axes.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        self.Axes.grid(True)
        self.Axes.get_xaxis().set_visible(False)
        self.Axes.legend(loc='upper left')

    def read_update_figure(self):
        global read
        global rtime
        global rcurrenttime
        global Axes
        global readval

        readpreval = readval
        readval = psutil.disk_io_counters()[2]
        read.append(readval - readpreval)

        rcurrenttime = rcurrenttime + 1
        rtime.append(str(rcurrenttime))

        if len(rtime) == 60:
            read.pop(0)
            rtime.pop(0)

        self.Axes.cla()
        self.Axes.plot(rtime, read, label='read bytes')
        self.Axes.set_xlabel("Seconds")
        self.Axes.set_ylabel("Bytes")
        self.Axes.set_title("Disk Read")
        self.Axes.set_xlim(0, 60)
        self.Axes.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        self.Axes.grid(True)
        self.Axes.get_xaxis().set_visible(False)
        self.Axes.legend(loc='upper left')
        self.draw()


class WriteCanvas(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        self.write_update_figure()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.write_update_figure)
        self.timer.start(1000)

    def compute_initial_figure(self):
        global write
        global wtime
        global wcurrenttime
        global Axes
        global writeval

        writeval = psutil.disk_io_counters()[1]
        write = []
        wtime = []
        wcurrenttime = 0

        self.Axes.plot(wtime, write, label='write bytes')
        self.Axes.set_xlabel("Seconds")
        self.Axes.set_ylabel("Bytes")
        self.Axes.set_title("Disk Write")
        self.Axes.set_xlim(0, 60)
        self.Axes.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        self.Axes.grid(True)
        self.Axes.get_xaxis().set_visible(False)
        self.Axes.legend(loc='upper left')

    def write_update_figure(self):
        global write
        global wtime
        global wcurrenttime
        global Axes
        global writeval

        writepreval = writeval
        writeval = psutil.disk_io_counters()[1]

        write.append(writeval - writepreval)
        wcurrenttime = wcurrenttime + 1
        wtime.append(str(wcurrenttime))

        if len(wtime) == 60:
            write.pop(0)
            wtime.pop(0)

        self.Axes.cla()
        self.Axes.plot(wtime, write, label='write bytes')
        self.Axes.set_xlabel("Seconds")
        self.Axes.set_ylabel("Bytes")
        self.Axes.set_title("Disk Write")
        self.Axes.set_xlim(0, 60)
        self.Axes.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        self.Axes.grid(True)
        self.Axes.get_xaxis().set_visible(False)
        self.Axes.legend(loc='upper left')
        self.draw()


class UsageResume(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        self.resume_update_figure()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.resume_update_figure)
        self.timer.start(1000)

    def compute_initial_figure(self):
        global Axes

        people = ('CPU', 'RAM', 'SWAP', 'DISK /')
        y_pos = [0, 1, 2, 3]

        usage = []
        usage.append(psutil.cpu_percent(percpu=False))
        usage.append(psutil.virtual_memory().percent)
        usage.append(psutil.swap_memory().percent)
        usage.append(psutil.disk_usage('/').percent)

        self.Axes.barh(y_pos, usage, align='center')
        self.Axes.set_yticks(y_pos)
        self.Axes.set_yticklabels(people)
        self.Axes.invert_yaxis()
        self.Axes.set_xlabel('Usage 100%')
        self.Axes.set_xlim(0, 100)
        self.Axes.set_title("System Usage")
        self.Axes.grid(True)

    def resume_update_figure(self):
        global Axes
        people = ('CPU', 'RAM', 'SWAP', 'DISK /')
        y_pos = [0, 1, 2, 3]

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
        self.cpus_update_figure()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.cpus_update_figure)
        self.timer.start(1000)

    def compute_initial_figure(self):
        global logicalcpus
        self.cpuLogicalCount = psutil.cpu_count(logical=True)

        logicalcpus = {}
        for c in range(self.cpuLogicalCount):
            logicalcpus[c] = []

        global cpus
        global cputime
        global cpucurrenttime

        cpus = []

        cputime = []
        cpucurrenttime = 0

        cpu = psutil.cpu_percent(percpu=True)

        i = 0
        for c in logicalcpus:
            logicalcpus[c].append(cpu[i])
            i = i + 1

        cpucurrenttime = cpucurrenttime + 1
        cputime.append(str(cpucurrenttime))
        cpus.append(psutil.cpu_percent())

        i = 0
        for c in logicalcpus:
            self.Axes.plot(cputime, logicalcpus[c], label=f'cpu{str(i)}')
            i = i + 1

        self.Axes.plot(cputime, cpus, label='All CPUs', color='black')
        self.Axes.set_xlim(0, 60)
        self.Axes.set_ylim(0, 100)
        self.Axes.set_xlabel('Seconds')
        self.Axes.set_ylabel('CPUs')
        self.Axes.set_title("CPUs Usage")
        self.Axes.grid(True)
        self.Axes.get_xaxis().set_visible(False)
        self.Axes.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        self.Axes.legend(loc='upper left')

    def cpus_update_figure(self):
        global logicalcpus
        global cpus
        global cputime
        global cpucurrenttime

        cpu = psutil.cpu_percent(percpu=True)

        i = 0
        for c in logicalcpus:
            logicalcpus[c].append(cpu[i])
            i = i + 1

        cpucurrenttime = cpucurrenttime + 1
        cputime.append(str(cpucurrenttime))
        cpus.append(psutil.cpu_percent())

        if len(cputime) == 60:
            for c in logicalcpus:
                logicalcpus[c].pop(0)

            cpus.pop(0)
            cputime.pop(0)

        self.Axes.cla()

        i = 0
        for c in logicalcpus:
            self.Axes.plot(cputime, logicalcpus[c], label=f'cpu{str(i)}')
            i = i + 1

        self.Axes.plot(cputime, cpus, label='All CPUs', color='black')
        self.Axes.set_title("CPUs Usage")
        self.Axes.set_xlim(0, 60)
        self.Axes.set_ylim(0, 100)
        self.Axes.set_xlabel('Seconds')
        self.Axes.set_ylabel('CPUs')
        self.Axes.grid(True)
        self.Axes.get_xaxis().set_visible(False)
        self.Axes.legend(loc='upper left')
        self.draw()
