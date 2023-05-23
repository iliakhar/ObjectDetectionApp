from email.charset import QP
import imp
import math
from re import A
from tkinter.tix import DirList
from PyQt5.QtCore import *
from PyQt5.QtGui import (QFont, QFontDatabase, QPixmap, QImage)
from PyQt5.QtWidgets import (QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QLabel, QTabWidget, QListWidget, QFileDialog)
from PyQt5 import QtCore
from pathlib import Path
import glob
import sys

import torch
from matplotlib import pyplot as plt
import numpy as np
import cv2

from DirListBox import DirListBox
            


class DetectObject():
    def __init__ (self, modelPath):
        self.SetModel(modelPath)

    def SetModel(self, modelPath):
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', modelPath, force_reload=True)

    def GetDetectPic(self, picPath):
            res = self.model(picPath)
            pic = np.squeeze(res.render())
            plt.imsave('Detectpic.png', pic)


class MainWindow(QWidget):
    def __init__(self):
        self.detect = DetectObject('../../yolov5/runs/train/exp18/weights/last.pt')
        self.currentFile = ""
        QWidget.__init__(self)
        self.InitUi()

    def InitUi(self):
        

        vLay = QVBoxLayout()
        hLay = QHBoxLayout()
        self.filesListWidget = DirListBox('Files list')

        self.setLayout(hLay)
        self.setMinimumSize(700,500)

        fontBig = QFont('Arial', 12)
        self.objDetectBtn = QPushButton("Detect")
        self.objDetectBtn.setFont(fontBig)
        self.objDetectBtn.setMinimumHeight(35)
        self.objDetectBtn.clicked.connect(self.DectectClick)
        self.objDetectBtn.setContentsMargins(30,0,30,0)

        self.origImg = QPixmap()
        self.lblImg = QLabel()
        self.lblImg.setPixmap(self.origImg)
        self.lblImg.setScaledContents(True)

        vLay.addWidget(self.filesListWidget)
        vLay.addWidget(self.objDetectBtn)
        hLay.addLayout(vLay)
        hLay.addStretch(1)
        hLay.addWidget(self.lblImg,2)
        hLay.addStretch(1)

        self.filesListWidget.changeSignal.connect(self.ChangeOrigImg)

    def resizeEvent(self,event):
        if(self.currentFile != ""):
            self.ChangeOrigImg(self.currentFile)
            


    @QtCore.pyqtSlot(str)
    def ChangeOrigImg(self, filename):
        self.origImg.load(filename)
        self.currentFile = filename
        maxPicSize = min([self.width() - 300,self.height() - 100])
        maxLen = max([self.origImg.size().width(), self.origImg.size().height()])
        koef = maxLen/maxPicSize
        self.origImg.scaled(math.floor(self.origImg.size().width()/koef), math.floor(self.origImg.size().height()/koef), Qt.KeepAspectRatio)
        self.lblImg.setFixedSize(math.floor(self.origImg.size().width()/koef), math.floor(self.origImg.size().height()/koef))
        self.lblImg.setPixmap(self.origImg)

    def DectectClick(self):
        #D:\lab\5sem\praktika2\yolov5\data\picsAll\images
        if self.currentFile!="":
            self.detect.GetDetectPic(self.currentFile)
            self.origImg.load('Detectpic.png')
            maxPicSize = min([self.width() - 300,self.height() - 100])
            maxLen = max([self.origImg.size().width(), self.origImg.size().height()])
            koef = maxLen/maxPicSize
            self.origImg.scaled(math.floor(self.origImg.size().width()/koef), math.floor(self.origImg.size().height()/koef), Qt.KeepAspectRatio)
            self.lblImg.setFixedSize(math.floor(self.origImg.size().width()/koef), math.floor(self.origImg.size().height()/koef))
            self.lblImg.setPixmap(self.origImg)



app = QApplication(sys.argv)
screen = MainWindow()
screen.show()
sys.exit(app.exec_())
