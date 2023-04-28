from PyQt6.QtWidgets import QWidget

from module.SerialPort.mesure import Ui_Form
from sdk_src.utils import utils
import ctypes
import hashlib
import os
import shutil


class chenzhong(Ui_Form):
    def __init__(self, comToolObj):
        self.widget = QWidget()
        self.setupUi(self.widget)
        self.comTool = comToolObj
        self.pushButton.setText("零点标定")
        self.pushButton_2.setText("重量1标定")
        self.pushButton_3.setText("重量2标定")
        self.pushButton_4.setText("查询")
        self.pushButton_5.setText("清除")

        self.widget.show()
        self.pushButton.clicked.connect(self.btn1)
        self.pushButton_2.clicked.connect(self.btn2)
        self.pushButton_3.clicked.connect(self.btn3)
        self.pushButton_4.clicked.connect(self.check)
        self.pushButton_5.clicked.connect(self.clear)

    def process(self, string):
        print(string)
        if string is None:
            return
        hexlist = utils.string2intlist(string)
        for i in range(0, len(hexlist) - 5):
            print(hexlist[i])
            if hexlist[i] == 0xb2 and hexlist[i + 1] == 0xa5:
                value = hexlist[i + 3] * 256 + hexlist[i + 4]
                if hexlist[i + 2] == 1:
                    value = -value
                    self.label.setText(str(value))
                i = i + 6

    def btn1(self):
        self.comTool.sendBytes(utils.intlist2bytes(utils.string2intlist("a15a3a4cc060")))

    def btn2(self):
        self.comTool.sendBytes(utils.intlist2bytes(utils.string2intlist("a15a3a4c839d")))

    def btn3(self):
        self.comTool.sendBytes(utils.intlist2bytes(utils.string2intlist("a15a3a4c45db")))

    def check(self):
        self.comTool.sendBytes(utils.intlist2bytes(utils.string2intlist("a15acac2ee2c")))

    def clear(self):
        self.label.setText("null")
        self.comTool.sendBytes(utils.intlist2bytes(utils.string2intlist("a15aF66FEE53")))

