'''

Script to run the info_window.ui

Shows the user information about the program

'''


from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtGui import QIcon
import sys


class Program_Info(QMainWindow):
    '''
    Class to run 
    '''
    def __init__(self, parent=None):
        super(Program_Info, self).__init__(parent)

        # loading ui file
        uic.loadUi('Program_Files/UI_Files/program_information.ui', self)
        # self.adjustSize()

        self.show()


class User_Info_Window(QMainWindow):
    def __init__(self):
        super(User_Info_Window, self).__init__()

        uic.loadUi('Program_Files/UI_Files/how_to_use.ui', self)

        self.show()
