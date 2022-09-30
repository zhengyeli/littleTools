from tokenize import String

from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QWidget

from Ui_MainWindow import Ui_MainWindow
from PyQt6 import QtCore, QtGui, QtWidgets

from module.LowPowerBlueTooth import bleMainWin
from module.SerialPort.Ui_frmComTool import Ui_frmComTool
from module.SerialPort.FrmComTool import FrmComTool
from module.photograph.graphDraw import BasicArrayPlot, dynamicArrayPlot


class MainWindow(QObject, Ui_MainWindow):
    btn_list = None

    def __init__(self, ui):
        super().__init__()
        self.ble = None
        self.comTool = None
        self.plot = None
        
        self.ui = ui
        self.button_init()
        self.ui.stackedWidget.setCurrentIndex(0)
        # self.ui = Ui_MainWindow(self.ui)

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

    def topWidget_Button_Clicked(self):
        name = self.ui.widgetTop.sender().text()
        btn_list = self.ui.widgetTop.findChildren(QtWidgets.QAbstractButton)
        for btn in btn_list:
            btn.setChecked(btn.text() == name)

        if name == "串口调试":
            self.ui.stackedWidget.setCurrentIndex(0)
        elif name == "蓝牙调试":
            self.ui.stackedWidget.setCurrentIndex(1)
        elif name == "警情查询":
            self.ui.stackedWidget.setCurrentIndex(2)
        elif name == "调试帮助":
            self.ui.stackedWidget.setCurrentIndex(3)
        elif name == "用户退出":
            exit(0)

