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
        uic.loadUi('Program_Files/UI_Files/info_window.ui', self)
        # self.adjustSize()

        self.show()


class User_Info_Window(QMainWindow):
    def __init__(self):
        super(User_Info_Window, self).__init__()

        uic.loadUi('Program_Files/UI_Files/how_to_use.ui', self)

        self.show()


class Add_Item_Window(QMainWindow):
    def __init__(self):
        super(Add_Item_Window, self).__init__()
        uic.loadUi('Program_Files/UI_Files/adding_item_window.ui', self)

        self.frame2 = self.findChild(QtWidgets.QFrame, 'frame_2')
        self.frame3 = self.findChild(QtWidgets.QFrame, 'frame_3')
        self.frame4 = self.findChild(QtWidgets.QFrame, 'frame_4')
        self.frame5 = self.findChild(QtWidgets.QFrame, 'frame_5')
        self.frame6 = self.findChild(QtWidgets.QFrame, 'frame_6')
        self.frame7 = self.findChild(QtWidgets.QFrame, 'frame_7')
        frames = [self.frame2, self.frame3, self.frame4,
                  self.frame5, self.frame6, self.frame7]

        for frame in frames:
            frame.setStyleSheet(
                '''
                QFrame {
                    border: 2px solid black;
                }
                QLabel {
                    border: none;
                }
                '''
            )

        self.show()

