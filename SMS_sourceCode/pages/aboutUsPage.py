from general_lib import *

class aboutUsPage():
    def __init__(self, mainSelf, previousPage):
        self.mainSelf = mainSelf
        self.previousPage=previousPage

        self.GUI_initialize_Objects()
        self.GUI_connect_buttons()

    def GUI_initialize_Objects(self):
        # ------------ Pages ------------
        self.aboutUS_widget = self.mainSelf.findChild(QtWidgets.QWidget, "aboutUS_widget")

        # ------------ Buttons ------------
        self.aboutUS_Back_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "aboutUS_Back_btn")
        self.aboutUS_Back_btn.setFocusPolicy(Qt.NoFocus)


    def GUI_connect_buttons(self):
        self.aboutUS_Back_btn.clicked.connect(self.aboutUS_Back_btn_clicked)

    # ------------------- Buttons Clicked -------------------
    def navigate(self, currnetPage, destinationPage):
        currnetPageObj = self.mainSelf.findChild(QtWidgets.QWidget, currnetPage)
        currnetPageObj.hide()
        destinationPageObj = self.mainSelf.findChild(QtWidgets.QWidget, destinationPage)
        destinationPageObj.show()
        destinationPageObj.raise_()

    def aboutUS_Back_btn_clicked(self):
        if self.previousPage== "Home":
            self.navigate("aboutUS_widget", "homeManagerScreen_widget")
        elif self.previousPage== "Welcome":
            self.navigate("aboutUS_widget", "welcomeScreen_widget")