from email.charset import QP
import imp
import math
from re import A
from PyQt5.QtCore import *
from PyQt5.QtGui import (QFont, QPixmap, QIcon)
from PyQt5.QtWidgets import (QWidget, QPushButton, QHBoxLayout, QVBoxLayout,
                            QApplication, QLabel, QFrame, QLineEdit)
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
            strRes = str(res)[0:str(res).find('Speed')-1]
            return strRes


class MainWindow(QWidget):
    def __init__(self):
        self.detect = DetectObject('../../yolov5/runs/train/exp18/weights/last.pt')
        self.currentFile = ""
        self.isDetected = False
        QWidget.__init__(self)
        self.InitUi()

    def InitUi(self):
        
        self.setWindowTitle('Chess pieces Detection')
        self.setWindowIcon(QIcon('icon/king.png'))
        vLay = QVBoxLayout()
        hLay = QHBoxLayout()
        hPicLay = QHBoxLayout()
        vPicLay = QVBoxLayout()
        hDetectBtnLay = QHBoxLayout()
        hInfoLay = QHBoxLayout()
        vWorkSpace = QVBoxLayout()
        
        self.filesListWidget = DirListBox('Files list')

        self.setLayout(hLay)
        self.setMinimumSize(900,500)

        self.frame = QFrame();
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setLayout(vWorkSpace)
        vPicLay.setContentsMargins(0,32,0,0)

        fontBig = QFont('Arial', 12)
        self.objDetectBtn = QPushButton("Detect")
        self.objDetectBtn.setMaximumWidth(255)
        self.objDetectBtn.setMinimumWidth(255)
        self.objDetectBtn.setFont(fontBig)
        self.objDetectBtn.setMinimumHeight(35)
        self.objDetectBtn.clicked.connect(self.DectectClick)

        self.infoLine = QLineEdit()
        self.infoLine.setMinimumHeight(35)
        self.infoLine.setFont(fontBig)
        self.infoLine.setReadOnly(True)

        self.infoTitle = QLabel(' Info: ')
        self.infoTitle.setFont(fontBig)

        self.origImg = QPixmap()
        self.lblImg = QLabel()
        self.lblImg.setPixmap(self.origImg)
        self.lblImg.setScaledContents(True)

        hDetectBtnLay.addWidget(self.objDetectBtn)
        hInfoLay.addWidget(self.infoTitle)
        hInfoLay.addWidget(self.infoLine,1)
        vPicLay.addWidget(self.frame,1)
        hPicLay.addWidget(self.lblImg)
        vWorkSpace.addLayout(hPicLay)
        vPicLay.addLayout(hInfoLay)
        vLay.addWidget(self.filesListWidget)
        vLay.addLayout(hDetectBtnLay)
        hLay.addLayout(vLay)
        #hLay.addStretch(1)
        hLay.addLayout(vPicLay,2)
        #hLay.addStretch(1)

        self.filesListWidget.changeSignal.connect(self.ChangeOrigImg)

    def resizeEvent(self,event):
        if(self.currentFile != ""):
            if(self.isDetected):
                self.ChangeOrigImg('Detectpic.png')
            else:
                self.ChangeOrigImg(self.currentFile)
                self.infoLine.setText('')


    @QtCore.pyqtSlot(str)
    def ChangeOrigImg(self, filename):
        self.isDetected = False
        self.currentFile = filename
        self.ShowImg(filename)
        

    def DectectClick(self):
        #D:\lab\5sem\praktika2\yolov5\data\picsAll\images
        if self.currentFile!="":
            self.isDetected = True
            info = self.detect.GetDetectPic(self.currentFile)
            self.infoLine.setText(' ' + info)
            self.ShowImg('Detectpic.png')

    def ShowImg(self, filename):
        self.origImg.load(filename)
        '''maxPicSize = min([self.origImg.size().width() - 15,self.frame.height() - 15])
        maxLen = max([self.origImg.size().width(), self.origImg.size().height()])
        koef = maxLen/maxPicSize'''
        koefW = self.origImg.size().width() / (self.frame.width()-15)
        koefH = self.origImg.size().height() / (self.frame.height()-15)
        koef = max([koefW, koefH])
        self.origImg.scaled(math.floor(self.origImg.size().width()/koef), math.floor(self.origImg.size().height()/koef), Qt.KeepAspectRatio)
        self.lblImg.setFixedSize(math.floor(self.origImg.size().width()/koef), math.floor(self.origImg.size().height()/koef))
        self.lblImg.setPixmap(self.origImg)


app = QApplication(sys.argv)
screen = MainWindow()
screen.show()
sys.exit(app.exec_())
