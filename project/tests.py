from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QProgressBar, QApplication

if __name__ == '__main__':
    cursor = QApplication.overrideCursor()
    waitCursor = (cursor is not None and cursor.shape() == Qt.WaitCursor)
