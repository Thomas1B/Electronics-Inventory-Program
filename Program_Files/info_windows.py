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
    Class to run program information window.
    '''

    def __init__(self, parent=None):
        super(Program_Info, self).__init__(parent)

        # loading ui file
        uic.loadUi('Program_Files/UI_Files/program_information.ui', self)
        # self.adjustSize()


class How_To_Use_Program_Window(QMainWindow):
    '''
    Class to run program how to use program window.
    '''

    def __init__(self):
        super(How_To_Use_Program_Window, self).__init__()

        uic.loadUi('Program_Files/UI_Files/how_to_use_program.ui', self)


class Add_Item_Manually_Window(QMainWindow):
    '''
    Class to run how to use "Add item Manually" window.
    '''

    def __init__(self):
        super(Add_Item_Manually_Window, self).__init__()
        uic.loadUi('Program_Files/UI_Files/how_to_use_add_manually.ui', self)
