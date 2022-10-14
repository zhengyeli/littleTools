from PyQt6.QtCore import QObject, QIODevice, QFile, QTextStream
from PyQt6.QtWidgets import QTabBar

from Ui_MainWindow import Ui_MainWindow
from PyQt6 import QtCore, QtGui, QtWidgets

from module.LowPowerBlueTooth.bleMainWin import BleMainWin
from module.SerialPort.FrmComTool import FrmComTool
from module.SerialPort.Ui_frmComTool import Ui_frmComTool
from module.iotLogAnalyzer.main import govee_mqtt_log
from module.photograph.graphDraw import BasicArrayPlot, dynamicArrayPlot

import qss


class CommonHelper:
    def __init__(self):
        pass

    # 根据文件路径读取qss
    @staticmethod
    def readQssFile(file_path):
        with open(file_path, 'r') as f:
            return f.read()

    # 从资源文件读取qss
    @staticmethod
    def readQssResource(resource_path):
        stream = QFile(resource_path)
        stream.open(QIODevice.OpenModeFlag.ReadOnly)
        return QTextStream(stream).readAll()


class MainWindow(QObject, Ui_MainWindow):
    btn_list = None

    def __init__(self, ui):
        super().__init__()
        self.main = None
        self.ble = None
        self.comTool = None
        self.plot = None

        self.mainWidget = None
        self.ui = ui

        self.styleFile = ""
        self.button_init()
        self.ui.stackedWidget.setCurrentIndex(0)
        # self.ui = Ui_MainWindow(self.ui)
        self.tabWidget_trigger_init()
        self.module_init()

    def widgetRegister(self, w):
        self.mainWidget = w
        self.styleFile = "./qss/daniu.qss"  # 根据文件路径加载
        self.windowStyleSheetRefresh()

    def windowStyleSheetRefresh(self):
        qssStyle = CommonHelper.readQssResource(self.styleFile)
        self.mainWidget.setStyleSheet(qssStyle)

    def eventFilter(self, obj, event):
        # print(123)
        return super().eventFilter(obj, event)

    def keyPressEvent(self, keyevent):
        print("keyevent")
        return False

    def button_init(self):
        btn_list = self.ui.widgetTop.findChildren(QtWidgets.QAbstractButton)
        for btn in btn_list:
            btn.setIconSize(QtCore.QSize(32, 32))
            btn.setMinimumWidth(85)
            btn.setCheckable(True)
            btn.clicked.connect(lambda: self.topWidget_Button_Clicked())
        self.ui.btnMain.setChecked(True)
        self.ui.page1.setStyleSheet("QWidget[flag=\"left\"] QAbstractButton{min-height:60px;max-height:%1px;}")
        self.ui.page2.setStyleSheet("QWidget[flag=\"left\"] QAbstractButton{min-height:25px;max-height:%1px;}")

    def tabWidget_trigger_init(self):
        self.ui.tabWidget.tabCloseRequested.connect(lambda i:
                                                    self.ui.tabWidget.removeTab(i))
        self.ui.tabWidget.tabBarClicked.connect(self.module_serialports_addPort)

    def topWidget_Button_Clicked(self):
        name = self.ui.widgetTop.sender().text()
        btn_list = self.ui.widgetTop.findChildren(QtWidgets.QAbstractButton)
        for btn in btn_list:
            btn.setChecked(btn.text() == name)

        if name == "串口调试":
            self.ui.stackedWidget.setCurrentIndex(0)
        elif name == "蓝牙调试":
            self.ui.stackedWidget.setCurrentIndex(1)
        elif name == "图表显示":
            self.ui.stackedWidget.setCurrentIndex(2)
        elif name == "日志分析":
            self.ui.stackedWidget.setCurrentIndex(3)
        elif name == "用户退出":
            exit(0)

    def module_init(self):
        self.module_photoGraph_init()
        self.module_serialports_init()
        self.module_lowPowerBle_init()
        self.module_logAnalyse_init()

    def module_logAnalyse_init(self):
        govee_mqtt_log(self)

    # 串口
    def module_serialports_init(self):
        # enable tab close button
        self.ui.tabWidget.setTabsClosable(True)
        self.ui.tabWidget.removeTab(0)
        widget = QtWidgets.QWidget()
        w = Ui_frmComTool()
        w.setupUi(widget)
        self.comTool = FrmComTool(w, self)
        self.ui.tabWidget.addTab(widget, "comx")

        self.ui.tabWidget.tabBar().setTabButton(self.ui.tabWidget.addTab(QtWidgets.QWidget(), "添加"), QTabBar.ButtonPosition.RightSide, None)

    def module_serialports_addPort(self, i):
        if self.ui.tabWidget.tabText(i) == "添加":
            self.ui.tabWidget.removeTab(i)
            widget = QtWidgets.QWidget(self.mainWidget)
            w = Ui_frmComTool()
            w.setupUi(widget)
            self.comTool = FrmComTool(w, self)
            self.ui.tabWidget.addTab(widget, "comx")
            self.ui.tabWidget.setCurrentIndex(i)

            self.ui.tabWidget.tabBar().setTabButton(self.ui.tabWidget.addTab(QtWidgets.QWidget(), "添加"), QTabBar.ButtonPosition.RightSide, None)
            self.windowStyleSheetRefresh()

    def module_lowPowerBle_init(self):
        self.ble = BleMainWin(self.ui.page2)

    def module_photoGraph_init(self):
        enable = False
        if enable:
            self.plot = BasicArrayPlot(self.ui.page3)
        else:
            self.plot = dynamicArrayPlot(self.ui.page3)
