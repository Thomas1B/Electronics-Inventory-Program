'''
Script to run the project_window.ui

Creates a second window to allow the user to create/edit a project
'''

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtWidgets
from PyQt5 import uic
import sys


class Project_Window(QMainWindow):
    def __init__(self, parent=None):
        super(Project_Window, self).__init__(parent)

        # loading ui file
        uic.loadUi('Program_Files/project_window.ui', self)
        


if __name__ == "__main__":
    # runnning program
    app = QApplication(sys.argv)
    Project_Window = Project_Window()
    Project_Window.show()
    app.exec_()
