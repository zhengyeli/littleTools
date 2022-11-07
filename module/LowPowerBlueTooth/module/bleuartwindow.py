import re

from PyQt6.QtCore import Qt, QSettings, QFile
from PyQt6.QtWidgets import QDockWidget, QPushButton, QToolButton, QInputDialog, QLineEdit, QGridLayout, QWidget, \
    QFileDialog

from module.LowPowerBlueTooth.module.MPushButton import MPushButton


class bleUartWindow:
    def __init__(self, BleMainClass):
        self.toolBtn = None
        self.dockBleUart = QDockWidget()
        self.motherClass = BleMainClass
        self.motherWidget = BleMainClass.superWidget

        self.gridlayout = None
        self.WidgetContents = None
        self.firstButton = None
        self.tempButton = None

        self.row = 0
        self.maxRow = 3
        self.line = 1

        self.last_dir = None

        self.form_init()

    def form_init(self):
        self.dockBleUart.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetClosable |
                                     QDockWidget.DockWidgetFeature.DockWidgetMovable |
                                     QDockWidget.DockWidgetFeature.DockWidgetFloatable)
        self.dockBleUart.setWindowTitle("自定")
        self.dockBleUart.setObjectName("自定窗口")

        self.WidgetContents = QWidget(self.dockBleUart)
        self.gridlayout = QGridLayout(self.WidgetContents)

        button_add_bleUart = QPushButton(self.WidgetContents)
        button_add_bleUart.setMaximumHeight(30)
        button_add_bleUart.setMaximumWidth(80)
        button_add_bleUart.setText("add")

        button_load_bleUart = QPushButton(self.WidgetContents)
        button_load_bleUart.setMaximumHeight(30)
        button_load_bleUart.setMaximumWidth(80)
        button_load_bleUart.setText("load")

        button_save_bleUart = QPushButton(self.WidgetContents)
        button_save_bleUart.setMaximumHeight(30)
        button_save_bleUart.setMaximumWidth(80)
        button_save_bleUart.setText("save")

        self.gridlayout.addWidget(button_add_bleUart, 0, 0)
        self.gridlayout.addWidget(button_load_bleUart, 0, 1)
        self.gridlayout.addWidget(button_save_bleUart, 0, 2)

        button_add_bleUart.clicked.connect(self.addButton)
        button_load_bleUart.clicked.connect(self.loadFile)
        button_save_bleUart.clicked.connect(self.saveFile)

        self.motherClass.creatNewDockWindow(self.dockBleUart, Qt.DockWidgetArea.TopDockWidgetArea)
        self.dockBleUart.setWidget(self.WidgetContents)

        self.toolBtn = QToolButton()  # 创建QToolButton
        # self.toolBtn1.setIcon(QIcon(":/src/menu.png")) # 添加图标
        self.toolBtn.setText(self.dockBleUart.windowTitle())
        self.toolBtn.clicked.connect(self.closeWindow)
        self.motherClass.toolbar.addWidget(self.toolBtn)  # 向工具栏添加QToolButton按钮
        self.dockBleUart.setVisible(False)

        settings = QSettings("setting.ini", QSettings.Format.IniFormat)
        settings.beginGroup("BleUartConfig")
        self.last_dir = settings.value("config_dir")
        settings.endGroup()

        if self.last_dir is not None:
            if len(self.last_dir) != 0:
                self.loadFile(True)

    '''  dynamic add button '''

    def addButton(self):
        name = QInputDialog.getText(self.WidgetContents, "我只是打酱油的~", "input button name", QLineEdit.EchoMode.Normal)

        if name[1]:
            buttonName = name[0]  # 获取输入
        else:
            return

        text = QInputDialog.getText(self.WidgetContents, "我只是打酱油的~", "(BB0101)", QLineEdit.EchoMode.Normal)

        if text[1]:
            cmd = text[0]  # 获取输入
        else:
            return

        self.tempButton = None

        if self.firstButton is None:
            self.motherClass.setInfo("firstButton is null")
            self.firstButton = MPushButton(self.WidgetContents)
            self.firstButton.setMaximumHeight(30)  # limit size
            self.firstButton.setMaximumWidth(100)
            self.firstButton.setText(buttonName)
            self.firstButton.nextButton = None
            self.firstButton.prevButton = None
            self.firstButton.cmd = cmd
            self.tempButton = self.firstButton
        else:
            self.motherClass.setInfo("firstButton is not null")
            self.tempButton = self.firstButton
            while self.tempButton.nextButton is None:
                self.tempButton = self.tempButton.nextButton

        self.tempButton.nextButton = MPushButton(self.WidgetContents)
        if self.tempButton.nextButton is None:
            self.motherClass.setInfo("new is FAIL")
            return

        self.tempButton = self.tempButton.nextButton
        self.tempButton.setMaximumHeight(20)  # limit size
        self.tempButton.setMaximumWidth(100)
        self.tempButton.setText(buttonName)
        self.tempButton.nextButton = None
        self.tempButton.prevButton = None
        self.tempButton.cmd = cmd

        if self.tempButton is None:
            self.motherClass.setInfo("self.tempButton is null")
            return

        self.tempButton.clicked.connect(self.bleSendData)

        if self.row <= self.maxRow:
            self.gridlayout.addWidget(self.tempButton, self.line, self.row)
            self.row += 1
        else:
            self.row = 0
            self.line += 1

        self.gridlayout.addWidget(self.tempButton, self.line, self.row)

    def bleSendData(self):
        mBtn = self.dockBleUart.sender()
        array = mBtn.cmd  # "aa11"
        self.motherClass.govee_ble_string_send(array)

    def saveFile(self):
        if self.firstButton is None:
            return
        buf = ""
        self.tempButton = self.firstButton
        while self.tempButton is not None:
            buf += self.tempButton.text()
            buf += "="
            buf += self.tempButton.cmd
            buf += '\n'
            self.tempButton = self.tempButton.nextButton

        widget = QWidget()
        saveFileDir = QFileDialog.getSaveFileName(widget, "save file", "")
        file = QFile(saveFileDir[0])
        file.open(QFile.OpenModeFlag.WriteOnly)
        file.write(bytes(buf, 'utf-8'))
        file.close()

    def loadFile(self, b):
        self.line = 1
        self.row = 0

        if b:
            if self.last_dir is None:
                return
            bleSendFileDir = self.last_dir
        else:
            widget = QWidget()
            dirInfo = QFileDialog.getOpenFileName(widget, "load file", "")
            bleSendFileDir = dirInfo[0]

        if len(bleSendFileDir) == 0:
            return

        file = QFile(bleSendFileDir)

        if file.open(QFile.OpenModeFlag.ReadOnly):
            settings = QSettings("setting.ini", QSettings.Format.IniFormat)
            settings.beginGroup("BleUartConfig")
            settings.setValue("config_dir", bleSendFileDir)
            settings.endGroup()

        buf = str(file.readAll(), "utf-8")
        file.close()

        self.tempButton = self.firstButton
        if self.tempButton is not None:
            while self.tempButton.nextButton is not None:
                self.tempButton = self.tempButton.nextButton

            self.tempButton = self.tempButton.prevButton

            while self.tempButton.nextButton is not None and self.tempButton.prevButton is not None:
                del self.tempButton.nextButton
                self.tempButton = self.tempButton.prevButton

            del self.tempButton.nextButton
            del self.tempButton
            self.tempButton = None

        btnConfigList = re.split('\n', buf)

        for i in range(0, len(btnConfigList)):
            if btnConfigList[i] == "":
                continue

            btn = re.split("=", btnConfigList[i])

            if i == 0:
                newButton = MPushButton(self.WidgetContents)
                newButton.setMaximumHeight(30)  # limit size
                newButton.setMaximumWidth(100)
                newButton.setText(btn[0].replace(' ', ''))
                newButton.cmd = btn[1].replace(' ', '')
                self.firstButton = newButton
                self.firstButton.nextButton = None
                self.firstButton.prevButton = None
                self.tempButton = self.firstButton
            else:
                newButton = MPushButton(self.WidgetContents)
                newButton.setMaximumHeight(30)  # limit size
                newButton.setMaximumWidth(100)
                newButton.setText(btn[0])
                newButton.cmd = btn[1]
                newButton.prevButton = self.tempButton
                newButton.nextButton = None

                self.tempButton.nextButton = newButton
                self.tempButton = newButton

        self.tempButton = self.firstButton
        while self.tempButton is not None:
            self.tempButton.clicked.connect(self.bleSendData)
            if self.row <= self.maxRow:
                self.gridlayout.addWidget(self.tempButton, self.line, self.row)
                self.row += 1
            else:
                self.gridlayout.addWidget(self.tempButton, self.line, self.row)
                self.row = 0
                self.line += 1

            self.tempButton = self.tempButton.nextButton

        self.row -= 1

    def closeWindow(self):
        # self.motherClass.closeAllWindow()
        self.dockBleUart.setVisible(bool(1 - self.dockBleUart.isVisible()))
