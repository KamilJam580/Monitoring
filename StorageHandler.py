from datetime import datetime
import cv2


class StorageHandler:
    def __init__(self, frame):
        self.time = datetime.now()
        baseFilename = "rec"
        extension = "avi"
        sTime = self.convertDateToStringMDYH(self.time)
        self.filename = self.createFileName(sTime)
        print(self.filename)
        self.videoWriter = self.initVideoWriter(frame, self.filename)

    def convertDateToStringMDYH(self, dateTime):
        return dateTime.strftime("%m_%d_%Y %H")

    def createFileName(self, sDateTime):
        return sDateTime + ".avi"

    def Save(self, frame):
        self.now = datetime.now()
        sNow = self.convertDateToStringMDYH(self.now)
        sTime = self.convertDateToStringMDYH(self.time)
        if (sNow != sTime):
            self.filename = self.createFileName(sNow)
            print(self.filename)
            self.videoWriter.release()
            self.videoWriter = self.initVideoWriter(frame, self.filename)
            self.time = self.now
        self.videoWriter.write(frame.copy())

    def initVideoWriter(self, frame, filename):
        dimensions = frame.shape
        height = dimensions[0]
        width = dimensions[1]
        self.videoWriter = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (width, height))
        return self.videoWriter

    def release(self):
        self.videoWriter.release()
