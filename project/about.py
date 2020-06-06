from PyQt5.QtGui import QPixmap

try:
    from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QLabel, QMessageBox, QPushButton, QHBoxLayout, \
    QVBoxLayout, QScrollArea, QGroupBox
except ImportError as e:
    print(f'package PyQt5 Not Found\n{e}\ntry :\npip3 install --user pyqt5\nOR\ndnf install python3-pyqt5, yum install python3-pyqt5\n')

try:
    import subprocess
except ImportError as e:
    print(f'package not found\n{e}\n')


class About(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 300, 500)
        self.setWindowTitle("About PyAdminDash")
        self.widgets()

    def widgets(self):
        top = QHBoxLayout()
        topright = QVBoxLayout()
        topleft = QVBoxLayout()

        logo = QLabel(self)
        pixmap = QPixmap('icons/logo.png')
        pixmap = pixmap.scaled(210, 210)
        logo.setPixmap(pixmap)
        logotext = QLabel("PyAdminDash")
        logotext.setStyleSheet("color: #303a46;font: bold 25px;")
        logotext.setContentsMargins(15,0,0,0)
        topleft.addWidget(logo)
        topleft.addWidget(logotext)
        topleft.addStretch()

        title = QLabel("PyAdminDash")
        text = QLabel("PyAdminDash is a GUI Linux System Administration Tool Based on Fedora/Centos/Redhat\nthe tool was designed and developped to provide an easy interaction with the operating system and its compenents,\nmaking the complex operating system tasks and compenents easy to deploy and monitor\nand by implementing plots and graphs you will have the full picture of your Opertaing System in realtime.")
        text2 = QLabel("\nPyAdminDash was developped as a bachelor final project in the university of Sidi Bel Abbes -Algeria-\nby Boudjemma Djawed  =>  github.com/DjawedBoudjemaa\nand Abdelmoumen Drici  =>  github.com/flyflyinit\nand supervised by Dr.Boukli\n")
        text3 = QLabel("\nPlease If you have any feedback or suggestion we will be happy to hear from you :)\ngithub.com/flyflyinit/GUI-admin-tool")
        text4 = QLabel("\nLicense: MIT")
        text5 = QLabel("\nContact: Abdelmoumen Drici, abdelmoumendrici@gmail.com\n               Boudjemaa Djawed, jawedbdj@gmail.com")
        title.setStyleSheet("color: #303a46;font: bold 20px;")
        text.setStyleSheet("color: #303a46;")
        text2.setStyleSheet("color: #303a46;font: bold ;")
        text3.setStyleSheet("color: #303a46;")
        text4.setStyleSheet("color: #303a46;font: bold ;")
        text5.setStyleSheet("color: #303a46;font: bold ;")

        groupBox = QGroupBox()
        title.setContentsMargins(30, 30, 30, 30)  # left ,#top ,#right , #bottom
        text.setContentsMargins(30,0, 30, 0)  # left ,#top ,#right , #bottom
        text2.setContentsMargins(30,0, 30, 0)  # left ,#top ,#right , #bottom
        text3.setContentsMargins(30,0, 30, 0)  # left ,#top ,#right , #bottom
        text4.setContentsMargins(30,0, 30, 0)  # left ,#top ,#right , #bottom
        text5.setContentsMargins(30,0, 30, 0)  # left ,#top ,#right , #bottom
        top.setContentsMargins(50,50, 50, 50)  # left ,#top ,#right , #bottom

        topright.addWidget(title)
        topright.addWidget(text)
        topright.addWidget(text2)
        topright.addWidget(text3)
        topright.addWidget(text4)
        topright.addWidget(text5)
        topright.addStretch()

        top.addLayout(topleft)
        top.addLayout(topright)
        top.addStretch()

        groupBox.setLayout(top)
        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)
        submain = QVBoxLayout()
        submain.addWidget(scroll)
        self.setLayout(submain)
