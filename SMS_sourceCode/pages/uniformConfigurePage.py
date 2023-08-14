from general_lib import *
from config import *

class uniformConfigurePage():
    def __init__(self, mainSelf):
        self.mainSelf = mainSelf

        self.GUI_initialize_Objects()
        self.GUI_connect_buttons()

    def GUI_initialize_Objects(self):
        # ------------ Pages ------------
        self.newUser_widget = self.mainSelf.findChild(QtWidgets.QWidget, "uniformConfig_widget")
        # ------------ Objects ------------
        self.HSV_Colors_Container_widget = self.mainSelf.findChild(QtWidgets.QWidget, "HSV_Colors_Container_widget")
        self.mainUniformColor_tbox = self.mainSelf.findChild(QtWidgets.QLineEdit, "mainUniformColor_tbox")
        self.seccondUniformColor_tbox_tbox = self.mainSelf.findChild(QtWidgets.QLineEdit, "seccondUniformColor_tbox_tbox")
        # self.mainUniformColor_tbox.enterEvent = self.show_tooltip
        # self.mainUniformColor_tbox.leaveEvent = self.hide_tooltip
        # ------------ Buttons ------------
        self.uniformConfig_Back_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "uniformConfig_Back_btn")
        self.uniformConfig_Back_btn.setFocusPolicy(Qt.NoFocus)
        self.unifromConfig_Save_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "unifromConfig_Save_btn")
        self.unifromConfig_Save_btn.setFocusPolicy(Qt.NoFocus)

    def GUI_connect_buttons(self):
        self.uniformConfig_Back_btn.clicked.connect(self.uniformConfig_Back_btn_clicked)
        self.unifromConfig_Save_btn.clicked.connect(self.unifromConfig_Save_btn_clicked)


    # ------------------- Buttons Clicked -------------------
    def navigate(self, currnetPage, destinationPage):
        currnetPageObj = self.mainSelf.findChild(QtWidgets.QWidget, currnetPage)
        currnetPageObj.hide()
        destinationPageObj = self.mainSelf.findChild(QtWidgets.QWidget, destinationPage)
        destinationPageObj.show()
        destinationPageObj.raise_()

    def uniformConfig_Back_btn_clicked(self):
        self.mainUniformColor_tbox.setText('')
        self.seccondUniformColor_tbox_tbox.setText('')
        self.navigate("uniformConfig_widget", "homeManagerScreen_widget")
    def unifromConfig_Save_btn_clicked(self):
        self.mainSelf.configuration.changeUniformColor(self.mainUniformColor_tbox.text(), self.seccondUniformColor_tbox_tbox.text())
        self.navigate("uniformConfig_widget", "homeManagerScreen_widget")