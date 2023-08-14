'''
File to store shared CSS styling throughout the program.
'''
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from .data_handling import labels


# style for toolbar
toolbar_styles = '''
QToolButton {
    padding: 5px;
}

QToolButton:hover {
    background-color: rgb(200, 200, 200);
}
'''

# style for refresh button


def style_central_widget(self) -> None:
    '''
    Functiont to style the central widget
    '''
    widget = self.findChild(QtWidgets.QWidget, 'centralwidget')
    widget.setStyleSheet(
        '''
        QWidget {
            background-color: rgb(204, 204, 204);
        }
        '''
    )


def style_refresh_btn(self) -> None:
    '''
    Function to style the refresh button.
    '''
    self.btn_refresh_opensheet.setStyleSheet(
        '''
        QPushButton {
            background-color: white;
            padding: 10px;
            border: 1.5px grey;
            border-radius: 5px;
            border-style: outset;
        }

        QPushButton:hover, QPushButton:focus {
            border: 2px solid blue;
        }

        QPushButton:pressed {
            border-style: inset;
        }
        '''
    )


def style_table(self) -> None:
    '''
    Function to style the table and set header names.
    '''

    # Styling headers
    self.table.setHorizontalHeaderLabels(labels)

    header = self.table.horizontalHeader()
    header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
    header.setSectionsClickable(False)

    header.setStyleSheet(
        '''
        QHeaderView::section {
            background-color: lightblue;
            padding: 5px 0px;
            padding-left: 5px;
        }

        QHeaderView {
            font-size: 16px;
            font-weight: bold;
            font-family: times;
        }
        '''
    )
    header.setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)

    # styling table
    self.table.setStyleSheet(
        '''
        QTableWidget {
            background-color: white;
            font-size: 12px;
        }
        '''
    )

def style_sorting_comboBox(self):
    '''
    Function to style the sorting combobox
    '''

    self.comboBox_section.setStyleSheet(
        '''
        QComboBox {
            background-color: white;
            padding: 5px;
        }

        QAbstractItemView {
            background-color: white;
        }
        '''
    )
