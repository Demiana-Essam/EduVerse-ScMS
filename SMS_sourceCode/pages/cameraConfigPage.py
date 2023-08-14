from general_lib import *
from config import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2
import threading

class cameraConfigPage(QThread):
    ImageUpdate_FaceID = pyqtSignal(QImage)
    ImageUpdate_Session = pyqtSignal(QImage)
    def initiate(self, mainSelf):
        self.mainSelf = mainSelf
        self.GUI_initialize_Objects()
        self.GUI_connect_buttons()
        # self.liveViewCamera = threading.Thread(target=self.liveView_worker)
        # self.liveViewCamera.start()

    def run(self):
        self.isThreadActive = True
        self.currentSessionPort = self.mainSelf.configuration.sessionCameraPort
        self.currentFaceIDPort = self.mainSelf.configuration.faceIDCameraPort
        self.liveViewCamera = threading.Thread(target=self.liveView_worker)
        self.liveViewCamera.start()
        self.ImageUpdate_FaceID.connect(self.ImageUpdate_FaceID_UpdateSlot)
        self.ImageUpdate_Session.connect(self.ImageUpdate_Session_UpdateSlot)
    def ImageUpdate_FaceID_UpdateSlot(self, Image):
        self.loginCameraConfig_Label.setPixmap(QPixmap.fromImage(Image))
    def ImageUpdate_Session_UpdateSlot(self, Image):
        self.sessionCameraConfig_Label.setPixmap(QPixmap.fromImage(Image))
    def GUI_initialize_Objects(self):
        # ------------ Pages ------------
        self.cameraConfig_widget = self.mainSelf.findChild(QtWidgets.QWidget, "cameraConfig_widget")
        # ------------ Objects ------------
        self.sessionCameraConfig_Label = self.mainSelf.findChild(QtWidgets.QLabel, "sessionCameraConfig_Label")
        self.loginCameraConfig_Label = self.mainSelf.findChild(QtWidgets.QLabel, "loginCameraConfig_Label")
        # ------------ Buttons ------------
        self.cameraConfig_Back_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "cameraConfig_Back_btn")
        self.cameraConfig_Back_btn.setFocusPolicy(Qt.NoFocus)

        self.changeSessionCamera_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "changeSessionCamera_btn")
        self.changeSessionCamera_btn.setFocusPolicy(Qt.NoFocus)
        self.changeLoginCamera_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "changeLoginCamera_btn")
        self.changeLoginCamera_btn.setFocusPolicy(Qt.NoFocus)
        self.cameraConfig_save_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "cameraConfig_save_btn")
        self.cameraConfig_save_btn.setFocusPolicy(Qt.NoFocus)
    def GUI_connect_buttons(self):
        self.cameraConfig_Back_btn.clicked.connect(self.cameraConfig_Back_btn_clicked)
        self.changeSessionCamera_btn.clicked.connect(self.changeSessionCamera_btn_clicked)
        self.changeLoginCamera_btn.clicked.connect(self.changeLoginCamera_btn_clicked)
        self.cameraConfig_save_btn.clicked.connect(self.cameraConfig_save_btn_clicked)
    def navigate(self, currnetPage, destinationPage):
        currnetPageObj = self.mainSelf.findChild(QtWidgets.QWidget, currnetPage)
        currnetPageObj.hide()
        destinationPageObj = self.mainSelf.findChild(QtWidgets.QWidget, destinationPage)
        destinationPageObj.show()
        destinationPageObj.raise_()
    def cameraConfig_Back_btn_clicked(self):
        self.isThreadActive = False
        self.liveViewCamera.join()
        self.mainSelf.configuration.changeCamerasPorts(sessionPort=self.currentSessionPort, faceIDPort=self.currentFaceIDPort)
        self.navigate("cameraConfig_widget", "homeManagerScreen_widget")
    def changeSessionCamera_btn_clicked(self):
        self.isThreadActive=False
        self.liveViewCamera.join()
        self.mainSelf.configuration.switchCameras(isSession=True)
        self.isThreadActive = True
        self.liveViewCamera = threading.Thread(target=self.liveView_worker)
        self.liveViewCamera.start()
    def changeLoginCamera_btn_clicked(self):
        self.isThreadActive = False
        self.liveViewCamera.join()
        self.mainSelf.configuration.switchCameras(isSession=False)
        self.isThreadActive = True
        self.liveViewCamera = threading.Thread(target=self.liveView_worker)
        self.liveViewCamera.start()
    def cameraConfig_save_btn_clicked(self):
        self.isThreadActive = False
        self.liveViewCamera.join()
        self.navigate("cameraConfig_widget", "homeManagerScreen_widget")
    def liveView_worker(self):
        if self.mainSelf.configuration.sessionCameraPort == self.mainSelf.configuration.faceIDCameraPort:
            self.Capture = cv2.VideoCapture(self.mainSelf.configuration.sessionCameraPort)
            while self.isThreadActive:
                _, Image = self.Capture.read()
                ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_BGR888)
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate_FaceID.emit(Pic)
                self.ImageUpdate_Session.emit(Pic)

                # self.sessionCameraConfig_Label.setPixmap(QPixmap.fromImage(Pic))
                # self.loginCameraConfig_Label.setPixmap(QPixmap.fromImage(Pic))
            self.Capture.release()
        else:
            self.CaptureSession = cv2.VideoCapture(self.mainSelf.configuration.sessionCameraPort)
            self.CaptureFaceID = cv2.VideoCapture(self.mainSelf.configuration.faceIDCameraPort)
            while self.isThreadActive:
                _, Image = self.CaptureSession.read()
                ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_BGR888)
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate_Session.emit(Pic)
                # self.sessionCameraConfig_Label.setPixmap(QPixmap.fromImage(Pic))

                _, Image2 = self.CaptureFaceID.read()
                ConvertToQtFormat2 = QImage(Image2.data, Image2.shape[1], Image2.shape[0], QImage.Format_BGR888)
                Pic2 = ConvertToQtFormat2.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate_FaceID.emit(Pic2)
                # self.loginCameraConfig_Label.setPixmap(QPixmap.fromImage(Pic2))
            self.CaptureSession.release()
            self.CaptureFaceID.release()