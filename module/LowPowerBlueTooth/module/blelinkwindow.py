from PyQt6 import QtWidgets
from PyQt6.QtCore import QSettings, Qt, QTimer
from PyQt6.QtWidgets import QWidget, QLineEdit, QPushButton, QListWidget, QVBoxLayout, QHBoxLayout

from module.utils import utils


class blelinkwindow():
    def __init__(self, blemainWin):
        super().__init__()

        self.timer_keepAlive = QTimer()
        self.timer_keepAlive.setInterval(2000)
        self.timer_keepAlive.timeout.connect(self.keepalive)

        self.toolBtn = None
        self.text_sku = None
        self.dockblelink = None
        self.sku_list = None
        self.button_continue = None
        self.button_stop = None
        self.button_discon = None
        self.cmd_send = None
        self.cmd_receive = None
        self.button_clear = None
        self.button_ble_send = None
        self.button_scan_sku = None
        self.text_ble_send = None
        self.superClass = blemainWin
        self.init()

    def init(self):
        settings = QSettings("setting.ini", QSettings.Format.IniFormat)
        settings.beginGroup("BleConfig")
        sku = settings.value("sku")
        settings.endGroup()
        # ----------------------------------------- 在界面添加窗口
        self.dockblelink = QtWidgets.QDockWidget()
        self.dockblelink.setWindowTitle("连接")
        self.dockblelink.setObjectName("连接蓝牙窗口")
        self.dockblelink.setMaximumWidth(300)

        dockWidgetContents = QWidget(self.dockblelink)
        # dockWidgetContents.setGeometry(QRect(10, 10, 100, 400)) # 从屏幕上（10，10）位置开始（即为最左上角的点），显示一个30 * 35的界面（宽30，高35）

        self.text_sku = QLineEdit(dockWidgetContents)
        if sku is not None:
            if len(sku) == 0:
                self.text_sku.setText("7160")
            else:
                self.text_sku.setText(sku)

        self.text_ble_send = QLineEdit(dockWidgetContents)
        self.text_ble_send.setText("aa01")

        self.button_scan_sku = QPushButton(dockWidgetContents)
        self.button_scan_sku.setText("scan")

        self.button_ble_send = QPushButton(dockWidgetContents)
        self.button_ble_send.setText("发送")
        self.button_stop = QPushButton(dockWidgetContents)
        self.button_stop.setText("stop")
        self.button_continue = QPushButton(dockWidgetContents)
        self.button_continue.setText("继续")
        self.sku_list = QListWidget(dockWidgetContents)
        self.sku_list.setMaximumHeight(250)
        self.button_discon = QPushButton(dockWidgetContents)
        self.button_discon.setText("断开")
        self.cmd_send = QLineEdit(dockWidgetContents)
        self.cmd_send.setReadOnly(True)
        self.cmd_receive = QLineEdit(dockWidgetContents)
        self.cmd_receive.setReadOnly(True)
        self.button_clear = QPushButton(dockWidgetContents)
        self.button_clear.setText("clear")
        # new QPushButton() 在空板上增加按键
        # new QPushButton(this) 在当前板上增加按键
        # new QPushButton(dock) 在dock板上增加按键

        # 左布局
        left_verticalLayout = QVBoxLayout()
        # left_verticalLayout.setSpacing(20) # 间距
        left_verticalLayout.setContentsMargins(5, 5, 5, 5)  # setMargin可以设置左、上、右、下的外边距，设置之后，该函数可以主动设置
        # left_verticalLayout.setObjectName(QString::fromUtf8("verticalLayout"))
        left_verticalLayout.addWidget(self.text_sku)
        left_verticalLayout.addWidget(self.text_ble_send)

        # 右布局
        right_verticalLayout = QVBoxLayout()
        # right_verticalLayout.setSpacing(20) # 间距
        right_verticalLayout.setContentsMargins(5, 5, 5, 5)  # setMargin可以设置左、上、右、下的外边距，设置之后，该函数可以主动设置
        right_verticalLayout.addWidget(self.button_scan_sku)
        right_verticalLayout.addWidget(self.button_ble_send)

        # 将两个垂直布局放入水平布局
        horizontalLayout = QHBoxLayout()
        # horizontalLayout.setSpacing(10) # 间距
        horizontalLayout.setContentsMargins(5, 5, 5, 5)  # setMargin可以设置左、上、右、下的外边距，设置之后，该函数可以主动设置
        horizontalLayout.addItem(left_verticalLayout)
        horizontalLayout.addItem(right_verticalLayout)

        # 将剩余按钮放入水平布局
        horizontalLayout1 = QHBoxLayout()
        # horizontalLayout1.setSpacing(10) # 间距
        horizontalLayout1.setContentsMargins(5, 5, 5, 5)  # setMargin可以设置左、上、右、下的外边距，设置之后，该函数可以主动设置
        horizontalLayout1.addWidget(self.button_discon)
        horizontalLayout1.addWidget(self.button_stop)
        horizontalLayout1.addWidget(self.button_continue)
        horizontalLayout1.addWidget(self.button_clear)

        # 将两个水平布局放入新的垂直布局
        updown_verticalLayout = QVBoxLayout(dockWidgetContents)
        updown_verticalLayout.addItem(horizontalLayout)
        updown_verticalLayout.addItem(horizontalLayout1)
        updown_verticalLayout.addWidget(self.cmd_send)
        updown_verticalLayout.addWidget(self.cmd_receive)
        updown_verticalLayout.addWidget(self.sku_list)

        # 绑定控件的回调函数
        self.button_scan_sku.clicked.connect(self.scanButton_clicked)
        self.sku_list.itemClicked.connect(self.bleDevlist_itemClicked)
        self.button_ble_send.clicked.connect(self.sendButton_clicked)
        self.button_stop.clicked.connect(self.pauseButton_clicked)
        self.button_continue.clicked.connect(self.continueButton_clicked)
        self.button_discon.clicked.connect(self.disconButton_clicked)
        self.button_clear.clicked.connect(self.clearButton_clicked)

        self.superClass.deviceFinder.signal_devicefound.connect(self.sku_list_item_append)
        self.superClass.deviceHandler.emit_bleConnectSuccessful.connect(self.bleDeviceConnectedOk)
        self.superClass.deviceHandler.emit_bleMessageChange.connect(self.ble_rx_data_func)

        self.dockblelink.setWidget(dockWidgetContents)
        # 进行布局
        self.superClass.superWidget.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, self.dockblelink)

        self.toolBtn = QtWidgets.QToolButton()  # 创建QToolButton
        self.toolBtn.setText(self.dockblelink.windowTitle())
        self.toolBtn.clicked.connect(self.closeWindow)
        self.superClass.toolbar.addWidget(self.toolBtn)  # 向工具栏添加QToolButton按钮

        self.dockblelink.setVisible(True)

    def sku_list_item_append(self, device):
        sku = self.text_sku.text()
        if sku in device.name():
            self.sku_list.addItem(device.name())

    def closeWindow(self):
        # self.superClass.closeAllWindow()
        self.dockblelink.setVisible(bool(1 - self.dockblelink.isVisible()))

    def scanButton_clicked(self):
        sku = self.button_scan_sku.text()
        if sku == "scan":
            self.sku_list.clear()
            self.button_scan_sku.setText("stop")
            self.superClass.deviceFinder.startSearch()
        elif sku == "stop":
            self.button_scan_sku.setText("scan")
            self.superClass.deviceFinder.stopSearch()

        settings = QSettings("setting.ini", QSettings.Format.IniFormat)
        settings.beginGroup("BleConfig")
        settings.setValue("sku", self.text_sku.text())
        settings.endGroup()

    def sendButton_clicked(self):
        data = self.text_ble_send.text()
        self.superClass.govee_ble_string_send(data)

    def disconButton_clicked(self):
        if self.timer_keepAlive:
            self.timer_keepAlive.stop()
        self.superClass.deviceHandler.disconnect()
        self.superClass.setInfo("disconnected.")

    def pauseButton_clicked(self):
        self.superClass.deviceHandler.disconnectService()

    def continueButton_clicked(self):
        self.superClass.deviceHandler.continueConnectService()

    def clearButton_clicked(self):
        self.cmd_send.setText("")
        self.cmd_receive.setText("")
        self.superClass.setInfo("clear")

    def bleDevlist_itemClicked(self, item):
        sku = self.button_scan_sku.text()
        if sku == "stop":
            self.button_scan_sku.setText("scan")
            self.superClass.deviceFinder.stopSearch()
        self.superClass.deviceFinder.connectToDevice(item.text())

    def bleDeviceConnectedOk(self):
        self.timer_keepAlive.start()

    def keepalive(self):
        self.superClass.govee_ble_string_send("aa01")

    def ble_rx_data_func(self, Bytes: bytes):
        self.cmd_receive.setText(bytes.hex(Bytes))
