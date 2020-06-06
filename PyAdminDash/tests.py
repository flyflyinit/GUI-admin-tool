from PyQt5.QtWidgets import QDateTimeEdit, QFormLayout, QLabel, QApplication, QWidget, QLineEdit, QHBoxLayout,  QPushButton, QRadioButton, QButtonGroup

class mainWindow(QWidget):
    def __init__(self, parent=None):
        super(mainWindow, self).__init__(parent)
        self.setWindowTitle("GUI admin tool")
        self.UI()

    def UI(self):
        layout = QHBoxLayout()  # layout for the central widget
        widget = QWidget(self)  # central widget
        widget.setLayout(layout)

        number_group = QButtonGroup(widget)  # Number group
        self.r0 = QRadioButton("0hhh")
        number_group.addButton(self.r0)
        self.r1 = QRadioButton("1dghdf")
        number_group.addButton(self.r1)
        layout.addWidget(self.r0)
        layout.addWidget(self.r1)

        letter_group = QButtonGroup(widget)  # Letter group
        self.ra = QRadioButton("afghnf")
        letter_group.addButton(self.ra)
        self.rb = QRadioButton("fhnfb")
        letter_group.addButton(self.rb)
        layout.addWidget(self.ra)
        layout.addWidget(self.rb)


        formLayout= QFormLayout()
        sex=QLabel("Sex: ")

        button = QPushButton("Submit")
        button.clicked.connect(self.getValue)

        formLayout.addRow(sex,layout)
        formLayout.addRow(button)

        self.setLayout(formLayout)
        self.show()

    def getValue(self):
        if self.r0.isChecked():
            print("r0")
        if self.r1.isChecked():
            print("r1")
        if self.ra.isChecked():
            print("ra")
        if self.rb.isChecked():
            print("rb")

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    main = mainWindow()
    main.show()
    sys.exit(app.exec_())
