import os, sys
import pandas as pd
from PyQt5 import uic
import traceback
import datetime



from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer


root = os.path.dirname(os.path.abspath(__file__))
# ui만든 파일의 경로
MainUI = uic.loadUiType(os.path.join(root, 'kiosk.ui'))[0]

class MainDialog(QMainWindow, MainUI):

    def __init__(self):


        try:

            super().__init__()

            self.cnt = 0
            self.setupUi(self)
        except Exception as e:
            print(e)
            print(traceback.format_exc())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainDialog()
    mainWindow.show()
    sys.exit(app.exec_())
