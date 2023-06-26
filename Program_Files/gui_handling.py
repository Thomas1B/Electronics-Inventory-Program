'''
Script to run shared functions in PyQt Windows.

All of the functions require a self parameter.
'''

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices, QIcon
import pandas as pd
import sys
import os
import shutil

from .data_handling import (
    dict_to_dataframe,
    get_subtotal
)


def show_btns(self, buttons: list) -> None:
    '''
    Function to show buttons

        Parameter:
            buttons: list of buttons
    '''
    for btn in buttons:
        btn.show()


def hide_btns(self, buttons: list) -> None:
    '''
    Function to hide buttons

        Parameter:
            buttons: list of buttons
    '''
    for btn in buttons:
        btn.hide()


def show_sorting_btns(self) -> None:
    '''
    Function to show sorting buttons
    '''
    show_btns(self, [
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


def hide_sorting_btns(self) -> None:
    '''
    Function to hide sorting buttons
    '''
    hide_btns(self, [
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


def open_website(self, website: str) -> None:
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


def wrong_filetype_msg(self) -> None:
    '''
    Function to display pop up message about a wrongfile type
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


def toggled_widgets(self,
                    widgets: list,
                    enable=False,
                    toggle_sorting_frame=True,
                    toggle_toolbar=True) -> None:
    """
    Function to toggle disabling/enabling buttons when in edit mode.

        Parameters:
            widgets: list of widgets to toggle, (can be None).
            enable: True -> enables widget, False -> disables widget.
            toggle_sorting_frame: toggle sorting buttons.
            toggle_toolbar: toggle ToolBar.
    """

    # toggling desired widgets
    if widgets:
        for btn in widgets:
            btn.setEnabled(enable)

    # toggling sorting buttons
    if toggle_sorting_frame:
        for btn in self.sorting_btns_frame.findChildren(QtWidgets.QPushButton):
            btn.setEnabled(enable)

    # toggling toolbar
    if toggle_toolbar:
        for action in self.toolbar.actions():
            action.setEnabled(enable)


def fill_table(self, dataframe) -> None:
    '''
    Function to fill in table.

        Parameter:
            dataframe: dict of category classes, single DataFrame or list of DataFrames of item.
    '''
    items = dataframe
    if type(dataframe) == dict:
        items = dict_to_dataframe(dataframe)
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
            items['Description'].astype(str)[row]))
        self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(
            items['Customer Reference'].fillna('')[row]))
        self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(
            items['Unit Price'].astype(float).round(2).astype(str)[row]))
        self.table.setItem(row, 5, QtWidgets.QTableWidgetItem(
            items['Quantity'].astype(int).astype(str)[row]))


def refresh_opensheet(self, items: dict) -> None:
    '''
    Function to refresh the last sheet that was opened.
        used for when a user is looking a specific category.

        Parameter:
            items: dictionary of category items.

    '''
    if 'looking at inventory' in self.header.text().lower():
        self.open_inventory()
    else:
        fill_table(self, items)
    self.sub_header.setText('')


def update_subtotal(self, dictionary) -> None:
    '''
    Function to update the subtotal of the project.
    '''
    subtotal = get_subtotal(dictionary)
    text = 'Subtotal: ${:.2f}'.format(subtotal)
    self.subtotal.setText(text)
