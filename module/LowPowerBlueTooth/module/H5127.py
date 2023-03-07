import math

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QDockWidget, QWidget, QGridLayout, QTextEdit, QPushButton, QToolButton, QLabel

from sdk_src.utils import utils


class H5127:
    def __init__(self, bleMainWindow):
        self.label_distance = None
        self.toolBtn = None
        self.label_Status = None
        self.gridlayout = None
        self.WidgetContents = None
        self.dock = None
        self.motherClass = bleMainWindow
        self.motherWidget = self.motherClass.superWidget
        self.form_init()

    def form_init(self):
        self.dock = QDockWidget()
        self.dock.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetClosable |
            QDockWidget.DockWidgetFeature.DockWidgetMovable |
            QDockWidget.DockWidgetFeature.DockWidgetFloatable)

        self.dock.setWindowTitle("H5127")
        self.dock.setObjectName("H5127")

        self.WidgetContents = QWidget(self.dock)
        self.gridlayout = QGridLayout(self.WidgetContents)

        self.label_Status = QLabel()
        self.label_Status.setText("状态")
        self.label_Status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = self.label_Status.font()
        font.setPointSize(50)
        self.label_Status.setFont(font)

        self.label_distance = QLabel()
        self.label_distance.setText("状态")
        self.label_distance.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = self.label_distance.font()
        font.setPointSize(50)
        self.label_distance.setFont(font)

        self.gridlayout.addWidget(self.label_Status, 0, 0)
        self.gridlayout.addWidget(self.label_distance, 1, 0)

        self.motherClass.creatNewDockWindow(self.dock, Qt.DockWidgetArea.TopDockWidgetArea)
        self.dock.setWidget(self.WidgetContents)

        self.toolBtn = QToolButton(self.WidgetContents)  # 创建QToolButton
        self.toolBtn.setText(self.dock.windowTitle())
        self.toolBtn.clicked.connect(self.closeWindow)
        self.motherClass.toolbar.addWidget(self.toolBtn)  # 向工具栏添加QToolButton按钮

    def closeWindow(self):
        # self.motherClass.closeAllWindow()
        self.dock.setVisible(bool(1 - self.dock.isVisible()))

    def ble_rx_data_func(self, Bytes: bytes):
        if Bytes[2] == 0x00:
            self.label_Status.setText("无人")
            self.label_Status.setStyleSheet("QLabel{background-color:rgb(255,0,0);}")
        if Bytes[2] == 0x01:
            self.label_Status.setText("有人")
            self.label_Status.setStyleSheet("QLabel{background-color:rgb(0,255,0);}")
        if Bytes[2] == 0x02:
            self.label_Status.setText("有人接近")
            self.label_Status.setStyleSheet("QLabel{background-color:rgb(0,0,255);}")
        if Bytes[2] == 0x03:
            self.label_Status.setText("有人远离")
            self.label_Status.setStyleSheet("QLabel{background-color:rgb(0,125,125);}")
        distance = (Bytes[3] << 8) + Bytes[4]
        self.label_distance.setText(str(distance))
