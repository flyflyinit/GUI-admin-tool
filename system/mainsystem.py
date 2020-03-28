from datetime import datetime
from system.system import MemoryCanvas
from system.system import CpuCanvas
from system.system import IoCanvas
from system.system import PolygonCPUs
from system.system import UsageResume
from PyQt5.QtWidgets import QGridLayout ,QFormLayout ,QLabel,QGroupBox,QScrollArea,QVBoxLayout
from PyQt5.QtCore import QTimer
import psutil
import platform
import subprocess

def getContentSystem(self):
    self.grid = QGridLayout()

    systemInformation(self)

    memoryC = MemoryCanvas(width=4.5, height=3, dpi=80)
    cpuC = CpuCanvas(width=4.5, height=3, dpi=80)
    ioC = IoCanvas(width=4.5, height=3, dpi=80)
    #iooC = IooCanvas(width=4.5, height=3, dpi=80)
    cpusC = PolygonCPUs(width=4.5, height=3, dpi=80)
    usg = UsageResume(width=4.5, height=3, dpi=80)

    self.grid.addWidget(memoryC, 0, 0)
    self.grid.addWidget(cpuC, 0, 1)
    self.grid.addWidget(cpusC, 0, 2)
    self.grid.addWidget(usg, 1, 0)
    self.grid.addWidget(ioC, 1, 1)
    #self.grid.addWidget(iooC, 1, 1)

    updateUpTimeAndLoadAvgLabel(self)
    updateCpuLabel(self)
    updateMemoryLabels(self)
    updateLabels(self)

def updateUpTimeAndLoadAvgLabel(self):
    with open("/proc/uptime", "r") as f:
        uptime = f.read().split(" ")[0].strip()
    uptime = int(float(uptime))
    uptime_hours = uptime // 3600
    uptime_minutes = (uptime % 3600) // 60

    loadavg = subprocess.Popen("cat /proc/loadavg | awk {'print $1, $2, $3'}",shell=True,stdout=subprocess.PIPE).communicate()[0].decode('utf-8')
    loadavgg = loadavg.split(" ")
    try:
        self.la.setText(f"last one minute:{loadavgg[0]},   5 minutes:{loadavgg[1]},   15 minutes:{loadavgg[2]}")
        self.ut.setText(str(uptime_hours) + ":" + str(uptime_minutes) + " hours")
    except Exception:
        return None
    QTimer.singleShot(3000, lambda: updateUpTimeAndLoadAvgLabel(self))


def updateCpuLabel(self):
    cpususage = ""
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        cpususage = cpususage + f"Core {i}: {percentage}%\n"
    try:
        self.tcu.setText(str(cpususage))
        self.tcu2.setText(f"{psutil.cpu_percent()}%")
    except Exception:
        return None
    QTimer.singleShot(3000, lambda: updateCpuLabel(self))


def updateMemoryLabels(self):
    svmem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    try:
        self.mu.setText(str(f"{svmem.percent}%"))
        self.tm.setText(str(get_size(svmem.total)))
        self.am.setText(str(get_size(svmem.available)))
        self.um.setText(str(get_size(svmem.used)))
        self.su.setText(str(f"{swap.percent}%"))
        self.ts.setText(str(get_size(swap.total)))
        self.fs.setText(str(get_size(swap.free)))
        self.us.setText(str(get_size(swap.used)))
    except Exception:
        return None
    QTimer.singleShot(3000, lambda: updateMemoryLabels(self))


