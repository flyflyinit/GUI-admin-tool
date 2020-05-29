import qtmodern
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QGroupBox, QVBoxLayout, QScrollArea
from project.main import *


class AboutWindow(QWidget):
    def __init__(self,plotstostart):
        super().__init__()
        self.plotstostart = plotstostart
        self.setGeometry(0, 0, 300, 500)
        self.setWindowTitle("About")
        self.UI()
        #self.setWindowIcon(QIcon("icon.png"))
        self.show()

    def UI(self):
        self.layouts()

    def layouts(self):
        top = QHBoxLayout()
        text = QLabel("ksdhfkisd sdihbskdh bsiu yhdbiu hsdbkfhusdfuk bhfb khu bkh uidkh ksdj vhbksd\nksjadhcbskdhv\nasfkajsdhaksjhdcb\n\n")
        groupBox = QGroupBox()
        text.setContentsMargins(30, 30, 30, 30)  # left ,#top ,#right , #bottom
        top.addWidget(text)

        groupBox.setLayout(top)
        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)
        # scroll.setFixedHeight(400)
        submain = QVBoxLayout()
        submain.addWidget(scroll)
        self.setLayout(submain)

    def closeEvent(self, event):
        for plot in self.plotstostart:
            try:
                plot.start(1000)
            except:
                pass


        #app = QApplication(sys.argv)
        #app.setApplicationName('MyWindow')
        #main = mainWindow()
        #qtmodern.styles.light(app)
        #mw = qtmodern.windows.ModernWindow(main)
        #mw.show()
        #sys.exit(app.exec_())
