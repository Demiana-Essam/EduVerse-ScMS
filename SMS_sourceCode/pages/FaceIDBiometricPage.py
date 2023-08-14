from general_lib import *
from config import *
from pages.homePage import homePage
from PyQt5.QtCore import QTimer
from faceRecognation import *
import cv2

class FaceIDBiometric():
    def __init__(self, mainSelf):
        self.mainSelf = mainSelf

        self.GUI_initialize_Objects()
        self.GUI_connect_buttons()
        self.fr = FaceRecognition()

    def GUI_initialize_Objects(self):
        # ------------ Pages ------------
        self.faceID_widget = self.mainSelf.findChild(QtWidgets.QWidget, "faceID_widget")
        # ------------ Icons ------------
        self.fingerPrintIcon_Label = self.mainSelf.findChild(QtWidgets.QWidget, "breakAnimation_Label_3")
        # Load the GIF using QMovie
        self.movie = QMovie("uis/materials/icons/wired-lineal-1021-rules.gif", QByteArray(), self.mainSelf)
        # Set the size of the QMovie to be the same as the QLabel
        self.movie.setScaledSize(self.fingerPrintIcon_Label.size())
        self.fingerPrintIcon_Label.setMovie(self.movie)
        self.movie.start()
        # ------------ Buttons ------------
        # ----- Face ID page -----
        self.faceID_Back_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "faceID_Back_btn")
        self.faceID_Back_btn.setFocusPolicy(Qt.NoFocus)
        self.tryAgain_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "tryAgain_btn")
        self.tryAgain_btn.setFocusPolicy(Qt.NoFocus)
        # -------- Start Session Timer --------
        self.counter = 0
        self.timer = QTimer(self.mainSelf)
        self.timer.timeout.connect(self.update_Timer)
        self.timer.start(1000)


    def GUI_connect_buttons(self):
        self.faceID_Back_btn.clicked.connect(self.faceID_Back_btn_clicked)
        self.tryAgain_btn.clicked.connect(self.tryAgain_btn_clicked)

    # ------------------- Buttons Clicked -------------------
    def navigate(self, currnetPage, destinationPage):
        currnetPageObj = self.mainSelf.findChild(QtWidgets.QWidget, currnetPage)
        currnetPageObj.hide()
        destinationPageObj = self.mainSelf.findChild(QtWidgets.QWidget, destinationPage)
        destinationPageObj.show()
        destinationPageObj.raise_()

    def faceID_Back_btn_clicked(self):
        self.navigate("faceID_widget", "loginScreen_widget")

    def tryAgain_btn_clicked(self):
        self.tryAgain_btn.setText("Waiting...")
        self.tryAgain_btn.setStyleSheet('''
                    QPushButton{
                    background-color: rgb(235, 168, 105);
                    color: rgb(255, 255, 255);
                    border-radius:20px;
                    }
                    
                    QPushButton:hover{
                    background-color: rgba(245, 178, 115,210);
                    }
                    
                    QPushButton:pressed{
                    padding-left:5px;
                    padding-top:5px;
                    background-color: rgba(245, 178, 115,210);
                    }
                    ''')
        self.counter=0
        self.timer.start(1000)
        self.movie.start()

    def update_Timer(self):
        self.counter += 1
        if self.counter==3:
            self.faceID_recognize()
            self.movie.stop()
            self.movie.jumpToFrame(0)
            self.timer.stop()

    def faceID_recognize(self):
        Capture = cv2.VideoCapture(self.mainSelf.configuration.faceIDCameraPort)
        _, frame = Capture.read()
        _, names = self.fr.run_recognition(frame)

        for name in names:
            if name!= "Unknown":
                self.login_handling(name)
                break
        if len(names) == 0 or names[0]=="Unknown":
            self.tryAgain_btn.setText("Try again")
            self.tryAgain_btn.setStyleSheet('''
            QPushButton{
            background-color: rgb(229, 108, 120);
                color: rgb(230, 230, 230);
            border-radius:20px;
            }

            QPushButton:hover{
            background-color: rgba(229, 108, 120,220);
            }

            QPushButton:pressed{
            padding-left:5px;
            padding-top:5px;
            background-color: rgba(229, 108, 120,220);
            }
            ''')

    # ------------------- Login Handler -------------------
    def login_handling(self, userFace):
        # Create an object of Home Page
        user, id = self.mainSelf.dataBase.getUser(userFace)
        self.homePage = homePage(self.mainSelf, user, id)

        self.navigate("loginScreen_widget", "homeManagerScreen_widget")