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

        # frames for plainTextEdit Boxes
        self.frame2 = self.findChild(QtWidgets.QFrame, 'frame_2')
        self.frame3 = self.findChild(QtWidgets.QFrame, 'frame_3')
        self.frame4 = self.findChild(QtWidgets.QFrame, 'frame_4')
        self.frame5 = self.findChild(QtWidgets.QFrame, 'frame_5')
        self.frame6 = self.findChild(QtWidgets.QFrame, 'frame_6')
        self.frame7 = self.findChild(QtWidgets.QFrame, 'frame_7')

        self.btn_add_to_inventory = self.findChild(
            QtWidgets.QPushButton, 'btn_add_to_inventory')

        self.btn_add_to_inventory.clicked.connect(self.read_textedits)

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
