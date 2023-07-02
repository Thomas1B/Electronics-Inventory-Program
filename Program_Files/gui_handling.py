'''
Script to run shared functions in PyQt Windows.

All of the functions require a self parameter.
'''

from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices, QIcon
import pandas as pd
import sys
import os
import shutil
from tkinter import Tk

from .data_handling import (
    dict_to_dataframe,
    get_subtotal,
    update_item,
    sort_order,
    Inventory,
    labels
)


def get_device_window_size() -> tuple:
    '''
    Function to get the device window size in pixels.

        Parameters:
            None

        Returns:
            tuple: width, height in pixels.
    '''
    root = Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    return width, height


def get_window_size(self) -> tuple:
    '''
    Function to get a PyQt Window size in pixels.

        Parameters:
            self: Window instance.

        Returns:
            tuple: width, height in pixels.
    '''
    width = self.size().width()  # Retrieve the window width
    height = self.size().height()  # Retrieve the window height
    return width, height


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
    self.sorting_btns_frame.show()


def hide_sorting_btns(self) -> None:
    '''
    Function to hide sorting buttons
    '''
    self.sorting_btns_frame.hide()


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


def fill_table(self, dataframe: dict | pd.DataFrame | list) -> None:
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
    if items.empty:
        return

    count = items.shape[0]
    self.table.setRowCount(count)

    for row in range(count):
        self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(
            items[labels[0]][row])
        )

        self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(
            items['Manufacturer Part Number'].fillna('').astype(str)[row])
        )

        self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(
            items['Description'].fillna('').astype(str)[row])
        )

        self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(
            items['Customer Reference'].fillna('').astype(str)[row])
        )

        self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(
            items['Unit Price'].astype(float).round(2).astype(str)[row])
        )

        self.table.setItem(row, 5, QtWidgets.QTableWidgetItem(
            items['Quantity'].astype(int).astype(str)[row])
        )


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


def get_table_data(self) -> pd.DataFrame:
    '''
    Function to get the displayed table data into a dataframe.

        Parameters:
            self: QWindow Class instance

        Returns:
            DataFrame
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


def change_item_quantity(self, dictionary: dict, row_index: int, remove_all=None):
    '''
    Function to change an item's quantity. Triggered by contextMenuEvent actions.

        Parameter:
            row_index - int: index to row that was clicked.
            remove_all - bool: False removes one, true deletes item, None for increasing by one.

    '''

    # getting item that was clicked on
    item = get_table_data(self).iloc[row_index]
    item = pd.DataFrame(item).T

    # conditions for updating item quantity
    delete = False
    match remove_all:
        case True:
            # deleting item
            delete = True
        case False:
            # minus 1 from quantity, if quantity > 1 otherwise delete
            if int(item['Quantity'].iloc[0]) > 1:
                item['Quantity'] = item['Quantity'].astype(int) - 1
            else:
                delete = True
        case None:
            # add 1 to quantity
            item['Quantity'] = item['Quantity'].astype(int) + 1

    # updating project dictionary
    self.editted_saved = False
    update_item(self, item=item, dictionary=dictionary, delete=delete)
    if hasattr(self, 'subtotal'):
        update_subtotal(self, dictionary)
    fill_table(self, dictionary)


def open_add_manually_window(self) -> None:
    '''
    Function to show "add item manually" window.
    '''

    # connecting window to function.
    self.add_item_window.data_sent.connect(self.receive_add_item_manually)
    self.add_item_window.show()


def get_editted_item(self, clicked_item: QtWidgets.QTableWidgetItem) -> pd.DataFrame:
    '''
    Function to get the item that has been editted.
        Triggered by itemChanged in table.

        Parameter:
            clicked_item: QTableItem that was clicked.

        Returns:
            DataFrame, (empty dataframe if there is a user error)
    '''

    data = get_table_data(self)

    column_name = data.keys()[clicked_item.column()]
    row_index = clicked_item.row()
    item = pd.DataFrame(data.iloc[row_index]).T

    # widgets to toggle if user entries has an error.
    widgets = [self.btn_save_list, self.btn_edit_mode]

    # checking if there is any letter in the editted price or quantity.
    if column_name in ['Unit Price', 'Quantity']:
        if any(char.isalpha() for char in clicked_item.text()):
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle('User Error')
            pixmapi = getattr(QtWidgets.QStyle, "SP_MessageBoxCritical")
            icon = self.style().standardIcon(pixmapi)
            msg.setWindowIcon(icon)
            msg.setIcon(QtWidgets.QMessageBox.Critical)

            msg.setText('You can only enter numbers!')
            text = 'Fix before continuing.'
            msg.setInformativeText(text)
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            _ = msg.exec_()

            self.editted_saved = 'error'
            toggled_widgets(self, widgets=widgets, enable=False)
            return pd.DataFrame()

    # checking if user left empty description
    elif item['Description'].iloc[0] == '':
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle('User Error')
        pixmapi = getattr(QtWidgets.QStyle, "SP_MessageBoxCritical")
        icon = self.style().standardIcon(pixmapi)
        msg.setWindowIcon(icon)
        msg.setIcon(QtWidgets.QMessageBox.Critical)

        msg.setText('You cannot have a blank item description!')
        text = 'Fix before continuing.'
        msg.setInformativeText(text)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        _ = msg.exec_()

        self.editted_saved = 'error'
        toggled_widgets(self, enable=False, widgets=widgets)
        return pd.DataFrame()

    # enabling widgets if they were disabled from user error.
    if self.editted_saved == 'error':
        toggled_widgets(self, enable=True, widgets=widgets)

    return item


def copySelectedCell(self, item):
    # selected_items = self.selectedItems()
    if item:
        text = ', '.join(info.text() for info in item)
        QApplication.clipboard().setText(text)
