from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QDockWidget, QTextEdit, QToolBar, QToolButton

from module.LowPowerBlueTooth.api.deviceFinder import DeviceFinder
from module.LowPowerBlueTooth.module.blelinkwindow import blelinkwindow
from module.LowPowerBlueTooth.module.bleuartwindow import bleUartWindow
from module.LowPowerBlueTooth.module.blewifiwindow import blecConfigWifi
from module.LowPowerBlueTooth.ui.Ui_BleMainWin import Ui_BleMainWin


def Govee_Utils_GetBccCode(data_array):
    ret = 0
    for data in data_array:
        ret ^= data

    return ret


class BleMainWin(QMainWindow):
    def __del__(self):
        pass

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

        self.DockWidgetInfo = QtWidgets.QDockWidget()
        self.text_info = QTextEdit()
        self.text_info.setReadOnly(True)
        self.DockWidgetInfo.setWidget(self.text_info)
        self.DockWidgetInfo.setObjectName("软件输出信息")
        self.DockWidgetInfo.setWindowTitle("信息")
        self.DockWidgetInfo.setVisible(True)
        self.DockWidgetInfo.setStyleSheet("border:none")
        self.superWidget.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.DockWidgetInfo)

        # ----------------------------------------- 在工具栏添加图标按钮
        self.toolbar = QToolBar(self.superWidget)
        self.toolbar.setObjectName("toolbar")
        self.toolbar.setWindowTitle("toolbar")
        self.toolbar.setMovable(False)

        self.DockWidgetInfo_toolBtn = QtWidgets.QToolButton(self.superWidget)  # 创建QToolButton
        self.DockWidgetInfo_toolBtn.setText(self.DockWidgetInfo.windowTitle())
        self.toolbar.addWidget(self.DockWidgetInfo_toolBtn)
        self.superWidget.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolbar)
        self.DockWidgetInfo_toolBtn.clicked.connect(self.DockWidgetInfo_btn_click)

        # -----------------------------------------  second: ble api init

        self.deviceFinder = DeviceFinder(self.text_info)
        self.deviceHandler = self.deviceFinder.m_deviceHandler

        # self.deviceFinder.scanDeviceResult.connect(self.addBleDevToList)
        self.deviceHandler.emit_bleMessageChange.connect(self.ble_rx_data_func)
        # self.deviceHandler.connectSuccess.connect(self.bleConnectSuccess)
        # self.deviceHandler.disconnectOccur.connect(self.disconButton_clicked)

        # ----------------------------------------- other
        self.bleLink = blelinkwindow(self)
        self.bleUart = bleUartWindow(self)
        self.bleWifi = blecConfigWifi(self)

        self.text_info.append("tip :\n"
                              "   window              usage        \n"
                              "1. info : some software info print\n"
                              "2. manual : send uart cmd to mcu via ble \n"
                              "3. tcpSocket : use tcp socket talk with dev\n"
                              "4. bleLink : connect to dev via ble\n"
                              "5. debug : view dev debug message via ble\n"
                              )

        self.superWidget.setStatusBar(None)
        self.superWidget.setMenuBar(None)
        self.superWidget.centralWidget().close()

        dockList = self.superWidget.findChildren(QtWidgets.QDockWidget)
        for dock in dockList:
            dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetClosable |
                             QDockWidget.DockWidgetFeature.DockWidgetMovable |
                             QDockWidget.DockWidgetFeature.DockWidgetFloatable)

        self.closeAllWindow()
        self.DockWidgetInfo_btn_click()

    def setInfo(self, string):
        if self.text_info:
            self.text_info.append(string)

    def DockWidgetInfo_btn_click(self):
        # self.closeAllWindow()
        self.DockWidgetInfo.setVisible(bool(1 - self.DockWidgetInfo.isVisible()))

    def closeAllWindow(self):
        dockList = self.superWidget.findChildren(QDockWidget)
        for dock in dockList:
            dock.setVisible(False)

        toolBtnList = self.toolbar.findChildren(QToolButton)
        for toolBtn in toolBtnList:
            toolBtn.setChecked(False)

    # def saveSettings(self):
    #     settings = QSettings("Software Inc.", "Icon Editor")
    #     settings.beginGroup("mainWindow")
    #     settings.setValue("geometry", self.superWidget.saveGeometry())
    #     settings.setValue("size", self.superWidget.size())
    #     settings.setValue("state", self.superWidget.saveState())
    #     settings.endGroup()
    #
    # def readSettings(self):
    #     settings = QSettings("Software Inc.", "Icon Editor")
    #     settings.beginGroup("mainWindow")
    #     self.superWidget.restoreGeometry(settings.value("geometry"))
    #     self.superWidget.restoreState(settings.value("state"))
    #     self.superWidget.resize(settings.value("size"))
    #     settings.endGroup()
    #

    def creatNewDockWindow(self, w, a):
        self.superWidget.addDockWidget(a, w)

    def ble_bytes_send(self, byte):
        self.deviceHandler.characteristicWrite(byte)

    def ble_string_send(self, string):
        string = string.replace(' ', '')
        self.deviceHandler.characteristicWrite(bytes.fromhex(string))

    def govee_ble_charArray_send(self, array):
        array[19] = Govee_Utils_GetBccCode(array)
        byteArray = bytearray(array)
        hex_string = bytearray.hex(byteArray)
        self.ble_bytes_send(bytes.fromhex(hex_string))

    def govee_ble_string_send(self, string):
        sendHex = bytes.fromhex(string)
        send_hex = [0] * 20
        for i in range(0, len(sendHex)):
            send_hex[i] = sendHex[i]
        send_hex[19] = Govee_Utils_GetBccCode(send_hex)
        byteArray = bytearray(send_hex)
        hex_string = bytearray.hex(byteArray)
        self.ble_bytes_send(bytes.fromhex(hex_string))

    def ble_rx_data_func(self, bytesArray):
        self.setInfo(str(bytesArray))
        self.bleLink.ble_rx_data_func(bytesArray)
