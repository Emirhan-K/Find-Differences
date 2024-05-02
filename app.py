from PyQt5.QtWidgets import QApplication
from start import Start_Page

app = QApplication([])
start = Start_Page()
start.show()
app.exec_()