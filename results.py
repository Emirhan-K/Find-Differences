from PyQt5.QtWidgets import *
from results_ui import Ui_ResultWindow
from PyQt5.QtGui import QPixmap

class Result_Page(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.resultPage = Ui_ResultWindow()
        self.resultPage.setupUi(self)


