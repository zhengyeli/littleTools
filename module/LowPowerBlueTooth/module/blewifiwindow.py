import math
import struct

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QDockWidget, QWidget, QGridLayout, QTextEdit, QPushButton, QToolButton
from numpy import byte

from module.utils import utils


class wifi_para:
    def __init__(self):
        self.ssid = [0] * 33
        self.password = [0] * 65
        self.environment = 0
        self.timezone = 0
        self.iot_environment = 0
        self.time_offset = 0
        self.url_len = [0] * 2
        self.url = [0] * 129


class bleconfigwifi:
    def __init__(self, bleMainWindow):
        self.byte_array = []
        self.send_str_maxIndex = 0
        self.ble_Send_len = 0
        self.send_str = [0] * 20
        self.indexHadSend = 0
        self.configWifi_timer = None
        self.motherClass = bleMainWindow
        self.motherWidget = self.motherClass.superWidget

        self.toolBtn = None
        self.gridlayout = None
        self.dockBleWifi = None
        self.WidgetContents = None

        self.form_init()

    def form_init(self):
        self.dockBleWifi = QDockWidget()
        self.dockBleWifi.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetClosable | 
            QDockWidget.DockWidgetFeature.DockWidgetMovable | 
            QDockWidget.DockWidgetFeature.DockWidgetFloatable)

        self.dockBleWifi.setWindowTitle("wifi")
        self.dockBleWifi.setObjectName("config wifi窗口")

        self.WidgetContents = QWidget(self.dockBleWifi)
        self.gridlayout = QGridLayout(self.WidgetContents)

        self.text_Ssid = QTextEdit(self.WidgetContents)
        self.text_Ssid.setText("Govee")
        self.text_Ssid.setMinimumHeight(30)
        self.text_Ssid.setMaximumHeight(30)

        self.text_Password = QTextEdit(self.WidgetContents)
        self.text_Password.setText("starstarlight")
        self.text_Password.setMinimumHeight(30)
        self.text_Password.setMaximumHeight(30)

        button_clear_wifi = QPushButton(self.WidgetContents)
        button_clear_wifi.setMaximumHeight(20) # limit
        button_clear_wifi.setMinimumWidth(80)
        button_clear_wifi.setText("clear all")

        button_set_wifi = QPushButton(self.WidgetContents)
        button_set_wifi.setMaximumHeight(20) # limit
        button_set_wifi.setMinimumWidth(80)
        button_set_wifi.setText("config wifi now")

        self.gridlayout.addWidget(self.text_Ssid, 0, 0)
        self.gridlayout.addWidget(button_clear_wifi, 0, 1)
        self.gridlayout.addWidget(self.text_Password, 1, 0)
        self.gridlayout.addWidget(button_set_wifi, 1, 1)

        button_clear_wifi.clicked.connect(self.clear)
        button_set_wifi.clicked.connect(self.setwifi)

        self.motherClass.creatNewDockWindow(self.dockBleWifi, Qt.DockWidgetArea.TopDockWidgetArea)
        self.dockBleWifi.setWidget(self.WidgetContents)

        self.toolBtn = QToolButton(self.WidgetContents)  # 创建QToolButton
        self.toolBtn.setText(self.dockBleWifi.windowTitle())
        self.toolBtn.clicked.connect(self.closeWindow)
        self.motherClass.toolbar.addWidget(self.toolBtn)  # 向工具栏添加QToolButton按钮

    def clear(self):
        self.text_Ssid.clear()
        self.text_Password.clear()

    def setwifi(self):
        url = "https://dev-device.govee.com"
        if len(self.text_Ssid.toPlainText()) == 0 or len(self.text_Password.toPlainText()) == 0:
            self.motherClass.setInfo("ssid or password is null")

        if len(self.text_Ssid.toPlainText()) == 0 or len(self.text_Password.toPlainText()) < 8:
            self.motherClass.setInfo("err ssid or password")

        self.ble_Send_len = len(self.text_Ssid.toPlainText()) + len(self.text_Password.toPlainText()) + len(url) + 8

        wifi_buf = wifi_para()
        wifi_buf.ssid.append(self.text_Ssid.toPlainText())
        wifi_buf.ssid.append(len(self.text_Ssid.toPlainText()) + 1)

        wifi_buf.password.append(self.text_Password.toPlainText())
        wifi_buf.password.append(len(self.text_Password.toPlainText()) + 1)

        wifi_buf.environment = 1
        wifi_buf.iot_environment = 1
        wifi_buf.time_offset = 8

        self.byte_array = utils().int2bytes(len(self.text_Ssid.toPlainText()))
        self.byte_array += bytes(self.text_Ssid.toPlainText(), 'utf-8')
        self.byte_array += utils().int2bytes(len(self.text_Password.toPlainText()))
        self.byte_array += bytes(self.text_Password.toPlainText(), 'utf-8')
        self.byte_array += utils().int2bytes(wifi_buf.environment)
        self.byte_array += utils().int2bytes(wifi_buf.time_offset)
        self.byte_array += utils().int2bytes(wifi_buf.iot_environment)
        self.byte_array += utils().int2bytes(len(url))
        self.byte_array += utils().string2bytes(url)

        self.motherClass.setInfo("start...")
        self.motherClass.setInfo(str(self.byte_array))

        self.configWifi_timer = QTimer()
        self.configWifi_timer.setInterval(500)
        self.configWifi_timer.timeout.connect(self.timerSendWifi)
        self.configWifi_timer.start()

        self.send_str[0] = 0xa1
        self.send_str[1] = 0x11
        self.send_str_maxIndex = math.ceil(self.ble_Send_len / 16)
        
    def timerSendWifi(self):
        if self.indexHadSend == 0:
            # first packet
            self.send_str[2:19] = [0] * 18
            self.send_str[2] = 0x00
            self.send_str[3] = self.ble_Send_len - 2
        elif 1 <= self.indexHadSend < self.send_str_maxIndex - 1:
            self.send_str[2:19] = [0] * 18
            self.send_str[2] = self.indexHadSend
            self.send_str[3:19] = self.byte_array[16 * self.indexHadSend : 16 * self.indexHadSend + 16]
        else:
            self.indexHadSend = 0
            self.send_str[2:19] = [0] * 18
            self.send_str[2] = 0xff
            self.ble_Send_len = 0
            self.send_str_maxIndex = 0

            if self.configWifi_timer is not None:
                self.configWifi_timer.stop()

            self.motherClass.govee_ble_charArray_send(self.send_str)
            return
        self.indexHadSend += 1
        self.motherClass.govee_ble_charArray_send(self.send_str)

    def closeWindow(self):
        # self.motherClass.closeAllWindow()
        self.dockBleWifi.setVisible(bool(1 - self.dockBleWifi.isVisible()))

