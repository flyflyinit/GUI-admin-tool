import datetime
import systemd.journal
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QDateTimeEdit

if __name__ == '__main__':
    import datetime
    s = 1591133789367049 / 1000000
    h = datetime.datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S.%f')
    print(h)