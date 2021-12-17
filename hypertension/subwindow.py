from PyQt5.QtWidgets import *
import sys
from PyQt5.QtCore import *

class SubWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('CrawlingBot Working')
        self.setGeometry(100,100,200,100)

        layout = QVBoxLayout()
        layout.addStretch(1)

        edit = QLineEdit()
        font = edit.font()
        font.setPointSize(20)
        edit.setFont(font)
        self.edit = edit

        subLayout = QHBoxLayout()

        btnOk = QPushButton('확인')
    
    def showModal(self):
        return super().exec_()