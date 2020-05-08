#!/bin/python3

import sys
try:
    from PyQt5 import QtCore, QtWidgets
    from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QDockWidget, QVBoxLayout, QListWidget, QAbstractItemView, QMessageBox, QApplication
    from PyQt5.QtGui import QIcon
    from PyQt5.QtGui import QPixmap
except ImportError as e:
    print(f'package PyQt5 Not Found\n{e}\ntry :\npip3 install --user pyqt5\nOR\ndnf install python3-pyqt5, yum install python3-pyqt5\n')

try:
    import qtmodern.styles
    import qtmodern.windows
except ImportError as e:
    print(f'package qtmodern Not Found\n{e}\ntry :\npip3 install --user qtmodern\n')

try:
    from system import mainsystem
    from users import mainusers
    from backup import mainbackup
    from terminal import mainterminal
except ImportError as e:
    print(f'package not found\n{e}\n')


class mainWindow(QWidget):
    def __init__(self):
        super().__init__()
        #self.setGeometry(0, 0, 1500, 500)
        self.setWindowTitle("GUI admin tool")
        self.setWindowIcon(QIcon('icons/admin.png'))
        self.UI()
        self.showFullScreen()


    def UI(self):
        self.layouts()
        self.widgets()

    def layouts(self):
        self.mainLayout=QVBoxLayout()
        self.topLayout=QHBoxLayout()
        self.bottomLayout=QHBoxLayout()

        self.bottomLeftLayout=QHBoxLayout()
        self.bottomRightLayout=QVBoxLayout()
        logo = QLabel(self)
        pixmap = QPixmap('icons/admin.png')
        pixmap = pixmap.scaled(50, 50)
        logo.setPixmap(pixmap)

        self.topLayout.addWidget(logo)

        self.bottomLayout.addLayout(self.bottomLeftLayout)
        self.bottomLayout.addLayout(self.bottomRightLayout)
        self.bottomLayout.addStretch()

        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.bottomLayout)

        self.setLayout(self.mainLayout)

    def widgets(self):
        self.dockWidget = QDockWidget(self)
        self.listWidget = QListWidget(self)
        self.listWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.listWidget.setStyleSheet("color: #2c3e50; selection-background-color: #2c3e50 ; selection-color: #95a5a6 ;border: 0px solid #95a5a6")

        self.dockWidget.setFixedWidth(180)

        self.item1 = QtWidgets.QListWidgetItem("System Information")
        self.item1.setSizeHint(QtCore.QSize(50, 50))
        self.listWidget.addItem(self.item1)
        self.item2 = QtWidgets.QListWidgetItem("Users Statistics")
        self.item2.setSizeHint(QtCore.QSize(50, 50))
        self.listWidget.addItem(self.item2)
        self.item3 = QtWidgets.QListWidgetItem("Backup")
        self.item3.setSizeHint(QtCore.QSize(50, 50))
        self.listWidget.addItem(self.item3)
        self.item4 = QtWidgets.QListWidgetItem("Terminal")
        self.item4.setSizeHint(QtCore.QSize(50, 50))
        self.listWidget.addItem(self.item4)
        self.listWidget.itemSelectionChanged.connect(self.getContentTrigger)

        self.dockWidget.setWidget(self.listWidget)
        self.dockWidget.setFloating(False)

        self.bottomLeftLayout.addWidget(self.dockWidget)
        self.listWidget.setCurrentItem(self.item3)


    def getContentTrigger(self):
        si = self.listWidget.selectedItems()[0]
        if si==self.item1:
            self.clearLayout(self.bottomRightLayout)
            mainsystem.getContentSystem(self)
        elif si==self.item2:
            self.clearLayout(self.bottomRightLayout)
            mainusers.getContentUsers(self)
        elif si==self.item3:
            self.clearLayout(self.bottomRightLayout)
            mainbackup.getContentBackup(self)
        elif si==self.item4:
            self.clearLayout(self.bottomRightLayout)
            mainterminal.main(self)

        else:
            QMessageBox.warning(self,"warning","no section selected, please selecet a section")

    def clearLayout(self,layout):
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
            del self.ioC
        except Exception:
            pass
        try:
            del self.iooC
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

        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clearLayout(child.layout())

def main():
    print("===================================================================")
    print("PS: this tool is RPM Distributions Based (Fedora,centos,redhat)\nMake Sure You execute this tool with the admin permission, and you installed the requirements")
    print("To setup your virtual environment:\n1- install pipenv \n  pip3 install pipenv\n2- install virtual environment dependecies\n  pipenv install")
    print("===================================================================\n\n")
    App = QApplication(sys.argv)
    window = mainWindow()
    qtmodern.styles.light(App)
    mw = qtmodern.windows.ModernWindow(window)
    mw.showFullScreen()
    sys.exit(App.exec_())

if __name__ == '__main__':
    main()
