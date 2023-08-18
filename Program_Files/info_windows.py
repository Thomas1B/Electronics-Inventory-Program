'''
Script to show pop up information windows.
'''


from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtGui, QtWidgets
from PyQt5 import uic
from PyQt5.QtGui import QIcon
import sys

from .styles import (
    style_central_widget
)


class Program_Info_Window(QMainWindow):
    '''
    Class to run overview of program information window.
    '''

    def __init__(self, parent=None):
        super(Program_Info_Window, self).__init__(parent=parent)

        # loading ui file
        uic.loadUi('Program_Files/UI_Files/program_information.ui', self)
        # self.adjustSize()


class Help_Window(QMainWindow):
    '''
    Class to run program how to use program window.
    '''

    def __init__(self, parent=None):
        super(Help_Window, self).__init__(parent=parent)
        uic.loadUi('Program_Files/UI_Files/help_page.ui', self)
        self.setMinimumSize(560, 400)
        self.resize(650, 600)
        self.central_widget = self.findChild(
            QtWidgets.QWidget, 'centralwidget')

        # Finding widgets
        self.title = self.findChild(QtWidgets.QLabel, 'title')
        self.comboBox = self.findChild(QtWidgets.QComboBox, 'comboBox')
        # self.frame_info = self.findChild(QtWidgets.QFrame, 'frame_info')
        self.label_info = self.findChild(QtWidgets.QLabel, 'label_info')

        # Styling widgets
        self.central_widget.setStyleSheet(
            '''
            QWidget {
                background-color: rgb(238, 238, 238);
            }
            '''
        )
        self.title.setStyleSheet(
            '''
            QLabel {
                font: 16px Times;
                font-weight: bold;
            }
            '''
        )
        self.comboBox.setStyleSheet(
            '''
            QComboBox {
                font: 14px Arial;
                background-color: white;
                padding: 5px;
                border: 2px solid lightgrey;
                border-style: inset;
                border-radius: 2px;
            }
            
            QComboBox:focus {
                border: 1px solid blue;
            }

            QComboBox::down-arrow {
                width: 50px;
            }

            QAbstractItemView {
                background-color: white;
            }
            '''
        )
        self.label_info.setStyleSheet(
            '''
            QLabel {
                border: none;
                font: 12px Times;
                padding: 5px;
            }
            '''
        )

        # Attaching functions
        self.comboBox.currentIndexChanged.connect(
            lambda: self.show_info(self.comboBox.currentText())
        )

        # Adding help sections to combo box, then loading initial info:
        # (Note: "general" is added by the ui file)
        help_sections = [
            'General', 'Inventory', 'Projects', 'Orders', 'File Management', 'Add Items Manually'
        ]
        self.comboBox.addItems(help_sections)
        self.show_info(help_section=self.comboBox.currentText())
        self.show()

    def closeEvent(self, event) -> None:
        event.accept()

    def get_help_section_info(self, help_section: str) -> str:
        '''
        Function to get the text for a given help section.

            Parameters:
                help_section: what section text to load.

            Returns:
                string of text.
        '''

        # matching help section to get the desired text.
        match help_section.lower():

            case 'welcome':
                text = '''To properly handle XLSX (Excel) files, it is necessary for the user to remove the 'Subtotal' line from the sheet.

This Electronics Inventory Management Program is a straightforward and efficient Python software designed to aid in the organization and management of electronic components. Its user-friendly interface allows users to easily import and read CSV (Comma-Separated Values) and XLSX (Excel) files that contain information about different electronic components. To successfully sort the parts, the program requires the following columns: 'Part Number', 'Manufacturer Part Number', 'Description', 'Customer Reference', 'Unit Price', and 'Quantity'. Any additional columns present in the data files will be skipped by the program.

When the user interacts with the system by opening a new order, accessing their inventory, reviewing projects, or checking past orders, they will be presented with options to choose from to filter the electronics types in that particular file. Additionally, they can save orders for future reference. When a new order is added to the inventory, the program automatically organizes the items and places them in the appropriate sections. Subsequently, the user is prompted to save the edited inventory.'''

            case 'general':
                text = '''Any unsaved work is prompted to save when closing a project or exiting the program.
                
Commands are presented as various buttons and also drop-down menus when right-clicked on tables.'''

            case 'add items manually':
                text = '''To add an item manually, open the inventory or a project and click the add item button, then fill in the respective fields.

- Part Number is a field that is specific to DigiKey.

- Manufacturer Part Number is given by the manufacturer.

- Description is nessecary since the software uses this to sort the components into categories, such as resistor, capacitor, etc. This field normally given by the saler, in the software it is assumed to be given by Digikey.

- Customer Reference is another field specific to DigiKey, it helps the buyer identify items. For example when buying a 10000pF capacitor, the buyer may put a reference "10000pF/10nF/0.01uF".

- Unit Price is the price of an individual item.

- Quantity is the amount of the item.
'''

            case _:
                text = 'More to come!'

        return text

    def show_info(self, help_section: str) -> None:
        '''
        Function to show the info when the comboBox item is changed

            Parameters:
                help_section: what help section to load (General, adding items, etc).
        '''
        text = self.get_help_section_info(help_section=help_section)
        self.label_info.setText(text)


class How_To_Use_Project_Window(QMainWindow):
    '''
    Class to run program how to use project window.
    '''

    def __init__(self, parent=None):
        super(How_To_Use_Project_Window, self).__init__(parent=parent)

        uic.loadUi('Program_Files/UI_Files/how_to_use_project_window.ui', self)


class How_Add_Item_Manually_Window(QMainWindow):
    '''
    Class to run how to use "Add item Manually" window.
    '''

    def __init__(self, parent=None):
        super(How_Add_Item_Manually_Window, self).__init__(parent=parent)
        uic.loadUi('Program_Files/UI_Files/how_to_use_add_manually.ui', self)

        self.frame = self.findChild(QtWidgets.QFrame, 'frame')
        self.frame.setStyleSheet(
            '''
            QScrollArea {
                border: 1px solid rgb(169, 169, 169);
                border-radius: 4px;
                padding: 4px;
            }
            '''
        )
