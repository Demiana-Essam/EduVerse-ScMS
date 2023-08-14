from general_lib import *
from pages.loginPage import *
from pages.aboutUsPage import *
from pages.contactPage import *
class welcomePage():
    def __init__(self,mainSelf):
        self.mainSelf = mainSelf

        self.GUI_initialize_Objects()
        self.GUI_connect_buttons()

    def GUI_initialize_Objects(self):
        # ------------ Pages ------------
        self.welcomeScreen_widget = self.mainSelf.findChild(QtWidgets.QWidget, "welcomeScreen_widget")
        self.welcomeScreen_widget.raise_()

        # ------------ Buttons ------------
        self.getStarted_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "getStarted_btn")
        self.getStarted_btn.setFocusPolicy(Qt.NoFocus)
        self.aboutUs_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "aboutUs_btn")
        self.aboutUs_btn.setFocusPolicy(Qt.NoFocus)
        self.contact_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "contact_btn")
        self.contact_btn.setFocusPolicy(Qt.NoFocus)
        self.welcomeExit_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "welcomeExit_btn")
        self.welcomeExit_btn.setFocusPolicy(Qt.NoFocus)
    def GUI_connect_buttons(self):
        self.getStarted_btn.clicked.connect(self.getStarted_btn_clicked)
        self.aboutUs_btn.clicked.connect(self.aboutUs_btn_clicked)
        self.contact_btn.clicked.connect(self.contact_btn_clicked)
        self.welcomeExit_btn.clicked.connect(self.welcomeExit_btn_clicked)
    # ------------------- Buttons Clicked -------------------
    def navigate(self, currnetPage, destinationPage):
        currnetPageObj = self.mainSelf.findChild(QtWidgets.QWidget, currnetPage)
        currnetPageObj.hide()
        destinationPageObj = self.mainSelf.findChild(QtWidgets.QWidget, destinationPage)
        destinationPageObj.show()
        destinationPageObj.raise_()
    def getStarted_btn_clicked(self):
        self.loginPage = loginPage(self.mainSelf)
        self.navigate("welcomeScreen_widget", "loginScreen_widget")
    def contact_btn_clicked(self):
        self.contactPage = contactPage(self.mainSelf)
        self.navigate("welcomeScreen_widget", "contactUS_widget")
    def aboutUs_btn_clicked(self):
        self.aboutUsPage = aboutUsPage(self.mainSelf,"Welcome")
        self.navigate("welcomeScreen_widget", "aboutUS_widget")
    def welcomeExit_btn_clicked(self):
        self.mainSelf.close()