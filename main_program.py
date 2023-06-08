from PyQt5.QtWidgets import QApplication
from program_modules.app import MainWindow
from program_modules.data_handing import load_Inventory
import sys


if __name__ == "__main__":
    # runnning program
    load_Inventory()
    app = QApplication(sys.argv)
    window1 = MainWindow()
    app.exec_()
