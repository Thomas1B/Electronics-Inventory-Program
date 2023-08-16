from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtCore import QUrl, QDir
from PyQt5.QtGui import QDesktopServices, QIcon
import pandas as pd
import sys
import os
import shutil


from .data_handling import (
    Data,
    Inventory,
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
    fill_table,
    refresh_opensheet
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
        self.resize(1000, 600)
        self.move(800, 100)

        self.is_sheet_open = False
        self.opened_orders = []  # names of orders that have been opened.
        self.new_orders_added = []  # names of new orders that have been added.
        self.Items = Data(dict_keys)

        # Finding widgets
        self.header_frame = self.findChild(QtWidgets.QFrame, 'header_frame')
        self.header = self.findChild(QtWidgets.QLabel, 'header')
        self.sub_header = self.findChild(QtWidgets.QLabel, 'sub_header')
        self.table = self.findChild(QtWidgets.QTableWidget, 'table')

        self.nav_btn_frame = self.findChild(QtWidgets.QFrame, 'nav_btn_frame')
        self.btn_prev = self.findChild(QtWidgets.QPushButton, 'btn_prev')
        self.btn_next = self.findChild(QtWidgets.QPushButton, 'btn_next')
        self.count_label = self.findChild(QtWidgets.QLabel, 'count_label')

        self.sorting_btns_frame = self.findChild(
            QtWidgets.QFrame, 'sorting_frame')
        self.comboBox_section = self.findChild(
            QtWidgets.QComboBox, 'comboBox_section'
        )
        self.btn_refresh_opensheet = self.findChild(
            QtWidgets.QPushButton, 'btn_refresh_opensheet'
        )

        self.command_btn_frame = self.findChild(
            QtWidgets.QFrame, 'command_btn_frame')
        self.btn_add_to_inventory = self.findChild(
            QtWidgets.QPushButton, 'btn_add_to_inventory'
        )
        self.btn_save_inventory = self.findChild(
            QtWidgets.QPushButton, 'btn_save_inventory'
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
        self.btn_prev.clicked.connect(self.prev_order)
        self.btn_next.clicked.connect(self.next_order)

        self.btn_refresh_opensheet.clicked.connect(
            lambda: refresh_opensheet(self, self.Items)
        )
        self.comboBox_section.currentIndexChanged.connect(
            lambda: self.show_section(
                self.comboBox_section.currentText())
        )

        self.btn_add_to_inventory.clicked.connect(self.add_to_inventory)
        self.btn_save_inventory.clicked.connect(self.save_inventory)

        # Calling styling functions
        style_central_widget(self)
        style_table(self)
        style_toolbar(self)
        style_refresh_btn(self)
        style_sorting_comboBox(self)

        # Styling
        self.nav_btn_frame.setStyleSheet(
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

            QLabel {
                font-size: 18px Arial;
            }
            '''
        )
        self.command_btn_frame.setStyleSheet(
            '''
            QPushButton {
                font: 14px Arial;
                font-weight: bold;
                background-color: rgb(255, 255, 255);
                padding: 10px;
                margin-left: 15px;
                border: 1.5px grey;
                border-radius: 5px;
                border-style: outset;
            }

            QPushButton:hover {
                border: 1px solid blue;
                background-color: #AFDCEC;
            }
            '''
        )

        # hiding some frames for initial load.
        self.count_label.hide()
        self.header_frame.hide()
        self.nav_btn_frame.hide()
        self.sorting_btns_frame.hide()
        self.command_btn_frame.hide()
        self.btn_save_inventory.hide()

        # adding category keys to comboBox
        for key in sorted(dict_keys):
            self.comboBox_section.addItem(key)

    def closeEvent(self, event) -> None:
        '''
        Function to hanlde closing event
        '''

        # checking if inventory has been saved before closing.
        if self.new_orders_added:
            user = QtWidgets.QMessageBox()
            pixmapi = getattr(QtWidgets.QStyle, "SP_MessageBoxWarning")
            icon = self.style().standardIcon(pixmapi)
            user.setWindowIcon(icon)
            user.setIcon(QtWidgets.QMessageBox.Warning)
            user.setStandardButtons(
                QtWidgets.QMessageBox.Yes |
                QtWidgets.QMessageBox.No |
                QtWidgets.QMessageBox.Cancel
            )
            user.setDefaultButton(QtWidgets.QMessageBox.Yes)
            header = 'New orders have been added to the inventory!'
            text = 'Would you like to save?'
            user.setWindowTitle("New Orders Added")
            user.setText(header)
            user.setInformativeText(text)
            user = user.exec_()

            match user:
                case QtWidgets.QMessageBox.Yes:
                    self.save_list()
                    event.accept()
                case QtWidgets.QMessageBox.No:
                    # user declines to save.
                    event.accept()
                case _:
                    event.ignore()

        else:
            event.accept()

    def custom_fill_table(self, filename: str) -> None:
        '''
        Function to fill the table.

            Parameters:
                filename: filename to 
        '''

        self.is_sheet_open = filename
        new_order = get_ordersheet(filename)
        load_Items(self, new_order)
        fill_table(self, self.Items)

        # updating Qlabels
        name = filename.split("/")[-1]
        text = f'Order: {name}'
        self.header.setText(text)
        self.header_frame.show()

        # checking if order has already been added
        past_order_path = os.path.join('Saved_Lists/Past Orders', name)
        if os.path.exists(past_order_path):
            self.btn_add_to_inventory.setText('Order Already Added')
            self.btn_add_to_inventory.setEnabled(False)
        else:
            self.btn_add_to_inventory.setText('Add to Inventory')
            self.btn_add_to_inventory.setEnabled(True)

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
            self.custom_fill_table(filename=filename)

            # updating buttons
            self.command_btn_frame.show()
            self.sorting_btns_frame.show()
            self.sub_header.setText('')

            # if more than one file is opened show nav buttons.
            if len(self.opened_orders) > 1:
                self.nav_btn_frame.show()
                self.count = 1
                self.update_count_label(count=self.count)

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
                self.custom_fill_table(filename=filename)

                # updating buttons
                self.btn_add_to_inventory.setEnabled(False)
                self.command_btn_frame.show()
                self.sorting_btns_frame.show()
                self.sub_header.setText('')

                # if more than one file is opened show nav buttons.
                if len(self.opened_orders) > 1:
                    self.nav_btn_frame.show()
                    self.update_count_label(index=0)

        else:
            header = 'There are no past orders to open!'
            no_files_msg(self, title='No Past Orders', header=header)

    def add_to_inventory(self) -> None:
        '''
        Function to add order to inventory
        '''
        self.parent().add_to_inventory(self.is_sheet_open)
        self.parent().btn_save_list.show()
        self.new_orders_added.append(self.is_sheet_open)
        self.btn_add_to_inventory.setText('Order Already Added')
        self.btn_add_to_inventory.setEnabled(False)
        self.btn_save_inventory.show()

    def prev_order(self) -> None:
        '''
        Function to open the previous order, used when multiple files are opened.
        '''
        # Getting index of file in list.
        index = self.opened_orders.index(self.is_sheet_open)
        index -= 1  # incrementing

        self.custom_fill_table(self.opened_orders[index])
        self.count = self.count - 1
        if self.count == 0:
            self.count = len(self.opened_orders)
        self.update_count_label(count=self.count)  # updating count label

    def next_order(self) -> None:
        '''
        Function to open the next order, used when multiple files are opened.
        '''
        # Getting index of file in list.
        index = self.opened_orders.index(self.is_sheet_open)
        index += 1  # incrementing

        # try block for hanlding index error
        try:
            self.custom_fill_table(self.opened_orders[index])
        except IndexError:  # index goes out of bounds.
            index = 0
            self.custom_fill_table(self.opened_orders[index])

        if self.count >= len(self.opened_orders):
            self.count = 1
        else:
            self.count = self.count + 1
        self.update_count_label(count=self.count)  # updating count label

    def show_section(self, section: str) -> None:
        '''
        Function to show the selected section.
        '''
        if section.lower() == 'all':
            refresh_opensheet(self, self.Items)
        else:
            items = self.Items.get_data(section=section)
            if items.empty:
                self.table.setRowCount(0)
            fill_table(self, items)
            self.sub_header.setText(section)

    def update_count_label(self, count: int) -> None:
        '''
        Function to update the label when cycling through multiple opened orders.

            Parameters:
                count: count of order in opened_orders list, (must adjust +/- 1 for cycling).
        '''
        text = f'Order {count}/{len(self.opened_orders)}'
        self.count_label.setText(text)
        self.count_label.show()

    def save_inventory(self) -> None:
        '''
        Function to save the inventory.
        '''
        self.parent().save_list()
        self.btn_save_inventory.hide()
