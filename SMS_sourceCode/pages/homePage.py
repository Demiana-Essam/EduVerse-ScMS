from general_lib import *
from pages.newSessionPage import *
from pages.sessionsHistoryPage import *
from pages.newUserPage import *
from pages.uniformConfigurePage import *
from pages.cameraConfigPage import *
from pages.aboutUsPage import *
from pages.personalInfoPage import *

class homePage():
    currentUser = {'Name': '...'}
    role = 1
    def __init__(self, mainSelf, user, roleID):
        self.mainSelf = mainSelf
        self.currentUser = user
        self.currentUserEmail = user['Email']
        self.role = roleID
        self.GUI_initialize_Objects()
        self.GUI_connect_buttons()
        self._setupPage()
    def GUI_initialize_Objects(self):
        # ------------ Pages ------------
        self.homeManagerScreen_widget = self.mainSelf.findChild(QtWidgets.QWidget, "homeManagerScreen_widget")

        # ------------ Buttons ------------
        # ----- Home page -----
        self.startNewSession_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "startNewSession_btn")
        self.startNewSession_btn.setFocusPolicy(Qt.NoFocus)
        self.sessionsHistory_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "sessionsHistory_btn")
        self.sessionsHistory_btn.setFocusPolicy(Qt.NoFocus)
        self.addNewStudent_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "addNewStudent_btn")
        self.addNewStudent_btn.setFocusPolicy(Qt.NoFocus)
        self.cameraConfigure_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "cameraConfigure_btn")
        self.cameraConfigure_btn.setFocusPolicy(Qt.NoFocus)
        self.uniformConfigure_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "uniformConfigure_btn")
        self.uniformConfigure_btn.setFocusPolicy(Qt.NoFocus)
        self.homeLogout_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "homeLogout_btn")
        self.homeLogout_btn.setFocusPolicy(Qt.NoFocus)
        self.homeAboutUs_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "homeAboutUs_btn")
        self.homeAboutUs_btn.setFocusPolicy(Qt.NoFocus)
        self.personal_Information_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "personal_Information_btn")
        self.personal_Information_btn.setFocusPolicy(Qt.NoFocus)
        # ------------ QLabels ------------
        self.homeUserImage_Label = self.mainSelf.findChild(QtWidgets.QLabel, "homeUserImage_Label")
        self.totalSystemUsers_label = self.mainSelf.findChild(QtWidgets.QLabel, "totalSystemUsers_label")
        self.activeStudents_label = self.mainSelf.findChild(QtWidgets.QLabel, "activeStudents_label")
        self.currentUserNameLabel = self.mainSelf.findChild(QtWidgets.QLabel, "homeUserName_label")
        self.homeRolelabel = self.mainSelf.findChild(QtWidgets.QLabel, "homeJobRole_label")

    def _setupPage(self):
        self.currentUserNameLabel.setText(self.currentUser['Name'])
        self.homeRolelabel.setText(self.mainSelf.dataBase.mapRole(self.role))
        numUsers, numStudents = self.mainSelf.dataBase.getSystem_Statistics()
        self.totalSystemUsers_label.setText(str(numUsers))
        self.activeStudents_label.setText(str(numStudents))

        imagePath = self.currentUserEmail+".jpg"

        if os.path.exists('students_Faces/' + imagePath):
            Image = cv2.imread(f"students_Faces/{imagePath}")
        else:
            Image = cv2.imread(f"blank/person-icon.png")


        if Image is not None:
            height, width = Image.shape[:2]
            # Set a desired maximum width or height
            max_dimension = 100
            # Calculate the proportional width and height
            if width < height:
                resized_width = max_dimension
                resized_height = int(height * max_dimension / width)
            else:
                resized_height = max_dimension
                resized_width = int(width * max_dimension / height)
            # Resize the image while maintaining the aspect ratio
            Image = cv2.resize(Image, (resized_width,resized_height))
            ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_BGR888)
            self.homeUserImage_Label.setPixmap(QPixmap.fromImage(ConvertToQtFormat))

    def GUI_connect_buttons(self):
        self.startNewSession_btn.clicked.connect(self.startNewSession_btn_clicked)
        self.sessionsHistory_btn.clicked.connect(self.sessionsHistory_btn_clicked)
        self.addNewStudent_btn.clicked.connect(self.addNewStudent_btn_clicked)
        self.uniformConfigure_btn.clicked.connect(self.uniformConfigure_btn_clicked)
        self.cameraConfigure_btn.clicked.connect(self.cameraConfigure_btn_clicked)
        self.homeLogout_btn.clicked.connect(self.homeLogout_btn_clicked)
        self.homeAboutUs_btn.clicked.connect(self.homeAboutUs_btn_clicked)
        self.personal_Information_btn.clicked.connect(self.personal_Information_btn_clicked)

    # ------------------- Buttons Clicked -------------------
    def navigate(self, currnetPage, destinationPage):
        currnetPageObj = self.mainSelf.findChild(QtWidgets.QWidget, currnetPage)
        currnetPageObj.hide()
        destinationPageObj = self.mainSelf.findChild(QtWidgets.QWidget, destinationPage)
        destinationPageObj.show()
        destinationPageObj.raise_()

    def startNewSession_btn_clicked(self):
        self.mainSelf.newSessionPage = newSessionPage(self.mainSelf)
        self.navigate("homeManagerScreen_widget", "NewSessionScreen_widget")
    def homeAboutUs_btn_clicked(self):
        self.aboutUsPage = aboutUsPage(self.mainSelf,"Home")
        self.navigate("homeManagerScreen_widget", "aboutUS_widget")
    def personal_Information_btn_clicked(self):
        self.personalInfoPage = personalInfoPage(self.mainSelf,self.currentUser)
        self.navigate("homeManagerScreen_widget", "personalInfo_widget")
    def sessionsHistory_btn_clicked(self):
        self.mainSelf.sessionsHistoryPage = sessionsHistoryPage(self.mainSelf)
        self.navigate("homeManagerScreen_widget", "sessionHistory_widget")
    def addNewStudent_btn_clicked(self):
        print(self.currentUser)
        # if(self.role != 4 ):
        self.newUserPage = newUserPage()
        self.newUserPage.initiate(self.mainSelf)
        self.newUserPage.start()
        self.navigate("homeManagerScreen_widget", "newUser_widget")
    def uniformConfigure_btn_clicked(self):
        self.uniformConfigurePage = uniformConfigurePage(self.mainSelf)
        self.navigate("homeManagerScreen_widget", "uniformConfig_widget")
    def cameraConfigure_btn_clicked(self):
        self.cameraConfigPage = cameraConfigPage()
        self.cameraConfigPage.initiate(self.mainSelf)
        self.cameraConfigPage.start()
        self.navigate("homeManagerScreen_widget", "cameraConfig_widget")
    def homeLogout_btn_clicked(self):
        self.navigate("homeManagerScreen_widget", "welcomeScreen_widget")