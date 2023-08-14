from general_lib import *
from cameras import *

class newSessionPage():
    def __init__(self,mainSelf):
        self.mainSelf = mainSelf

        self.GUI_initialize_Objects()
        self.GUI_connect_buttons()
        self.start_NewSession()

    def GUI_initialize_Objects(self):
        # ------------ Pages ------------
        self.NewSessionScreen_widget = self.mainSelf.findChild(QtWidgets.QWidget, "NewSessionScreen_widget")
        self.sessionComponentContainer_widget = self.mainSelf.findChild(QtWidgets.QWidget,"sessionComponentContainer_widget")
        # self.sessionComponentContainer_widget.raise_()

        # ------------ Camera Label ------------
        self.cameraAttendance_Label = self.mainSelf.findChild(QLabel, "cameraAttendance_Label")

        # ------------ Buttons ------------
        # ----- New Session page -----
        self.attendanceRecord_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "attendanceRecord_btn")
        self.attendanceRecord_btn.setFocusPolicy(Qt.NoFocus)
        self.startBreak_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "startBreak_btn")
        self.startBreak_btn.setFocusPolicy(Qt.NoFocus)
        self.endSession_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "endSession_btn")
        self.endSession_btn.setFocusPolicy(Qt.NoFocus)
        # ------------ Tabel ------------
        self.studentsAttendance_tableWidget = self.mainSelf.findChild(QtWidgets.QTableWidget, "studentsAttendance_tableWidget")
        self.studentsAttendance_tableWidget.setColumnWidth(0, 200)

    def GUI_connect_buttons(self):
        self.endSession_btn.clicked.connect(self.endSession_btn_clicked)
        self.attendanceRecord_btn.clicked.connect(self.attendanceRecord_btn_clicked)
        self.startBreak_btn.clicked.connect(self.startBreak_btn_clicked)

    #------------ Session ------------
    #----- Camera Thread -----
    def start_NewSession(self):
        self.sessionCameras_Worker = Cameras_Worker()
        self.sessionCameras_Worker.initiate_Session(self.mainSelf)
        self.sessionCameras_Worker.start()
        self.sessionCameras_Worker.ImageUpdate.connect(self.LiveViewCamera_UpdateSlot)

    def LiveViewCamera_UpdateSlot(self, Image):
        self.cameraAttendance_Label.setPixmap(QPixmap.fromImage(Image))

    # ------------------- Buttons Clicked -------------------
    def attendanceRecord_btn_clicked(self):
        # check if the system in break mode, Continue the session first
        if not self.sessionCameras_Worker.LiveView:
            self.startBreak_btn_clicked()
        self.sessionCameras_Worker.enableAttendanceCamera_Worker()

    def startBreak_btn_clicked(self):
        if self.sessionCameras_Worker.LiveView:
            self.sessionCameras_Worker.cameraAttendance_Label.hide()
            # self.sessionCameras_Worker.waitingImage_Label.show()
            self.sessionCameras_Worker.movie.start()
            self.sessionCameras_Worker.breakAnimation_Label.show()
            self.sessionCameras_Worker.LiveView=False
            self.sessionCameras_Worker.measureAttention=False
            self.startBreak_btn.setText(" Continue")
        else:
            self.sessionCameras_Worker.LiveView = True
            self.startBreak_btn.setText(" Start a break")
            self.sessionCameras_Worker.waitingImage_Label.hide()
            self.sessionCameras_Worker.movie.stop()
            self.sessionCameras_Worker.breakAnimation_Label.hide()
            self.sessionCameras_Worker.cameraAttendance_Label.show()

    def navigate(self, currnetPage, destinationPage):
        currnetPageObj = self.mainSelf.findChild(QtWidgets.QWidget, currnetPage)
        currnetPageObj.hide()
        destinationPageObj = self.mainSelf.findChild(QtWidgets.QWidget, destinationPage)
        destinationPageObj.show()
        destinationPageObj.raise_()

    def endSession_btn_clicked(self):
        self.sessionCameras_Worker.end_Session()
        # Calculate session statistics & display Charts
        self.mainSelf.sessionChartsPage.displayCharts(self.sessionCameras_Worker)


