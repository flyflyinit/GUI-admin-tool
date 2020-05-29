'''
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


class embterminal(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.process = QProcess(self)
        self.terminal = QWidget(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.terminal)
        self.terminal.setFixedSize(1100,550)

        # Works also with urxvt:
        self.process.start('urxvt',['-embed', str(int(self.winId()))])
        #self.process.start(f'xterm -into {str(int(self.winId()))} -hold -geometry 298x500')
        print(self.winId())
        self.setGeometry(1, 1, 800, 600)

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 tabs - pythonspot.com'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        self.show()

class MyTableWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300, 200)

        # Add tabs
        self.tabs.addTab(self.tab1, "Tab 1")
        self.tabs.addTab(self.tab2, "Tab 2")

        # Create first tab
        self.tab1.layout1 = QVBoxLayout(self)
        self.embterminal1 = embterminal()
        self.tab1.layout1.addWidget(self.embterminal1)
        self.tab1.setLayout(self.tab1.layout1)

        # Create second tab
        self.tab2.layout2 = QVBoxLayout(self)
        self.embterminal2 = embterminal()
        self.tab2.layout2.addWidget(self.embterminal2)
        self.tab2.setLayout(self.tab2.layout2)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
'''


from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QStyle, QStyleOptionTitleBar, QPushButton, QVBoxLayout


class MyWindow(QWidget):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)

        self.pushButtonClose = QPushButton(self)
        self.pushButtonClose.setText("Close")
        self.pushButtonClose.clicked.connect(self.on_pushButtonClose_clicked)

        self.layoutVertical = QVBoxLayout(self)
        self.layoutVertical.addWidget(self.pushButtonClose)

        titleBarHeight = self.style().pixelMetric(
            QStyle.PM_TitleBarHeight,
            QStyleOptionTitleBar(),
            self
        )

        geometry = app.desktop().availableGeometry()
        geometry.setHeight(geometry.height() - (titleBarHeight*2))

        self.setGeometry(geometry)

    @QtCore.pyqtSlot()
    def on_pushButtonClose_clicked(self):
        QApplication.instance().quit()

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setApplicationName('MyWindow')

    main = MyWindow()
    main.show()

    sys.exit(app.exec_())