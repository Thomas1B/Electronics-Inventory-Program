'''
Script to display the add item manually window.

Allows users to add items manually.
'''

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtGui import QIcon
import sys


class Add_Item_Window(QMainWindow):
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

        # adding stylesheet to sub frames 2-7
        frames = [self.frame2, self.frame3, self.frame4,
                  self.frame5, self.frame6, self.frame7]
        for frame in frames:
            frame.setStyleSheet(
                '''
                QFrame {
                    border: 1px solid black;
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

        self.btn_add_to_inventory.clicked.connect(self.read_textedits)

        self.show()

    def read_textedits(self):
        '''
        Function to get in the plainTextEdits.
        '''

        part_number = self.part_number.toPlainText()
        manu_part_number = self.manu_part_number.toPlainText()
        description = self.description.toPlainText()
        customer_ref = self.customer_ref.toPlainText()
        unit_price = self.unit_price.value()
        quantity = self.quantity.value()
        k = [part_number, manu_part_number, description,
             customer_ref, unit_price, quantity]
        for i in k:
            print(i, type(i))

    def how_to_use(self):
        '''
        Function to how to use window.
        '''
        pass
