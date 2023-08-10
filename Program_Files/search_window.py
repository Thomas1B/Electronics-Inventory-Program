'''
Script to run search window
'''

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices, QIcon
import pandas as pd
import os

from .data_handling import (
    Inventory,
    Items,
    dataframe_to_dict,
    get_ordersheet,
    sort_order,
)

from .gui_handling import (
    no_files_msg,
    fill_table,
    copySelectedCell,
    get_table_data,
)

from .styles import (
    style_central_widget,
    style_table
)


class SearchWindow(QMainWindow):
    '''
    Search Window class
    '''

    def __init__(self, parent=None) -> None:
        super(SearchWindow, self).__init__(parent=parent)
        uic.loadUi('Program_Files/UI_Files/search_window.ui', self)
        style_central_widget(self)
        style_table(self)

        if self.size().width() < 800:
            self.resize(800, 800)
        self.move(1000, 50)

        ''' Finding Widgets '''

        # Search Frame
        self.search_frame = self.findChild(QtWidgets.QFrame, 'search_frame')
        self.comboBox_section = self.findChild(
            QtWidgets.QComboBox, 'comboBox_section'
        )
        self.comboBox_category = self.findChild(
            QtWidgets.QComboBox, 'comboBox_category'
        )
        self.search_lineEdit = self.findChild(
            QtWidgets.QLineEdit, 'search_lineEdit'
        )
        self.btn_search = self.findChild(
            QtWidgets.QPushButton, 'btn_search'
        )

        # table
        self.table = self.findChild(
            QtWidgets.QTableWidget, 'table'
        )
        # self.table.cellClicked.connect(self.get_clicked_row)
        # project window from the parent window (from gui_app.py)
        self.project_window = parent.project_window

        ''' Attaching Functions to widgets '''

        # search button
        self.btn_search.clicked.connect(self.get_user_entries)

        ''' Styling some widgets'''
        self.search_frame.setStyleSheet(
            '''
            QComboBox {
                padding: 5px;
                background-color: white;
            }
            '''
        )
        self.search_lineEdit.setStyleSheet(
            '''
            QLineEdit {
                background-color: white;
                padding: 5px;
                border: 1px solid rgba(0, 0, 0, 0.5)
            }
            '''
        )
        self.btn_search.setStyleSheet(
            '''
            QPushButton {
                background-color: white;
            }

            QPushButton:hover {
                background-color: rgb(0, 255, 0);
            }
            '''
        )

        ''' adding Initial values to some widgets '''
        self.comboBox_category.addItems(Inventory.keys)

    def closeEvent(self, event) -> None:
        self.comboBox_section.setCurrentIndex(0)
        self.comboBox_category.setCurrentIndex(0)
        self.search_lineEdit.clear()
        self.table.setRowCount(0)
        event.accept()

    def contextMenuEvent(self, event) -> None:
        '''
        Function to handle right click on table
        '''

        # only allow contextMenuEvent if there items in the table
        pos = self.table.viewport().mapFromGlobal(event.globalPos())
        row_index = self.table.rowAt(pos.y())
        if row_index >= 0:

            menu = QtWidgets.QMenu()
            menu = QtWidgets.QMenu(self)
            copy_selected_action = QtWidgets.QAction("Copy Selected")
            add_to_project_action = QtWidgets.QAction("Add Item to Project")

            copy_selected_action.triggered.connect(
                lambda: copySelectedCell(
                    self,
                    self.table.selectedItems()
                )
            )
            add_to_project_action.triggered.connect(
                lambda: self.get_clicked_row(row_index)
            )

            menu.addAction(copy_selected_action)
            if self.project_window.isVisible():
                menu.addSeparator()
                menu.addAction(add_to_project_action)

            menu.exec_(event.globalPos())  # showing menu

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
            self.project_window.add_to_project(item)

    def clear_search_entires(self) -> None:
        '''
        Function to clear the search entries.
        '''

        self.comboBox_section.setCurrentIndex(0)
        self.comboBox_category.setCurrentIndex(0)
        self.search_lineEdit.clear()

    def get_user_entries(self) -> None:
        '''
        Function to get the user entries and check them.
        '''

        section = self.comboBox_section.currentText()
        category = self.comboBox_category.currentText()
        text = self.search_lineEdit.text()

        # checking if user typed anything in search bar or is whitespace.
        if text.isspace() or not text:
            text = 'All'

        self.search_for((section, category, text))

    def get_inventory_items(self) -> pd.DataFrame:
        '''
        Function to get all items from the inventory.

            Parameter:
                None

            Returns:
                DataFrame of items
        '''
        if os.path.exists('Saved_Lists/Inventory.xlsx'):
            return Inventory.dict_to_dataframe()
        else:
            return pd.DataFrame()

    def get_project_items(self, project_name='') -> pd.DataFrame:
        '''
        Function to get all the items from all project files.

            Parameter:
                project_name (optional): specific project name to get items from, default all projects.

            Returns:
                DataFrame of items
        '''

        folder = 'Saved_Lists/Projects'  # project folder

        # if project_name is passed, get the projects items
        if len(project_name) != 0:
            project_items = get_ordersheet(f'{folder}/{project_name}')

        # if there are any projects, get items from each and make one DataFrame.
        elif len(os.listdir(folder)) > 0:
            project_items = []
            for filename in os.listdir(folder):
                if os.path.isfile(os.path.join(folder, filename)):
                    file = get_ordersheet(f'{folder}/{filename}')
                    for items in file:
                        if not items.empty:
                            # checking if sorted section is non empty.
                            project_items.append(items)
            if project_items:
                project_items = pd.concat(project_items)
            else:
                project_items = pd.DataFrame()
        else:
            project_items = pd.DataFrame()

        return project_items

    def get_past_order_items(self, order_name='') -> pd.DataFrame:
        '''
        Function to get all the items from all project files.

            Parameter:
                order_name (optional): specific project name to get items from, default all projects.

            Returns:
                DataFrame of items
        '''
        folder = 'Saved_Lists/Past Orders'  # past orders folder

        # if order_name is passed, get the order items
        if len(order_name) != 0:
            order_items = get_ordersheet(f'{folder}/{order_name}')

        # if there are any past orders, get items from each and make one DataFrame.
        elif len(os.listdir(folder)) > 0:
            order_items = []
            for filename in os.listdir(folder):
                file = get_ordersheet(f'{folder}/{filename}')
                for items in file:
                    if not items.empty:
                        # checking if sorted section is non empty.
                        order_items.append(items)
            order_items = pd.concat(order_items)
        else:
            order_items = pd.DataFrame()

        return order_items

    def get_category_items(self, items: pd.DataFrame, category: str) -> pd.DataFrame:
        '''
        Function to get items from a given DataFrame of items using the category type.

            Parameter:
                items: DataFrame of items to look at.
                category: what category to look at.

            Returns:
                DataFrame of items
        '''
        sorted_items = sort_order(items)
        category_items = dataframe_to_dict(sorted_items)[category]
        return category_items

    def get_items_using_text(self, category_items: pd.DataFrame, search_info: tuple) -> pd.DataFrame:
        '''
        Function to get items using the text the user typed in

            Parameters:

        '''
        section, category, user_text = search_info
        user_text = user_text.lower().split(' ')

        # checking the dataframe's 'Description' for each word in the string
        results = [category_items[category_items['Description'].str.contains(
            text, case=False)] for text in user_text]
        results = pd.concat(results)

        # checking if the search result is empty
        if results.empty:
            user = QtWidgets.QMessageBox()
            user.setWindowIcon(
                QIcon('Program_Files/Icons/magnifier.png'))
            user.setIcon(QtWidgets.QMessageBox.Warning)
            user.setStandardButtons(
                QtWidgets.QMessageBox.Ok
            )
            user.setWindowTitle("No Search Results")
            text = " ".join(user_text)
            header = f'There are no search results for:\n{section}, {category}, {text}.'
            user.setText(header)
            _ = user.exec_()
            return pd.DataFrame()

        return results.reset_index(drop=True).drop_duplicates()

    def search_for(self, search_info: tuple):
        '''
        Function to search for items with desired criteria.

            Parameter:
                search_info: tuple of strings for criteria (section, category, text)
        '''
        section, category, user_text = search_info

        # DataFrames to pass
        section_items = None
        category_items = None
        found_items = None

        # getting the section_items from the desired sections.
        match section.lower():
            case "inventory":
                if os.path.exists('Saved_Lists/Inventory.xlsx'):
                    section_items = self.get_inventory_items()
                else:
                    title = 'No Inventory'
                    header = 'No inventory to search.'
                    no_files_msg(self, title=title, header=header)
                    return

            case 'projects':  # searches all projects files
                file_items = []
                folder = 'Saved_Lists/Projects'
                if len(os.listdir(folder)) > 0:
                    section_items = self.get_project_items()
                    if section_items.empty:
                        title = 'No Project Files'
                        header = 'No projects to search.'
                        no_files_msg(self, title=title, header=header)
                        return

                else:
                    title = 'No Project Files'
                    header = 'No projects to search.'
                    no_files_msg(self, title=title, header=header)
                    return

            case 'past orders':  # searches all pass orders.
                file_items = []
                folder = 'Saved_Lists/Past Orders'
                if len(os.listdir(folder)) > 0:
                    section_items = self.get_past_order_items()
                else:
                    title = 'No Past Orders'
                    header = 'No past orders to search.'
                    no_files_msg(self, title=title, header=header)
                    return

            case _:  # default searches all
                inventory_items = Inventory.dict_to_dataframe()
                project_items = self.get_project_items()
                past_order_items = self.get_past_order_items()

                all_items = [inventory_items, project_items, past_order_items]
                all_items = [items for items in all_items if not items.empty]

                if not all_items:
                    title = 'No Files'
                    header = 'There are no files to search.'
                    no_files_msg(self, title=title, header=header)
                    return

                section_items = pd.concat(all_items)
                section_items.drop_duplicates(
                    inplace=True, subset=['Description'])

        # getting items in the desired category
        match category.lower():
            case 'all':
                category_items = section_items
            case _:
                category_items = self.get_category_items(
                    section_items, category)

        # getting the items based on criteria from 'text'
        match user_text.lower():
            case 'all':
                found_items = category_items.reset_index(drop=True)
            case _:
                found_items = self.get_items_using_text(
                    category_items=category_items,
                    search_info=(section, category, user_text)
                )

        self.show_found_items(found_items)

    def show_found_items(self, found_items):
        '''
        Function to display the found items
        '''
        fill_table(self, found_items)
