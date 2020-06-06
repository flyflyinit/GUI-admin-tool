try:
    from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QLabel, QMessageBox, QPushButton, QHBoxLayout, \
    QVBoxLayout, QScrollArea, QGroupBox
except ImportError as e:
    print(f'package PyQt5 Not Found\n{e}\ntry :\npip3 install --user pyqt5\nOR\ndnf install python3-pyqt5, yum install python3-pyqt5\n')

try:
    import subprocess
except ImportError as e:
    print(f'package not found\n{e}\n')


class ConfigureSystemWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 300, 500)
        self.setWindowTitle("About PyAdminDash")
        self.widgets()

    def widgets(self):
        top = QVBoxLayout()
        title = QLabel("PyAdminDash")
        text = QLabel("PyAdminDash is a GUI Linux System Administration Tool Based on Fedora/Centos/Redhat\nthe tool was designed and developped to provide an easy interaction with the operating system and its compenents,\nmaking the complex operating system tasks and compenents easy to deploy and monitor\nand by implementing plots and graphs you will have the full picture of your Opertaing System in realtime.\n\nPyAdminDash was developped as an bachelor final project in the university of Sidi Bel Abbes -Algeria-\nby Boudjemma Djawed  =>  github.com/DjawedBoudjemaa\nand Abdelmoumen Drici  =>  github.com/flyflyinit\n\nPlease If you have any feedback or suggestion we will be happy to hear from you :)\nYour contributions are very welcomed :D\ngithub.com/flyflyinit/GUI-admin-tool")
        title.setStyleSheet("color: #303a46;font: bold 14px;")
        text.setStyleSheet("color: #303a46;")
        groupBox = QGroupBox()
        title.setContentsMargins(30, 30, 30, 30)  # left ,#top ,#right , #bottom
        text.setContentsMargins(30,0, 30, 30)  # left ,#top ,#right , #bottom
        top.addWidget(title)
        top.addWidget(text)
        top.addStretch()

        groupBox.setLayout(top)
        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)
        submain = QVBoxLayout()
        submain.addWidget(scroll)
        self.setLayout(submain)
