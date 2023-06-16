'''
Script to run PyQt app functions and classes.
'''

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices, QIcon
import pandas as pd
import sys
import os
import shutil
import re

from .info_window import Info_Window
from .project_window import Project_Window

from .data_handling import (Inventory,
                            load_Inventory,
                            get_ordersheet,
                            add_order_to_Inventory,
                            dict_to_dataframe,
                            sort_order,
                            get_inventory)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.move(100, 300)

        # variable to keep track if a table is opened.
        # Used for getting openning sorted parts
        self.is_sheet_open = False

        # Loading .ui file
        uic.loadUi('Program_Files/gui_app.ui', self)

        # Setting default table column widths
        self.table.setColumnWidth(0, 175)
        self.table.setColumnWidth(1, 175)
        self.table.setColumnWidth(2, 175)
        self.table.setColumnWidth(3, 175)
        self.table.setColumnWidth(4, 75)
        self.table.setColumnWidth(5, 75)

        ''' defining widgets'''
        # Menu Bar
        self.action_open_program_info = self.findChild(
            QtWidgets.QAction, 'actionProgram_Info')

        self.action_open_Digikey = self.findChild(
            QtWidgets.QAction, 'actionDigiKey')
        self.action_open_adafruit = self.findChild(
            QtWidgets.QAction, 'actionAdafruit')
        self.action_open_BCrobotics = self.findChild(
            QtWidgets.QAction, 'actionBC_Robotics')

        # Info Labels
        self.header = self.findChild(QtWidgets.QLabel, 'header')
        self.sub_header = self.findChild(QtWidgets.QLabel, 'sub_header')
        self.table = self.findChild(QtWidgets.QTableWidget, 'table')

        self.table.cellClicked.connect(self.get_clicked_row)

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
        self.btn_export = self.findChild(
            QtWidgets.QPushButton, 'btn_export')
        self.btn_create_project = self.findChild(
            QtWidgets.QPushButton, 'btn_create_project')

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

        self.btn_refresh_opensheet = self.findChild(
            QtWidgets.QPushButton, 'btn_refresh_opensheet')

        '''
            Attaching Functions to buttons and other clicked things.
        '''

        # Menu
        self.action_open_program_info.triggered.connect(self.show_program_info)

        self.action_open_Digikey.triggered.connect(
            lambda: self.open_website('Digikey')
        )
        self.action_open_adafruit.triggered.connect(
            lambda: self.open_website('Adafruit')
        )
        self.action_open_BCrobotics.triggered.connect(
            lambda: self.open_website('BC Robotics')
        )

        # buttons
        self.btn_open_inventory.clicked.connect(self.open_inventory)
        self.btn_open_new_order.clicked.connect(self.open_new_order)
        self.btn_open_project_lists.clicked.connect(self.open_project_lists)
        self.btn_add_to_inventory.clicked.connect(self.add_to_inventory)
        self.btn_open_past_order.clicked.connect(self.open_past_order)
        self.btn_export.clicked.connect(
            lambda: self.export_file(autoname=True))
        self.btn_create_project.clicked.connect(self.create_project)

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

        self.btn_refresh_opensheet.clicked.connect(
            lambda: self.refresh_opensheet(self.is_sheet_open))

        self.hide_btns([
            self.btn_save_list,
            self.btn_add_to_inventory
        ])
        self.hide_sorting_btns()

        self.project_window = Project_Window(self)

        self.show()  # needs to here in order to work

    def show_program_info(self):
        '''
        Function to show user the program info.

        Opens a second window
        '''
        self.info_window = Info_Window()

    def open_website(self, website=''):
        '''
        Function to open a website link on the user's default bowser.

        Parameters:
            website - str: website's name (used for conditions)
        '''
        match website.lower():
            case 'digikey':
                website = 'https://www.digikey.ca/'
            case 'adafruit':
                website = 'https://www.adafruit.com/'
            case 'bc robotics':
                website = 'https://bc-robotics.com/'

        QDesktopServices.openUrl(QUrl(website))

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
            self.btn_refresh_opensheet,
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
            self.btn_refresh_opensheet,
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

    def no_files_msg(self, title='No Files', header="", text=""):
        '''
        Function to display a pop up warning user there are no files to open

        Parameters:
            header - str: "header" text to pop up.
            text - str: informative text for pop up.
        '''
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle(title)
        pixmapi = getattr(QtWidgets.QStyle, "SP_MessageBoxWarning")
        icon = self.style().standardIcon(pixmapi)
        msg.setWindowIcon(icon)

        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setText(header)
        msg.setInformativeText(text)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        _ = msg.exec_()

    def wrong_filetype_msg(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle('Wrong File Type')
        pixmapi = getattr(QtWidgets.QStyle, "SP_MessageBoxCritical")
        icon = self.style().standardIcon(pixmapi)
        msg.setWindowIcon(icon)
        msg.setIcon(QtWidgets.QMessageBox.Critical)

        msg.setText('Cannot user that file type!')
        text = "You can only use 'CSV' (Comma-Seperated-Values) and 'XLSX' (Excel) files."
        msg.setInformativeText(text)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        _ = msg.exec_()

    def export_file(self, autoname=True):
        '''
        Function to export a file.

        Parameters:
            autoname - bool: true - automatically named the final.
                if true, exports to 'Downloads\exported_electrontics_lists'
        '''
        if autoname:
            file_toexport, _ = QtWidgets.QFileDialog.getOpenFileName(
                self,
                "Electronics Inventory Program - Exporting File",
                "Saved_lists",
                "All Files (*);; CSV Files (*.csv) ;; XLSX Files (*.xlsx)"
            )

            if file_toexport:

                export_filename, export_filetype = file_toexport.split(
                    '/')[-1].split('.')

                destination_folder = os.path.expanduser(
                    "~" + os.sep + "Downloads\exported_electrontics_lists"
                )
                if not os.path.exists(destination_folder):
                    os.mkdir(destination_folder)

                # while loop to check if file has already be exported,
                # if it does then add a number to the filename name.
                # DO NOT CHANGE THE ORDER OF THESE VARIABLES
                # new_name = file_toexport
                new_name = f'{destination_folder}\{export_filename}.{export_filetype}'
                base, ext = os.path.splitext(file_toexport)
                counter = 1
                while os.path.exists(new_name):
                    new_name = f'{base}({counter}){ext}'
                    counter += 1
                shutil.copy2(file_toexport, new_name)

            else:
                pass

    def open_inventory(self):
        '''
        Function to open the inventory
        '''
        self.sub_header.setText('')
        self.hide_btns([self.btn_add_to_inventory, self.btn_save_list])
        if os.path.exists("Saved_Lists/Inventory.xlsx"):
            self.is_sheet_open = "Saved_Lists/Inventory.xlsx"
            self.header.setText('Looking at Inventory')
            self.fill_table(Inventory)
            self.show_sorting_btns()
        else:
            header = 'There is no inventory file.'
            text = 'Either import one or create one!'
            title = 'No Inventory'
            self.no_files_msg(title=title, header=header, text=text)
            self.hide_sorting_btns()

    def open_new_order(self):
        '''
        Function to open an order
        '''
        self.sub_header.setText('')
        # if len(os.listdir("Saved_Lists/New Orders")) > 0:
        downloads_path = os.path.expanduser("~" + os.sep + "Downloads")
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Opening New Order', downloads_path, 'All Files (*) ;; CSV Files (*.csv);; Excel Files (*.xlsx)')
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
                        return

                new_order = get_ordersheet(filename)
                if new_order:
                    text = f'Looking at new order: {order_name}'
                    self.header.setText(text)
                    self.btn_save_list.setText('Save Order')
                    self.btn_save_list.clicked.connect(
                        lambda: self.save_list('save_order')
                    )
                    self.show_btns(
                        [self.btn_save_list, self.btn_add_to_inventory])
                    self.show_sorting_btns()
                    self.fill_table(
                        [section for section in new_order if not section.empty][0])
            else:
                self.wrong_filetype_msg()

    def open_past_order(self):
        '''
        Function to open a past order
        '''
        self.sub_header.setText('')
        if len(os.listdir('Saved_Lists/Past Orders')) > 0:
            filename, _ = QtWidgets.QFileDialog.getOpenFileName(
                self,
                'Electronics Inventory Program - Opening Past Orders',
                'Saved_Lists/Past Orders',
                'All Files (*) ;; CSV Files (*.csv);; Excel Files (*.xlsx)'
            )
            filetype = filename.split(".")[-1]
            if filetype in ['csv', 'xlsx']:
                self.is_sheet_open = filename
                self.header.setText(f'Past Order: {filetype}')
                self.fill_table(get_ordersheet(filename))
                self.show_sorting_btns()
            elif filetype:
                self.wrong_filetype_msg()
            else:
                pass

        else:
            header = 'There are no past orders to open!'
            self.no_files_msg(title='No Past Orders', header=header)

    def open_project_lists(self):
        '''
        Function to open project lists.
        '''
        self.project_window.open_project()

    def show_sorted_section(self, section):
        '''
        Function to show the sorted sections

        Parameter:
            section - str: name of category to display.
        '''

        if 'looking at inventory' in self.header.text().lower():
            self.fill_table(Inventory[section].get_items())
        else:
            data = get_ordersheet(self.is_sheet_open)
            sorted = {}
            keys = Inventory.keys()
            for i, key in enumerate(keys):
                sorted[key] = data[i]
            self.fill_table(sorted[section].reset_index(drop=True))
        self.sub_header.setText(section)

    def refresh_opensheet(self, filename=None):
        '''
        Function to refresh the last sheet that was opened.
            used for when a user is looking a specific category.

        '''
        filename = self.is_sheet_open
        if 'looking at inventory' in self.header.text().lower():
            self.open_inventory()
        else:
            data = get_ordersheet(filename)
            self.fill_table(data)
            self.sub_header.setText('')

    def save_list(self, called_from=None):
        '''
        Function to save a list.

        Parameters:
            called_from = str: dummy to see where the function was called from,
                                used for some of the following if statements.
        '''

        if called_from.lower() == 'save_order':  # if new order is being saved.

            # popup to ask user if they where they want to save the order.
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle('Saving New Order')
            pixmapi = getattr(QtWidgets.QStyle, "SP_DialogSaveButton")
            icon = self.style().standardIcon(pixmapi)
            msg.setWindowIcon(icon)
            msg.setIcon(QtWidgets.QMessageBox.Question)

            text = 'Would you like save the order to the "Past Orders" folder or elsewhere?'
            info_text = "Note: Orders should be added the inventory first."
            msg.setText(text)
            msg.setInformativeText(info_text)
            msg.setStandardButtons(
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Cancel)
            msg.setDefaultButton(QtWidgets.QMessageBox.Yes)
            user = msg.exec_()

            filename = self.is_sheet_open.split('/')[-1]

            if user == QtWidgets.QMessageBox.Yes:  # user want to save to "Past Order" Folder
                destination_folder = 'Saved_Lists/Past Orders'
                shutil.copy2(self.is_sheet_open, destination_folder)
                if os.path.exists(destination_folder+f'/{filename}'):
                    # displays successfully save popup
                    msg = QtWidgets.QMessageBox()
                    msg.setWindowTitle('Filed Saved Successfully')
                    msg.setIcon(QtWidgets.QMessageBox.Information)
                    msg.setText(
                        'The new order was successfully saved.')
                    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    _ = msg.exec_()
                else:
                    # displays unsuccessfully save popup
                    msg = QtWidgets.QMessageBox()
                    msg.setWindowTitle('Unsuccessfully saved!')
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setText(
                        'The new order was unsuccessfully copied to "Past Orders".')
                    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    _ = msg.exec_()
            elif user == QtWidgets.QMessageBox.Save:  # user want to save to elsewhere.
                destination_folder = QtWidgets.QFileDialog.getExistingDirectory(
                    self, 'Select Destination Folder')
                if destination_folder:  # user picks a location.
                    location = f'{destination_folder}/{filename}'
                    try:
                        shutil.copy2(self.is_sheet_open, location)
                    except Exception as err:
                        print(err)
                    if os.path.exists(destination_folder+f'/{filename}'):
                        # displays successfully save popup
                        msg = QtWidgets.QMessageBox()
                        msg.setWindowTitle('Filed Saved Successfully')
                        msg.setIcon(QtWidgets.QMessageBox.Information)
                        msg.setText(
                            'The new order was successfully saved.')
                        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                        _ = msg.exec_()
                    else:
                        # displays unsuccessfully save popup
                        msg = QtWidgets.QMessageBox()
                        msg.setWindowTitle('Unsuccessfully saved!')
                        msg.setIcon(QtWidgets.QMessageBox.Critical)
                        msg.setText(
                            'The new order was unsuccessfully copied to "Past Orders".')
                        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                        _ = msg.exec_()
            else:
                pass

        # automatically called when an order is added to the inventory.
        elif called_from.lower() == 'add_to_inventory':
            new_inventory = get_inventory()
            with pd.ExcelWriter(f'Saved_Lists/Inventory.xlsx') as writer:
                # Saves the new inventory as a spreadsheet, with each sheetname as the category name.
                for cat in new_inventory.keys():
                    new_inventory[cat].save_toexcel(writer=writer)

    def add_to_inventory(self):
        # using function from data_handling.py
        add_order_to_Inventory(self.is_sheet_open)

        # popup to ask user if wants to save the "new" inventory.
        user = QtWidgets.QMessageBox()
        user.setWindowTitle("Saving new Inventory")
        pixmapi = getattr(QtWidgets.QStyle, "SP_DialogSaveButton")
        icon = self.style().standardIcon(pixmapi)
        user.setWindowIcon(icon)

        user.setIcon(QtWidgets.QMessageBox.Question)
        user.setText('Would you like to save the new inventory?')
        user.setStandardButtons(
            QtWidgets.QMessageBox.Yes |
            QtWidgets.QMessageBox.No
        )
        user.setDefaultButton(QtWidgets.QMessageBox.Yes)
        user = user.exec_()

        if user == QtWidgets.QMessageBox.Yes:
            # saving to inventory
            self.save_list(called_from='add_to_inventory')
            # text file to store files that have been added.
            added_orders = 'Saved_lists/added_to_inventory.txt'
            line_count = 0  # count used to increment added orders.
            if os.path.exists(added_orders):
                # this file exists, count the number of line
                with open(added_orders, 'r') as file:
                    # Read the lines and count them
                    line_count = sum(1 for line in file)
            with open(added_orders, 'a') as file:
                # adding order name to text of previous added orders.
                filename = self.is_sheet_open.split('/')[-1]
                text = '{:>3}: {:s}\n'.format(line_count+1, filename)
                file.write(text)

    def fill_table(self, dataframe):
        '''
        Function to fill in table.

        Parameter:
            dataframe: can take a dict, pandas dataframe or list of dataframes.
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

    def get_table_data(self):
        '''
        Function to get the displayed table data into a dataframe.

        Returns a pandas dataframe.
        '''
        rows = self.table.rowCount()
        cols = self.table.columnCount()
        data = []

        if rows:
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
        else:
            print("NO ROWS IN TABLE")

    def create_project(self):
        '''
        Function to create a new project using a second window.

        Prompt user to enter a enter project name, then checks if it exists.
        If the project name exists popup appears to tell the user, otherwise
        it asks the user what filetype they want and creates the project file.
        '''
        dialog = QtWidgets.QInputDialog(self)
        text = 'Enter a project name and the filetype seperated by a comma.\t\n\n'
        text += 'Example: "Temperature Gauge, CSV"\n\n'
        text += 'Filetype options:\n\t- CSV (Comma-Seperated-Values)\n\t- XLSX (Excel)'
        user, ok = dialog.getText(
            self,
            "Creating New Project",
            text
        )
        filetype = None   # obtained in try block.
        name = None       # obtained in try block.

        # User clicks 'ok', goes into try block to split user's string
        # into a filename and filetype.
        title = 'Electronics Inventory Program - Creating New Project'  # window title
        if ok:
            try:
                # try block to split user's string into a name and filetype
                name, filetype = user.split(',')
                name = name.strip()
                filetype = filetype.strip()
            except Exception as err:
                # popup to tell user entered information is in the wrong format.
                user = QtWidgets.QMessageBox()
                user.setWindowTitle(title)
                pixmapi = getattr(QtWidgets.QStyle, "SP_MessageBoxCritical")
                icon = self.style().standardIcon(pixmapi)
                user.setWindowIcon(icon)

                text = 'You entered the information in the wrong format, try again.'
                user.setText(text)
                user.setIcon(QtWidgets.QMessageBox.Critical)
                user.setStandardButtons(QtWidgets.QMessageBox.Ok)
                user = user.exec_()
                return

        # user enters a project name and clicks the "ok" button.
        if ok and name and filetype:
            # checking for correct filetype.
            if filetype.lower() in ['csv', 'xlsx', 'excel', '.csv', '.xlsx']:
                if filetype.lower() == 'excel':
                    # if user enter "excel", changes filetype to '.xlsx'
                    filetype = 'xlsx'
                elif "." in filetype.lower():
                    # if user enters "." in the filetype, remove it so program doesn.t crash.
                    filetype = filetype.strip('.')
                filepath = f'Saved_Lists/Projects/{name}.{filetype}'

                if not os.path.exists(filepath):
                    # if project doesn't exist, open the project window
                    # to allow the user to create a new project.
                    self.project_window.setWindowTitle(title)
                    text = f'New Project: {name}.{filetype}'
                    self.project_window.header.setText(text)
                    self.project_window.load_Project(filepath)
                    self.project_window.show()
                else:
                    # popup telling user project name already exists.
                    user = QtWidgets.QMessageBox()
                    user.setWindowTitle(title)
                    pixmapi = getattr(
                        QtWidgets.QStyle,
                        "SP_MessageBoxCritical"
                    )
                    icon = self.style().standardIcon(pixmapi)
                    user.setWindowIcon(icon)
                    user.setIcon(QtWidgets.QMessageBox.Critical)

                    text = f'Project name "{name}.{filetype}" already exsits!'
                    user.setText(text)
                    user.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    user = user.exec_()
            else:
                # pop to tell user they enter a wrong filetype.
                self.wrong_filetype_msg()

        # User clicks "ok", but doesn't enter a project name.
        elif ok and not name:
            user = QtWidgets.QMessageBox()
            user.setWindowTitle(title)
            pixmapi = getattr(QtWidgets.QStyle, "SP_MessageBoxWarning")
            icon = self.style().standardIcon(pixmapi)
            user.setWindowIcon(icon)
            user.setIcon(QtWidgets.QMessageBox.Warning)
            text = 'You must enter a project name!'
            user.setText(text)
            user.setStandardButtons(QtWidgets.QMessageBox.Ok)
            user = user.exec_()

        # User clicks "ok", but doesn't enter a filetype.
        elif ok and not filetype:
            user = QtWidgets.QMessageBox()
            user.setWindowTitle(title)
            pixmapi = getattr(QtWidgets.QStyle, "SP_MessageBoxWarning")
            icon = self.style().standardIcon(pixmapi)
            user.setWindowIcon(icon)
            user.setIcon(QtWidgets.QMessageBox.Warning)
            text = 'You must enter a filetype!'
            user.setText(text)
            user.setStandardButtons(QtWidgets.QMessageBox.Ok)
            user = user.exec_()

    def get_clicked_row(self, index, labels):
        '''
        Function to get the item row when user clicks a cell
        '''

        if self.project_window.isVisible():
            '''
            if project window is open, then send the clicked row to
            the project window.
            '''

            data = self.get_table_data()

            # getting the individual item and putting into a dataframe.
            item = pd.Series([cell for cell in data.iloc[index]])
            item = pd.DataFrame(item).T
            item.columns = data.keys()
            item['Quantity'] = 1  # need this for incrementing quantities.

            # passing item to project window.
            self.project_window.item_from_main_window(item)


if __name__ == "__main__":
    # runnning program
    load_Inventory()
    app = QApplication(sys.argv)
    window1 = MainWindow()
    app.exec_()
