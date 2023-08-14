from config import *
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2
from faceRecognation import *
import threading
import time
import datetime
import mediapipe as mp
import numpy as np
import copy
import tensorflow as tf
from dataBase import *
class Cameras_Worker(QThread):
    ImageUpdate = pyqtSignal(QImage)
    def initiate_Session(self, mainSelf):
        self.mainSelf = mainSelf
        self.Capture = cv2.VideoCapture(self.mainSelf.configuration.sessionCameraPort)
        self.all_Students = [[],[],[]]
        self.face_locations = []
        self.LiveView = True
        self.ThreadActive = True
        self.takingAttendance = False
        self.measureAttention=False
        self.fr = FaceRecognition()
        # -------- load Yawn model --------
        self.YawnCNN = tf.keras.models.load_model('YawnModel')
        #-------- Object init --------
        self.sessionTime_label = self.mainSelf.findChild(QLabel, "sessionTime_label")
        self.waitingImage_Label = self.mainSelf.findChild(QLabel, "waitingImage_Label")
        self.waitingImage_Label.hide()
        self.studentsAttendance_tableWidget = self.mainSelf.findChild(QTableWidget, "studentsAttendance_tableWidget")
        self.cameraAttendance_Label = self.mainSelf.findChild(QLabel, "cameraAttendance_Label")
        self.cameraAttendance_Label.show()
        self.currentAvgAttention_label = self.mainSelf.findChild(QLabel, "currentAvgAttention_label")
        # ------------ Icons ------------
        self.breakAnimation_Label = self.mainSelf.findChild(QLabel, "breakAnimation_Label")
        # Load the GIF using QMovie
        self.movie = QMovie("uis/materials/icons/break_animation2.gif", QByteArray(), self.mainSelf)

        # Set the size of the QMovie to be the same as the QLabel
        self.movie.setScaledSize(self.breakAnimation_Label.size())
        self.breakAnimation_Label.setMovie(self.movie)
        self.breakAnimation_Label.hide()
        #-------- Start Session Timer --------
        self.counter = 0
        self.timer = QTimer(self.mainSelf)
        self.timer.timeout.connect(self.update_Timer)
        self.timer.start(1000)

    def run(self):
        # -------- Start Session Threads --------
        self.liveViewCamera = threading.Thread(target=self.liveViewCamera_Worker)
        self.liveViewCamera.start()
        self.attentionCamera = threading.Thread(target=self.track_students_Attention)
        self.attentionCamera.start()

    def SessionCamera_UpdateSlot(self, Image):
        self.cameraAttendance_Label.setPixmap(QPixmap.fromImage(Image))
    def liveViewCamera_Worker(self):
        # scaleFactor = 0.8
        processFrame=0
        while self.ThreadActive:
            while self.LiveView and self.ThreadActive:
                # start = time.time()
                ret, Image = self.Capture.read()
                Image = cv2.flip(Image, 1)
                if processFrame==0:
                    rgb_small_frame = cv2.cvtColor(Image, cv2.COLOR_BGR2RGB)
                    face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
                    if self.measureAttention== False:
                        self.attentionImg = copy.copy(Image)
                        self.face_locations=copy.copy(face_locations)
                        self.measureAttention = True
                for (top, right, bottom, left) in face_locations:
                    # ---------------- Display Detection ------------------
                    cv2.rectangle(Image, (left, top), (right, bottom), (0, 255, 0), 2)
                ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_BGR888)
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
                # self.cameraAttendance_Label.setPixmap(QPixmap.fromImage(Pic))
                processFrame += 1
                if processFrame==4:
                    processFrame=0
                # end = time.time()
                # totalTime = end - start
                # fps = 1 / totalTime
                # if processFrame==1:
                #     print("FPS: ", fps)
            if not self.LiveView and self.takingAttendance and self.ThreadActive:
                self.cameraAttendance_Label.hide()
                self.waitingImage_Label.show()
                self.recordAttendance()
                self.waitingImage_Label.hide()
                self.cameraAttendance_Label.show()
                self.LiveView= True
                self.takingAttendance=False

    def enableAttendanceCamera_Worker(self):
        self.LiveView =False
        self.takingAttendance=True
    def recordAttendance(self):
        for i in range(1):
            ret, frame = self.Capture.read()
            facesLocations ,currentStudents_Names = self.fr.run_recognition(frame)
            for i, student_ID in enumerate(currentStudents_Names):
                if student_ID != 'Unknown':
                    student_Name=self.mainSelf.dataBase.getUserName_ByEmail(student_ID)
                    if student_Name not in self.all_Students[0]:
                        current_time = datetime.datetime.now().time().strftime("%H:%M:%S H/M/S")
                        student_Uniforms_status = self.detect_Student_uniform(frame, facesLocations[i])
                        self.all_Students[0].append(student_Name)
                        self.all_Students[1].append(current_time)
                        self.all_Students[2].append(student_Uniforms_status)
                    else:
                        index = self.all_Students[0].index(student_Name)
                        self.all_Students[2][index] = self.detect_Student_uniform(frame, facesLocations[i])
        self.update_GUI_Tabel()

    def track_students_Attention(self):
        mp_face_mesh = mp.solutions.face_mesh
        face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.avg_attentionLevel = []
        while self.ThreadActive:
            while self.measureAttention and self.ThreadActive :
                unfocusedStudent_Counter=1
                temp_avg_attentionLevel=[]
                for (top, right, bottom, left) in self.face_locations:
                    margen = int((right - left) / 4)
                    roi_color = self.attentionImg[max((top - margen),0):bottom + margen, max((left - margen),0):right + margen]

                    image = cv2.cvtColor(roi_color, cv2.COLOR_BGR2RGB)

                    # ------- Yawn Detection Model -------
                    self.track_students_Yawn(image)

                    image = cv2.resize(image, (128, 128))
                    # image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

                    # To improve performance
                    image.flags.writeable = False
                    # Get the result
                    results = face_mesh.process(image)
                    # To improve performance
                    image.flags.writeable = True
                    # Convert the color space from RGB to BGR
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    img_h, img_w, img_c = image.shape
                    face_3d = []
                    face_2d = []
                    if results.multi_face_landmarks:
                        for idx, lm in enumerate(results.multi_face_landmarks[0].landmark):
                            if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                                if idx == 1:
                                    nose_2d = (lm.x * img_w, lm.y * img_h)
                                    nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 3000)

                                x, y = int(lm.x * img_w), int(lm.y * img_h)

                                # Get the 2D Coordinates
                                face_2d.append([x, y])

                                # Get the 3D Coordinates
                                face_3d.append([x, y, lm.z])

                                # Convert it to the NumPy array
                        face_2d = np.array(face_2d, dtype=np.float64)
                        # Convert it to the NumPy array
                        face_3d = np.array(face_3d, dtype=np.float64)
                        # The camera matrix
                        focal_length = 1 * img_w
                        cam_matrix = np.array([[focal_length, 0, img_h / 2],[0, focal_length, img_w / 2],[0, 0, 1]])
                        # The distortion parameters
                        dist_matrix = np.zeros((4, 1), dtype=np.float64)
                        # Solve PnP
                        success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)
                        # Get rotational matrix
                        rmat, jac = cv2.Rodrigues(rot_vec)
                        # Get angles
                        angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)
                        # Get the y rotation degree
                        x = angles[0] * 360
                        y = angles[1] * 360
                        z = angles[2] * 360

                        # See where the user's head tilting
                        if y < -110:
                            text = "Looking Left"
                        elif y > 110:
                            text = "Looking Right"
                        elif x < -110:
                            text = "Looking Down"
                        elif x > 110:
                            text = "Looking Up"
                        else:
                            text = "Forward"

                        if text =="Forward" or text =="Looking Down":
                            temp_avg_attentionLevel.append(1)
                            self.avg_attentionLevel.append(1)

                        else:
                            temp_avg_attentionLevel.append(0)
                            self.avg_attentionLevel.append(0)

                            # Display the nose direction
                            nose_3d_projection, jacobian = cv2.projectPoints(nose_3d, rot_vec, trans_vec,cam_matrix,dist_matrix)
                            p1 = (int(nose_2d[0]), int(nose_2d[1]))
                            p2 = (int(nose_2d[0] + y * 10), int(nose_2d[1] - x * 10))
                            cv2.line(image, p1, p2, (255, 0, 0), 3)

                            imageLabel_Name_count= 'unfocusedStudentImage_Label_'+str(unfocusedStudent_Counter)
                            unfocusedStudentImage1_Label = self.mainSelf.findChild(QLabel,imageLabel_Name_count)
                            ConvertToQtFormat = QImage(image.data, image.shape[1], image.shape[0],QImage.Format_BGR888)
                            unfocusedStudentImage1_Label.setPixmap(QPixmap.fromImage(ConvertToQtFormat.scaled(128, 128, Qt.KeepAspectRatio)))
                            unfocusedStudent_Counter+=1
                            if unfocusedStudent_Counter==5:
                                unfocusedStudent_Counter=1
                            # cv2.imwrite("extracted_faces/" + str(img_number) + text + ".jpg", image)

                if len(temp_avg_attentionLevel)!=0:
                    temp_avg_attentionLevel =int((sum(temp_avg_attentionLevel) / len(temp_avg_attentionLevel))*100)
                    self.currentAvgAttention_label.setText(str(temp_avg_attentionLevel)+'%')
                time.sleep(1)
                self.measureAttention=False
    def track_students_Yawn(self,face):
        pass
        # # cv2.imwrite("tessst/xad.jpg", face)
        # images = []
        #
        # # image = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
        # image = cv2.resize(face, (224, 224))
        # images.append(image)
        #
        # images = np.array(images, dtype='float32')
        # images = images / 255.
        # results = self.YawnCNN.predict(images)
        #
        # for i in results:
        #     if np.argmax(i) == 0:
        #         print("No Yawn", i[0], '%')
        #     else:
        #         print("Yawn", i[1], '%')

    def detect_Student_uniform(self, frame, facesLocations):
        top = facesLocations[0]
        right = facesLocations[1]
        bottom = facesLocations[2]
        left = facesLocations[3]
        margen = int((right - left) / 2)
        roi_color = frame[bottom + margen:(2*bottom+2*margen-top),max((left - margen), 0):right + margen]
        height, width, _ = np.shape(roi_color)
        if height ==0 or width == 0:
            return False

        data = np.reshape(roi_color, (height * width, 3))
        data = np.float32(data)

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        _, _, centers = cv2.kmeans(data, self.mainSelf.configuration.clustersNumber, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

        bar = np.zeros((1, 1, 3), np.uint8)
        bar[:] = centers[0]
        hsv = cv2.cvtColor(bar, cv2.COLOR_BGR2HSV)
        # Split the HSV image into its channels
        h, s, v = cv2.split(hsv)
        print(hsv[0][0][0])

        if hsv[0][0][0]>= self.mainSelf.configuration.uniformColorRange[0] and hsv[0][0][0]<= self.mainSelf.configuration.uniformColorRange[1]:
            return True
        else:
            return False

    def update_GUI_Tabel(self):
        self.studentsAttendance_tableWidget.setRowCount(0)
        for i in range(len(self.all_Students[0])):
            # Get the current number of rows & Add a new row
            row = self.studentsAttendance_tableWidget.rowCount()
            self.studentsAttendance_tableWidget.insertRow(row)

            # Add student_data to the new row
            student_data = [self.all_Students[0][i],self.all_Students[1][i],self.all_Students[2][i]]
            for i, item in enumerate(student_data):
                table_item = QTableWidgetItem(str(item))
                # set Uniform statue text color
                if i == 2 and item == True:
                    table_item.setForeground(QBrush(QColor(255, 255, 255)))
                    table_item.setBackground(QBrush(QColor(33, 140, 116,160)))
                elif i == 2 and item == False:
                    table_item.setForeground(QBrush(QColor(255, 255, 255)))
                    table_item.setBackground(QBrush(QColor(229, 108, 120,200)))
                self.studentsAttendance_tableWidget.setItem(row, i, table_item)

    def update_Timer(self):
        self.counter += 1
        hours, remainder = divmod(self.counter, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.sessionTime_label.setText('Session time elapsed: {}:{:02d}:{:02d}'.format(hours, minutes, seconds))

    def end_Session(self):
        # deActive camera thread and release resources
        self.timer.stop()
        self.ThreadActive = False
        self.liveViewCamera.join()
        self.Capture.release()
        cv2.destroyAllWindows()









