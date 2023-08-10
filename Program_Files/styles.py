'''
File to store shared CSS styling throughout the program.
'''
from PyQt5 import QtWidgets

# style for central widget


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
refresh_btn_styles = '''
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


def style_table(self) -> None:
    '''
    Functiont to style the table
    '''
    # styling table
    header = self.table.horizontalHeader()
    header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
    header.setStyleSheet(
        '''
        QHeaderView {
            font-size: 14px;
            font-weight: bold;
        }
        '''
    )
