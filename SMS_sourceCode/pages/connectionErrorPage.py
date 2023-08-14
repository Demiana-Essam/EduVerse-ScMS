from general_lib import *
from config import *
from dataBase import *
class connectionErrorPage():
    def __init__(self, mainSelf):
        self.mainSelf = mainSelf

        self.GUI_initialize_Objects()
        self.GUI_connect_buttons()

    def GUI_initialize_Objects(self):
        # ------------ Pages ------------
        self.connectionError_widget = self.mainSelf.findChild(QtWidgets.QWidget, "connectionError_widget")
        self.connectionError_widget.raise_()
        # ------------ Buttons ------------
        self.connError_Exit_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "connError_Exit_btn")
        self.connError_Exit_btn.setFocusPolicy(Qt.NoFocus)
        self.connection_tryAgain_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "connection_tryAgain_btn")
        self.connection_tryAgain_btn.setFocusPolicy(Qt.NoFocus)


    def GUI_connect_buttons(self):
        self.connError_Exit_btn.clicked.connect(self.connError_Exit_btn_clicked)
        self.connection_tryAgain_btn.clicked.connect(self.connection_tryAgain_btn_clicked)

    # ------------------- Buttons Clicked -------------------
    def navigate(self, currnetPage, destinationPage):
        currnetPageObj = self.mainSelf.findChild(QtWidgets.QWidget, currnetPage)
        currnetPageObj.hide()
        destinationPageObj = self.mainSelf.findChild(QtWidgets.QWidget, destinationPage)
        destinationPageObj.show()
        destinationPageObj.raise_()

    def connection_tryAgain_btn_clicked(self):
        try:
            self.mainSelf.dataBase.start_Firebase_Connection()
            self.mainSelf.configuration = config(self.mainSelf)
            destinationPageObj = self.mainSelf.findChild(QtWidgets.QWidget, "welcomeScreen_widget")
            destinationPageObj.raise_()
        except:
            pass

    def connError_Exit_btn_clicked(self):
        self.mainSelf.close()