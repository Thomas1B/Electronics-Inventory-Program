from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtWidgets
from PyQt5 import uic
import sys


class info_window(QMainWindow):
    def __init__(self):
        super(info_window, self).__init__()

        # loading ui file
        uic.loadUi('Program_Files/info_window.ui')

        self.show()



if __name__ == "__main__":
    # runnning program
    app = QApplication(sys.argv)
    window1 = info_window()
    app.exec_()
