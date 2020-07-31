from datetime import datetime
import cv2
import numpy as np
import time
import threading
from PIL import Image
from PIL import ImageTk
from CameraFileNameHandler import CameraFileNameHandler
class Camera:
    frameRate = 15
    kSize = 3
    scaleFactor = 0.5
    bmovementDetected = False
    brecording = False
    cRecoringTime = 0

    def __init__(self, device):
        global filenameHandler
        self.capture = cv2.VideoCapture(device)
        ret, frame = self.readFrame(self.capture)
        ret, previousFrame = self.readFrame(self.capture)
        self.filenameHandler = CameraFileNameHandler(frame)
        self.thread = threading.Thread(target=self.mainloop, args=( previousFrame, frame, ret))
        self.thread.start()

    def mainloop(self, previousFrame, frame, ret):
        self.exitFlag = False
        while not self.exitFlag:
            time.sleep(0.01)
            try:
                previousFrame = frame
                ret, frame = self.readFrame(self.capture)
                bluredFrame, bluredPreviousFrame = self.prepareFrame(frame, previousFrame)
                differenceImage = self.subs(bluredPreviousFrame, bluredFrame)
                self.detectMovement(differenceImage)
                frameToRecord = self.addTimeToFrame(frame)
                #cv2.imshow("frame", frameToRecord)
                self.Img = frameToRecord
                self.record(frameToRecord)
                if cv2.waitKey(int(1000/self.frameRate)) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    self.capture.release()
                    ##videoWriter.release()
                    break
            except:
                self.filenameHandler.release()
                print("Error!!!")
                break


    def destoroy(self):
        cv2.destroyAllWindows()
        self.capture.release()
        self.exitFlag = True

    def prepareFrame(self, frame1, frame2):
        grayFrame1, grayFrame2 = self.convertFramesToGray(frame1, frame2)
        scaledFrame1, scaledFrame2= self.scaleFrames(grayFrame1, grayFrame2)
        bluredFrame1 = cv2.GaussianBlur(scaledFrame1, (self.kSize, self.kSize), 0)
        bluredFrame2 = cv2.GaussianBlur(scaledFrame2, (self.kSize, self.kSize), 0)
        return bluredFrame1, bluredFrame2

    def readFrame(self, cap):
        return cap.read()

    def subs(self, previousFrame, frame):
        self.differenceImage = cv2.absdiff(previousFrame, frame)
        return self.differenceImage

    def detectMovement(self, differenceImage):
        ret, differenceImage = cv2.threshold(differenceImage, 20, 255, cv2.THRESH_BINARY)
        cv2.imshow("normalized", differenceImage)
        movementStrenght = np.sum(differenceImage) / 255
        if movementStrenght > 5:
            self.bmovementDetected = True
           # print("Movement!!!")
            return True
        else:
            self.bmovementDetected = False
            return False

    def record(self, frame):
        if self.bmovementDetected:
            self.brecording = True
            self.cRecoringTime = 10
        if self.brecording and not self.bmovementDetected and self.cRecoringTime <= 0:
            self.brecording = False
        if self.brecording:
            self.filenameHandler.Save(frame)
        if self.cRecoringTime > 0:
            self.cRecoringTime = self.cRecoringTime - 1
        #self.PrintFlags()

    def PrintFlags(self):
        print("Movement: " + str(self.bmovementDetected))
        print("Recordig: " + str(self.brecording))
        print("Record Time Counting: " + str(self.cRecoringTime))

    def initVideoWriter(self, frame, filename):
        dimensions = frame.shape
        height = dimensions[0]
        width = dimensions[1]
        videoWriter = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (width, height))
        return videoWriter

    def convertFramesToGray(self, frame1, frame2):
        frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        return frame1, frame2

    def scaleFrames(self, frame1, frame2):
        dimensions = frame1.shape
        height = int(dimensions[0] * self.scaleFactor)
        width = int(dimensions[1] * self.scaleFactor)
        newDimension = (width, height)
        scaledFrame1 = cv2.resize(frame1, newDimension, interpolation=cv2.INTER_AREA)
        scaledFrame2 = cv2.resize(frame2, newDimension, interpolation=cv2.INTER_AREA)
        return scaledFrame1, scaledFrame2

    def addTimeToFrame(self, frame):
        tempFrame = frame.copy()
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        org = (50, 50)
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1
        color = (255, 255, 255)
        thickness = 2
        tempFrame = cv2.putText(tempFrame, current_time, org, font, fontScale, color, thickness, cv2.LINE_AA)
        return tempFrame

    def setImagePanel(self, panel):
        self.panel = panel

    def getImg(self):
        imageRGB = cv2.cvtColor(self.Img, cv2.COLOR_BGR2RGB)
        return imageRGB

    @staticmethod
    def getDevicesList():
        index = 0
        arr = []
        while True:
            cap = cv2.VideoCapture(index)
            if not cap.read()[0]:
                break
            else:
                arr.append(index)
            cap.release()
            index += 1
        return arr