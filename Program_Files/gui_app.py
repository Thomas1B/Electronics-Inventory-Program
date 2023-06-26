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

from .info_windows import Program_Info_Window, How_To_Use_Program_Window
from .add_item_window import Add_Item_Window
from .project_window import Project_Window

from .gui_handling import (
    show_btns,
    hide_btns,
    show_sorting_btns,
    hide_sorting_btns,
    open_website,
    wrong_filetype_msg,
    toggled_widgets,
    refresh_opensheet,
    fill_table,
    get_table_data,
    open_add_manually_window,
    get_editted_item,
    change_item_quantity,
    copySelectedCell
)

from .data_handling import (
    Category,
    Inventory,
    labels,
    load_Inventory,
    get_ordersheet,
    add_order_to_Inventory,
    dict_to_dataframe,
    sort_order,
    get_inventory,
    drop_all_from_dict,
    update_item
)


'''
dictionary used a temporary holder for opening files.
'''
Items = {key: Category(key) for key in Inventory.keys()}


class MainWindow(QMainWindow):
    '''
    Class to run the main window of the program.
    '''

    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        uic.loadUi('Program_Files/UI_Files/gui_app.ui', self)
        self.move(50, 50)

        # Other Windows used in the program.
        self.project_window = Project_Window(self)
        self.add_item_window = Add_Item_Window(self)
        self.window_program_info = Program_Info_Window()
        self.how_to_use_window = How_To_Use_Program_Window()

        # variable to keep track of States:
        self.is_sheet_open = False  # what sheet is opened.
        self.editted_saved = True  # if inventory has been saveed.
        self.in_edit_mode = False  # if in edit mode.

        ''' Defining Widgets'''

        # Menu Bar
        self.action_open_program_info = self.findChild(
            QtWidgets.QAction, 'actionProgram_Info'
        )
        self.action_how_to_use = self.findChild(
            QtWidgets.QAction, 'actionHow_To_Use'
        )
        self.action_open_Digikey = self.findChild(
            QtWidgets.QAction, 'actionDigiKey'
        )
        self.action_open_adafruit = self.findChild(
            QtWidgets.QAction, 'actionAdafruit'
        )
        self.action_open_BCrobotics = self.findChild(
            QtWidgets.QAction, 'actionBC_Robotics'
        )

        # Toolbar
        self.toolbar = self.findChild(QtWidgets.QToolBar, 'toolBar')
        self.action_open_new_order = self.findChild(
            QtWidgets.QAction, 'actionOpen_New_Order'
        )
        self.action_open_past_orders = self.findChild(
            QtWidgets.QAction, 'actionOpen_Past_Orders'
        )
        self.action_open_inventory = self.findChild(
            QtWidgets.QAction, 'actionOpen_Inventory'
        )
        self.action_open_projects = self.findChild(
            QtWidgets.QAction, 'actionOpen_Projects'
        )
        self.action_export_file = self.findChild(
            QtWidgets.QAction, 'actionExport_File'
        )
        self.action_create_project = self.findChild(
            QtWidgets.QAction, 'actionCreate_Project'
        )

        # Info Labels
        self.header_frame = self.findChild(QtWidgets.QFrame, 'header_frame')
        self.header = self.findChild(QtWidgets.QLabel, 'header')
        self.sub_header = self.findChild(QtWidgets.QLabel, 'sub_header')
        self.table = self.findChild(QtWidgets.QTableWidget, 'table')

        # Buttons
        self.btn_save_list = self.findChild(
            QtWidgets.QPushButton, 'btn_save_list'
        )
        self.btn_add_to_inventory = self.findChild(
            QtWidgets.QPushButton, 'btn_add_to_inventory'
        )
        self.btn_edit_mode = self.findChild(
            QtWidgets.QPushButton, 'btn_edit_mode'
        )
        self.btn_add_item_manually = self.findChild(
            QtWidgets.QPushButton, 'btn_add_item_manually'
        )

        # Sorting Buttons
        self.sorting_btns_frame = self.findChild(QtWidgets.QFrame, 'frame')
        self.btn_refresh_opensheet = self.findChild(
            QtWidgets.QPushButton, 'btn_refresh_opensheet'
        )
        self.btn_resistors = self.findChild(
            QtWidgets.QPushButton, 'btn_resistors'
        )
        self.btn_capacitors = self.findChild(
            QtWidgets.QPushButton, 'btn_capacitors'
        )
        self.btn_inductors = self.findChild(
            QtWidgets.QPushButton, 'btn_inductors')
        self.btn_transistors = self.findChild(
            QtWidgets.QPushButton, 'btn_transistors'
        )
        self.btn_diodes = self.findChild(
            QtWidgets.QPushButton, 'btn_diodes'
        )
        self.btn_ics = self.findChild(
            QtWidgets.QPushButton, 'btn_ics'
        )
        self.btn_leds = self.findChild(
            QtWidgets.QPushButton, 'btn_leds'
        )
        self.btn_buttons = self.findChild(
            QtWidgets.QPushButton, 'btn_buttons'
        )
        self.btn_connectors = self.findChild(
            QtWidgets.QPushButton, 'btn_connectors'
        )
        self.btn_displays = self.findChild(
            QtWidgets.QPushButton, 'btn_displays'
        )
        self.btn_audio = self.findChild(QtWidgets.QPushButton, 'btn_audio')
        self.btn_modules = self.findChild(
            QtWidgets.QPushButton, 'btn_modules'
        )
        self.btn_other = self.findChild(
            QtWidgets.QPushButton, 'btn_other'
        )

        ''' Attaching Functions to Widgets '''

        # Table
        self.table.cellClicked.connect(self.get_clicked_row)

        # Menu
        self.action_open_program_info.triggered.connect(self.show_program_info)
        self.action_how_to_use.triggered.connect(self.show_how_to_use)
        self.action_open_Digikey.triggered.connect(
            lambda: open_website(self, 'Digikey')
        )
        self.action_open_adafruit.triggered.connect(
            lambda: open_website(self, 'Adafruit')
        )
        self.action_open_BCrobotics.triggered.connect(
            lambda: open_website(self, 'BC Robotics')
        )

        # toolbar
        self.action_open_inventory.triggered.connect(self.open_inventory)
        self.action_open_new_order.triggered.connect(self.open_new_order)
        self.action_open_projects.triggered.connect(self.open_project_lists)
        self.action_create_project.triggered.connect(self.create_project)
        self.action_open_past_orders.triggered.connect(self.open_past_order)
        self.action_export_file.triggered.connect(
            lambda: self.export_file(autoname=True))

        # Command Buttons
        self.btn_add_to_inventory.clicked.connect(self.add_to_inventory)
        self.btn_edit_mode.clicked.connect(self.edit_mode)
        self.btn_add_item_manually.clicked.connect(
            lambda: open_add_manually_window(self)
        )

        # Sorting Buttons
        self.btn_refresh_opensheet.clicked.connect(
            lambda: refresh_opensheet(self, Items)
        )
        self.btn_resistors.clicked.connect(
            lambda: self.show_sorted_section('Resistors')
        )
        self.btn_capacitors.clicked.connect(
            lambda: self.show_sorted_section('Capacitors')
        )
        self.btn_inductors.clicked.connect(
            lambda: self.show_sorted_section('Inductors')
        )
        self.btn_transistors.clicked.connect(
            lambda: self.show_sorted_section('Transistors')
        )
        self.btn_diodes.clicked.connect(
            lambda: self.show_sorted_section('Diodes')
        )
        self.btn_ics.clicked.connect(
            lambda: self.show_sorted_section('ICs')
        )
        self.btn_leds.clicked.connect(
            lambda: self.show_sorted_section('LEDs')
        )
        self.btn_buttons.clicked.connect(
            lambda: self.show_sorted_section('Buttons')
        )
        self.btn_connectors.clicked.connect(
            lambda: self.show_sorted_section('Connectors')
        )
        self.btn_displays.clicked.connect(
            lambda: self.show_sorted_section('Displays')
        )
        self.btn_audio.clicked.connect(
            lambda: self.show_sorted_section('Audio')
        )
        self.btn_modules.clicked.connect(
            lambda: self.show_sorted_section('Modules')
        )
        self.btn_other.clicked.connect(
            lambda: self.show_sorted_section('Other')
        )

        # Styles
        self.table.setColumnWidth(0, 175)  # Default columns widths
        self.table.setColumnWidth(1, 175)
        self.table.setColumnWidth(2, 175)
        self.table.setColumnWidth(3, 175)
        self.table.setColumnWidth(4, 75)
        self.table.setColumnWidth(5, 75)

        self.toolbar.setStyleSheet(  # Toolbar styles
            '''
            QToolButton {
                padding: 5px;
            }
             QToolButton:hover {
                background-color: rgb(200, 200, 200);
            }
            '''
        )

        # Hidiing some buttons for initial start.
        hide_btns(self, [
            self.btn_save_list,
            self.btn_add_to_inventory,
            self.header_frame,
            self.btn_edit_mode,
            self.btn_add_item_manually,
        ])
        hide_sorting_btns(self)

        self.show()  # showing window

    def closeEvent(self, event) -> None:
        '''
        Function to detect when user closes the window.

            Parameters:
                event: QtGui.QCloseEvent.
        '''

        if self.editted_saved:  # inventory has been saved
            # closing other windows.
            for window in [self.project_window, self.add_item_window]:
                window.close()
            event.accept()  # close this window.

        else:  # inventory has NOT been saved
            event.ignore()  # stopping window closing.

            # Pop up telling user that the inventory has not been saved yet.
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
            header = 'Inventory has been editted!'
            text = 'Would you like to save before closing the program?'
            user.setWindowTitle("Closing Program")
            user.setText(header)
            user.setInformativeText(text)
            user = user.exec_()

            # checking user's response:
            match user:
                case QtWidgets.QMessageBox.Yes:
                    self.save_list('editted')
                    event.accept()
                case QtWidgets.QMessageBox.No:
                    # user declines to save.
                    event.accept()
                case _:  # Cancel
                    event.ignore()

    def contextMenuEvent(self, event) -> None:
        '''
        Function to show a menu when right clicked on item in the table.

            Parameters:
                event: QtGui.QCloseEvent.
        '''

        # only show contextMenu when inventory is opened.
        conditions = ['Inventory']
        if any(word.lower() in self.header.text().lower() for word in conditions):

            # getting table geometry
            pos = self.table.viewport().mapFromGlobal(event.globalPos())
            row_index = self.table.rowAt(pos.y())

            # if right click on a row_index, row_index >= 0
            if row_index >= 0:

                # Creating Menu
                menu = QtWidgets.QMenu()
                menu = QtWidgets.QMenu(self)
                copy_selected_action = QtWidgets.QAction("Copy Selected")
                add_one_action = QtWidgets.QAction("Add One")
                delete_action = QtWidgets.QAction("Remove One")
                delete_item_action = QtWidgets.QAction("Delete")

                # Attaching Functions to actions
                copy_selected_action.triggered.connect(
                    lambda: copySelectedCell(
                        self,
                        self.table.selectedItems()
                    )
                )
                add_one_action.triggered.connect(
                    lambda: change_item_quantity(
                        self,
                        Inventory,
                        row_index,
                        remove_all=None
                    )
                )
                delete_action.triggered.connect(
                    lambda: change_item_quantity(
                        self,
                        Inventory,
                        row_index,
                        remove_all=False
                    )
                )
                delete_item_action.triggered.connect(
                    lambda: change_item_quantity(
                        self,
                        Inventory,
                        row_index,
                        remove_all=True
                    )
                )

                # Adding to actions to menu
                menu.addAction(copy_selected_action)
                menu.addAction(add_one_action)
                menu.addAction(delete_action)
                menu.addAction(delete_item_action)

                menu.exec_(event.globalPos())  # showing menu

    def show_program_info(self) -> None:
        '''
        Function to show user the program info.

        Opens a second window
        '''
        self.window_program_info.show()

    def show_how_to_use(self) -> None:
        '''
        Function to show the "how to use" window for the user.
        '''
        self.how_to_use_window.show()

    def no_files_msg(self, title='No Files', header="", text="") -> None:
        '''
        Function to display a pop up warning user there are no files to open

        Parameters:
            title - str: pop up window title
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

    def disable_feature_msg(self, header='', text=None) -> None:
        '''
        Function to display a pop that a feature has been disable.

        Parameter:
            header: header text.
            text: informatiive text.
        '''

        if not header:
            header = 'Feature is disabled.'
        if text:
            msg.setInformativeText(text)

        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle('Disabled Feature')
        pixmapi = getattr(QtWidgets.QStyle, "SP_MessageBoxCritical")
        icon = self.style().standardIcon(pixmapi)
        msg.setWindowIcon(icon)
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText(header)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        _ = msg.exec_()

    def export_file(self, autoname=True) -> None:
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
                "Saved_Lists",
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
                    new_name = f'{destination_folder}/{export_filename}({counter}){ext}'
                    counter += 1
                shutil.copy2(file_toexport, new_name)
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Exporting File')
                pixmapi = getattr(QtWidgets.QStyle, "SP_MessageBoxInformation")
                icon = self.style().standardIcon(pixmapi)
                msg.setWindowIcon(icon)
                msg.setIcon(QtWidgets.QMessageBox.Information)

                msg.setText('File exported!')
                text = f'File exported to "exported_electronics_lists" in your downloads.'
                msg.setInformativeText(text)
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                _ = msg.exec_()

            else:
                pass

    def load_Items(self, order: list) -> None:
        '''
        Function to load items into the Item dictionary.

            Parameters:
                order: list of items to load into the the dictionary
        '''
        drop_all_from_dict(Items)
        for items, section in zip(order, Items.keys()):
            if len(order) > 0:
                if not items.empty:
                    Items[section].add_item(items)
                    Items[section].remove_duplicates()

    def open_inventory(self) -> None:
        '''
        Function to open the inventory
        '''
        hide_btns(self, [self.btn_add_to_inventory, self.btn_save_list])
        if os.path.exists("Saved_Lists/Inventory.xlsx"):
            if not self.editted_saved:
                self.btn_save_list.clicked.connect(
                    lambda: self.save_list('add_to_inventory')
                )
                self.btn_save_list.show()
            self.is_sheet_open = "Saved_Lists/Inventory.xlsx"
            self.sub_header.setText('')
            self.header.setText('Looking at Inventory')
            fill_table(self, Inventory)
            show_sorting_btns(self)
            show_btns(self,
                      [self.header_frame, self.btn_edit_mode, self.btn_add_item_manually])
        else:
            header = 'There is no inventory file.'
            text = 'Create an inventory by reading in some orders!'
            title = 'No Inventory'
            self.no_files_msg(title=title, header=header, text=text)
            hide_sorting_btns(self)

    def open_new_order(self) -> None:
        '''
        Function to open a new order.
        '''

        downloads_path = os.path.expanduser("~" + os.sep + "Downloads")
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Opening New Order', downloads_path, 'All Files (*) ;; CSV Files (*.csv);; Excel Files (*.xlsx)')
        filetype = filename.split('.')[-1]

        if filetype:
            # checking filetype
            if filetype in ['csv', 'xlsx']:

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

                new_order = get_ordersheet(filename)
                self.load_Items(new_order)

                self.is_sheet_open = filename
                text = f'Looking at new order: {filename.split("/")[-1]}'
                self.header.setText(text)
                self.sub_header.setText('')
                self.header_frame.show()

                fill_table(self, Items)
                hide_btns(self, [
                    self.btn_add_item_manually,
                    self.btn_edit_mode
                ])
                show_btns(self,
                          [self.btn_add_to_inventory])
                show_sorting_btns(self)
            else:
                wrong_filetype_msg(self)

    def open_past_order(self) -> None:
        '''
        Function to open a past order
        '''
        if len(os.listdir('Saved_Lists/Past Orders')) > 0:
            self.sub_header.setText('')
            filename, _ = QtWidgets.QFileDialog.getOpenFileName(
                self,
                'Electronics Inventory Program - Opening Past Orders',
                'Saved_Lists/Past Orders',
                'All Files (*) ;; CSV Files (*.csv);; Excel Files (*.xlsx)'
            )
            filetype = filename.split(".")[-1]
            name = filename.split('/')[-1]
            if filetype in ['csv', 'xlsx']:
                self.sub_header.setText('')
                self.header.setText(f'Past Order: {name}')
                self.header_frame.show()

                self.is_sheet_open = filename
                past_order = get_ordersheet(filename)
                self.load_Items(past_order)
                fill_table(self, Items)

                show_sorting_btns(self)
                hide_btns(self, [
                    self.btn_add_item_manually,
                    self.btn_edit_mode,
                    self.btn_add_to_inventory,
                    self.btn_save_list
                ])

            elif len(filetype) == 0:
                # no file selected
                pass

            else:
                wrong_filetype_msg(self)

        else:
            header = 'There are no past orders to open!'
            self.no_files_msg(title='No Past Orders', header=header)

    def open_project_lists(self) -> None:
        '''
        Function to open project lists.
        '''
        self.project_window.open_project()

    def show_sorted_section(self, section: str) -> None:
        '''
        Function to show the sorted sections

            Parameter:
                section - str: name of category to display.
        '''
        if 'looking at inventory' in self.header.text().lower():
            fill_table(self, Inventory[section].get_items())
        else:
            fill_table(self, Items[section].get_items())
        self.sub_header.setText(section)

    def save_list(self, called_from: str) -> None:
        '''
        Function to save a list.

        Parameters:
            called_from: where the function was called from
        '''

        if called_from.lower() == 'save_order':  # if new order is being saved.
            destination_folder = 'Saved_Lists/Past Orders'
            shutil.copy2(self.is_sheet_open, destination_folder)

            # automatically called when an order is added to the inventory.
        elif called_from.lower() == 'add_to_inventory' or 'edited':
            self.editted_saved = True
            new_inventory = get_inventory()
            with pd.ExcelWriter(f'Saved_Lists/Inventory.xlsx') as writer:
                # Saves the new inventory as a spreadsheet, with each sheetname as the category name.
                for cat in new_inventory.keys():
                    new_inventory[cat].save_toexcel(writer=writer)

            # displays successfully save popup
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle('Inventory Saved Successfully')
            pixmapi = getattr(QtWidgets.QStyle, "SP_DialogApplyButton")
            icon = self.style().standardIcon(pixmapi)
            msg.setWindowIcon(icon)
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText(
                'Inventory saved was successfully.')
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            _ = msg.exec_()

        self.btn_save_list.hide()

    def add_to_inventory(self) -> None:
        '''
        Function to add an order to inventory.
            - Triggered by add_to_inventory button.
        '''

        # checking if order has been added already.
        read_orders_list = 'Saved_Lists/Orders_added_to_inventory.txt'
        if os.path.exists(read_orders_list):
            read_orders = pd.read_csv(read_orders_list, delimiter='\s+')

            files = []
            with open(read_orders_list, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    line = line.rstrip()
                    line = line.split(": ")[-1]
                    line = line.split('.')[0]
                    files.append(line)

            name = self.is_sheet_open.split("/")[-1].split('.')[0]

            if name in files:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Reading New Order')
                pixmapi = getattr(QtWidgets.QStyle, "SP_MessageBoxInformation")
                icon = self.style().standardIcon(pixmapi)
                msg.setWindowIcon(icon)
                header = 'Order already added!'
                msg.setText(header)
                info_text = f'The order "{name}" has already been added to the inventory.'
                msg.setInformativeText(info_text)
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msg.exec_()
                return

        # using function from data_handling.py
        add_order_to_Inventory(Items)

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

        # checking user's response
        # text file to store files that have been added.
        added_orders = 'Saved_lists/Orders_added_to_inventory.txt'
        line_count = 0  # count used to increment added orders.
        match user:
            case QtWidgets.QMessageBox.Yes:
                # saving to inventory

                self.save_list(called_from='add_to_inventory')
            case _:
                self.editted_saved = False
                self.btn_save_list.clicked.connect(
                    lambda: self.save_list(called_from='editted')
                )
                self.btn_save_list.show()

        # this file exists, count the number of line
        if os.path.exists(added_orders):
            with open(added_orders, 'r') as file:
                # Read the lines and count them
                line_count = sum(1 for line in file)
        with open(added_orders, 'a') as file:
            # adding order name to text of previous added orders.
            filename = self.is_sheet_open.split('/')[-1]
            text = '{:>3}: {:s}\n'.format(line_count+1, filename)
            file.write(text)

    def create_project(self) -> None:
        '''
        Function to create a new project using a second window.

            Prompts user to enter a project name, then checks if it exists.
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
                wrong_filetype_msg(self)

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

    def get_clicked_row(self, index: int) -> None:
        '''
        Function to get the item from the table

            Parameter:
                index: index of item, starts at 0.
        '''

        if self.project_window.isVisible():
            '''
            if project window is open, then send the clicked row to
            the project window.
            '''

            data = get_table_data(self)

            # getting the individual item and putting into a dataframe.
            item = pd.Series([cell for cell in data.iloc[index]])
            item = pd.DataFrame(item).T
            item.columns = data.keys()
            item['Quantity'] = 1  # need this for incrementing quantities.

            # passing item to project window.
            self.project_window.item_from_main_window(item)

    def edit_mode(self) -> None:
        '''
        Function to update the Project inventory when the table is in edit mode.
        '''

        # buttons to toggle in edit mode.
        btns = [
            self.btn_add_to_inventory,
            self.btn_add_item_manually
        ]

        if not self.in_edit_mode:
            self.in_edit_mode = True
            self.btn_edit_mode.setText('Exit Edit Mode')
            text = f'Editting Inventory'
            self.header.setText(text)
            self.header.setStyleSheet('color: red;')
            self.table.setEditTriggers(QtWidgets.QTableWidget.DoubleClicked)
            self.table.itemChanged.connect(self.get_editted)
            toggled_widgets(self, widgets=btns, enable=False)
        else:
            self.in_edit_mode = False
            self.btn_edit_mode.setText('Edit Mode')
            text = 'Looking at Inventory'
            self.header.setText(text)
            self.header.setStyleSheet('color: black;')
            self.table.itemChanged.disconnect(self.get_editted)
            self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            toggled_widgets(self, widgets=btns, enable=True)

    def get_editted(self, clicked_item: QtWidgets.QTableWidgetItem) -> None:
        '''
        Function to get the item that has been editted.
            Triggered by itemChanged in table.

            Parameter:
                clicked_item: QTableItem that was clicked.
        '''

        item = get_editted_item(self, clicked_item)
        if item.shape[0] < 1:
            return
        else:
            self.editted_saved = False
            self.btn_save_list.clicked.connect(
                lambda: self.save_list(called_from='editted')
            )
            self.btn_save_list.show()
            # updating project
            update_item(self, item, Inventory)

    def receive_add_item_manually(self, item) -> None:
        '''
        Function to read user's input when adding an item manually.
            Triggered when btn "Add to inventory" clicked.
        '''

        items = sort_order(item)  # sorting item.
        add_order_to_Inventory(items)  # adding to inventory.
        fill_table(self, Inventory)  # updating table.

        self.editted_saved = False
        self.btn_save_list.setText('Save Inventory')
        self.btn_save_list.clicked.connect(
            lambda: self.save_list('edited')
        )
        self.btn_save_list.show()


if __name__ == "__main__":
    # runnning program
    load_Inventory()
    app = QApplication(sys.argv)
    window1 = MainWindow()
    app.exec_()
