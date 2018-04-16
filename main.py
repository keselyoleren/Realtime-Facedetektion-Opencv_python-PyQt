import cv2
import os
import sys
import csv
from os import path
import numpy as np
import subprocess
import sqlite3
import nexmo
from PIL import Image
from twilio.rest import Client 
from glob import glob; 
from os.path import expanduser
from datetime import date, datetime
try:
    from PyQt5.QtCore import pyqtSlot
    from PyQt5 import QtCore
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
    from PyQt5.uic import loadUi
    from PyQt5 import QtGui
    from PyQt5 import QtWidgets 

except ImportError:
    if sys.version_info.major >= 3:
        import sip
        sip.setapi('QVariant', 2)
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *

class Kamera(QMainWindow):
    face_cascades = os.path.join(os.getcwd(),'haarcascade_frontalface_default.xml')
    def __init__(self):
        super(Kamera, self).__init__()
        loadUi('ui/main.ui', self)

        #buka kamera
        self.image  = None
        self.startCam.clicked.connect(self.start_cam)

        #deteksi wajah
        self.deteksi_wajah = False
        self.deteksi.toggled.connect(self.deteksiWajah)
        self.deteksi.setCheckable(True)


    @pyqtSlot()
    def start_cam(self):
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 450)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(5)

    def update_frame(self):
        ret, self.image = self.capture.read()
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.displayCam(self.image, 1)

        if(self.deteksi_wajah):
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV) if len(self.image.shape) >= 3 else self.image
            faces = self.face_cascades.detectMultiScale(gray,1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(self.image, (x,y), (x+w, y+h),(255,0,0), 2 )
                roy_gray = gray[y:y+h, x:x+w]
                roi_color = self.image[y:y+h, x:x+w]
        self.displayCam(self.image, 2)


    def deteksiWajah(self, status):
        if status:
            self.deteksi_wajah = True
            self.deteksi.setText('STOP')
        else:
            self.deteksi_wajah = False
            self.deteksi.setText('Deteksi Wajah')

    def displayCam(self,frame, window = 1):
        height, width, channels = self.image.shape
        bytesPerLine = channels * width
        qImg = QImage(self.image.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        pixmap01 = QPixmap.fromImage(qImg)
        pixmap_image = QPixmap(pixmap01)

        if  window == 1:
            self.camLabel.setPixmap(pixmap_image)
            self.camLabel.setAlignment(QtCore.Qt.AligentCenter)
            self.camLabel.setScaledContents(True)
            self.setMinimumSize(1,1)

app = QApplication(sys.argv)
window = Kamera()
window.setWindowTitle("kamera deteksi wajah")
window.show()
sys.exit(app.exec_())
