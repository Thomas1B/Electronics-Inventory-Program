'''

Script to run the info_window.ui

Shows the user information about the program

'''


from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtGui import QIcon
import sys


class Info_Window(QMainWindow):
    def __init__(self, parent=None):
        super(Info_Window, self).__init__(parent)

        # loading ui file
        uic.loadUi('Program_Files/info_window.ui', self)
        # self.adjustSize()

        self.show()


class User_Info_Window(QMainWindow):
    def __init__(self):
        super(User_Info_Window, self).__init__()

        uic.loadUi('Program_Files/how_to_use.ui', self)

        self.show()


if __name__ == "__main__":
    # runnning program
    app = QApplication(sys.argv)
    info_window = Info_Window()
    info_window.show()
    app.exec_()