def updateLabels(self):
    partitions = psutil.disk_partitions()
    disks = psutil.disk_io_counters(perdisk=True)
    disk_io = psutil.disk_io_counters()

    partitionn = ''
    for partition in partitions:
        partitionn = partitionn + f"Device: {partition.device}\nMountpoint: {partition.mountpoint}\nFile system type: {partition.fstype}\n"
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            partitionn = partitionn + "\n"
            continue
        partitionn=partitionn+f"Total Size: {get_size(partition_usage.total)}\nUsed: {get_size(partition_usage.used)}\nFree: {get_size(partition_usage.free)}\nPercentage: {partition_usage.percent}%\n\n"

    disksIO = ''
    for disk in disks:
        disksIO = disksIO + f"Disk:{disk}\nRead: {get_size(disks[disk].read_bytes)}\nWrite: {get_size(disks[disk].write_bytes)}\n\n"

    try:
        self.prts.setText(str(partitionn))
        self.rw.setText(str(disksIO))
        self.tr.setText(str(get_size(disk_io.read_bytes)))
        self.tw.setText(str(get_size(disk_io.write_bytes)))
    except Exception:
        return None
    QTimer.singleShot(3000, lambda: updateLabels(self))


#############################################################################

def systemInformation(self):
    self.form = QFormLayout()
    self.groupBox = QGroupBox()

    formright = []
    formleft = []

    with open("/proc/uptime", "r") as f:
        uptime = f.read().split(" ")[0].strip()
    uptime = int(float(uptime))
    uptime_hours = uptime // 3600
    uptime_minutes = (uptime % 3600) // 60

    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)

    loadavg = subprocess.Popen("cat /proc/loadavg | awk {'print $1, $2, $3'}",shell=True,stdout=subprocess.PIPE).communicate()[0].decode('utf-8')
    loadavgg = loadavg.split(" ")

    formleft.append(QLabel('General Informations :'))
    formright.append(QLabel(''))

    formleft.append(QLabel('Hostname :'))
    formright.append(QLabel(platform.node()))

    formleft.append(QLabel('Platform :'))
    formright.append(QLabel(platform.platform()))

    formleft.append(QLabel('Operating Sysyem :'))
    formright.append(QLabel(platform.system()))

    formleft.append(QLabel('Distribution :'))
    formright.append(QLabel(platform.linux_distribution()[0]))

    formleft.append(QLabel('Operating Sysyem release :'))
    formright.append(QLabel(platform.release()))

    formleft.append(QLabel('Machine Architecture :'))
    formright.append(QLabel(platform.architecture()[0]))

    formleft.append(QLabel('Machine Type :'))
    formright.append(QLabel(platform.machine()))

    formleft.append(QLabel('Processor Architecture :'))
    formright.append(QLabel(platform.processor()))

    formleft.append(QLabel('Boot Time :'))
    formright.append(QLabel(f"{bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}"))

    self.ut = QLabel(str(uptime_hours) + ":" + str(uptime_minutes) + " hours")
    formleft.append(QLabel('Uptime :'))
    formright.append(self.ut)

    self.la = QLabel(f"last one minute:{loadavgg[0]},   5 minutes:{loadavgg[1]},   15 minutes:{loadavgg[2]}")
    formleft.append(QLabel('Load Average :'))
    formright.append(self.la)

##################################################################################
    cpufreq = psutil.cpu_freq()

    formleft.append(QLabel(''))
    formright.append(QLabel(''))

    formleft.append(QLabel('CPU informations :'))
    formright.append(QLabel(''))

    cpususage = ""
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        cpususage = cpususage + f"Core {i}: {percentage}%\n"

    self.tcu = QLabel(cpususage)
    formleft.append(QLabel('CPU Usage Per Core :'))
    formright.append(self.tcu)

    self.tcu2 = QLabel(f"{psutil.cpu_percent()}%")
    formleft.append(QLabel('Total CPU Usage :'))
    formright.append(self.tcu2)

    with open("/proc/cpuinfo", "r")  as f:
        info = f.readlines()
    cpuinfo = [x.strip().split(":")[1] for x in info if "model name" in x]
    processors=''
    for index, item in enumerate(cpuinfo):
        processors+="CPU "+str(index) + ": " + item+"\n"

    formleft.append(QLabel('CPUs :'))
    formright.append(QLabel(processors))

    formleft.append(QLabel('Physical Cores :'))
    formright.append(QLabel(str(psutil.cpu_count(logical=False))))

    formleft.append(QLabel('Total Cores :'))
    formright.append(QLabel(str(psutil.cpu_count(logical=True))))

    formleft.append(QLabel('Max Frequency :'))
    formright.append(QLabel(f"{cpufreq.max:.2f}Mhz"))

    formleft.append(QLabel('Min Frequency :'))
    formright.append(QLabel(f'{cpufreq.min:.2f}Mhz'))

    self.cf = QLabel(f"{cpufreq.current:.2f}Mhz")
    formleft.append(QLabel('Current Frequency :'))
    formright.append(self.cf)

