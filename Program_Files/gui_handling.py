'''
Script to run shared functions in PyQt Windows.
'''

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtGui import QIcon
import sys


def toggled_widgets(self,
                    widgets: list,
                    enable=False,
                    toggle_sorting_frame=True,
                    toggle_toolbar=True) -> None:
    """
    Function to toggle disabling/enabling buttons when in edit mode.

        Parameters:
            widgets: list of widgets to toggle, (can be None).
            enable: Tue -> enables widget, False -> disables widget.
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
