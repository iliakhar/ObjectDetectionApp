from email.charset import QP
import imp
import math
from re import A
from PyQt5.QtCore import *
from PyQt5.QtGui import (QFont, QPixmap, QImage)
from PyQt5.QtWidgets import (QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QLabel, QFrame)
from PyQt5 import QtCore
from pathlib import Path
import sys

import torch
from matplotlib import pyplot as plt
import numpy as np

from DirListBox import DirListBox
            


class DetectObject():
    def __init__ (self, modelPath):
        self.SetModel(modelPath)

    def SetModel(self, modelPath):
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', modelPath, force_reload=False)

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
        hPicLay = QHBoxLayout()
        self.filesListWidget = DirListBox('Files list')

        self.setLayout(hLay)
        self.setMinimumSize(900,500)

        self.frame = QFrame();
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setLayout(hPicLay)

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

        hPicLay.addWidget(self.lblImg)
        vLay.addWidget(self.filesListWidget)
        vLay.addWidget(self.objDetectBtn)
        hLay.addLayout(vLay)
        #hLay.addStretch(1)
        hLay.addWidget(self.frame,2)
        #hLay.addStretch(1)

        self.filesListWidget.changeSignal.connect(self.ChangeOrigImg)

    def resizeEvent(self,event):
        if(self.currentFile != ""):
            self.ChangeOrigImg(self.currentFile)
            


    @QtCore.pyqtSlot(str)
    def ChangeOrigImg(self, filename):
        self.origImg.load(filename)
        self.currentFile = filename

        maxPicSize = min([self.frame.width() - 50,self.frame.height() - 50])
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
