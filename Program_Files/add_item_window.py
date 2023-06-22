'''
Script to display the add item manually window.

Allows users to add items manually.
'''

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal
import sys
from .info_windows import Add_Item_Manually_Window


class Add_Item_Window(QMainWindow):
    data_sent = pyqtSignal(list)

    def __init__(self):

        super(Add_Item_Window, self).__init__()
        uic.loadUi('Program_Files/UI_Files/adding_item_window.ui', self)

        # menu
        self.action_how_to_use = self.findChild(
            QtWidgets.QAction, 'actionHow_to_Use')

        # frames for plainTextEdit Boxes
        self.frame2 = self.findChild(QtWidgets.QFrame, 'frame_2')
        self.frame3 = self.findChild(QtWidgets.QFrame, 'frame_3')
        self.frame4 = self.findChild(QtWidgets.QFrame, 'frame_4')
        self.frame5 = self.findChild(QtWidgets.QFrame, 'frame_5')
        self.frame6 = self.findChild(QtWidgets.QFrame, 'frame_6')
        self.frame7 = self.findChild(QtWidgets.QFrame, 'frame_7')

        self.btn_add_to_inventory = self.findChild(
            QtWidgets.QPushButton, 'btn_add_to_inventory')

        self.btn_add_to_inventory.setStyleSheet(
            '''
            QPushButton {
                background-color: white;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: rgb(200, 255, 200);
            }
            '''
        )

        # adding stylesheet to sub frames 2-7
        frames = [self.frame2, self.frame3, self.frame4,
                  self.frame5, self.frame6, self.frame7]
        for frame in frames:
            frame.setStyleSheet(
                '''
                QFrame {
                    background-color: rgb(236, 236, 236);
                    border: 1px solid rgb(169, 169, 169);
                    border-radius: 4px;
                    padding: 4px;
                }
                QLabel {
                    border: none;
                }
                '''
            )

        self.part_number = self.findChild(
            QtWidgets.QPlainTextEdit, 'plainTextEdit_part_number')
        self.manu_part_number = self.findChild(
            QtWidgets.QPlainTextEdit, 'plainTextEdit_manu_part_number')
        self.description = self.findChild(
            QtWidgets.QPlainTextEdit, 'plainTextEdit_description')
        self.customer_ref = self.findChild(
            QtWidgets.QPlainTextEdit, 'plainTextEdit_customer_ref')

        self.unit_price = self.findChild(
            QtWidgets.QDoubleSpinBox, 'SpinBox_unit_price')
        self.quantity = self.findChild(
            QtWidgets.QSpinBox, 'spinBox_quantity')

        # attaching functions
        self.action_how_to_use.triggered.connect(self.how_to_use)
        self.btn_add_to_inventory.clicked.connect(self.send_to_main_window)

        self.show()

    def how_to_use(self):
        '''
        Function to how to use window.
        '''
        self.how_add_manually_window = Add_Item_Manually_Window()
        self.how_add_manually_window.show()

    def send_to_main_window(self):
        '''
        Function to get in the plainTextEdits.
        '''

        self.data_sent.emit([22])
