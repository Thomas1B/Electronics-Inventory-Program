'''
Script to run shared functions in PyQt Windows.

All of the functions require a self parameter.
'''


from PyQt5.QtWidgets import QApplication, QDesktopWidget
from PyQt5 import QtWidgets
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices, QIcon
import pandas as pd

from .data_handling import (
    Inventory,
    labels,
    Data
)


def custom_contextMenuEvent(self, event) -> None:
    '''
        Function to show a menu when right clicked on item in the table.

            Parameters:
                event: QtGui.QCloseEvent.
        '''

    # only show contextMenu when inventory is opened.
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
            add_to_project_action = QtWidgets.QAction(
                QIcon("Program_Files/Icons/document--plus.png"),
                "Add Item to Project"
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
            add_to_project_action.triggered.connect(
                lambda: self.get_clicked_row(row_index)
            )

            # Adding to actions to menu
            if self.project_window.isVisible():
                menu.addAction(add_to_project_action)
                menu.addSeparator()
                menu.addAction(web_search_action)
                menu.addSeparator()
                menu.addAction(copy_selected_action)
                menu.addAction(add_one_action)
                menu.addAction(remove_one_action)
                menu.addAction(delete_item_action)

            menu.exec_(event.globalPos())  # showing menu


def web_search_item(self, row_index: int) -> None:
    '''
    Function to google search "DigiKey Part Number".

        Parameters:
            row_index: index of item in DataFrame.
    '''

    items = get_table_data(self)
    part_number = items.iloc[row_index][labels[0]]
    website = f'https://www.google.ca/search?q=Digikey {part_number}'
    open_website(self, website)


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


def fill_table(self, dataframe: dict | pd.DataFrame | list | Data) -> None:
    '''
    Function to fill in table.

        Parameter:
            dataframe: dict of category classes, single DataFrame, list of DataFrames of item or Data Object.
    '''

    items = dataframe
    if type(dataframe) == dict:
        print("\nOLD CODE in fill_table() in gui_handling.py")
        # items = dict_to_dataframe(dataframe)
        return
    elif type(dataframe) == list:
        items = pd.concat(dataframe)
    elif type(dataframe) == Data:
        items = dataframe.dict_to_dataframe()
    if items.empty:
        return

    count = items.shape[0]
    self.table.setRowCount(count)

    for row in range(count):
        self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(
            items[labels[0]][row])
        )

        self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(
            items[labels[1]].fillna('').astype(str)[row])
        )

        self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(
            items[labels[2]].fillna('').astype(str)[row])
        )

        self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(
            items[labels[3]].fillna('').astype(str)[row])
        )

        self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(
            items[labels[4]].astype(float).round(2).astype(str)[row])
        )

        self.table.setItem(row, 5, QtWidgets.QTableWidgetItem(
            items[labels[5]].astype(int).astype(str)[row])
        )

    # Modifying styling for table and headers.
    header = self.table.horizontalHeader()
    header.setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
    header.resizeSections(QtWidgets.QHeaderView.Stretch)
    header.setSectionsClickable(True)


def refresh_opensheet(self, items: dict | Data) -> None:
    '''
    Function to refresh the last sheet that was opened.
        used for when a user is looking a specific category.

        Parameter:
            items: dictionary of category items or Data Object.

    '''
    if 'looking at inventory' in self.header.text().lower():
        self.open_inventory()
    else:
        fill_table(self, items)
    self.sub_header.setText('')
    self.comboBox_section.setCurrentIndex(0)


def update_subtotal(self, data: Data) -> None:
    '''
    Function to update the subtotal of the project.
    '''
    subtotal = data.get_subtotal()
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

        data = pd.DataFrame(data, columns=labels)
        return data
    else:
        print("NO ROWS IN TABLE")


def change_item_qty(self, data: Data, row_index: int, remove_all=None):
    '''
    Function to change an item's quantity. Triggered by contextMenuEvent actions.

        Parameter:
            row_index - int: index to row that was clicked.
            remove_all - bool: False removes one, true deletes item, None for increasing by one.

    '''

    # getting item that was clicked on
    table_items = get_table_data(self)
    item = table_items.iloc[row_index]
    item = pd.DataFrame(item).T

    # conditions for updating item quantity
    delete = False
    match remove_all:
        case True:
            # deleting item
            delete = True
        case False:
            # minus 1 from quantity, if quantity > 1 otherwise delete
            if int(item['Quantity'].iloc[0]) > 0:
                item['Quantity'] = item['Quantity'].astype(int) - 1
            else:
                delete = True
        case None:
            # add 1 to quantity
            item['Quantity'] = item['Quantity'].astype(int) + 1

    # updating displayed table item for viewing.
    item_index = item.index[0]
    table_items.loc[item_index, 'Quantity'] = item.loc[item_index, 'Quantity']

    if delete:
        # pop up messeges asking user if they're sure they want to delete item.
        popup = QtWidgets.QMessageBox()
        popup.setWindowTitle("EIP - Deleting Item")
        pixmapi = getattr(QtWidgets.QStyle, "SP_MessageBoxQuestion")
        icon = self.style().standardIcon(pixmapi)
        popup.setWindowIcon(icon)
        popup.setText("Are you sure you want to delete the item?")
        popup.setStandardButtons(
            QtWidgets.QMessageBox.Yes |
            QtWidgets.QMessageBox.No
        )
        popup.setDefaultButton(QtWidgets.QMessageBox.Yes)
        user = popup.exec_()

        if user == QtWidgets.QMessageBox.No:
            return
        else:
            table_items.drop(item_index, inplace=True)
            table_items.reset_index(drop=True, inplace=True)

    # updating dictionary
    self.editted_saved = False
    data.update_item(item=item, delete=delete)

    if hasattr(self, 'subtotal'):
        update_subtotal(self, data)
    fill_table(self, table_items)
    self.btn_save_list.show()


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
