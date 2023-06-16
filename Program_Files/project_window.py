'''
Script to run the project_window.ui

Creates a second window to allow the user to create/edit a project
'''

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtWidgets
from PyQt5 import uic
import sys
import os
import pandas as pd


from .data_handling import (
    Category,
    sort_order,
    get_ordersheet,
    dict_to_dataframe,
    sort_order
)

Project = {
    'Resistors': Category("Resistors"),
    'Capacitors': Category("Capacitors"),
    'Inductors': Category("Inductors"),
    'Transistors': Category("Transistors"),
    'Diodes': Category('Diodes'),
    "ICs": Category('ICs'),
    "Connectors": Category('Connectors'),
    'Displays': Category('Displays'),
    "Buttons": Category('Buttons'),
    'LEDs': Category('LEDs'),
    'Modules': Category('Modules'),
    'Other': Category("Other"),
}


class Project_Window(QMainWindow):
    def __init__(self, parent=None):
        super(Project_Window, self).__init__(parent)
        # loading ui file
        uic.loadUi('Program_Files/project_window.ui', self)
        self.resize(1000, 800)
        self.move(1200, 300)

        # variable to see if project has been loaded.
        self.project_loaded = False

        # variable to keep track of what sheet is opened.
        self.is_sheet_open = False

        # variable to keep track if the sheet was been editted.
        self.editted_saved = True  # used for saving

        self.header = self.findChild(QtWidgets.QLabel, 'header')
        self.sub_header = self.findChild(QtWidgets.QLabel, 'sub_header')
        self.table = self.findChild(QtWidgets.QTableWidget, 'table')
        self.subtotal = self.findChild(QtWidgets.QLabel, 'subtotal')

        self.btn_save_project = self.findChild(
            QtWidgets.QPushButton, 'btn_save_project')

        self.btn_open_project = self.findChild(
            QtWidgets.QPushButton, 'btn_open_project')

        self.btn_create_project = self.findChild(
            QtWidgets.QPushButton, 'btn_create_project')

        # self.btn_open_project.hide()

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

        self.btn_save_project.clicked.connect(self.save_project)
        self.btn_open_project.clicked.connect(self.open_project)
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

    def wrong_filetype_msg(self):
        '''
        Function to display a pop telling user they selected a wrong filetype.
        '''
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

    def open_project(self):
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
                    self.wrong_filetype_msg()
            else:
                pass
        else:
            title = 'No Projects'
            header = 'There are no projects to open!'
            self.no_files_msg(title=title, header=header)

    def refresh_opensheet(self, filename=None):
        '''
        Function to refresh the last sheet that was opened.
            used for when a user is looking a specific category.

        '''
        self.fill_table(Project)
        self.sub_header.setText('')

    def load_Project(self, filename=None):
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
        self.fill_table(Project)

        Project['Resistors'].get_subtotal()

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

    def show_sorted_section(self, section):
        '''
        Function to show the sorted sections

        Parameter:
            section - str: name of category to display.
        '''
        self.fill_table(Project[section].get_items())
        self.sub_header.setText(section)

    def save_project(self):
        '''
        Function to save the project.
        '''
        filetype = self.is_sheet_open.split('.')[-1]
        if filetype == 'csv':
            data = dict_to_dataframe(Project)
            data.to_csv(self.is_sheet_open)
        elif filetype == 'xlsx':
            with pd.ExcelWriter(self.is_sheet_open) as writer:
                # Saves the new inventory as a spreadsheet, with each sheetname as the category name.
                for cat in Project.keys():
                    Project[cat].save_toexcel(writer=writer)
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

    def item_from_main_window(self, items):
        '''
        Function to get items from the Main UI Window.
        '''
        items = sort_order(items)
        for item, section in zip(items, Project.keys()):
            if len(item) > 0:
                Project[section].add_item(item)
                Project[section].remove_duplicates()
        self.editted_saved = False
        self.fill_table(Project)

    def closeEvent(self, event):
        '''
        Function to detect when user closes the window.
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
                    event.accept()
                case _:
                    # user cancels selection.
                    event.ignore()


if __name__ == "__main__":
    # runnning program
    app = QApplication(sys.argv)
    project_window = Project_Window()
    project_window.show()
    app.exec_()
