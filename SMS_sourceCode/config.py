from dataBase import *
import cv2
class config():
    def __init__(self, mainSelf, uniformColorRange=[160,180], clustersNumber = 1, cameraPort ={'session':0, 'faceID':0}):
        self.mainSelf = mainSelf
        # --------------- Uniform Configuration ---------------
        uniformConfig_results=self.mainSelf.dataBase.db.child("Configuration").child("UniformConfig").get()
        if uniformConfig_results.val() is not None:
            self.clustersNumber =uniformConfig_results.val()['clustersNumber']
            self.uniformColorRange=uniformConfig_results.val()['ColorRange']
        else:
            self.clustersNumber = clustersNumber
            self.uniformColorRange = uniformColorRange
        # --------------- Camera Configuration ---------------
        self.numOfCameras = self.get_available_cameras()
        cameraConfig_results = self.mainSelf.dataBase.db.child("Configuration").child("CameraConfig").get()
        if cameraConfig_results.val() is not None:
            sessionCameraPort=cameraConfig_results.val()['cameraPort']['session']
            faceIDCameraPort=cameraConfig_results.val()['cameraPort']['faceID']

            if sessionCameraPort<len(self.numOfCameras):
                self.sessionCameraPort = sessionCameraPort
            else:
                self.sessionCameraPort =0
            if faceIDCameraPort<len(self.numOfCameras):
                self.faceIDCameraPort = faceIDCameraPort
            else:
                self.faceIDCameraPort =0
        else:
            self.sessionCameraPort=cameraPort['session']
            self.faceIDCameraPort=cameraPort['faceID']

    def get_available_cameras(self):
        available_cameras = []
        index = 0
        while True:
            cap = cv2.VideoCapture(index)
            if not cap.read()[0]:
                break
            else:
                available_cameras.append(index)
            cap.release()
            index += 1
        return available_cameras

    def switchCameras(self, isSession):
        if isSession:
            cameraPort = (self.sessionCameraPort+1) % len(self.numOfCameras)
            self.sessionCameraPort = cameraPort
            self.mainSelf.dataBase.db.child("Configuration").child("CameraConfig").set({'cameraPort': {'session':cameraPort, 'faceID':self.faceIDCameraPort}})
        else:
            cameraPort = (self.faceIDCameraPort + 1) % len(self.numOfCameras)
            self.faceIDCameraPort = cameraPort
            self.mainSelf.dataBase.db.child("Configuration").child("CameraConfig").set({'cameraPort': {'session': self.sessionCameraPort, 'faceID': cameraPort}})
    def changeCamerasPorts(self,sessionPort,faceIDPort):
        self.sessionCameraPort = sessionPort
        self.faceIDCameraPort = faceIDPort
        self.mainSelf.dataBase.db.child("Configuration").child("CameraConfig").set({'cameraPort': {'session': sessionPort, 'faceID': faceIDPort}})
    def changeUniformColor(self,mainUniformColor_tbox, seccondUniformColor_tbox_tbox):
        if seccondUniformColor_tbox_tbox =='':
            clustersNumber=1
            uniformColorRange=[int(mainUniformColor_tbox)-7,int(mainUniformColor_tbox)+7]
        else:
            clustersNumber = 2
            uniformColorRange = [int(mainUniformColor_tbox) - 7, int(mainUniformColor_tbox) + 7,
                                 int(seccondUniformColor_tbox_tbox) - 7, int(seccondUniformColor_tbox_tbox) + 7]
        self.uniformColorRange=uniformColorRange
        self.clustersNumber=clustersNumber
        data ={
        'clustersNumber': clustersNumber,
        'ColorRange': uniformColorRange
        }
        self.mainSelf.dataBase.db.child("Configuration").child("UniformConfig").set(data)