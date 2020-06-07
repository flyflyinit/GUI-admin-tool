#!/bin/python3
import qtmodern.styles
import qtmodern.windows
from PyQt5.QtCore import Qt

from project import about
from project.about import *
from project.dashboard import mainDashboard
from project.system import mainsystem
from project.users import mainusers
from project.networking import mainnetworking
from project.firewall import mainFirewall
from project.services import mainServices
from project.backup import mainbackup
from project.terminal import mainterminal
from project.logs import mainLogs

try:
    from PyQt5 import QtCore, QtWidgets
    from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QDockWidget, QVBoxLayout, QListWidget, QAbstractItemView, \
        QMessageBox, QApplication, QSizePolicy, QPushButton, QGroupBox, QScrollArea, QStyleOptionTitleBar, QStyle
    from PyQt5.QtGui import QIcon
    from PyQt5.QtGui import QPixmap
except ImportError as e:
    print(
        f'package PyQt5 Not Found\n{e}\ntry :\npip3 install --user pyqt5\nOR\ndnf install python3-pyqt5, yum install python3-pyqt5\n')

try:
    import qtmodern.styles
    import qtmodern.windows
except ImportError as e:
    print(f'package qtmodern Not Found\n{e}\ntry :\npip3 install --user qtmodern\n')


except ImportError as e:
    print(f'package not found\n{e}\n')


