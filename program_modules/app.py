'''
Script to run PyQt app functions and classes.
'''

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtWidgets
from PyQt5 import uic
import sys
import os
import pandas as pd

from .data_handling import (Category,
                          load_Inventory,
                          get_new_ordersheet,
                          add_order_to_Inventory,
                          inventory_to_dataframe,
                          sort_order)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.sheet_open = False  # variable to keep keep if a table is opened.

        # Loading .ui file
        uic.loadUi('gui_app.ui', self)

        # Setting default table column widths
        self.table.setColumnWidth(0, 175)
        self.table.setColumnWidth(1, 175)
        self.table.setColumnWidth(2, 175)
        self.table.setColumnWidth(3, 175)
        self.table.setColumnWidth(4, 75)
        self.table.setColumnWidth(5, 75)

        ''' defining widgets'''
        # Menu Bar
        self.menu_open_order = self.findChild(
            QtWidgets.QAction, 'actionOpen_Order')

        self.header = self.findChild(QtWidgets.QLabel, 'header')
        self.sub_header = self.findChild(QtWidgets.QLabel, 'sub_header')
        self.table = self.findChild(QtWidgets.QTableWidget, 'table')

        # Buttons
        self.btn_open_inventory = self.findChild(
            QtWidgets.QPushButton, 'btn_open_inventory')
        self.btn_open_new_order = self.findChild(
            QtWidgets.QPushButton, 'btn_open_new_order')
        self.btn_open_project_lists = self.findChild(
            QtWidgets.QPushButton, 'btn_open_project_lists')
        self.btn_save_list = self.findChild(
            QtWidgets.QPushButton, 'btn_save_list')
        self.btn_add_to_inventory = self.findChild(
            QtWidgets.QPushButton, 'btn_add_to_inventory')

        self.btn_resistors = self.findChild(
            QtWidgets.QPushButton, 'btn_resistors')
        self.btn_capacitors = self.findChild(
            QtWidgets.QPushButton, 'btn_capacitors')
        self.btn_inductors = self.findChild(
            QtWidgets.QPushButton, 'btn_inductors')
        self.btn_transistors = self.findChild(
            QtWidgets.QPushButton, 'btn_transistors')
        self.btn_diodes = self.findChild(
            QtWidgets.QPushButton, 'btn_diodes')
        self.btn_ics = self.findChild(
            QtWidgets.QPushButton, 'btn_ics')
        self.btn_leds = self.findChild(
            QtWidgets.QPushButton, 'btn_leds')
        self.btn_buttons = self.findChild(
            QtWidgets.QPushButton, 'btn_buttons')
        self.btn_connectors = self.findChild(
            QtWidgets.QPushButton, 'btn_connectors')
        self.btn_displays = self.findChild(
            QtWidgets.QPushButton, 'btn_displays')
        self.btn_modules = self.findChild(
            QtWidgets.QPushButton, 'btn_modules')
        self.btn_other = self.findChild(
            QtWidgets.QPushButton, 'btn_other')

        # attaching functions
        self.btn_open_inventory.clicked.connect(self.open_inventory)
        self.btn_open_new_order.clicked.connect(self.open_new_order)
        self.btn_open_project_lists.clicked.connect(self.open_project_lists)
        self.btn_save_list.clicked.connect(self.save_list)
        self.btn_add_to_inventory.clicked.connect(self.add_to_inventory)

        self.btn_resistors.clicked.connect(
            lambda: self.show_sorted_section('Resistors'))
        self.btn_capacitors.clicked.connect(
            lambda: self.show_sorted_section('Capacitors'))
        self.btn_inductors.clicked.connect(
            lambda: self.show_sorted_section('Inductors'))
        self.btn_transistors.clicked.connect(
            lambda: self.show_sorted_section('Transistors'))
        self.btn_diodes.clicked.connect(
            lambda: self.show_sorted_section('Diodes'))
        self.btn_ics.clicked.connect(lambda: self.show_sorted_section('ICs'))
        self.btn_leds.clicked.connect(lambda: self.show_sorted_section('LEDs'))
        self.btn_buttons.clicked.connect(
            lambda: self.show_sorted_section('Buttons'))
        self.btn_connectors.clicked.connect(
            lambda: self.show_sorted_section('Connectors'))
        self.btn_displays.clicked.connect(
            lambda: self.show_sorted_section('Displays'))
        self.btn_modules.clicked.connect(
            lambda: self.show_sorted_section('Modules'))
        self.btn_other.clicked.connect(
            lambda: self.show_sorted_section('Other'))

        # testing
        self.btn_test = self.findChild(QtWidgets.QPushButton, 'btn_test')
        self.btn_test.clicked.connect(self.get_table_data)

        self.hide_btns([
            self.btn_save_list,
            self.btn_add_to_inventory,
            self.btn_resistors,
            self.btn_capacitors,
            self.btn_inductors,
            self.btn_transistors,
            self.btn_diodes,
            self.btn_ics,
            self.btn_leds,
            self.btn_buttons,
            self.btn_connectors,
            self.btn_displays,
            self.btn_modules,
            self.btn_other
        ])

        self.show()  # needs to here in order to work

    def show_btns(self, buttons):
        '''
        takes list of buttons to hide.
        '''
        for btn in buttons:
            btn.show()

    def hide_btns(self, buttons):
        '''
        takes list of buttons to show.
        '''
        for btn in buttons:
            btn.hide()

    def popup_nofiles(self, header="", text=""):
        '''
        Function to display a pop up warning user there are no files to open

        Parameters:
            header - str: "header" text to pop up.
            text - str: informative text for pop up.
        '''
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle('Missing Files')
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText(header)
        msg.setInformativeText(f'{text}')
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        _ = msg.exec_()

    def fill_table(self, dataframe):
        '''
        Function to fill in table
        '''
        items = dataframe
        if type(dataframe) == dict:
            items = pd.concat([dataframe[cat].get_items()
                               for cat in dataframe]).reset_index(drop=True)
        elif type(dataframe) == list:
            items = pd.concat(dataframe)

        count = items.shape[0]
        self.table.setRowCount(count)

        for row in range(count):
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(
                items['Part Number'][row]))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(
                items['Manufacturer Part Number'][row]))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(
                items['Description'][row]))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(
                items['Customer Reference'].fillna('')[row]))
            self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(
                items['Unit Price'].astype(float).round(2).astype(str)[row]))
            self.table.setItem(row, 5, QtWidgets.QTableWidgetItem(
                items['Quantity'].astype(int).astype(str)[row]))

    def open_inventory(self):
        '''
        Function to open the inventory
        '''
        self.sub_header.setText('')
        if os.path.exists("Inventory.xlsx"):
            self.sheet_open = "Inventory.xlsx"
            self.header.setText('Looking at Inventory')
            self.fill_table(inventory_to_dataframe())
            self.show_btns([
                self.btn_resistors,
                self.btn_capacitors,
                self.btn_inductors,
                self.btn_transistors,
                self.btn_diodes,
                self.btn_ics,
                self.btn_leds,
                self.btn_buttons,
                self.btn_connectors,
                self.btn_displays,
                self.btn_modules,
                self.btn_other
            ])
        else:
            text = 'There is no inventory file!\n\n'
            text += 'Check for a file called "Inventory.xlsx"\n'
            self.hide_btns([
                self.btn_resistors,
                self.btn_capacitors,
                self.btn_inductors,
                self.btn_transistors,
                self.btn_diodes,
                self.btn_ics,
                self.btn_leds,
                self.btn_buttons,
                self.btn_connectors,
                self.btn_displays,
                self.btn_modules,
                self.btn_other
            ])
            self.popup_nofiles(text=text)

    def open_new_order(self):
        '''
        Function to open an order
        '''
        self.sub_header.setText('')
        if len(os.listdir("New Orders")) > 0:
            filename, _ = QtWidgets.QFileDialog.getOpenFileName(
                self, 'Opening New Order', 'New Orders', 'All Files(*);; CSV Files (*.csv);; Excel Files (*.xlsx)')
            filetype = filename.split('.')[-1]
            self.sheet_open = filename
            if filename:
                order_name = filename.split('/')[-1]

                if filetype == 'xlsx':
                    user = QtWidgets.QMessageBox.question(
                        self, 'Opening an excel file', 'Make sure to that the subtotal line is removed from the excel file, otherwise the program will crash.\n\nWould you like to continue?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
                    if user == QtWidgets.QMessageBox.No:
                        return

                new_order = get_new_ordersheet(filename)
                if new_order:
                    text = f'Looking at a new order: {order_name}'
                    self.header.setText(text)
                    self.show_btns([
                        self.btn_save_list,
                        self.btn_add_to_inventory,
                        self.btn_resistors,
                        self.btn_capacitors,
                        self.btn_inductors,
                        self.btn_transistors,
                        self.btn_diodes,
                        self.btn_ics,
                        self.btn_leds,
                        self.btn_buttons,
                        self.btn_connectors,
                        self.btn_displays,
                        self.btn_modules,
                        self.btn_other
                    ])
                    self.fill_table(
                        [section for section in new_order if not section.empty][0])
                else:
                    header = 'Cannot open files from that location!'
                    text = 'New order files must be in the "New_Orders" folder.\n'
                    text += 'Move the file and try again...'
                    self.popup_nofiles(header=header, text=text)

        else:
            self.popup_nofiles(text='There are no orders to open...')

    def open_project_lists(self):
        '''
        Function to open project lists.
        '''
        if len(os.listdir("Project_Lists")) > 0:
            filename, _ = QtWidgets.QFileDialog.getOpenFileName(
                self, 'Opening Project List', 'Project_Lists', 'All Files(*);; CSV Files (*.csv);; Excel Files (*.xlsx)')
            filetype = filename.split('.')[-1]
            if filename:
                order_name = filename.split('/')[-1]
                if filetype == 'xlsx':
                    self.popup_nofiles(
                        text="No feature to open excel files yet...")
                else:
                    text = f'Project: {order_name.split(".")}'
                    self.header.setText(text)
                    new_order = get_new_ordersheet(
                        f'Project_Lists/{order_name}')
                    if new_order:
                        self.fill_table(new_order)
                        self.show_btns([
                            self.btn_save_list,
                            self.btn_add_to_inventory,
                            self.btn_resistors,
                            self.btn_capacitors,
                            self.btn_inductors,
                            self.btn_transistors,
                            self.btn_diodes,
                            self.btn_ics,
                            self.btn_leds,
                            self.btn_buttons,
                            self.btn_connectors,
                            self.btn_displays,
                            self.btn_modules,
                            self.btn_other
                        ])
                    else:
                        header = 'Cannot open files from that location!'
                        text = 'Project files must be in the "Project_Lists" folder.\n'
                        text += 'Move the file and try again...'
                        self.hide_btns([
                            self.btn_save_list,
                            self.btn_add_to_inventory,
                            self.btn_resistors,
                            self.btn_capacitors,
                            self.btn_inductors,
                            self.btn_transistors,
                            self.btn_diodes,
                            self.btn_ics,
                            self.btn_leds,
                            self.btn_buttons,
                            self.btn_connectors,
                            self.btn_displays,
                            self.btn_modules,
                            self.btn_other
                        ])
                        self.popup_nofiles(header=header, text=text)
        else:
            self.popup_nofiles(text='There are no projects to open...')

    def save_list(self):
        self.popup_nofiles(
            header="Testing Save function", text='Need to finish function.')

    def add_to_inventory(self):
        filename = self.header.text().split(" ")[-1]
        if filename:
            add_order_to_Inventory(f'New_Orders/{filename}.csv')

            user = QtWidgets.QMessageBox.question(self, 'Saving New Inventory', 'Would you like to save the new inventory?',
                                                  QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
            if user == QtWidgets.QMessageBox.Yes:
                self.save_list()

    def show_sorted_section(self, section):

        data = self.get_table_data()
        if 'inventory' in self.header.text().lower().split(' '):
            data = inventory_to_dataframe()
        elif 'new orders' in self.sheet_open.lower():
            data = get_new_ordersheet(self.sheet_open)

        if type(data) == pd.DataFrame:
            data = sort_order(data)
        sorted = {}
        keys = [
            'Resistors',
            'Capacitors',
            'Inductors',
            'Transistors',
            'Diodes',
            'ICs',
            'Connectors',
            'Displays',
            'Buttons',
            'LEDs',
            'Modules',
            'Other'
        ]

        for i, key in enumerate(keys):
            sorted[key] = data[i]
        self.fill_table(sorted[section].reset_index(drop=True))
        self.sub_header.setText(section)

    def get_table_data(self):
        '''
        return current table data into a dataframe.
        '''
        rows = self.table.rowCount()
        cols = self.table.columnCount()
        data = []

        for r in range(rows):
            row_data = []
            for c in range(cols):
                item = self.table.item(r, c)
                if item:
                    row_data.append(item.text())
            data.append(row_data)

        data = pd.DataFrame(data, columns=['Part Number', 'Manufacturer Part Number',
                            'Description', 'Customer Reference', 'Unit Price', 'Quantity'])
        return data


if __name__ == "__main__":
    # runnning program
    load_Inventory()
    app = QApplication(sys.argv)
    window1 = MainWindow()
    app.exec_()
