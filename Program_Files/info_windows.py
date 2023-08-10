'''
Script to show pop up information windows.
'''


from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtGui import QIcon
import sys


class Program_Info_Window(QMainWindow):
    '''
    Class to run overview of program information window.
    '''

    def __init__(self, parent=None):
        super(Program_Info_Window, self).__init__(parent=parent)

        # loading ui file
        uic.loadUi('Program_Files/UI_Files/program_information.ui', self)
        # self.adjustSize()


class How_To_Use_Program_Window(QMainWindow):
    '''
    Class to run program how to use program window.
    '''

    def __init__(self, parent=None):
        super(How_To_Use_Program_Window, self).__init__(parent=parent)

        uic.loadUi('Program_Files/UI_Files/how_to_use_program.ui', self)


class How_To_Use_Project_Window(QMainWindow):
    '''
    Class to run program how to use project window.
    '''

    def __init__(self, parent=None):
        super(How_To_Use_Project_Window, self).__init__(parent=parent)

        uic.loadUi('Program_Files/UI_Files/how_to_use_project_window.ui', self)


class How_Add_Item_Manually_Window(QMainWindow):
    '''
    Class to run how to use "Add item Manually" window.
    '''

    def __init__(self, parent=None):
        super(How_Add_Item_Manually_Window, self).__init__(parent=parent)
        uic.loadUi('Program_Files/UI_Files/how_to_use_add_manually.ui', self)

        self.frame = self.findChild(QtWidgets.QFrame, 'frame')
        self.frame.setStyleSheet(
            '''
            QScrollArea {
                border: 1px solid rgb(169, 169, 169);
                border-radius: 4px;
                padding: 4px;
            }
            '''
        )


