from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtWidgets import QMainWindow, QDockWidget, QTextEdit, QToolBar, QToolButton

from module.LowPowerBlueTooth.api.BluetoothBaseClass import BluetoothBaseClass
from module.LowPowerBlueTooth.module.blelinkwindow import blelinkwindow
from module.LowPowerBlueTooth.ui.Ui_BleMainWin import Ui_BleMainWin
from module.LowPowerBlueTooth.api.deviceHandler import DeviceHandler
from module.LowPowerBlueTooth.api.deviceFinder import DeviceFinder
from PyQt6 import QtWidgets


class BleMainWin(QMainWindow):
    def __init__(self, widget):
        super().__init__()
        self.superWidget = None
        if widget is None:
            self.superWidget = QMainWindow()
        else:
            if type(widget) == QMainWindow:
                self.superWidget = widget
            else:
                self.superWidget = QMainWindow()
                widget.layout().addWidget(self.superWidget)
        self.ui = Ui_BleMainWin()
        self.ui.setupUi(self.superWidget)

        self.superWidget.setDockNestingEnabled(True)

        # --------------------------- dock widget window config

        self.DockwidgetInfo = QtWidgets.QDockWidget()
        self.text_info = QTextEdit()
        self.text_info.setReadOnly(True)
        self.DockwidgetInfo.setWidget(self.text_info)
        self.DockwidgetInfo.setObjectName("软件输出信息")
        self.DockwidgetInfo.setWindowTitle("信息")
        self.DockwidgetInfo.setVisible(True)
        self.DockwidgetInfo.setStyleSheet("border:none")
        self.superWidget.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.DockwidgetInfo)

        # ----------------------------------------- 在工具栏添加图标按钮
        self.toolbar = QToolBar(self.superWidget)
        self.toolbar.setObjectName("toolbar")
        self.toolbar.setWindowTitle("toolbar")
        self.toolbar.setMovable(False)

        self.DockwidgetInfo_toolBtn = QtWidgets.QToolButton(self.superWidget) # 创建QToolButton
        self.DockwidgetInfo_toolBtn.setText(self.DockwidgetInfo.windowTitle())
        self.toolbar.addWidget(self.DockwidgetInfo_toolBtn)
        self.superWidget.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolbar)
        self.DockwidgetInfo_toolBtn.clicked.connect(self.DockwidgetInfo_btn_click)

        # -----------------------------------------  second: ble api init

        self.deviceFinder = DeviceFinder(self.text_info)
        self.deviceHandler = self.deviceFinder.m_deviceHandler

        # self.deviceFinder.scanDeviceResult.connect(self.addBleDevToList)
        # self.deviceHandler.bleMessageChange.connect(self, ble_rx_data_func)
        # self.deviceHandler.connectSuccess.connect(self.bleConnectSuccess)
        # self.deviceHandler.disconnectOccur.connect(self.disconButton_clicked)

        # ----------------------------------------- other
        self.blelink = blelinkwindow(self)
        # self.blesku = bleskumsghandle()
        # self.SocketClient = tcpSocketClient(self.superWidget)
        # self.bleuart = bleUartWindow(self.superWidget)
        # self.bleSensor = bleSensorWindow(self.superWidget)

        self.text_info.append("tip :\n"
                "   window              usage        \n"
                "1. info : some software info print\n"
                "2. manual : send uart cmd to mcu via ble \n"
                "3. tcpsocket : use tcp socket talk with dev\n"
                "4. blelink : connect to dev via ble\n"
                "5. debug : view dev debug message via ble\n"
                )

        self.superWidget.setStatusBar(None)
        self.superWidget.setMenuBar(None)

        dockList = self.superWidget.findChildren(QtWidgets.QDockWidget)
        for dock in dockList:
            dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetClosable | QDockWidget.DockWidgetFeature.DockWidgetMovable | QDockWidget.DockWidgetFeature.DockWidgetFloatable)

        self.readSettings()

    def setInfo(self, string):
        if self.text_info:
            self.text_info.append(string)

    def DockwidgetInfo_btn_click(self):
        self.closeAllWindow()
        if self.DockwidgetInfo.isVisible():
            self.DockwidgetInfo.setVisible(False)
        else:
            self.DockwidgetInfo.setVisible(True)
        self.DockwidgetInfo_toolBtn.setChecked(True)

    def closeAllWindow(self):
        dockList = self.superWidget.findChildren(QDockWidget)
        # for dock in dockList:
        #     dock.setVisible(False)
        #
        # toolBtnList = self.toolbar.findChildren(QToolButton)
        # for toolBtn in toolBtnList:
        #     toolBtn.setChecked(True)

    def readSettings(self):

        settings = QSettings("Software Inc.", "Icon Editor")
        settings.beginGroup("mainWindow")
        self.superWidget.restoreGeometry(settings.value("geometry"))
        self.superWidget.restoreState(settings.value("state"))
        self.superWidget.resize(settings.value("size"))
        settings.endGroup()

        toolbtnList = self.toolbar.findChildren(QToolButton)
        for toolbtn in toolbtnList:
            if toolbtn.isChecked():
                toolbtn.click()

    def creatNewDockWindow(self, w, a):
        self.superWidget.addDockWidget(a, w)

    def ble_bytes_send(self, byte):
        self.deviceHandler.characteristicWrite(byte)

    def ble_string_send(self, string):
        string = string.replace(' ', '')
        self.deviceHandler.characteristicWrite(bytes.fromhex(string))

    def govee_ble_send(self, string):
        hex = bytes.fromhex(string)
        send_hex = [0] * 20
        for i in range(0, len(hex)):
            send_hex[i] = hex[i]
        send_hex[19] = self.Govee_Utils_GetBccCode(send_hex)
        byteArray = bytearray(send_hex)
        hex_string = bytearray.hex(byteArray)
        self.ble_bytes_send(bytes.fromhex(hex_string))

    def Govee_Utils_GetBccCode(self, data_array):
        ret = 0
        for data in data_array:
            ret ^= data

        return ret








