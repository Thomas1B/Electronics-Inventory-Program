'''
This is a Python script that runs an electronics inventory program, utilizing pandas for data handling and PyQt5 for the user interface.

The "gui_app" and "data_handling" modules can be found in the "program_modules" folder of this program. The "data_handling" module uses pandas to handle the data, while the "gui_app" module runs the GUI using PyQt5. The GUI was designed with PyQt Designer, available for download at: https://build-system.fman.io/qt-designer-download.


Need python packages
- PyQt5
- Pandas

'''


from PyQt5.QtWidgets import QApplication
from Program_Files.gui_app import MainWindow
from Program_Files.data_handling import load_Inventory
import sys


if __name__ == "__main__":
    # runnning program
    load_Inventory()
    app = QApplication(sys.argv)
    window1 = MainWindow()
    app.exec_()