class mainWindow(QWidget):
    def __init__(self, parent=None):
        super(mainWindow, self).__init__(parent)
        self.setWindowTitle("PyAdminDash")
        self.setWindowIcon(QIcon('/home/abdelmoumen/test.png'))
        self.UI()

        titleBarHeight = self.style().pixelMetric(
            QStyle.PM_TitleBarHeight,
            QStyleOptionTitleBar(),
            self
        )
        geometry = app.desktop().availableGeometry()
        geometry.setHeight(geometry.height() - (titleBarHeight * 2))

        self.setGeometry(geometry)

    def UI(self):
        QMessageBox.information(self,'Information','Make Sure You execute this tool with the required permission, and you installed the requirements\ncheck README.md, Pipfile')
        self.layouts()
        self.widgets()

    def layouts(self):
        menuLayout = QVBoxLayout()
        menuLayout.setContentsMargins(0, 0, 0, 0)
        about = QPushButton("|  About")
        about.clicked.connect(lambda: aboutClicked(self))
        about.setFixedHeight(30)
        about.setFixedWidth(80)
        about.setStyleSheet("color: #303a46 ; border: 0px solid #303a46")
        menuLayout.addWidget(about)

        self.mainLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QHBoxLayout()

        self.bottomLeftLayout = QHBoxLayout()
        self.bottomRightLayout = QVBoxLayout()

        logo = QLabel(self)
        pixmap = QPixmap('icons/logo.png')
        pixmap = pixmap.scaled(80, 80)
        logo.setPixmap(pixmap)

        refresh = QPushButton("🔁")
        refresh.clicked.connect(self.getContentTrigger)
        refresh.setStyleSheet("color: #95a5a6; background-color: #303a46 ; border: 0px solid #303a46")
        refresh.setFixedHeight(30)
        refresh.setFixedWidth(30)
        b = QHBoxLayout()
        b.addWidget(refresh)

        logotext = QLabel("PyAdminDash")
        logotext.setStyleSheet("color: #303a46;font: bold 25px;")
        logotext.setContentsMargins(15, 0, 0, 0)
        self.topLayout.addWidget(logo)
        self.topLayout.addWidget(logotext)
        self.topLayout.addLayout(menuLayout)
        self.topLayout.addStretch()
        self.topLayout.addLayout(b)

        self.bottomLayout.addLayout(self.bottomLeftLayout)
        self.bottomLayout.addLayout(self.bottomRightLayout, 1)

        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.bottomLayout)

        self.setLayout(self.mainLayout)

    def widgets(self):
        self.dockWidget = QDockWidget(self)
        self.listWidget = QListWidget(self)
        self.listWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.listWidget.setStyleSheet(
            "color: #303a46; selection-background-color: #303a46 ; selection-color: #95a5a6 ;border: 0px solid #95a5a6")

        self.dockWidget.setFixedWidth(180)

        self.item0 = QtWidgets.QListWidgetItem("   ️💻  Dashboard")
        self.item0.setSizeHint(QtCore.QSize(50, 50))
        self.listWidget.addItem(self.item0)

        self.item1 = QtWidgets.QListWidgetItem("   ️🌐  System Information")
        self.item1.setSizeHint(QtCore.QSize(50, 50))
        self.listWidget.addItem(self.item1)

        self.item2 = QtWidgets.QListWidgetItem("  🚹 ‍ Users Statistics")
        self.item2.setSizeHint(QtCore.QSize(50, 50))

        self.listWidget.addItem(self.item2)
        self.item3 = QtWidgets.QListWidgetItem("  📚  Backup")
        self.item3.setSizeHint(QtCore.QSize(50, 50))
        self.listWidget.addItem(self.item3)

        self.item4 = QtWidgets.QListWidgetItem("  📶  Networking")
        self.item4.setSizeHint(QtCore.QSize(50, 50))
        self.listWidget.addItem(self.item4)

        self.item5 = QtWidgets.QListWidgetItem("  🏢  Firewall")
        self.item5.setSizeHint(QtCore.QSize(50, 50))
        self.listWidget.addItem(self.item5)

        self.item6 = QtWidgets.QListWidgetItem("  ⚙  Services")
        self.item6.setSizeHint(QtCore.QSize(50, 50))
        self.listWidget.addItem(self.item6)

        self.item7 = QtWidgets.QListWidgetItem("  📚  Logs")
        self.item7.setSizeHint(QtCore.QSize(50, 50))
        self.listWidget.addItem(self.item7)

        self.item8 = QtWidgets.QListWidgetItem("  ⌨  Terminal")
        self.item8.setSizeHint(QtCore.QSize(50, 50))
        self.listWidget.addItem(self.item8)

        self.listWidget.itemSelectionChanged.connect(self.getContentTrigger)

        self.dockWidget.setWidget(self.listWidget)
        self.dockWidget.setFloating(False)

        self.bottomLeftLayout.addWidget(self.dockWidget)
        self.listWidget.setCurrentItem(self.item0)

    def getContentTrigger(self):
        si = self.listWidget.selectedItems()[0]
        if si == self.item0:
            self.setCursor(Qt.WaitCursor)
            self.clearLayout(self.bottomRightLayout)
            mainDashboard.getContentDashboard(self)
            self.setCursor(Qt.ArrowCursor)
        elif si == self.item1:
            self.setCursor(Qt.WaitCursor)
            self.clearLayout(self.bottomRightLayout)
            mainsystem.getContentSystem(self)
            self.setCursor(Qt.ArrowCursor)
        elif si == self.item2:
            self.setCursor(Qt.WaitCursor)
            self.clearLayout(self.bottomRightLayout)
            mainusers.getContentUsers(self)
            self.setCursor(Qt.ArrowCursor)
        elif si == self.item3:
            self.setCursor(Qt.WaitCursor)
            self.clearLayout(self.bottomRightLayout)
            mainbackup.getContentBackup(self)
            self.setCursor(Qt.ArrowCursor)
        elif si == self.item4:
            self.setCursor(Qt.WaitCursor)
            self.clearLayout(self.bottomRightLayout)
            mainnetworking.getContentNetwork(self)
            self.setCursor(Qt.ArrowCursor)
        elif si == self.item5:
            self.setCursor(Qt.WaitCursor)
            self.clearLayout(self.bottomRightLayout)
            mainFirewall.getContentFirewall(self)
            self.setCursor(Qt.ArrowCursor)
        elif si == self.item6:
            self.setCursor(Qt.WaitCursor)
            self.clearLayout(self.bottomRightLayout)
            mainServices.getContentServices(self)
            self.setCursor(Qt.ArrowCursor)
        elif si == self.item7:
            self.setCursor(Qt.WaitCursor)
            self.clearLayout(self.bottomRightLayout)
            mainLogs.getContentLogs(self)
            self.setCursor(Qt.ArrowCursor)
        elif si == self.item8:
            self.setCursor(Qt.WaitCursor)
            self.clearLayout(self.bottomRightLayout)
            mainterminal.main(self)
            self.setCursor(Qt.ArrowCursor)

        else:
            QMessageBox.warning(self, "warning", "no section selected, please selecet a section")

    def clearLayout(self, layout):
        try:
            del self.memoryC
        except Exception:
            pass
        try:
            del self.cpuC
        except Exception:
            pass
        try:
            del self.cpusC
        except Exception:
            pass
        try:
            del self.usg
        except Exception:
            pass
        try:
            del self.read
        except Exception:
            pass
        try:
            del self.write
        except Exception:
            pass
        try:
            del self.all
        except Exception:
            pass
        try:
            del self.all2
        except Exception:
            pass
        try:
            del self.lastbadlogins
        except Exception:
            pass
        try:
            del self.lastlogins
        except Exception:
            pass
        try:
            del self.netSent
        except Exception:
            pass
        try:
            del self.netRec
        except Exception:
            pass
        try:
            del self.sw
        except Exception:
            pass

        try:
            del self.tableIncBackup
        except Exception:
            pass
        try:
            del self.tableFullBackup
        except Exception:
            pass
        try:
            del self.tableFw
        except Exception:
            pass
        try:
            del self.dic
        except Exception:
            pass
        try:
            del self.tableNet
        except Exception:
            pass
        try:
            del self.tableLogs
        except Exception:
            pass
        try:
            del self.dic
        except Exception:
            pass
        try:
            del self.dic2
        except Exception:
            pass
        try:
            del self.dic3
        except Exception:
            pass
        try:
            del self.dic4
        except Exception:
            pass
        try:
            del self.dic5
        except Exception:
            pass
        try:
            del self.dic6
        except Exception:
            pass
        try:
            del self.tableServices
        except Exception:
            pass
        try:
            del self.form
        except Exception:
            pass
        try:
            del self.tableUsers
        except Exception:
            pass
        try:
            del self.listLoggedOn
        except Exception:
            pass

        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clearLayout(child.layout())


def aboutClicked(self):
    self.aboutWindow = about.About()
    self.aw = qtmodern.windows.ModernWindow(self.aboutWindow)
    self.aw.show()


if __name__ == '__main__':
    import sys

    print("===================================================================")
    print(
        "PS: this tool is RPM Distributions Based (Fedora,centos,redhat)\nMake Sure You execute this tool with the admin permission, and you installed the requirements")
    print(
        "To setup your virtual environment:\n1- install pipenv \n  pip3 install pipenv\n2- install virtual environment dependecies\n  pipenv sync")
    print("===================================================================\n\n")

    app = QApplication(sys.argv)
    main = mainWindow()
    qtmodern.styles.light(app)
    mw = qtmodern.windows.ModernWindow(main)
    mw.show()
    sys.exit(app.exec_())
