from general_lib import *

class contactPage():
    def __init__(self, mainSelf):
        self.mainSelf = mainSelf

        self.GUI_initialize_Objects()
        self.GUI_connect_buttons()

    def GUI_initialize_Objects(self):
        # ------------ Pages ------------
        self.contactUS_widget = self.mainSelf.findChild(QtWidgets.QWidget, "contactUS_widget")

        # ------------ Buttons ------------
        self.contactUS_Back_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "contactUS_Back_btn")
        self.contactUS_Back_btn.setFocusPolicy(Qt.NoFocus)


    def GUI_connect_buttons(self):
        self.contactUS_Back_btn.clicked.connect(self.contactUS_Back_btn_clicked)

    # ------------------- Buttons Clicked -------------------
    def navigate(self, currnetPage, destinationPage):
        currnetPageObj = self.mainSelf.findChild(QtWidgets.QWidget, currnetPage)
        currnetPageObj.hide()
        destinationPageObj = self.mainSelf.findChild(QtWidgets.QWidget, destinationPage)
        destinationPageObj.show()
        destinationPageObj.raise_()

    def contactUS_Back_btn_clicked(self):
        self.navigate("contactUS_widget", "welcomeScreen_widget")