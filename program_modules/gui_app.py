'''
Script to run PyQt app functions and classes.
'''

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtWidgets
from PyQt5 import uic
import pandas as pd
import sys
import os
import shutil


from .data_handling import (Inventory,
                            load_Inventory,
                            get_ordersheet,
                            add_order_to_Inventory,
                            inventory_to_dataframe,
                            sort_order)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # variable to keep track if a table is opened.
        # Used for getting openning sorted parts
        self.is_sheet_open = False

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
        self.btn_open_past_order = self.findChild(
            QtWidgets.QPushButton, 'btn_open_past_order')

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
        self.btn_open_past_order.clicked.connect(self.open_past_order)

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

        self.hide_btns([
            self.btn_save_list,
            self.btn_add_to_inventory,
        ])
        self.hide_sorting_btns()

        self.show()  # needs to here in order to work

    def get_is_sheet_open(self):
        # Variable to keep keep if a table is opened.

        # Returns a filepath to the ordersheet that was last opened.

        return self.is_sheet_open

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

    def hide_sorting_btns(self):
        '''
        Function to hide sorting buttons
        '''
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

    def show_sorting_btns(self):
        '''
        Function to show sorting buttons
        '''
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

    def wrong_filetyle_msg(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle('Wrong File Type')
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText('Cannot open that file type!')
        text = "You can only open '.csv' and '.xlsx' files"
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
        if os.path.exists("Saved_Lists/Inventory.xlsx"):
            self.is_sheet_open = "Saved_Lists/Inventory.xlsx"
            self.header.setText('Looking at Inventory')
            self.fill_table(inventory_to_dataframe())
            self.show_sorting_btns()
        else:
            text = 'There is no inventory file!\n\n'
            text += 'Check for a file called "Inventory.xlsx"\n'
            self.hide_sorting_btns()
            self.popup_nofiles(text=text)

    def open_new_order(self):
        '''
        Function to open an order
        '''
        self.sub_header.setText('')
        # if len(os.listdir("Saved_Lists/New Orders")) > 0:
        downloads_path = os.path.expanduser("~" + os.sep + "Downloads")
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Opening New Order', downloads_path, 'CSV Files (*.csv);; Excel Files (*.xlsx);; All Files(*)')
        filetype = filename.split('.')[-1]
        if filetype:
            if filetype in ['csv', 'xlsx']:
                self.is_sheet_open = filename
                order_name = filename.split('/')[-1]

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
                        pass

                new_order = get_ordersheet(filename)
                if new_order:
                    text = f'Looking at new order: {order_name}'
                    self.header.setText(text)
                    self.show_btns(
                        [self.btn_save_list, self.btn_add_to_inventory])
                    self.show_sorting_btns()
                    self.fill_table(
                        [section for section in new_order if not section.empty][0])
            else:
                self.wrong_filetyle_msg()
        # else:
        #     header = 'No order files to open!'
        #     text = 'Make sure that new orders are in the "New Orders" folder.'
        #     self.popup_nofiles(header=header, text=text)

    def open_past_order(self):
        '''
        Function to open a past order
        '''
        self.sub_header.setText('')
        if len(os.listdir('Saved_Lists/Past Orders')) > 0:
            filename, _ = QtWidgets.QFileDialog.getOpenFileName(
                self, 'Opening Past Orders', 'Saved_Lists/Past Orders', 'All Files(*);; CSV Files (*.csv);; Excel Files (*.xlsx)')
            filetype = filename.split(".")[-1]
            if filetype in ['csv', 'xlsx']:
                self.is_sheet_open = filename
                self.header.setText(f'Past Order: {filetype}')
                self.fill_table(get_ordersheet(filename))
                self.show_sorting_btns()
            elif filetype == '':
                self.wrong_filetyle_msg()
            else:
                pass

        else:
            self.hide_sorting_btns()
            header = 'There are no past orders!\n\n'
            self.popup_nofiles(header=header)

    def open_project_lists(self):
        '''
        Function to open project lists.
        '''
        if len(os.listdir("Saved_Lists/Projects")) > 0:
            filename, _ = QtWidgets.QFileDialog.getOpenFileName(
                self, 'Opening Project List', 'Saved_Lists/Projects', 'All Files(*);; CSV Files (*.csv);; Excel Files (*.xlsx)')
            filetype = filename.split('.')[-1]
            if filename:
                order_name = filename.split('/')[-1]
                if filetype == 'xlsx':
                    self.popup_nofiles(
                        header="No feature to open excel files yet...")
                else:
                    text = f'Project: {order_name.split(".")}'
                    self.header.setText(text)
                    new_order = get_ordersheet(
                        f'Project_Lists/{order_name}')
                    if new_order:
                        self.fill_table(new_order)
                        self.show_sorting_btns()
                    else:
                        header = 'Cannot open files from that location!'
                        text = 'Project files must be in the "Project_Lists" folder.\n'
                        text += 'Move the file and try again...'
                        self.hide_sorting_btns()
                        self.popup_nofiles(header=header, text=text)
        else:
            self.popup_nofiles(header='There are no projects to open...')

    def save_list(self, called_from=None):
        '''
        Function to save a list.

        Parameters:
            called_from = str: dummy to see where the function was called from,
                                used for some of the following if statements.
        '''

        if called_from == 'add_to_inventory':
            new_inventory = self.get_table_data()
            new_inventory = sort_order(new_inventory)
            with pd.ExcelWriter(f'Saved_Lists/Inventory.xlsx') as writer:
                for sheet, cat in zip(new_inventory, Inventory):
                    sheet.to_excel(writer, sheet_name=f'{cat}')

        elif 'new order' in self.header.text():
            downloads_path = os.path.expanduser("~" + os.sep + "Downloads")
            filename = self.is_sheet_open.split('/')[-1]

            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle('Saving New Order')
            msg.setIcon(QtWidgets.QMessageBox.Question)
            text = 'Would you like save the order to the "Past Orders" folder or elsewhere?'
            msg.setText(text)
            msg.setStandardButtons(
                QtWidgets.QMessageBox.Yes |
                QtWidgets.QMessageBox.Save |
                QtWidgets.QMessageBox.Cancel)
            msg.setDefaultButton(QtWidgets.QMessageBox.Yes)
            user = msg.exec_()

            downloads_path = os.path.expanduser(f"~/Downloads/{filename}")
            if user == QtWidgets.QMessageBox.Yes:
                destination = 'Saved_Lists/Past Orders'
                shutil.copy2(downloads_path, destination)
                if os.path.exists(destination+f'/{filename}'):
                    msg = QtWidgets.QMessageBox()
                    msg.setWindowTitle('Successfully Copied!')
                    msg.setIcon(QtWidgets.QMessageBox.Information)
                    msg.setText(
                        'The new order was successfully copied to "Past Orders".')
                    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    _ = msg.exec_()
                else:
                    msg = QtWidgets.QMessageBox()
                    msg.setWindowTitle('Unsuccessfully Copied!')
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setText(
                        'The new order was unsuccessfully copied to "Past Orders".')
                    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    _ = msg.exec_()
            elif user == QtWidgets.QMessageBox.Save:
                filename, _ = QtWidgets.QFileDialog.getSaveFileName(
                    self, "Saving New Order", "", "(*.csv;; *.xlsx)")
                shutil.copy2(downloads_path, filename)
            else:
                pass

        elif 'project' in self.header.text():
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle('Saving Project')
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Saving projects feature is woring yet")
            _ = msg.exec()

    def add_to_inventory(self):
        add_order_to_Inventory(self.is_sheet_open) # using function from data_handling.py

        # popup to ask user if wants to save the "new" inventory.
        user = QtWidgets.QMessageBox.question(
            self,
            'Saving New Inventory',
            'Would you like to save the new inventory?',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.Yes)
        if user == QtWidgets.QMessageBox.Yes:
            self.save_list(called_from='add_to_inventory')

    def show_sorted_section(self, section):
        '''
        Function to show the sorted sections

        Parameter:
            section - str: name of category to display.
        '''

        data = self.get_table_data()
        if 'inventory' in self.header.text().lower():
            data = inventory_to_dataframe()
        elif 'new order' in self.header.text().lower():
            data = get_ordersheet(self.is_sheet_open)

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
        returns current table data into a dataframe.
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
