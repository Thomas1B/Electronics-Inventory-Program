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
from .info_windows import How_Add_Item_Manually_Window
from .data_handling import labels
import pandas as pd


class Add_Item_Window(QMainWindow):
    '''
    Class to show adding Item manually window.
    '''

    # Signal for sending data (see function send_item_info).
    data_sent = pyqtSignal(pd.DataFrame)

    def __init__(self, parent=None) -> None:
        super(Add_Item_Window, self).__init__(parent)
        uic.loadUi('Program_Files/UI_Files/adding_item_window.ui', self)

        # info window
        self.how_to_use_window = How_Add_Item_Manually_Window()

        # Menu
        self.action_how_to_use = self.findChild(
            QtWidgets.QAction, 'actionHow_to_Use')

        # Buttons
        self.btn_add_to_inventory = self.findChild(
            QtWidgets.QPushButton, 'btn_add_to_inventory'
        )

        # plainTextEdits
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

        # frames for plainTextEdit Boxes
        self.entries_frame = self.findChild(QtWidgets.QFrame, 'entries_frame')
        self.part_num_frame = self.findChild(
            QtWidgets.QFrame, 'part_num_frame'
        )
        self.manu_part_num_frame = self.findChild(
            QtWidgets.QFrame, 'manu_part_num_frame'
        )
        self.descrip_frame = self.findChild(QtWidgets.QFrame, 'descrip_frame')
        self.cus_ref_frame = self.findChild(QtWidgets.QFrame, 'cus_ref_frame')
        self.price_frame = self.findChild(QtWidgets.QFrame, 'price_frame')
        self.quantity_frame = self.findChild(
            QtWidgets.QFrame, 'quantity_frame'
        )

        self.entry_frames_list = [
            self.part_num_frame, self.manu_part_num_frame, self.descrip_frame,
            self.cus_ref_frame, self.price_frame, self.quantity_frame
        ]

        ''' Attaching Functions '''
        # Menu
        self.action_how_to_use.triggered.connect(self.how_to_use)

        # Buttons
        self.btn_add_to_inventory.clicked.connect(self.send_item_info)

        ''' Styling '''

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

        # adding stylesheet to sub frames
        for frame in self.entry_frames_list:
            frame.setStyleSheet(
                '''
                QFrame {
                    background-color: rgb(236, 236, 236);
                    border: 1px solid rgb(169, 169, 169);
                    border-radius: 4px;
                    padding: 5px;
                }

                QPlainTextEdit {
                    font-size: 14px;
                }

                QLabel {
                    font-size: 16px;
                    font-family: Arial;
                    font-weight: bold;
                    border: none;
                }

                QSpinBox, QDoubleSpinBox {
                    border: 1px solid rgb(169, 169, 169);
                    background-color: white;
                    padding: 5px;
                }
                '''
            )

    def how_to_use(self) -> None:
        '''
        Function to how to use window.
        '''
        self.how_to_use_window.show()

    def closeEvent(self, event) -> None:
        '''
        Function to detect when user closes the window.

            Parameters:
                event: QtGui.QCloseEvent.
        '''
        event.accept()

    def check_user_entries(self) -> list:
        '''
        Function to read in the user entries and check if they meant the requirments

            Parameters:
                None

            Returns
                list of item info.
        '''

        # reading the plainTextEdits
        part_number = self.part_number.toPlainText()
        manu_part_number = self.manu_part_number.toPlainText()
        description = self.description.toPlainText()
        customer_ref = self.customer_ref.toPlainText()
        unit_price = self.unit_price.value()
        quantity = self.quantity.value()

        # Condition the user must meet when adding an item
        if not description:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Entry Needed")
            pixmapi = getattr(QtWidgets.QStyle, "SP_MessageBoxCritical")
            icon = self.style().standardIcon(pixmapi)
            msg.setWindowIcon(icon)
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Item description is nessecary!")
            text = 'This is used to sort items into their respective category.'
            msg.setInformativeText(text)
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            _ = msg.exec_()
            return

        elif unit_price == 0:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("No Price")
            pixmapi = getattr(QtWidgets.QStyle, "SP_MessageBoxWarning")
            icon = self.style().standardIcon(pixmapi)
            msg.setWindowIcon(icon)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            header = 'Unit Price is recommended!'
            msg.setText(header)
            text = "Only leave blank if you are sure you do not need this field."
            msg.setInformativeText(text)
            msg.setStandardButtons(
                QtWidgets.QMessageBox.Ok |
                QtWidgets.QMessageBox.Cancel
            )
            user = msg.exec_()
            if user == QtWidgets.QMessageBox.Cancel:
                return

        # List must be in the same order as "labels" in data_handling.py
        item_info = [part_number,
                     manu_part_number,
                     description,
                     customer_ref,
                     unit_price,
                     quantity]

        return item_info

    def send_item_info(self) -> None:
        '''
        Function to send data to the main window.

        Data must be emitted as a "DataFrame"
        '''
        item_info = self.check_user_entries()

        if item_info:
            # if there is item info, turn into a DataFrame.
            item = pd.DataFrame(pd.Series(item_info)).T
            item.columns = labels
            self.data_sent.emit(item)  # sending data to another window.
