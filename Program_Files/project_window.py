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


from .data_handling import (
    dict_keys,
    labels,
    sort_order,
    get_ordersheet,
    sort_order,
    sort_by,
    Data
)

from .gui_handling import (
    wrong_filetype_msg,
    toggled_widgets,
    refresh_opensheet,
    fill_table,
    update_subtotal,
    get_table_data,
    change_item_qty,
    open_add_manually_window,
    get_editted_item,
    copySelectedCell,
    web_search_item
)

from .styles import (
    style_central_widget,
    style_table,
    style_sorting_comboBox,
    style_refresh_btn,
    style_menubar,
    style_toolbar
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
        style_central_widget(self)
        self.resize(900, 600)
        self.move(900, 50)

        # Items dictonary of categories
        # self.Project = {key: Category(key) for key in dict_keys}
        self.Project = Data(dict_keys)

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
        self.btn_refresh_opensheet = self.findChild(
            QtWidgets.QPushButton, 'btn_refresh_opensheet'
        )
        self.sorting_btns_frame = self.findChild(QtWidgets.QFrame, 'frame')
        self.comboBox_section = self.findChild(
            QtWidgets.QComboBox, 'comboBox_section'
        )

        # adding category to sorting comboBox

        for key in sorted(dict_keys):
            self.comboBox_section.addItem(key)
        ''' Attaching Functions to gui Objects '''

        # Table
        self.table.itemChanged.connect(
            lambda: update_subtotal(self, self.Project)
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
            lambda: refresh_opensheet(self, self.Project)
        )
        self.comboBox_section.currentIndexChanged.connect(
            lambda: self.show_sorted_section(
                self.comboBox_section.currentText())
        )

        # calling styling functions
        style_refresh_btn(self)
        style_sorting_comboBox(self)
        style_table(self)
        style_toolbar(self)
        style_menubar(self)

        # labels in header frame.
        for label in [self.header, self.sub_header]:
            label.setStyleSheet(
                '''
                QLabel {
                    font-size: 22px;
                    font-weight: bold;
                }
                '''
            )

    def closeEvent(self, event) -> None:
        '''
        Function to detect when user closes the window.

            Parameters:
                event: QtGui.QCloseEvent.
        '''

        if self.editted_saved:  # if editted project has been saved already.
            if self in self.parent().project_windows:
                index = self.parent().project_windows.index(self)
                del self.parent().project_windows[index]
            event.accept()  # let the window close.
        # popup to warning user editted project has not been saved.
        elif not self.editted_saved and self.table.rowCount() > 0:
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
                    if self in self.parent().project_windows:
                        self.parent().project_windows.remove(self)
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
                    self.Project.data,
                    row_index,
                    remove_all=None
                )
            )
            remove_one_action.triggered.connect(
                lambda: change_item_qty(
                    self,
                    self.Project.data,
                    row_index,
                    remove_all=False
                )
            )
            delete_item_action.triggered.connect(
                lambda: change_item_qty(
                    self,
                    self.Project.data,
                    row_index,
                    remove_all=True
                )
            )

            # Adding to actions to menu
            menu.addAction(web_search_action)
            menu.addSeparator()
            menu.addAction(copy_selected_action)
            menu.addAction(add_one_action)
            menu.addAction(remove_one_action)
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
            self.parent().project_windows.append(project_window)

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
                    self.show()  # needs to be before load_project to apply table styles
                    self.load_Project(filename)
                else:
                    wrong_filetype_msg(self)
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
        for section in self.Project.sections:
            self.Project.data[section].drop_all_items()

        if not os.path.exists(filename):
            self.editted_saved = False

        project = get_ordersheet(filename)
        self.is_sheet_open = filename
        if project:
            for section, cat in zip(project, self.Project.sections):
                if not section.empty:
                    self.Project.data[cat].add_item(section)
            self.project_loaded = True
        fill_table(self, self.Project)

    def add_to_project_dict(self, items) -> None:
        '''
        Function to add items to the project dictionary

        Parameter:
            items - list: list of SORTED Category classes, can also take unsorted dataframe.
        '''
        if type(items) == pd.DataFrame:
            items = sort_order(items)

        for item, section in zip(items, self.Project.sections):
            if len(item) > 0:
                self.Project.add_item(item, section)
                self.Project.remove_duplicates(section)
        self.editted_saved = False

    def show_sorted_section(self, section: str) -> None:
        '''
        Function to show the sorted sections

            Parameter:
                section: name of category to display.
        '''
        if section.lower() == 'all':
            refresh_opensheet(self, self.Project)
        else:
            items = self.Project.data[section].get_items()
            if items.empty:
                self.table.setRowCount(0)
            self.sub_header.setText(section)
            fill_table(self, items)

    def save_project(self) -> None:
        '''
        Function to save the project.
        '''

        if self.table.rowCount() > 0:
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
                data = self.Project.to_dataframe()
                data.to_csv(self.is_sheet_open, index=False)
            elif filetype == 'xlsx':
                with pd.ExcelWriter(self.is_sheet_open) as writer:
                    # Saves the new inventory as a spreadsheet, with each sheetname as the category name.
                    for cat in self.Project.sections:
                        self.Project.data[cat].save_toexcel(
                            writer=writer, index=True)
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
        else:
            # Pop up telling user project is
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle('Blank Project')
            pixmapi = getattr(QtWidgets.QStyle, "SP_MessageBoxCritical")
            icon = self.style().standardIcon(pixmapi)
            msg.setWindowIcon(icon)
            msg.setIcon(QtWidgets.QMessageBox.Critical)

            msg.setText("Project is blank!")
            text = 'Blank projects cannot be saved.'
            msg.setInformativeText(text)
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
                lambda: update_subtotal(self, self.Project.data)
            )
            toggled_widgets(self, enable=True, widgets=btns)

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
            self.Project.update_item(item=item)
            update_subtotal(self, self.Project.data)

    def add_to_project(self, item: pd.DataFrame) -> None:
        '''
        Function to receive item from the other window.
            Triggered when btn "Add External Item" is clicked.

            Parameter:
                item: item DataFrame.
        '''
        item = sort_order(item)  # sorting item.
        self.add_to_project_dict(item)  # adding to project.
        fill_table(self, self.Project.data)  # updating table.
        self.editted_saved = False

    def receive_add_item_manually(self, item) -> None:
        '''
        Function to read user's input when adding an item manually.
            Triggered when btn "Add to ..." clicked.
        '''
        self.add_to_project(item)  # adding to project.
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
