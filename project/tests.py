import datetime
import systemd.journal
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QDateTimeEdit

if __name__ == '__main__':

    dateEdit = QDateTimeEdit(QDate.currentDate())
    dateEdit.setMinimumDate(QDate.currentDate().addDays(-365))
    dateEdit.setMaximumDate(QDate.currentDate().addDays(365))
    dateEdit.setDisplayFormat("yyyy.MM.dd")

