'''
Script to run PyQt app functions and classes.
'''

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QUrl, QDir
from PyQt5.QtGui import QDesktopServices, QIcon
import pandas as pd
import sys
import os
import shutil

from .info_windows import Program_Info_Window, How_To_Use_Program_Window
from .add_item_window import Add_Item_Window
from .project_window import Project_Window
from .search_window import SearchWindow, open_search_window

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
    change_item_qty,
    copySelectedCell,
    web_search_item
)

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
)


from .styles import (
    toolbar_styles,
    style_central_widget,
    style_table,
    style_sorting_comboBox,
    style_refresh_btn
)


class MainWindow(QMainWindow):
    '''
    Class to run the main window of the program.
    '''

    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        uic.loadUi('Program_Files/UI_Files/gui_app.ui', self)
        self.setWindowIcon(QIcon('Program_files/Icons/circuit.png'))
        # self.findChild(QtWidgets.QWidget, 'centralwidget').setStyleSheet(
        # central_widget_style)
        style_central_widget(self)
        self.showMaximized()

        # Other Windows used in the program.
        # self.project_window = Project_Window(self)
        self.add_item_window = Add_Item_Window(self)
        self.window_program_info = Program_Info_Window()
        self.how_to_use_window = How_To_Use_Program_Window()

        # variable to keep track of States:
        self.is_sheet_open = False  # what sheet is opened.
        self.editted_saved = True  # if inventory has been saved.
        self.in_edit_mode = False  # if in edit mode.
        self.new_orders_list = []
        self.new_orders_count = 0  # count how many orders have been added
        self.sort_by = {key: True for key in labels}
        self.project_windows = []

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
        self.action_search = self.findChild(
            QtWidgets.QAction, 'actionSearch'
        )
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
        self.action_import_file = self.findChild(
            QtWidgets.QAction, 'actionImport_File'
        )
        self.action_import_folder = self.findChild(
            QtWidgets.QAction, 'actionImport_Folder'
        )
        self.action_export_file = self.findChild(
            QtWidgets.QAction, 'actionExport_File'
        )
        self.action_export_folder = self.findChild(
            QtWidgets.QAction, 'actionExport_Folder'
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
        self.sorting_btns_frame = self.findChild(
            QtWidgets.QFrame, 'sorting_frame')
        self.comboBox_section = self.findChild(
            QtWidgets.QComboBox, 'comboBox_section'
        )
        self.btn_refresh_opensheet = self.findChild(
            QtWidgets.QPushButton, 'btn_refresh_opensheet'
        )

        ''' Attaching Functions to Widgets '''

        # Table
        self.table.horizontalHeader().sectionClicked.connect(self.get_clicked_header)

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
        self.action_search.triggered.connect(lambda: open_search_window(self))
        self.action_open_inventory.triggered.connect(self.open_inventory)
        self.action_open_new_order.triggered.connect(self.open_new_order)
        self.action_open_projects.triggered.connect(self.open_project_lists)
        self.action_create_project.triggered.connect(self.create_project)
        self.action_open_past_orders.triggered.connect(self.open_past_order)
        self.action_export_file.triggered.connect(
            lambda: self.exporting(kind='file')
        )
        self.action_export_folder.triggered.connect(
            lambda: self.exporting(kind='dir')
        )
        self.action_import_file.triggered.connect(
            lambda: self.importing(kind='file')
        )
        self.action_import_folder.triggered.connect(
            lambda: self.importing(kind='dir')
        )

        # Command Buttons
        self.btn_save_list.clicked.connect(self.save_list)
        self.btn_add_to_inventory.clicked.connect(self.add_to_inventory)
        self.btn_edit_mode.clicked.connect(self.edit_mode)
        self.btn_add_item_manually.clicked.connect(
            lambda: open_add_manually_window(self)
        )

        # Sorting Buttons
        self.btn_refresh_opensheet.clicked.connect(
            lambda: refresh_opensheet(self, Items)
        )
        self.comboBox_section.currentIndexChanged.connect(
            lambda: self.show_sorted_section(
                self.comboBox_section.currentText())
        )

        # styling refresh button
        style_refresh_btn(self)

        style_table(self)  # styling table

        # toolbar
        self.toolbar.setStyleSheet(toolbar_styles)

        # adding category to sorting comboBox and styling
        style_sorting_comboBox(self)
        for key in sorted(dict_keys):
            self.comboBox_section.addItem(key)

        # Hidiing some buttons for initial start.
        hide_btns(self, [
            self.btn_save_list,
            self.btn_add_to_inventory,
            self.header_frame,
            self.btn_edit_mode,
            self.btn_add_item_manually,
        ])
        hide_sorting_btns(self)

        # stying labels in header frame
        for label in self.header_frame.findChildren(QtWidgets.QLabel):
            label.setStyleSheet(
                '''
                QLabel {
                    font-size: 22px;
                    font-weight: bold;
                }
                '''
            )

        self.show()  # showing window

    def closeEvent(self, event) -> None:
        '''
        Function to detect when user closes the window.

            Parameters:
                event: QtGui.QCloseEvent.
        '''

        if self.editted_saved:  # inventory has been saved
            # closing children windows.
            children = self.get_children_windows()
            for child in children:
                child.close()
            event.accept()  # close this window.

        else:  # inventory has NOT been saved
            # stopping window closing.
            event.ignore()

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
                    self.save_list()
                    event.accept()
                case QtWidgets.QMessageBox.No:
                    # user declines to save.
                    past_orders = 'Saved_Lists/Past Orders'
                    for file in self.new_orders_list:
                        os.remove(file)
                    event.accept()
                case _:  # Cancel
                    event.ignore()

    def contextMenuEvent(self, event) -> None:
        '''
        Function to show a menu when right clicked on item in the table.

            Parameters:
                event: QtGui.QCloseEvent.
        '''

        # # only show contextMenu when inventory is opened.
        conditions = ['Inventory', 'Project']
        if any(word.lower() in self.header.text().lower() for word in conditions):

            # getting table geometry
            pos = self.table.viewport().mapFromGlobal(event.globalPos())
            row_index = self.table.rowAt(pos.y())

            # if right click on a row_index, row_index >= 0
            if row_index >= 0:

                # Creating Menu
                menu = QtWidgets.QMenu(self)
                web_search_action = QtWidgets.QAction(
                    QIcon("Program_Files/Icons/application-browser.png"),
                    "Web Search"
                )
                copy_selected_action = QtWidgets.QAction(
                    QIcon("Program_Files/Icons/document.png"),
                    "Copy Selected"
                )
                add_one_action = QtWidgets.QAction(
                    QIcon("Program_Files/Icons/plus.png"),
                    "Add One"
                )
                remove_one_action = QtWidgets.QAction(
                    QIcon("Program_Files/Icons/minus.png"),
                    "Remove One"
                )
                delete_item_action = QtWidgets.QAction(
                    QIcon("Program_Files/Icons/minus-circle-frame.png"),
                    'Delete Item'
                )

                # creating QActions for adding items to projects
                add_to_project_actions = []
                for widget in self.get_children_windows(instances=(Project_Window)):
                    filename = widget.header.text().split(':')[-1]
                    filename = filename.split('.')[0]
                    action = QtWidgets.QAction(
                        QIcon("Program_Files/Icons/document--arrow.png"),
                        f"Add Item to Project: {filename}"
                    )
                    add_to_project_actions.append(action)

                # Attaching Functions to actions
                copy_selected_action.triggered.connect(
                    lambda: copySelectedCell(
                        self,
                        self.table.selectedItems()
                    )
                )
                web_search_action.triggered.connect(
                    lambda: web_search_item(self, row_index)
                )
                add_one_action.triggered.connect(
                    lambda: change_item_qty(
                        self,
                        Inventory,
                        row_index,
                        remove_all=None
                    )
                )
                remove_one_action.triggered.connect(
                    lambda: change_item_qty(
                        self,
                        Inventory,
                        row_index,
                        remove_all=False
                    )
                )
                delete_item_action.triggered.connect(
                    lambda: change_item_qty(
                        self,
                        Inventory,
                        row_index,
                        remove_all=True
                    )
                )
                for action_index, action in enumerate(add_to_project_actions):
                    action.triggered.connect(
                        # dummy is need since signal sends the current variable
                        lambda dummy, action_index=action_index: self.add_to_project(
                            row_index, action_index)
                    )

                # Adding to actions to menu
                menu.addAction(web_search_action)
                menu.addSeparator()
                menu.addAction(copy_selected_action)
                menu.addAction(add_one_action)
                menu.addAction(remove_one_action)
                menu.addAction(delete_item_action)
                menu.addSeparator()
                for action in add_to_project_actions:
                    menu.addAction(action)

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

    def importing(self, kind: str) -> None:
        '''
        Function to import file(s) and Folders.

        Parameter:
            kind: "file"/"dir", importing file or directory.
        '''

        imported = None

        # directory is being imported.
        match kind:
            case 'dir':

                # getting the selected directory.
                imported = QtWidgets.QFileDialog.getExistingDirectory(
                    self,
                    "EIP - Importing",
                    os.path.expanduser("~/Downloads")
                )

                if imported:  # if a directory is selected:

                    # getting the destination directory.
                    destination = QtWidgets.QFileDialog.getExistingDirectory(
                        self,
                        'EIP - Selecting Destination',
                        'Saved_Lists'
                    )

                    if destination:  # if a destination is selected:
                        imported_filename = imported.split("/")[-1]
                        destination += f'/{imported_filename}'

                        # try block to copy directory:
                        try:
                            shutil.copytree(imported, destination)
                        except FileExistsError:
                            # Pop up telling user that the directory has called been imported.
                            # then asks if they want to overwrite it
                            msg = QtWidgets.QMessageBox()
                            pixmapi = getattr(QtWidgets.QStyle,
                                              "SP_MessageBoxWarning")
                            icon = self.style().standardIcon(pixmapi)
                            msg.setWindowIcon(icon)
                            msg.setWindowTitle("Folder Already Imported")
                            text = f'Folder "{imported_filename}" has already been imported.\nWould you like to overwrite?'
                            msg.setText(text)
                            msg.setStandardButtons(
                                QtWidgets.QMessageBox.Yes |
                                QtWidgets.QMessageBox.No |
                                QtWidgets.QMessageBox.Cancel
                            )
                            msg.setDefaultButton(QtWidgets.QMessageBox.Yes)
                            user = msg.exec_()

                            if user == QtWidgets.QMessageBox.Yes:
                                # user wants to overwrite the directory
                                shutil.rmtree(destination)
                                shutil.copytree(imported, destination)

                            elif user == QtWidgets.QMessageBox.No:
                                # user does not want to overwrite.
                                # autonames file
                                count = 1
                                while True:
                                    try:
                                        shutil.copytree(imported, destination)
                                        break
                                    except FileExistsError:
                                        destination = destination.split(
                                            ' (')[0]
                                        destination += f' ({count})'
                                        count += 1

            case 'file':

                # getting the selected files to import
                imported, _ = QtWidgets.QFileDialog.getOpenFileNames(
                    self,
                    "EIP - Importing File(s)",
                    '',
                    'All Files (*);;CSV Files (*.csv);;Excel Files (*.xlsx)'
                )

                if imported:  # if files are selected:

                    # getting the destination for importing.
                    destination_folder = QtWidgets.QFileDialog.getExistingDirectory(
                        self,
                        "EIP - Selecting Desination",
                        'Saved_Lists'
                    )

                    if destination_folder:  # if a destination was selected:

                        for import_file in imported:
                            filename = os.path.basename(import_file)
                            destination_path = os.path.join(
                                destination_folder, filename)

                            count = 1
                            if os.path.exists(destination_path):
                                # Pop up telling user that the file has already been imported.
                                msg = QtWidgets.QMessageBox()
                                pixmapi = getattr(QtWidgets.QStyle,
                                                  "SP_MessageBoxWarning")
                                icon = self.style().standardIcon(pixmapi)
                                msg.setWindowIcon(icon)
                                msg.setWindowTitle(
                                    "File Already Imported")
                                text = f'File {filename} has already been imported.\nWould you like to overwrite it?'
                                msg.setText(text)
                                msg.setStandardButtons(
                                    QtWidgets.QMessageBox.Yes |
                                    QtWidgets.QMessageBox.No |
                                    QtWidgets.QMessageBox.Cancel
                                )
                                msg.setDefaultButton(
                                    QtWidgets.QMessageBox.Yes)
                                user = msg.exec_()
                                match user:
                                    case QtWidgets.QMessageBox.Cancel:
                                        return
                                    case QtWidgets.QMessageBox.Yes:
                                        break
                                    case _:
                                        base_path, extension = os.path.splitext(
                                            destination_path)
                                        while os.path.exists(destination_path):
                                            destination_path = f'{base_path} ({count}){extension}'
                                            count += 1

                            shutil.copy2(import_file, destination_path)

    def exporting(self, kind: str) -> None:
        '''
        Function to export file(s) and Folders.

        Parameter:
            kind: "file"/"dir", importing file or directory.
        '''

        destination_folder = os.path.expanduser(
            "~" + os.sep + "Downloads\EIP Exported Files"
        )

        match kind:
            case 'file':
                files_to_export, _ = QtWidgets.QFileDialog.getOpenFileNames(
                    self,
                    "EIP - Exporting",
                    "Saved_Lists",
                    "All Files (*);; CSV Files (*.csv) ;; XLSX Files (*.xlsx)"
                )

                if files_to_export:
                    for file in files_to_export:
                        filename = os.path.basename(file)
                        destination_path = os.path.join(
                            destination_folder, filename)

                        # checking if file has already been exported, if so modify file name.
                        count = 1
                        base, ext = os.path.splitext(destination_path)
                        while os.path.exists(destination_path):
                            destination_path = f'{base} ({count}){ext}'
                            count += 1
                        shutil.copy2(file, destination_path)

            case 'dir':
                exporting = QtWidgets.QFileDialog.getExistingDirectory(
                    self,
                    "EIP - Exporting",
                    'Saved_Lists'
                )
                if exporting:
                    filename = exporting.split('/')[-1]
                    destination = f'{destination_folder}/{filename}'
                    count = 1
                    base, ext = os.path.splitext(destination)
                    while os.path.exists(destination):
                        destination = f'{base} ({count}){ext}'
                        count += 1
                    shutil.copytree(exporting, destination)

    def load_Items(self, order: list) -> None:
        '''
        Function to load items into the Item dictionary.

            Parameters:
                order: list of items to load into the the dictionary
        '''
        Items.drop_all_items()
        for items, section in zip(order, Items.sections):
            if len(order) > 0:
                if not items.empty:
                    Items.data[section].add_item(items)
                    Items.data[section].remove_duplicates()

    def open_inventory(self) -> None:
        '''
        Function to open the inventory
        '''
        if os.path.exists("Saved_Lists/Inventory.xlsx") or Inventory.check_if_empty():
            hide_btns(
                self, [self.btn_add_to_inventory, self.btn_save_list]
            )
            if not self.editted_saved:
                self.btn_save_list.show()
            self.is_sheet_open = "Saved_Lists/Inventory.xlsx"
            self.sub_header.setText('')
            self.header.setText('Looking at Inventory')
            fill_table(self, Inventory)
            self.comboBox_section.setCurrentIndex(0)
            show_sorting_btns(self)
            show_btns(self,
                      [self.header_frame, self.btn_edit_mode, self.btn_add_item_manually])
        else:
            # No inventory to open...
            header = 'There is no inventory file.'
            text = 'Create an inventory by reading in some orders!'
            title = 'No Inventory'
            self.no_files_msg(title=title, header=header, text=text)

    def open_new_order(self) -> None:
        '''
        Function to open a new order.
        '''
        self.btn_add_to_inventory.setEnabled(True)
        downloads_path = os.path.expanduser("~" + os.sep + "Downloads")
        filename, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self, 'EIP - Opening New Order', downloads_path, 'CSV Files (*.csv);; Excel Files (*.xlsx)')

        filetype = None
        if len(filename) > 1:
            print("Multiple Files")
        elif filename:
            filename = filename[0]
            filetype = filename.split('.')[-1]

            if filetype:

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
        project_window = Project_Window(self)
        project_window.open_project()
        self.project_windows.append(project_window)

    def show_sorted_section(self, section: str) -> None:
        '''
        Function to show the sorted sections

            Parameter:
                section - str: name of category to display.
        '''

        if section.lower() == 'all':
            refresh_opensheet(self, Items.data)

        else:
            items = Items.data[section].get_items()
            if 'looking at inventory' in self.header.text().lower():
                items = Inventory.data[section].get_items()

            if items.empty:
                self.table.setRowCount(0)
            fill_table(self, items)
            self.sub_header.setText(section)

    def save_list(self) -> None:
        '''
        Function to save a list.

        Parameters:
            called_from: where the function was called from
        '''
        self.editted_saved = True

        new_inventory = get_inventory()
        with pd.ExcelWriter(f'Saved_Lists/Inventory.xlsx') as writer:
            # Saves the new inventory as a spreadsheet, with each sheetname as the category name.
            for cat in new_inventory.keys():
                new_inventory[cat].save_toexcel(writer=writer)

        if self.new_orders_list:
            self.new_orders_list.clear()

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
        past_order_path = 'Saved_Lists/Past Orders'
        _, file = os.path.split(self.is_sheet_open)

        destination_full_path = os.path.join(past_order_path, file)

        # if order has already been added.
        if os.path.exists(destination_full_path):
            self.btn_add_to_inventory.setEnabled(False)

            popup_msg = QtWidgets.QMessageBox()
            popup_msg.setWindowTitle("EIP - Adding Order to Inventory")
            popup_msg.setText(
                f'Order "{file}" has already been added to the inventory.'
            )
            popup_msg.setIcon(QtWidgets.QMessageBox.Information)

            _ = popup_msg.exec_()

        else:  # if order has not been added.
            # copying order to past order folder.
            shutil.copy2(self.is_sheet_open, destination_full_path)

            # adding the order to the inventory
            order = get_ordersheet(destination_full_path)
            add_order_to_Inventory(order)
            self.new_orders_list.append(destination_full_path)
            self.editted_saved = False

            # Successfully added popup msg.
            popup_msg = QtWidgets.QMessageBox()
            popup_msg.setWindowTitle("EIP - Adding Order to Inventory")
            text = f'Order "{file}" was added to the inventory.\n Would you like to save?'
            popup_msg.setText(text)
            popup_msg.setIcon(QtWidgets.QMessageBox.Information)
            popup_msg.setStandardButtons(
                QtWidgets.QMessageBox.Yes |
                QtWidgets.QMessageBox.No
            )
            popup_msg.setDefaultButton(QtWidgets.QMessageBox.Yes)
            user = popup_msg.exec_()

            match user:
                case QtWidgets.QMessageBox.Yes:
                    self.save_list()
                case _:
                    pass

    def create_project(self) -> None:
        '''
        Function to create a new project using a second window.

            Prompts user to enter a project name, then checks if it exists.
            If the project name exists popup appears to tell the user, otherwise
            it asks the user what filetype they want and creates the project file.
        '''
        save_filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            'EIP - New Project Save Location',
            'Saved_Lists/Projects',
            'CSV (*.csv);; Excel (*.xlsx)'
        )

        if save_filename:
            base_path, filepath = os.path.split(save_filename)
            filename, ext = os.path.splitext(filepath)

            self.project_window.setWindowTitle(f"EIP - Project {filename}")
            text = f'New Project: {filename}{ext}'
            self.project_window.header.setText(text)
            self.project_window.load_Project(save_filename)
            self.project_window.show()

    def get_clicked_header(self, index):
        '''
        Function to get the header that was clicked on, then sort the table respectivitely.
        '''
        data = get_table_data(self)
        data = sort_by(self, index, data)
        fill_table(self, data)

    def add_to_project(self, row_index: int, action_index: int) -> None:
        '''
        Function to get the item from the table

            Parameter:
                index: index of item, starts at 0.
        '''
        project_windows = self.get_children_windows(
            instances=(Project_Window))[action_index]

        if project_windows:
            '''
            if project window is open, then send the clicked row to
            the project window.
            '''

            data = get_table_data(self)

            # getting the individual item and putting into a dataframe.
            item = pd.Series([cell for cell in data.iloc[row_index]])
            item = pd.DataFrame(item).T
            item.columns = data.keys()
            item['Quantity'] = 1  # need this for incrementing quantities.

            # passing item to project window.
            project_windows.add_to_project(item)

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
            self.btn_save_list.show()
            # updating project
            Inventory.update_item(item=item)

    def receive_add_item_manually(self, item) -> None:
        '''
        Function to read user's input when adding an item manually.
            Triggered when btn "Add to ..." clicked.
        '''

        items = sort_order(item)  # sorting item.
        add_order_to_Inventory(items)  # adding to inventory.
        fill_table(self, Inventory)  # updating table.

        self.editted_saved = False
        self.btn_save_list.setText('Save Inventory')
        self.btn_save_list.show()

    def get_children_windows(self, instances=(Project_Window,
                                              SearchWindow, Add_Item_Window,
                                              How_To_Use_Program_Window,
                                              Program_Info_Window)):
        '''
        Function to get custom windows object if there any.

            Parameters:
                instances: tuple of window classes to look for.

            Returns: 
                list of window objects.
        '''

        children = []
        for child in self.children():
            if isinstance(child, instances):
                children.append(child)

        return children


if __name__ == "__main__":
    # runnning program
    load_Inventory()
    app = QApplication(sys.argv)
    window1 = MainWindow()
    app.exec_()
