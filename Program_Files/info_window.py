from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtWidgets
from PyQt5 import uic
import sys


class Info_Window(QMainWindow):
    def __init__(self, parent=None):
        super(Info_Window, self).__init__(parent)

        # loading ui file
        uic.loadUi('Program_Files/info_window.ui', self)
        


if __name__ == "__main__":
    # runnning program
    app = QApplication(sys.argv)
    info_window = Info_Window()
    app.exec_()
