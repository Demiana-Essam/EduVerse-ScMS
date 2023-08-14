from general_lib import *
from config import *
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import *
import cv2
import threading


class newUserPage(QThread):
    ImageUpdate = pyqtSignal(QImage)
    def initiate(self, mainSelf):
        self.mainSelf = mainSelf
        self.GUI_initialize_Objects()
        self.GUI_connect_buttons()
    def run(self):
        self.isThreadActive = True
        self.liveViewCamera = threading.Thread(target=self.liveView_worker)
        self.liveViewCamera.start()
        self.ImageUpdate.connect(self.ImageUpdate_UpdateSlot)
    def ImageUpdate_UpdateSlot(self, Image):
        self.cameraNewUserImage_Label.setPixmap(QPixmap.fromImage(Image))
    def GUI_initialize_Objects(self):
        # ------------ Pages ------------
        self.newUser_widget = self.mainSelf.findChild(QtWidgets.QWidget, "newUser_widget")
        # ------------ Objects ------------
        self.userImage = None
        self.userImageRegister_Label = self.mainSelf.findChild(QtWidgets.QLabel, "userImageRegister_Label")
        self.cameraNewUserImage_Label = self.mainSelf.findChild(QtWidgets.QLabel, "cameraNewUserImage_Label")

        # ------------ Buttons ------------
        self.newUser_Back_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "newUser_Back_btn")
        self.newUser_Back_btn.setFocusPolicy(Qt.NoFocus)
        self.newUser_openImage_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "newUser_openImage_btn")
        self.newUser_openImage_btn.setFocusPolicy(Qt.NoFocus)
        self.takePic_newUser_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "takePic_newUser_btn")
        self.takePic_newUser_btn.setFocusPolicy(Qt.NoFocus)
        self.registerNewUser_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "registerNewUser_btn")
        self.registerNewUser_btn.setFocusPolicy(Qt.NoFocus)

        self.nameTextBox = self.mainSelf.findChild(QtWidgets.QLineEdit, "loginUserName_tbox_2")
        self.nameTextBox.textChanged.connect(self.onTextChanged)
        self.emailTextBox = self.mainSelf.findChild(QtWidgets.QLineEdit, "loginUserName_tbox_3")
        self.emailTextBox.textChanged.connect(self.onTextChanged)
        self.passwordTextBox = self.mainSelf.findChild(QtWidgets.QLineEdit, "loginPassword_tbox_2")
        self.passwordTextBox.textChanged.connect(self.onTextChanged)
        self.addressTextBox = self.mainSelf.findChild(QtWidgets.QLineEdit, "loginPassword_tbox_3")
        self.addressTextBox.textChanged.connect(self.onTextChanged)
        self.phoneTextBox = self.mainSelf.findChild(QtWidgets.QLineEdit, "loginUserName_tbox_4")
        self.phoneTextBox.textChanged.connect(self.onTextChanged)
        self.dobTextBox = self.mainSelf.findChild(QtWidgets.QLineEdit, "loginPassword_tbox_4")
        self.dobTextBox.textChanged.connect(self.onTextChanged)
        self.genderTextBox = self.mainSelf.findChild(QtWidgets.QLineEdit, "loginUserName_tbox_5")
        self.genderTextBox.textChanged.connect(self.onTextChanged)
        self.idTextBox = self.mainSelf.findChild(QtWidgets.QLineEdit, "loginUserName_tbox_6")
        self.idTextBox.textChanged.connect(self.onTextChanged)

        self.roleComboBox = self.mainSelf.findChild(QtWidgets.QComboBox, "roleComboBox")
        self.roleComboBox.addItems(['Manager', 'Vice Manager', 'Teacher', 'Student', 'Student Affair'])

    def onTextChanged(self):
        self.registerNewUser_btn.setText('Register')

    def GUI_connect_buttons(self):
        self.newUser_Back_btn.clicked.connect(self.newUser_Back_btn_clicked)
        self.newUser_openImage_btn.clicked.connect(self.open_file_dialog)
        self.takePic_newUser_btn.clicked.connect(self.takePic_newUser_btn_clicked)
        self.registerNewUser_btn.clicked.connect(self.registerNewUser_btn_clicked)

    # ------------------- Buttons Clicked -------------------
    def navigate(self, currnetPage, destinationPage):
        currnetPageObj = self.mainSelf.findChild(QtWidgets.QWidget, currnetPage)
        currnetPageObj.hide()
        destinationPageObj = self.mainSelf.findChild(QtWidgets.QWidget, destinationPage)
        destinationPageObj.show()
        destinationPageObj.raise_()

    def newUser_Back_btn_clicked(self):
        self.isThreadActive = False
        self.liveViewCamera.join()
        self.navigate("newUser_widget", "homeManagerScreen_widget")

    def takePic_newUser_btn_clicked(self):
        self.userImageRegister_Label.hide()
        self.cameraNewUserImage_Label.show()
        self.isThreadActive = False
        self.liveViewCamera.join()
        self.Capture = cv2.VideoCapture(self.mainSelf.configuration.faceIDCameraPort)
        _, Image = self.Capture.read()
        self.userImage = Image
        Image = cv2.flip(Image, 1)
        ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_BGR888)
        Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
        self.cameraNewUserImage_Label.setPixmap(QPixmap.fromImage(Pic))
        self.Capture.release()

    def liveView_worker(self):
        self.isThreadActive = True
        self.Capture = cv2.VideoCapture(self.mainSelf.configuration.faceIDCameraPort)
        while self.isThreadActive:
            _, Image = self.Capture.read()
            Image = cv2.flip(Image, 1)
            ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_BGR888)
            Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
            self.ImageUpdate.emit(Pic)
            # self.cameraNewUserImage_Label.setPixmap(QPixmap.fromImage(Pic))
        self.Capture.release()

    def open_file_dialog(self):
        self.isThreadActive = False
        self.liveViewCamera.join()
        self.cameraNewUserImage_Label.hide()
        self.userImageRegister_Label.show()
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self.mainSelf, "Open File")
        if file_path:
            Image = cv2.imread(file_path)
            self.userImage = Image
            height, width = Image.shape[:2]
            # Set a desired maximum width or height
            max_dimension = 460
            # Calculate the proportional width and height
            if width > height:
                resized_width = max_dimension
                resized_height = int(height * max_dimension / width)
            else:
                resized_height = max_dimension
                resized_width = int(width * max_dimension / height)
            # Resize the image while maintaining the aspect ratio
            Image = cv2.resize(Image, (resized_width, resized_height))
            ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_BGR888)
            Pic = ConvertToQtFormat.scaled(620, 460, Qt.KeepAspectRatio)
            self.userImageRegister_Label.setPixmap(QPixmap.fromImage(Pic))

    def registerNewUser_btn_clicked(self):
        if self.mainSelf.dataBase.isID_exist(self.idTextBox.text()):
            self.registerNewUser_btn.setText("Seat number incorrect \n"
                                             " Type another Seat number that isn't already taken")

        elif self.nameTextBox.text() == '':
            self.registerNewUser_btn.setText("Name can't be empty")

        elif self.emailTextBox.text() == '':
            self.registerNewUser_btn.setText("Email can't be empty")

        elif self.passwordTextBox.text() == '':
            self.registerNewUser_btn.setText("Password can't be empty")

        elif len(self.passwordTextBox.text()) < 6:
            self.registerNewUser_btn.setText("Password is too short \n Should be more than 6 characters")

        elif self.idTextBox.text() == '':
            self.registerNewUser_btn.setText("Seat number can't be empty")

        elif self.addressTextBox.text() == '' or self.genderTextBox.text() == '' or self.phoneTextBox.text() == '' or self.dobTextBox.text() == '':
            self.registerNewUser_btn.setText("Please fill in the missing data")

        else:
            newUser = {'Name': self.nameTextBox.text(), 'Address': self.addressTextBox.text(),
                       'Email': self.emailTextBox.text(),
                       'Password': self.passwordTextBox.text(), 'PhoneNumber': self.phoneTextBox.text(),
                       'Sex': self.genderTextBox.text()}

            self.mainSelf.dataBase.addUser(self.idTextBox.text(), self.roleComboBox.currentIndex() + 1, newUser)
