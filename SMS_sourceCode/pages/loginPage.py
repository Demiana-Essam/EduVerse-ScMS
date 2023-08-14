from general_lib import *
from dataBase import *
from pages.homePage import homePage
from pages.FaceIDBiometricPage import FaceIDBiometric

class loginPage():
    def __init__(self, mainSelf):
        self.mainSelf = mainSelf

        self.GUI_initialize_Objects()
        self.GUI_connect_buttons()

    def GUI_initialize_Objects(self):
        # ------------ Pages ------------
        self.loginScreen_widget = self.mainSelf.findChild(QtWidgets.QWidget, "loginScreen_widget")

        # ------------ Icons ------------
        self.fingerPrintIcon_Label = self.mainSelf.findChild(QtWidgets.QWidget, "fingerPrintIcon_Label")
        # Load the GIF using QMovie
        self.movie = QMovie("uis/materials/icons/fingerprint.gif", QByteArray(), self.mainSelf)

        # Set the size of the QMovie to be the same as the QLabel
        self.movie.setScaledSize(self.fingerPrintIcon_Label.size())
        self.fingerPrintIcon_Label.setMovie(self.movie)
        self.movie.start()

        # ------------ Buttons ------------
        # ----- Login page -----
        self.loginHome_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "loginHome_btn")
        self.loginHome_btn.setFocusPolicy(Qt.NoFocus)
        self.loginExit_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "loginExit_btn")
        self.loginExit_btn.setFocusPolicy(Qt.NoFocus)
        self.login_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "login_btn")
        self.login_btn.setFocusPolicy(Qt.NoFocus)
        self.faceRecognation_login_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "faceRecognation_login_btn")
        self.faceRecognation_login_btn.setFocusPolicy(Qt.NoFocus)

        self.loginUserName_tbox = self.mainSelf.findChild(QtWidgets.QLineEdit, "loginUserName_tbox")
        self.loginUserName_tbox.textChanged.connect(self.onTextChanged)
        self.loginPassword_tbox = self.mainSelf.findChild(QtWidgets.QLineEdit, "loginPassword_tbox")
        self.loginPassword_tbox.textChanged.connect(self.onTextChanged)


    def onTextChanged(self):
        login_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "login_btn")
        if(login_btn.text() == "Invalid Credentials, Try again"):
            login_btn.setText("Login")

    def GUI_connect_buttons(self):
        self.loginHome_btn.clicked.connect(self.home_btn_clicked)
        self.loginExit_btn.clicked.connect(self.loginExit_btn_clicked)
        self.login_btn.clicked.connect(self.login_btn_clicked)
        self.faceRecognation_login_btn.clicked.connect(self.faceRecognation_login_btn_clicked)

    # ------------------- Buttons Clicked -------------------
    def navigate(self, currnetPage, destinationPage):
        currnetPageObj = self.mainSelf.findChild(QtWidgets.QWidget, currnetPage)
        currnetPageObj.hide()
        destinationPageObj = self.mainSelf.findChild(QtWidgets.QWidget, destinationPage)
        destinationPageObj.show()
        destinationPageObj.raise_()

    def login_btn_clicked(self):
        self.login_handling()

    def home_btn_clicked(self):
        self.navigate("loginScreen_widget", "welcomeScreen_widget")
    def faceRecognation_login_btn_clicked(self):
        self.FaceIDBiometric = FaceIDBiometric(self.mainSelf)
        self.navigate("loginScreen_widget", "faceID_widget")
    def loginExit_btn_clicked(self):
        self.mainSelf.close()


    # ------------------- Login Handler -------------------
    def login_handling(self):
        loginUserName_tbox = self.mainSelf.findChild(QtWidgets.QLineEdit, "loginUserName_tbox")
        loginPassword_tbox = self.mainSelf.findChild(QtWidgets.QLineEdit, "loginPassword_tbox")
        if self.mainSelf.dataBase.login(loginUserName_tbox.text(), loginPassword_tbox.text()):
            # Create an object of Home Page
            user, id = self.mainSelf.dataBase.getUser(loginUserName_tbox.text())
            self.homePage = homePage(self.mainSelf, user, id)

            self.navigate("loginScreen_widget", "homeManagerScreen_widget")
            # Reset fields
            login_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "login_btn")
            login_btn.setText("Login")
            loginUserName_tbox.setText("")
            loginPassword_tbox.setText("")

        else:
            login_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "login_btn")
            login_btn.setText("Invalid Credentials, Try again")
