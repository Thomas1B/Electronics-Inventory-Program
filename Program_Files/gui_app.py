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

from .info_windows import Program_Info_Window, Help_Window
from .add_item_window import Add_Item_Window
from .project_window import Project_Window
from .search_window import SearchWindow, open_search_window
from .new_order_window import Order_Window

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


from .styles import (
    style_central_widget,
    style_table,
    style_sorting_comboBox,
    style_refresh_btn,
    style_toolbar,
    style_menubar
)


class MainWindow(QMainWindow):
    '''
    Class to run the main window of the program.
    '''

    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        uic.loadUi('Program_Files/UI_Files/gui_app.ui', self)
        self.setWindowIcon(QIcon('Program_files/Icons/circuit.png'))
        style_central_widget(self)
        self.showMaximized()

        self.Items = Data(dict_keys)

        # Other Windows used in the program.
        self.order_window = None
        self.add_item_window = Add_Item_Window(self)
        self.window_program_info = Program_Info_Window(self)
        self.help_page = Help_Window(self)

        # variable to keep track of States:
        self.is_sheet_open = False  # what sheet is opened.
        self.editted_saved = True  # if inventory has been saved.
        self.in_edit_mode = False  # if in edit mode.
        # used keep track of acsending/decending when sorting.
        self.sort_by = {key: True for key in labels}
        # keeping track of dynamically created project windows.
        self.project_windows = []

        ''' Defining Widgets'''

        # Menu Bar
        self.action_open_program_info = self.findChild(
            QtWidgets.QAction, 'actionProgram_Info'
        )
        self.actionHelp = self.findChild(
            QtWidgets.QAction, 'actionHelp'
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
        self.action_open_order_window = self.findChild(
            QtWidgets.QAction, 'actionOpen_Order_Window')
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
        self.actionHelp.triggered.connect(self.show_help_page)
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
        self.action_open_order_window.triggered.connect(
            self.open_blank_new_order_window)
        self.action_open_new_order.triggered.connect(self.open_new_orders)
        self.action_open_projects.triggered.connect(self.open_project_lists)
        self.action_create_project.triggered.connect(self.create_project)
        self.action_open_past_orders.triggered.connect(self.open_past_orders)
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
        self.btn_edit_mode.clicked.connect(self.edit_mode)
        self.btn_add_item_manually.clicked.connect(
            lambda: open_add_manually_window(self)
        )

        # Sorting Buttons
        self.btn_refresh_opensheet.clicked.connect(
            lambda: refresh_opensheet(self, self.Items)
        )
        self.comboBox_section.currentIndexChanged.connect(
            lambda: self.show_sorted_section(
                self.comboBox_section.currentText())
        )

        # calling styling functions
        style_refresh_btn(self)
        style_table(self)
        style_toolbar(self)
        style_menubar(self)

        # adding category to sorting comboBox and styling
        style_sorting_comboBox(self)
        for key in sorted(dict_keys):
            self.comboBox_section.addItem(key)

        # Hidiing some buttons for initial start.
        hide_btns(self, [
            self.btn_save_list,
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
                    if self.order_window:
                        for file in self.order_window.new_orders_added:
                            file = file.split('/')[-1]
                            os.remove(f'Saved_Lists/Past Orders/{file}')
                        self.order_window.new_orders_added.clear()
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
                    "Copy Highlighted"
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
                for widget in self.project_windows:
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

    def show_help_page(self) -> None:
        '''
        Function to show the "how to use" window for the user.
        '''
        self.help_page.show()

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

        imported = None  # dummy var

        # filepath where to when opening a filedialog.
        downloads_folder = os.path.expanduser("~/Downloads")

        match kind:  # match case for if a file or directory is being exported

            case 'file':  # file is being exported.

                # getting the selected files to import
                imported, _ = QtWidgets.QFileDialog.getOpenFileNames(
                    self,
                    "EIP - Importing File(s)",
                    downloads_folder,
                    'All Files (*);;CSV Files (*.csv);;Excel Files (*.xlsx)'
                )

                if imported:  # if user selects files:

                    # getting the destination for importing.
                    destination_folder = QtWidgets.QFileDialog.getExistingDirectory(
                        self,
                        "EIP - Selecting Desination",
                        'Saved_Lists'
                    )

                    if destination_folder:  # if a destination was selected:

                        # looping through each file to check conditions, then import
                        for import_file in imported:
                            filename = os.path.basename(import_file)
                            destination_path = os.path.join(
                                destination_folder, filename)

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

                                # checking user's response
                                match user:
                                    case QtWidgets.QMessageBox.Yes:
                                        break
                                    case QtWidgets.QMessageBox.No:
                                        base_path, extension = os.path.splitext(
                                            destination_path)
                                        count = 1
                                        while os.path.exists(destination_path):
                                            destination_path = f'{base_path} ({count}){extension}'
                                            count += 1

                            shutil.copy2(import_file, destination_path)

            case 'dir':  # directory is being exported.

                # getting the selected directory.
                imported = QtWidgets.QFileDialog.getExistingDirectory(
                    self,
                    "EIP - Importing",
                    downloads_folder
                )

                if imported:  # if user selects a directory:

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

                            # checking user's response
                            match user:
                                case QtWidgets.QMessageBox.Yes:
                                    # user wants to overwrite the directory
                                    shutil.rmtree(destination)
                                    shutil.copytree(imported, destination)

                                case QtWidgets.QMessageBox.No:
                                    # user does not want to overwrite.
                                    # modifies file name.
                                    count = 1
                                    while True:
                                        try:
                                            shutil.copytree(
                                                imported, destination)
                                            break
                                        except FileExistsError:
                                            destination = destination.split(
                                                ' (')[0]
                                            destination += f' ({count})'
                                            count += 1

    def exporting(self, kind: str) -> None:
        '''
        Function to export file(s) and Folders.

        Parameter:
            kind: "file"/"dir", importing "file" or "directory".
        '''

        destination_folder = os.path.expanduser(
            f"~{os.sep}Downloads{os.path.sep}EIP Exported Files"
        )

        # try to block make export location in the downloads folder of the computer.
        try:
            os.mkdir(destination_folder)
        except FileExistsError as err:
            # location already exists.
            pass

        match kind:  # match case for if a file or directory is being exported

            case 'file':  # file is being exported.

                # getting filenames to export
                files_to_export, _ = QtWidgets.QFileDialog.getOpenFileNames(
                    self,
                    "EIP - Exporting",
                    "Saved_Lists",
                    "All Files (*);; CSV Files (*.csv) ;; XLSX Files (*.xlsx)"
                )

                if files_to_export:  # check if user selects files.

                    # loop through each file to check conditions, then export.
                    for file in files_to_export:
                        filename = os.path.basename(file)
                        destination_path = os.path.join(
                            destination_folder, filename)

                        # checking if file has already been exported, if so modify file name then export.
                        base, ext = os.path.splitext(destination_path)
                        count = 1
                        while os.path.exists(destination_path):
                            destination_path = f'{base} ({count}){ext}'
                            count += 1
                        shutil.copy2(file, destination_path)

            case 'dir':  # folder is being exported.

                # getting the directory to export
                exporting = QtWidgets.QFileDialog.getExistingDirectory(
                    self,
                    "EIP - Exporting",
                    'Saved_Lists'
                )

                if exporting:  # check if user selects a directory

                    # getting the filename from the entire path, then making the destination path
                    _, filename = os.path.split(exporting)
                    destination_path = os.path.join(destination_folder,
                                                    filename)

                    # checking if the file has already been exported, if so modify the filename then export.
                    base, ext = os.path.splitext(destination_path)
                    count = 1
                    while os.path.exists(destination_path):
                        destination_path = f'{base} ({count}){ext}'
                        count += 1
                    shutil.copytree(exporting, destination_path)

    def open_inventory(self) -> None:
        '''
        Function to open the inventory
        '''
        if os.path.exists("Saved_Lists/Inventory.xlsx") or Inventory.check_if_empty():
            hide_btns(
                self, [self.btn_save_list]
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

    def open_blank_new_order_window(self) -> None:
        '''
        Function to open a blank new order window.

        Opens seperate window.
        '''
        self.order_window = Order_Window(self)
        self.order_window.show()

    def open_new_orders(self) -> None:
        '''
        Function to open a new order.

        Opens seperate window.
        '''
        self.order_window = Order_Window(self)
        self.order_window.show()
        self.order_window.open_order()

    def open_past_orders(self) -> None:
        '''
        Function to open a past order.

        Opens seperate window.
        '''
        self.order_window = Order_Window(self)
        self.order_window.show()
        self.order_window.open_past_order()

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
            refresh_opensheet(self, self.Items.get_data())

        else:
            items = self.Items.data[section].get_items()
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

        if self.order_window:
            if self.order_window.new_orders_added:
                self.order_window.new_orders_added.clear()

        self.btn_save_list.hide()

    def add_to_inventory(self, filename: str) -> None:
        '''
        Function to add an order to inventory.
            - Triggered by add_to_inventory button.

            Parameters:
                filename: filename to order
        '''

        # checking if order has been added already.
        past_order_path = 'Saved_Lists/Past Orders'
        _, file = os.path.split(filename)

        destination_full_path = os.path.join(past_order_path, file)

        # if order has already been added.
        if os.path.exists(destination_full_path):

            popup_msg = QtWidgets.QMessageBox()
            popup_msg.setWindowTitle("EIP - Adding Order to Inventory")
            popup_msg.setText(
                f'Order "{file}" has already been added to the inventory.'
            )
            popup_msg.setIcon(QtWidgets.QMessageBox.Information)

            _ = popup_msg.exec_()

        else:  # if order has not been added.
            # copying order to past order folder.
            shutil.copy2(filename, destination_full_path)

            # adding the order to the inventory
            order = get_ordersheet(destination_full_path)
            add_order_to_Inventory(order)
            self.editted_saved = False

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

            project_window = Project_Window(self)
            project_window.setWindowTitle(f"EIP - Project {filename}")
            project_window.header.setText(f'Project: {filename}.{ext}')
            project_window.load_Project(save_filename)
            project_window.show()
            self.project_windows.append(project_window)

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
        project_windows = self.project_windows[action_index]

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
                                              Help_Window,
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
