from general_lib import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QVBoxLayout, QTableWidgetItem
from PyQt5.QtChart import QChart, QChartView, QPieSeries
from datetime import datetime
class sessionChartsPage():
    def __init__(self, mainSelf):
        self.mainSelf = mainSelf

        self.GUI_initialize_Objects()
        self.GUI_connect_buttons()
        self.create_Chart()

    def GUI_initialize_Objects(self):
        # ------------ Pages ------------
        self.sessionReportScreen_widget = self.mainSelf.findChild(QtWidgets.QWidget, "sessionReportScreen_widget")

        # ------------ Charts ------------
        self.mainSelf.unifromPieChartwidget = self.mainSelf.findChild(QtWidgets.QWidget, "unifromPieChartwidget")

        # ------------ Labels ------------
        self.averageAttentionLevel_label = self.mainSelf.findChild(QtWidgets.QLabel, "averageAttentionLevel_label")
        self.numOfStudents_label = self.mainSelf.findChild(QtWidgets.QLabel, "numOfStudents_label")
        self.reportSessionTime_label = self.mainSelf.findChild(QtWidgets.QLabel, "reportSessionTime_label")

        # ------------ Tabel ------------
        self.reportAttendance_tableWidget = self.mainSelf.findChild(QtWidgets.QTableWidget,"reportAttendance_tableWidget")
        self.reportAttendance_tableWidget.setColumnWidth(0, 170)

        # ------------ Buttons ------------
        self.save_backHome_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "save_backHome_btn")
        self.save_backHome_btn.setFocusPolicy(Qt.NoFocus)
        self.reportSave_exit_btn = self.mainSelf.findChild(QtWidgets.QPushButton, "reportSave_exit_btn")
        self.reportSave_exit_btn.setFocusPolicy(Qt.NoFocus)

    def GUI_connect_buttons(self):
        self.save_backHome_btn.clicked.connect(self.save_backHome_btn_clicked)
        self.reportSave_exit_btn.clicked.connect(self.reportSave_exit_btn_clicked)

    def create_Chart(self):
        # prepare Fonts
        labelFont = QFont()
        labelFont.setPointSize(8)
        labelFont.setFamily("Poppins Medium")
        titleFont = QFont()
        titleFont.setPointSize(14)
        titleFont.setFamily("Poppins Medium")

        # prepare dataContainer
        self.series = QPieSeries()
        self.series.setHoleSize(0.50)

        Uniform_Item = self.series.append("In Uniform: " + str(0), 0)
        Uniform_Item.setLabelVisible(True)
        Uniform_Item.setLabelFont(labelFont)

        NotInUniform_item = self.series.append("Not in Uniform: " + str(0), 0)
        NotInUniform_item.setExploded(True)
        NotInUniform_item.setLabelVisible(True)
        NotInUniform_item.setLabelFont(labelFont)

        # Create Chart
        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.setTitleFont(titleFont)

        # Create Chart Viewer
        self.chartView = QChartView(self.chart)
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.chartView)
        self.mainSelf.unifromPieChartwidget.setLayout(self.vbox)

    def displayCharts(self, sessionInfo):
        self.sessionInfo=sessionInfo
        self.sessionReportScreen_widget.show()
        self.sessionReportScreen_widget.raise_()

        # prepare Data
        self.reportSessionTime_label.setText(self.sessionInfo.sessionTime_label.text())
        if(len(self.sessionInfo.all_Students[2])):
            self.avg_attentionLevel = int((sum(self.sessionInfo.avg_attentionLevel) / len(self.sessionInfo.avg_attentionLevel))*100)
            self.averageAttentionLevel_label.setText(str(self.avg_attentionLevel)+'%')
        else:
            self.avg_attentionLevel = 0
            self.averageAttentionLevel_label.setText(str(self.avg_attentionLevel) + '%')

        # Display & Count the number of students
        self.numOfStudents_label.setText(str(len(sessionInfo.all_Students[0])))
        self.fill_GUI_Tabel(sessionInfo)

        uniformCount=0
        notInUniformCount = 0
        for student_In_Uniform in self.sessionInfo.all_Students[2]:
            if student_In_Uniform:
                uniformCount+=1
            else:
                notInUniformCount+=1

        # Clear Previous Items
        self.series.clear()
        # New: Uniform Item
        self.series.append("In Uniform: " + str(uniformCount), uniformCount)
        # New: Not In Uniform item
        self.series.append("Not in Uniform: " + str(notInUniformCount), notInUniformCount)

        slice = self.series.slices()[0]
        slice.setBrush(QColor(33, 140, 116,160))
        slice = self.series.slices()[1]
        slice.setBrush(QColor(229, 108, 120,200))

    def fill_GUI_Tabel(self, sessionInfo):
        self.reportAttendance_tableWidget.setRowCount(0)
        for i in range(len(sessionInfo.all_Students[0])):
            # Get the current number of rows & Add a new row
            row = self.reportAttendance_tableWidget.rowCount()
            self.reportAttendance_tableWidget.insertRow(row)

            # Add student_data to the new row
            student_data = [sessionInfo.all_Students[0][i],sessionInfo.all_Students[1][i],sessionInfo.all_Students[2][i]]
            for i, item in enumerate(student_data):
                table_item = QTableWidgetItem(str(item))
                # set Uniform statue text color
                if i == 2 and item == True:
                    table_item.setForeground(QBrush(QColor(255, 255, 255)))
                    table_item.setBackground(QBrush(QColor(33, 140, 116,160)))
                elif i == 2 and item == False:
                    table_item.setForeground(QBrush(QColor(255, 255, 255)))
                    table_item.setBackground(QBrush(QColor(229, 108, 120,200)))
                self.reportAttendance_tableWidget.setItem(row, i, table_item)

    # ------------------- Buttons Clicked -------------------
    def navigate(self, currnetPage, destinationPage):
        currnetPageObj = self.mainSelf.findChild(QtWidgets.QWidget, currnetPage)
        currnetPageObj.hide()
        destinationPageObj = self.mainSelf.findChild(QtWidgets.QWidget, destinationPage)
        destinationPageObj.show()
        destinationPageObj.raise_()

    def save_backHome_btn_clicked(self):
        self.navigate("NewSessionScreen_widget", "homeManagerScreen_widget")
        self.storeSessionInfo_in_dataBase()
        self.sessionInfo.studentsAttendance_tableWidget.setRowCount(0)
        self.sessionInfo.sessionTime_label.setText('Session time elapsed: 0:00:00')

    def reportSave_exit_btn_clicked(self):
        self.storeSessionInfo_in_dataBase()
        self.mainSelf.close()
    def storeSessionInfo_in_dataBase(self):
        sessionInfo={
            'sessionAttendanceInfo': self.sessionInfo.all_Students,
            'subject':'ML',
            'date':str(datetime.now()),
            'sessionDuration': str(self.sessionInfo.sessionTime_label.text()),
            'avgAttentionLevel':self.avg_attentionLevel
        }
        self.mainSelf.dataBase.db.child("Sessions").push(sessionInfo)