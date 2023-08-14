from general_lib import *
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QImage,QPixmap
import cv2
import os
class personalInfoPage():
    def __init__(self, mainSelf, userInfo):
        self.mainSelf = mainSelf
        self.userInfo = userInfo
        self.GUI_initialize_Objects()
        self.GUI_connect_buttons()
        self.fill_UserInfo()

    def GUI_initialize_Objects(self):
        # ------------ Pages ------------
        self.personalInfo_widget = self.mainSelf.findChild(QtWidgets.QWidget, "personalInfo_widget")
        # ------------ QLineEdit ------------
        self.updateUserName_tbox = self.mainSelf.findChild(QtWidgets.QLineEdit, "updateUserName_tbox")
        self.updateLoginPassword_tbox = self.mainSelf.findChild(QtWidgets.QLineEdit, "updateLoginPassword_tbox")
        self.updatePhoneNumber_tbox = self.mainSelf.findChild(QtWidgets.QLineEdit, "updatePhoneNumber_tbox")
        self.updateAddress_tbox = self.mainSelf.findChild(QtWidgets.QLineEdit, "updateAddress_tbox")

        self.BOG_dateEdit = self.mainSelf.findChild(QtWidgets.QDateEdit, "BOG_dateEdit")
        self.updateUserImageRegister_Label = self.mainSelf.findChild(QtWidgets.QLabel, "updateUserImageRegister_Label")
        self.updateCameraNewUserImage_Label = self.mainSelf.findChild(QtWidgets.QLabel, "updateCameraNewUserImage_Label")
        self.updateCameraNewUserImage_Label.hide()
        # ------------ Buttons ------------
        self.personalInfo_Back_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "personalInfo_Back_btn")
        self.personalInfo_Back_btn.setFocusPolicy(Qt.NoFocus)
        self.personalInfo_save_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "personalInfo_save_btn")
        self.personalInfo_save_btn.setFocusPolicy(Qt.NoFocus)
        self.personalInfo_openImage_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "personalInfo_openImage_btn")
        self.personalInfo_openImage_btn.setFocusPolicy(Qt.NoFocus)

    def GUI_connect_buttons(self):
        self.personalInfo_Back_btn.clicked.connect(self.personalInfo_Back_btn_clicked)
        self.personalInfo_save_btn.clicked.connect(self.personalInfo_save_btn_clicked)
        self.personalInfo_openImage_btn.clicked.connect(self.open_file_dialog)
    def fill_UserInfo(self):
        #--------- Fill Text Values ----------
        self.updateUserName_tbox.setText(self.userInfo['Name'])
        self.updateLoginPassword_tbox.setText(str(self.userInfo['Password']))
        self.updatePhoneNumber_tbox.setText(str(self.userInfo['PhoneNumber']))
        self.updateAddress_tbox.setText(str(self.userInfo['Address']))
        day, month, year = map(int, str(self.userInfo['DOB']).split('/'))
        date = QDate(year, month, day)
        self.BOG_dateEdit.setDate(date)
        # --------- Fill User Image ----------
        imagePath = self.userInfo['Email']+".jpg"
        if os.path.exists('students_Faces/' + imagePath):
            Image = cv2.imread(f"students_Faces/{imagePath}")
        else:
            Image = cv2.imread(f"blank/person-icon.png")

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
        self.updateUserImageRegister_Label.setPixmap(QPixmap.fromImage(Pic))

    # ------------------- Buttons Clicked -------------------
    def navigate(self, currnetPage, destinationPage):
        currnetPageObj = self.mainSelf.findChild(QtWidgets.QWidget, currnetPage)
        currnetPageObj.hide()
        destinationPageObj = self.mainSelf.findChild(QtWidgets.QWidget, destinationPage)
        destinationPageObj.show()
        destinationPageObj.raise_()

    def personalInfo_save_btn_clicked(self):
        #-------- Update Image ---------
        imagePath = self.userInfo['Email'] + ".jpg"
        #cv2.imwrite(f"students_Faces/{imagePath}", img)
        # -------- Update User Data ---------
        selected_date = self.BOG_dateEdit.date()

        day = str(selected_date.day())
        month = str(selected_date.month())
        year = str(selected_date.year())
        date = day + "/" + month + "/" + year

        #------------- Fill the Dictionary with needed data then push --------------
        self.updateUserName_tbox.text()
        self.updateLoginPassword_tbox.text()
        self.updatePhoneNumber_tbox.text()
        self.updateAddress_tbox.text()
        updatedUserData={

        }

        self.navigate("personalInfo_widget", "homeManagerScreen_widget")

    def open_file_dialog(self):
        # self.isThreadActive = False
        # self.liveViewCamera.join()
        self.updateCameraNewUserImage_Label.hide()
        self.updateUserImageRegister_Label.show()
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
            self.updateUserImageRegister_Label.setPixmap(QPixmap.fromImage(Pic))

    def personalInfo_Back_btn_clicked(self):
        self.navigate("personalInfo_widget", "homeManagerScreen_widget")
