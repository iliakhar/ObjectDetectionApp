from types import NoneType
from PyQt5.QtCore import *
from PyQt5.QtGui import (QFont)
from PyQt5.QtWidgets import (QWidget, QPushButton, QHBoxLayout, QVBoxLayout,QLabel, QListWidget, QFileDialog)
from PyQt5 import QtCore
from pathlib import Path
import glob

class DirListBox(QWidget):
    changeSignal = QtCore.pyqtSignal(str)
    def __init__ (self, title):
        super().__init__()
        self.initUI(title)

    def initUI(self, title):

        
        vLay = QVBoxLayout()
        hLay = QHBoxLayout()
        self.dirList = QListWidget()
        self.titleLbl = QLabel(title)
        self.openDirBtn = QPushButton('Open Dir')
        self.openFileBtn = QPushButton('Open File')
        fontBig = QFont('Arial', 12)
        fontSmall = QFont('Arial', 11)

        self.dirList.setFont(fontSmall)

        self.titleLbl.setContentsMargins(5,0,0,0)
        self.titleLbl.setFont(fontBig)

        self.openDirBtn.setFont(fontBig)
        self.openDirBtn.setMinimumHeight(30)
        self.openDirBtn.clicked.connect(self.SelectFolder)

        self.openFileBtn.setFont(fontBig)
        self.openFileBtn.setMinimumHeight(30)
        self.openFileBtn.clicked.connect(self.SelectFile)

        self.setMinimumWidth(250)
        #self.setMaximumWidth(250)

        hLay.addWidget(self.openDirBtn)
        

        hLay.addWidget(self.openFileBtn)

        self.dirList.currentItemChanged.connect(self.ChangeElem)

        vLay.addWidget(self.titleLbl)
        vLay.addWidget(self.dirList)
        vLay.addLayout(hLay)

        self.setLayout(vLay)

    @QtCore.pyqtSlot()
    def ChangeElem(self):
        if self.dirList.currentItem() != None:
            self.changeSignal.emit(self.dirList.currentItem().text())

    def SelectFile(self):
        filenames, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Files",
            "C:\\",
            "Images (*.png *.jpg)"
            )
        if filenames:
            self.dirList.clear()
            self.dirList.addItems([str(Path(filename)) for filename in filenames])
        
    def SelectFolder(self):
        types = ('*.png', '*.jpg', '*.jpeg')
        dir_name = QFileDialog.getExistingDirectory(self, "Select a Directory","C:\\")
        if dir_name:
            self.dirList.clear()
            path = Path(dir_name)
            lst = []
            for tp in types:
                filenames = glob.glob(str(path) + "\\" + tp)
                if filenames:
                    self.dirList.addItems([str(Path(filename)) for filename in filenames])
