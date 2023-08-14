from PyQt5 import uic
# from PyQt5 import pyrcc
from uis import res
from pages.welcomePage import *
import sys
from pages.sessionChartsPage import *
from pages.connectionErrorPage import *
from config import *

class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("uis\GUI.ui",self)
        self.GUI_initialize_properities()
        self.GUI_initialize_Pages()

        try:
            self.configuration= config(self)
        except:
            self.connectionErrorPage = connectionErrorPage(self)

    def GUI_initialize_properities(self):
        self.setWindowIcon(QIcon("uis\materials\systemLogo.png"))
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.dataBase=dataBase()

    def GUI_initialize_Pages(self):
        # ------------ Pages ------------
        self.welcomePage = welcomePage(self)
        self.sessionChartsPage = sessionChartsPage(self)
    def navigate(self, currnetPage, destinationPage):
        currnetPageObj = self.mainSelf.findChild(QtWidgets.QWidget, currnetPage)
        currnetPageObj.hide()
        destinationPageObj = self.mainSelf.findChild(QtWidgets.QWidget, destinationPage)
        destinationPageObj.show()
        destinationPageObj.raise_()
    def mousePressEvent(self, event):
        self.oldPosition = event.globalPos()
    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint(event.globalPos() - self.oldPosition)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPosition = event.globalPos()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window =Window()
    window.show()
    sys.exit(app.exec())