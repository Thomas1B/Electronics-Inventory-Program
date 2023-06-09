'''
Script to run the project_window.ui

Creates a second window to allow the user to create/edit a project
'''

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtWidgets
from PyQt5.QtGui import QDesktopServices, QIcon
from PyQt5.QtCore import QUrl
from PyQt5 import uic
import sys
import os
import pandas as pd
import shutil


from .data_handling import (
    dict_keys,
    labels,
    Category,
    sort_order,
    get_ordersheet,
    dict_to_dataframe,
    sort_order,
    get_subtotal,
    update_item,
    Inventory,
    Project,
    Items,
    sort_by
)

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
    update_subtotal,
    get_table_data,
    change_item_quantity,
    open_add_manually_window,
    get_editted_item,
    copySelectedCell,
)

from .info_windows import How_To_Use_Project_Window
from .add_item_window import Add_Item_Window


class Project_Window(QMainWindow):
    '''
    Class to run the project window
    '''

    def __init__(self, parent=None) -> None:
        super(Project_Window, self).__init__(parent)
        uic.loadUi('Program_Files/UI_Files/project_window.ui', self)
        self.move(1050, 50)

        ''' Finding/Declaring variables and Widgets '''

        # Other windows used
        self.how_to_use_window = How_To_Use_Project_Window()
        self.add_item_window = Add_Item_Window()

        # vairable to keep track of States:
        self.project_loaded = False  # if project has been loaded.
        self.is_sheet_open = False  # what sheet is opened.
        self.editted_saved = True  # if project has been saved
        self.in_edit_mode = False  # if in edit mode.
        self.sort_by = {key: True for key in labels}

        # display labels
        self.header = self.findChild(QtWidgets.QLabel, 'header')
        self.sub_header = self.findChild(QtWidgets.QLabel, 'sub_header')
        self.subtotal = self.findChild(QtWidgets.QLabel, 'subtotal')

        # Table
        self.table = self.findChild(QtWidgets.QTableWidget, 'table')

        # Menu Actions
        self.action_how_to_use = self.findChild(
            QtWidgets.QAction, 'actionHow_to_use_Project_tool'
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

        # ToolBar
        self.toolbar = self.findChild(QtWidgets.QToolBar, 'toolBar')
        self.actionExport_Project = self.findChild(
            QtWidgets.QAction, 'actionExport_Project'
        )
        self.actionOpen_Project = self.findChild(
            QtWidgets.QAction, 'actionOpen_Project'
        )
        self.actionCreate_Project = self.findChild(
            QtWidgets.QAction, 'actionCreate_Project'
        )

        # Command Buttons
        self.btn_save_list = self.findChild(
            QtWidgets.QPushButton, 'btn_save_project'
        )
        self.btn_edit_mode = self.findChild(
            QtWidgets.QPushButton, 'btn_edit_mode'
        )
        self.btn_add_item = self.findChild(
            QtWidgets.QPushButton, 'btn_add_item_manually'
        )

        # Sorting buttons
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
            QtWidgets.QPushButton, 'btn_inductors'
        )
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

        ''' Attaching Functions to gui Objects '''

        # Table
        self.table.itemChanged.connect(
            lambda: update_subtotal(self, Project)
        )
        self.table.horizontalHeader().sectionClicked.connect(self.get_clicked_header)

        # Menu Actions
        self.action_how_to_use.triggered.connect(self.show_how_to_use)
        self.action_open_Digikey.triggered.connect(
            lambda: self.open_website('Digikey')
        )
        self.action_open_adafruit.triggered.connect(
            lambda: self.open_website('Adafruit')
        )
        self.action_open_BCrobotics.triggered.connect(
            lambda: self.open_website('BC Robotics')
        )

        # ToolBar
        self.actionExport_Project.triggered.connect(
            lambda: self.export_project(autoname=True)
        )
        self.actionOpen_Project.triggered.connect(self.open_project)
        self.actionCreate_Project.triggered.connect(self.create_project)

        # Command Buttons
        self.btn_save_list.clicked.connect(self.save_project)
        self.btn_edit_mode.clicked.connect(self.edit_mode)
        self.btn_add_item.clicked.connect(
            lambda: open_add_manually_window(self)
        )

        # Sorting Buttons
        self.btn_refresh_opensheet.clicked.connect(
            lambda: refresh_opensheet(self, Project)
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
            lambda: self.show_sorted_section('Diodes'))
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
            lambda: self.show_sorted_section("Audio")
        )
        self.btn_modules.clicked.connect(
            lambda: self.show_sorted_section('Modules')
        )
        self.btn_other.clicked.connect(
            lambda: self.show_sorted_section('Other')
        )

    def closeEvent(self, event) -> None:
        '''
        Function to detect when user closes the window.

            Parameters:
                event: QtGui.QCloseEvent.
        '''

        if self.editted_saved:  # if editted project has been saved already.
            event.accept()  # let the window close.
        else:  # popup to warning user editted project has not been saved.
            title = "Electronics Inventory Program - Saving Project"
            text = 'Project has been editted!\n\nWould you like to save?'
            event.ignore()  # dont let window close.

            user = QtWidgets.QMessageBox()
            user.setWindowTitle(title)
            pixmapi = getattr(QtWidgets.QStyle, "SP_MessageBoxWarning")
            icon = self.style().standardIcon(pixmapi)
            user.setWindowIcon(icon)
            user.setIcon(QtWidgets.QMessageBox.Warning)
            user.setText(text)
            user.setStandardButtons(
                QtWidgets.QMessageBox.Yes |
                QtWidgets.QMessageBox.No |
                QtWidgets.QMessageBox.Cancel
            )
            user.setDefaultButton(QtWidgets.QMessageBox.Yes)
            user = user.exec_()

            match user:  # checking user's response:
                case QtWidgets.QMessageBox.Yes:
                    # user accepts to save.
                    self.save_project()
                    event.accept()
                case QtWidgets.QMessageBox.No:
                    # user declines to save.
                    self.editted_saved = True
                    event.accept()
                case _:
                    # user cancels selection.
                    event.ignore()

    def contextMenuEvent(self, event) -> None:
        '''
        Function to show a menu when right clicked on item in the table.

            Parameters:
                event: QtGui.QCloseEvent.
        '''

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
                    Project,
                    row_index,
                    remove_all=None
                )
            )
            delete_action.triggered.connect(
                lambda: change_item_quantity(
                    self,
                    Project,
                    row_index,
                    remove_all=False
                )
            )
            delete_item_action.triggered.connect(
                lambda: change_item_quantity(
                    self,
                    Project,
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

    def show_how_to_use(self) -> None:
        '''
        Function to show the "how to use" window.
        '''
        self.how_to_use_window.show()

    def open_website(self, website: str) -> None:
        '''
        Function to open a website link on the user's default bowser.

            Parameters:
                website - str: website's name (used for conditions).
        '''
        match website.lower():
            case 'digikey':
                website = 'https://www.digikey.ca/'
            case 'adafruit':
                website = 'https://www.adafruit.com/'
            case 'bc robotics':
                website = 'https://bc-robotics.com/'

        QDesktopServices.openUrl(QUrl(website))

    def export_project(self, autoname=True) -> None:
        '''
        Function to export a Project.

            Parameters:
                autoname - bool: true - automatically named the final.
        '''
        if autoname:
            file_toexport, _ = QtWidgets.QFileDialog.getOpenFileName(
                self,
                "Electronics Inventory Program - Exporting Project",
                "Saved_Lists/Projects",
                "All Files (*);; CSV Files (*.csv) ;; XLSX Files (*.xlsx)"
            )

            if file_toexport:
                export_filename, export_filetype = file_toexport.split(
                    '/')[-1].split('.')

                destination_folder = os.path.expanduser(
                    "~" + os.sep + "Downloads\exported_electronics_lists"
                )
                # if the destination folder doesn't exists, make it.
                if not os.path.exists(destination_folder):
                    os.mkdir(destination_folder)
                    destination_folder += '/projects'
                    os.mkdir(destination_folder)
                # if the subfolder doesn't exsits, make it.
                elif not os.path.exists(destination_folder + '/projects'):
                    destination_folder += '/projects'
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
                text = f'Project exported to "exported_electronics_lists/Project" in your downloads.'
                msg.setInformativeText(text)
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                _ = msg.exec_()

            else:
                pass

    def no_files_msg(self, title='No Files', header="", text=""):
        '''
        Function to display a pop up warning user there are no files to open

            Parameters:
                title - str: Window title.
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

    def create_project(self) -> None:
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
                    # if project doesn't exist, create it
                    self.setWindowTitle(title)
                    text = f'New Project: {name}.{filetype}'
                    self.header.setText(text)
                    self.load_Project(filepath)
                    self.show()
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

    def open_project(self) -> None:
        '''
        Function to open a project
        '''
        if len(os.listdir("Saved_Lists/Projects")) > 0:
            filename, _ = QtWidgets.QFileDialog.getOpenFileName(
                self,
                'Electronics Inventory Program - Opening Project',
                'Saved_Lists/Projects',
                'All Files (*) ;; CSV Files (*.csv);; Excel Files (*.xlsx)'
            )
            filetype = filename.split('.')[-1]
            if filename:
                if filetype in ['csv', 'xlsx']:
                    order_name = filename.split('/')[-1]
                    self.header.setText(
                        f'Project: {order_name}'
                    )
                    self.load_Project(filename)
                    self.show()
                else:
                    wrong_filetype_msg(self)
            else:
                pass
        else:
            title = 'No Projects'
            header = 'There are no projects to open!'
            self.no_files_msg(title=title, header=header)

    def load_Project(self, filename=None) -> None:
        '''
        Function to load the project into the Project dictionary of classes.

        Skips empty classes.
        '''

        # deleting items from the Project dictionary so items don't append.
        for section in Project.keys():
            Project[section].drop_all_items()

        if not os.path.exists(filename):
            self.editted_saved = False

        project = get_ordersheet(filename)
        self.is_sheet_open = filename
        if project:
            for section, cat in zip(project, Project.keys()):
                if not section.empty:
                    Project[cat].add_item(section)
            self.project_loaded = True
        fill_table(self, Project)

    def add_to_project_dict(self, items) -> None:
        '''
        Function to add items to the project dictionary

        Parameter:
            items - list: list of SORTED Category classes, can also take unsorted dataframe.
        '''
        if type(items) == pd.DataFrame:
            items = sort_order(items)

        for item, section in zip(items, Project.keys()):
            if len(item) > 0:  # if the list
                Project[section].add_item(item)
                Project[section].remove_duplicates()
                self.editted_saved = False

    def show_sorted_section(self, section: str) -> None:
        '''
        Function to show the sorted sections

            Parameter:
                section: name of category to display.
        '''
        items = Project[section].get_items()
        if items.empty:
            self.table.setRowCount(0)
        self.sub_header.setText(section)
        fill_table(self, items)

    def save_project(self) -> None:
        '''
        Function to save the project.
        '''

        if self.editted_saved == 'error':
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle('Project Error')
            pixmapi = getattr(QtWidgets.QStyle, "SP_MessageBoxCritical")
            icon = self.style().standardIcon(pixmapi)
            msg.setWindowIcon(icon)
            msg.setIcon(QtWidgets.QMessageBox.Critical)

            msg.setText(
                'There are letters in the "Unit Price" or "Quantity" columns.')
            text = 'Project cannot be saved until this is fixed.'
            msg.setInformativeText(text)
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            _ = msg.exec_()
            return

        filetype = self.is_sheet_open.split('.')[-1]
        if filetype == 'csv':
            data = dict_to_dataframe(Project)
            data.to_csv(self.is_sheet_open, index=False)
        elif filetype == 'xlsx':
            with pd.ExcelWriter(self.is_sheet_open) as writer:
                # Saves the new inventory as a spreadsheet, with each sheetname as the category name.
                for cat in Project.keys():
                    Project[cat].save_toexcel(writer=writer, index=True)
        self.editted_saved = True

        # showing pop up msg
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle('File Save Successful')
        pixmapi = getattr(QtWidgets.QStyle, "SP_DialogApplyButton")
        icon = self.style().standardIcon(pixmapi)
        msg.setWindowIcon(icon)
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText('Saving Project was successful!')
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        _ = msg.exec_()

    def edit_mode(self) -> None:
        '''
        Function to update the Project inventory when the table is in edit mode.
        '''

        # buttons to toggle during edit mode.
        btns = [self.actionOpen_Project,
                self.actionCreate_Project,
                self.actionExport_Project,
                self.btn_add_item
                ]

        if not self.in_edit_mode:
            self.in_edit_mode = True
            self.btn_edit_mode.setText('Exit Edit Mode')
            project_name = self.header.text().split(':')[-1].strip()
            text = f'Editting project: {project_name}'
            self.header.setText(text)
            self.header.setStyleSheet('color: red;')
            self.table.setEditTriggers(QtWidgets.QTableWidget.DoubleClicked)
            self.table.itemChanged.connect(self.get_editted)
            toggled_widgets(self, enable=False, widgets=btns)
        else:
            self.in_edit_mode = False
            self.btn_edit_mode.setText('Edit Mode')
            project_name = self.header.text().split(':')[-1].strip()
            text = f'Project: {project_name}'
            self.header.setText(text)
            self.header.setStyleSheet('color: black;')
            self.table.itemChanged.disconnect(self.get_editted)
            self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            self.table.itemChanged.connect(
                lambda: update_subtotal(self, Project)
            )
            toggled_widgets(self, enable=True, widgets=btns)

    # going to move this to gui_handling
    def get_editted(self, clicked_item: QtWidgets.QTableWidgetItem) -> None:
        '''
        Function to get the item that has been editted.

        Triggered by itemChanged in table.

            Parameter:
                clicked_item: item that was clicked one
        '''

        item = get_editted_item(self, clicked_item)
        if item.shape[0] < 1:
            return
        else:
            # updating project
            self.editted_saved = False
            update_item(self, item, Project)
            update_subtotal(self, Project)

    def add_to_project(self, item: pd.DataFrame) -> None:
        '''
        Function to receive item from the other window.
            Triggered when btn "Add External Item" is clicked.

            Parameter:
                item: item DataFrame.
        '''
        item = sort_order(item)  # sorting item.
        self.add_to_project_dict(item)  # adding to project.
        fill_table(self, Project)  # updating table.

    def receive_add_item_manually(self, item) -> None:
        '''
        Function to read user's input when adding an item manually.
            Triggered when btn "Add to ..." clicked.
        '''

        item = sort_order(item)  # sorting item.
        self.add_to_project(item)  # adding to project.
        fill_table(self, Project)  # updating table.

        self.editted_saved = False

    def get_clicked_header(self, index):
        '''
        Function to get the header that was clicked on, then sort the table respectivitely.
        '''

        data = get_table_data(self)
        data = sort_by(self, index, data)
        fill_table(self, data)


if __name__ == "__main__":
    # runnning program
    app = QApplication(sys.argv)
    project_window = Project_Window()
    project_window.show()
    app.exec_()