######################################################################
    svmem = psutil.virtual_memory()
    swap = psutil.swap_memory()

    formleft.append(QLabel(''))
    formright.append(QLabel(''))
    formleft.append(QLabel('Memory Informations :'))
    formright.append(QLabel(''))

    self.mu = QLabel(f"{svmem.percent}%")
    formleft.append(QLabel('Memory Usage :'))
    formright.append(self.mu)

    self.tm = QLabel(get_size(svmem.total))
    formleft.append(QLabel('Total Memory :'))
    formright.append(self.tm)

    formleft.append(QLabel('Available Memory :'))
    self.am = QLabel(get_size(svmem.available))
    formright.append(self.am)

    self.um = QLabel(get_size(svmem.used))
    formleft.append(QLabel('Used Memory :'))
    formright.append(self.um)

    self.su = QLabel(f"{swap.percent}%")
    formleft.append(QLabel('Swap Usage :'))
    formright.append(self.su)

    self.ts = QLabel(get_size(swap.total))
    formleft.append(QLabel('Total Swap :'))
    formright.append(self.ts)

    formleft.append(QLabel('Free Swap :'))
    self.fs = QLabel(get_size(swap.free))
    formright.append(self.fs)

    self.us = QLabel(get_size(swap.used))
    formleft.append(QLabel('Used Swap :'))
    formright.append(self.us)

##############################################################
    formleft.append(QLabel(''))
    formright.append(QLabel(''))
    formleft.append(QLabel('Disk Informations :'))
    formright.append(QLabel(''))
    partitions = psutil.disk_partitions()
    partitionn = ''
    for partition in partitions:
        partitionn = partitionn + f"Device: {partition.device}\nMountpoint: {partition.mountpoint}\nFile system type: {partition.fstype}\n"
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            partitionn = partitionn + "\n"
            continue
        partitionn=partitionn+f"Total Size: {get_size(partition_usage.total)}\nUsed: {get_size(partition_usage.used)}\nFree: {get_size(partition_usage.free)}\nPercentage: {partition_usage.percent}%\n\n"

    self.prts=QLabel(partitionn)
    formleft.append(QLabel('Partitions :'))
    formright.append(self.prts)

##################################################################

    formleft.append(QLabel('Disk I/O Informations :'))
    formright.append(QLabel(''))
    disk_io = psutil.disk_io_counters()

    disks = psutil.disk_io_counters(perdisk=True)
    disksIO = ''
    for disk in disks:
        disksIO = disksIO + f"Disk:{disk}\nRead: {get_size(disks[disk].read_bytes)}\nWrite: {get_size(disks[disk].write_bytes)}\n\n"

    self.rw = QLabel(disksIO)
    formleft.append(QLabel('Read/Write :'))
    formright.append(self.rw)

    self.tr = QLabel(get_size(disk_io.read_bytes))
    formleft.append(QLabel('Total Read :'))
    formright.append(self.tr)

    self.tw = QLabel(get_size(disk_io.write_bytes))
    formleft.append(QLabel('Total Write :'))
    formright.append(self.tw)



    for i in range(len(formleft)):
        self.form.addRow(formleft[i], formright[i])

    self.form.setContentsMargins(50, 50, 30, 30)  # left ,#top ,#right , #bottom
    self.groupBox.setLayout(self.form)
    self.scroll = QScrollArea()
    self.scroll.setWidget(self.groupBox)
    self.scroll.setWidgetResizable(True)
    #scroll.setFixedHeight(250)

    self.bottomRightLayout.addLayout(self.grid)
    self.bottomRightLayout.addWidget(self.scroll)


def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

