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
    dict_to_dataframe
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

        self.is_sheet_open = False

        self.btn_save_project = self.findChild(
            QtWidgets.QPushButton, 'btn_save_project')
        
        self.btn_open_project = self.findChild(
            QtWidgets.QPushButton, 'btn_open_project')
        
        self.btn_open_project.hide()


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

    def load_Project(self, filename=None):
        '''
        Function to load the project into the Project dictionary of classes.
        '''
        project = get_ordersheet(filename)
        self.is_sheet_open = filename
        if project:
            for section, cat in zip(project, Project.keys()):
                if not section.empty:
                    Project[cat].add_item(section)
            self.fill_table(Project)

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

        if 'looking at inventory' in self.header.text().lower():
            self.fill_table(Project[section].get_items())
        else:
            data = get_ordersheet(self.is_sheet_open)
            sorted = {}
            keys = Project.keys()
            for i, key in enumerate(keys):
                sorted[key] = data[i]
            self.fill_table(sorted[section].reset_index(drop=True))
        self.sub_header.setText(section)

    def save_project(self):
        '''
        Function to save the project.
        '''
        user = QtWidgets.QMessageBox()
        user.setWindowTitle("Electronics Inventory Program - Saving Project")
        user.setIcon(QtWidgets.QMessageBox.Question)
        user.setText('\nWould you like to save the project?\n')
        user.setStandardButtons(
            QtWidgets.QMessageBox.Yes |
            QtWidgets.QMessageBox.No
        )
        user.setDefaultButton(QtWidgets.QMessageBox.Yes)
        user = user.exec_()
        if user == QtWidgets.QMessageBox.Yes:
            print('dog')



if __name__ == "__main__":
    # runnning program
    app = QApplication(sys.argv)
    project_window = Project_Window()
    project_window.show()
    app.exec_()
