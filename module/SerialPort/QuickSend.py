import re

from PyQt6.QtCore import QSettings, QFile
from PyQt6.QtWidgets import QWidget, QGridLayout, QCheckBox, QLineEdit, QPushButton, QFileDialog, QLabel

from module.utils import utils

dict = {
    "True": True,
    "False": False,
}
class blockItem(QWidget):
    def __init__(self, isHex: bool, string: str):
        super().__init__()
        self.itemLayout = QGridLayout()
        self.itemLayout.setContentsMargins(1, 1, 1, 1)

        labIsHex = QLabel("hex")
        self.cboxIsHex = QCheckBox()
        self.cboxIsHex.setChecked(isHex)
        self.ldtString = QLineEdit(string)
        self.pbtSend = QPushButton("send")
        self.itemLayout.addWidget(labIsHex, 0, 0)
        self.itemLayout.addWidget(self.cboxIsHex, 0, 1)
        self.itemLayout.addWidget(self.ldtString, 0, 2)
        self.itemLayout.addWidget(self.pbtSend, 0, 3)
        self.setLayout(self.itemLayout)


class blockItemList:
    def __init__(self, mainClass, widget: QWidget):
        if widget is None:
            widget = QWidget(None)
        else:
            pass

        self.mainClass = mainClass
        self.itemList = []
        self.currentIndex = 0

        self.gridlayout = QGridLayout(widget)
        self.btnAddItem = QPushButton("添加")
        self.btnAddItem.clicked.connect(lambda: self.addItem())

        self.btnLoadItem = QPushButton("加载")
        self.btnLoadItem.clicked.connect(lambda: self.init_load(False))

        self.btnSaveItem = QPushButton("保存")
        self.btnSaveItem.clicked.connect(self.init_save)

        self.headLayout = QGridLayout(widget)
        self.headLayout.setContentsMargins(1, 1, 1, 1)

        self.headLayout.addWidget(self.btnAddItem, 0, 0)
        self.headLayout.addWidget(self.btnLoadItem, 0, 1)
        self.headLayout.addWidget(self.btnSaveItem, 0, 2)

        widget.setLayout(self.gridlayout)
        self.gridlayout.addLayout(self.headLayout, 0, 0)

        settings = QSettings("Software Inc.", "Icon Editor")
        settings.beginGroup("mainWindow")
        self.last_dir = settings.value("quickSnd_dir")
        settings.endGroup()

        if len(self.last_dir) > 0:
            self.init_load(True)

    def addItem(self, ishex=False, string=""):
        blk = blockItem(ishex, string)
        self.itemList.append(blk)
        self.itemList[self.currentIndex].pbtSend.clicked.connect(lambda: self.send(blk))
        self.gridlayout.addWidget(self.itemList[self.currentIndex], self.currentIndex + 1, 0)
        self.currentIndex += 1

    def send(self, blk: blockItem):
        string = blk.ldtString.text()
        if blk.cboxIsHex.isChecked():
            self.mainClass.sendBytes(utils.stringHex2bytes(string))
            print(utils.stringHex2bytes(string))
        else:
            self.mainClass.sendString(string)

    def init_load(self, b):
        self.currentIndex = 0

        if b:
            init_dir = self.last_dir
        else:
            widget = QWidget()
            init_dir = QFileDialog.getOpenFileName(widget, "load file", self.last_dir)
            init_dir = init_dir[0]

        if len(init_dir) == 0:
            return

        file = QFile(init_dir)

        if file.open(QFile.OpenModeFlag.ReadOnly):
            settings = QSettings("Software Inc.", "Icon Editor")
            settings.beginGroup("mainWindow")
            settings.setValue("quickSnd_dir", init_dir)
            settings.endGroup()

        buf = str(file.readAll(), "utf-8")
        file.close()

        if len(self.itemList) > 0:
            for i in range(0, len(self.itemList) - 1):
                del self.itemList[0]

        list = re.split('\n', buf)

        for i in range(0, len(list)):
            if list[i] == '':
                continue

            listItem = re.split(',', list[i])
            self.addItem(dict[listItem[0]], listItem[1])

    def init_save(self):
        if len(self.itemList) == 0:
            return
        buf = ""
        for i in range(0, len(self.itemList)):
            if self.itemList[i] == "":
                continue
            else:
                buf += str(self.itemList[i].cboxIsHex.isChecked())
                buf += ','
                buf += self.itemList[i].ldtString.text()
                buf += '\n'

        widget = QWidget()
        dir = QFileDialog.getSaveFileName(widget, "save file", "")
        file = QFile(dir[0])
        file.open(QFile.OpenModeFlag.WriteOnly)
        file.write(bytes(buf, 'utf-8'))
        file.close()
