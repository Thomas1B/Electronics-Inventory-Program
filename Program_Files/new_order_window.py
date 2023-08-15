from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtCore import QUrl, QDir
from PyQt5.QtGui import QDesktopServices, QIcon
import pandas as pd
import sys
import os
import shutil


from .data_handling import (
    Inventory,
    Items,
    labels,
    dict_keys,
    load_Inventory,
    get_ordersheet,
    add_order_to_Inventory,
    sort_order,
    get_inventory,
    sort_by,
    load_Items
)

from .gui_handling import (
    wrong_filetype_msg,
    no_files_msg,
    fill_table
)

from .styles import (
    style_central_widget,
    style_table,
    style_sorting_comboBox,
    style_refresh_btn,
    style_toolbar,
    style_menubar
)


class Order_Window(QMainWindow):
    '''
    class to run new order window
    '''

    def __init__(self, parent=None) -> None:
        super(Order_Window, self).__init__(parent=parent)
        uic.loadUi('Program_Files/UI_Files/new_order_window.ui', self)
        self.setWindowIcon(QIcon('Program_files/Icons/circuit.png'))
        self.resize(800, 600)
        self.move(800, 100)

        self.is_sheet_open = False
        self.opened_orders = []  # names of orders that have been opened.
        self.new_orders_list = []  # names of new orders that have been added.
        self.new_orders_count = 0  # count how many orders have been added.

        # Finding widgets
        self.header_frame = self.findChild(QtWidgets.QFrame, 'header_frame')
        self.header = self.findChild(QtWidgets.QLabel, 'header')
        self.sub_header = self.findChild(QtWidgets.QLabel, 'sub_header')
        self.table = self.findChild(QtWidgets.QTableWidget, 'table')

        self.nav_btn_frame = self.findChild(QtWidgets.QFrame, 'nav_btn_frame')
        self.btn_prev = self.findChild(QtWidgets.QPushButton, 'btn_prev')
        self.btn_next = self.findChild(QtWidgets.QPushButton, 'btn_next')

        self.command_btn_frame = self.findChild(
            QtWidgets.QFrame, 'command_btn_frame')
        self.btn_add_to_inventory = self.findChild(
            QtWidgets.QPushButton, 'btn_add_to_inventory'
        )

        # Defining actions
        self.action_open_new_order = self.findChild(
            QtWidgets.QAction, 'actionOpen_New_Order'
        )
        self.action_open_past_orders = self.findChild(
            QtWidgets.QAction, 'actionOpen_Past_Orders'
        )

        # Attaching functions
        self.action_open_new_order.triggered.connect(self.open_order)
        self.action_open_past_orders.triggered.connect(self.open_past_order)
        self.btn_add_to_inventory.clicked.connect(self.add_to_inventory)

        # Calling styling functions
        style_central_widget(self)
        style_table(self)
        style_toolbar(self)

        # styling
        nav_btn_styles = '''
        QPushButton {
            font-size: 14px;
            font-family: Arial;
            background-color: white;
            padding: 10px 15px;
            border: 1.5px grey;
            border-radius: 5px;
            border-style: outset;
        }

        QPushButton:hover {
            border: 1px solid blue;
            background-color: #AFDCEC;
        }

        QPushButton:pressed {
            border-style: inset;
        }
        '''
        for btn in self.nav_btn_frame.findChildren(QtWidgets.QPushButton):
            btn.setStyleSheet(
                '''
                QPushButton {
                    font-size: 14px;
                    font-family: Arial;
                    background-color: white;
                    padding: 10px 15px;
                    border: 1.5px grey;
                    border-radius: 5px;
                    border-style: outset;
                }

                QPushButton:hover {
                    border: 1px solid blue;
                    background-color: #AFDCEC;
                }

                QPushButton:pressed {
                    border-style: inset;
                }
                '''
            )

        for btn in self.command_btn_frame.findChildren(QtWidgets.QPushButton):
            btn.setStyleSheet(
                '''
                QPushButton {
                    font: 10pt Arial;
                    font-weight: bold;
                    background-color: rgb(255, 255, 255);
                }
                '''
            )

        self.header_frame.hide()
        self.nav_btn_frame.hide()
        self.command_btn_frame.hide()

    def closeEvent(self, event) -> None:
        '''
        Function to handle close event
        '''
        self.opened_orders.clear()
        event.accept()

    def open_order(self) -> None:
        '''
        Function to open a order
        '''

        downloads_path = os.path.expanduser("~" + os.sep + "Downloads")
        filenames, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self, 'EIP - Opening New Order', downloads_path, 'CSV Files (*.csv);; Excel Files (*.xlsx)')

        if filenames:
            self.opened_orders.clear()
            for filename in filenames:
                filetype = filename.split('.')[-1]
                self.opened_orders.append(filename)

                # checking if excel file
                if filetype == 'xlsx':
                    '''
                    only needs a check for '.xlsx' files, since the program has a condition to remove the subtotal line from new order sheets.

                    This may change at some time...
                    '''
                    user = QtWidgets.QMessageBox.question(
                        self,
                        'Opening an excel file', 'Make sure to that the subtotal line is removed from the excel file, otherwise the program will crash.\n\nWould you like to continue?',
                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                        QtWidgets.QMessageBox.No
                    )
                    if user == QtWidgets.QMessageBox.No:
                        return

            # loading first order
            filename = self.opened_orders[0]
            self.is_sheet_open = filename
            new_order = get_ordersheet(filename)
            load_Items(self, new_order)
            fill_table(self, Items)

            # updating Qlabels
            text = f'New Order: {filename.split("/")[-1]}'
            self.header.setText(text)
            self.sub_header.setText('')
            self.header_frame.show()

            # updating buttons
            self.btn_add_to_inventory.setEnabled(True)
            self.command_btn_frame.show()

            # if more than one file is opened show nav buttons.
            if len(self.opened_orders) > 1:
                self.nav_btn_frame.show()

    def open_past_order(self) -> None:
        '''
        Function to open a past order
        '''

        if len(os.listdir('Saved_Lists/Past Orders')) > 0:
            self.sub_header.setText('')
            filenames, _ = QtWidgets.QFileDialog.getOpenFileNames(
                self,
                'Electronics Inventory Program - Opening Past Orders',
                'Saved_Lists/Past Orders',
                'All Files (*) ;; CSV Files (*.csv);; Excel Files (*.xlsx)'
            )

            if filenames:
                self.opened_orders.clear()

                for filename in filenames:
                    filetype = filename.split(".")[-1]
                    if filetype in ['csv', 'xlsx']:
                        self.opened_orders.append(filename)
                    else:
                        wrong_filetype_msg(self)

                # loading first order
                filename = self.opened_orders[0]
                self.is_sheet_open = filename
                past_order = get_ordersheet(filename)
                load_Items(self, past_order)
                fill_table(self, Items)

                # updating Qlabels
                text = f'Past Order: {filename.split("/")[-1]}'
                self.header.setText(text)
                self.sub_header.setText('')
                self.header_frame.show()

                # updating buttons
                self.btn_add_to_inventory.setEnabled(False)
                self.command_btn_frame.show()

                # if more than one file is opened show nav buttons.
                if len(self.opened_orders) > 1:
                    self.nav_btn_frame.show()
        else:
            header = 'There are no past orders to open!'
            no_files_msg(self, title='No Past Orders', header=header)

    def add_to_inventory(self) -> None:
        '''
        Function to add order to inventory
        '''
        self.parent().add_to_inventory(self.is_sheet_open)
        self.btn_add_to_inventory.setEnabled(False)