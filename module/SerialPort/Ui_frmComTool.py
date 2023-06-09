# Form implementation generated from reading ui file 'Ui_frmComTool.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QTextEdit

from module.iotLogAnalyzer.MTextEdit import MTextEdit


class Ui_frmComTool(object):
    def setupUi(self, frmComTool):
        frmComTool.setObjectName("frmComTool")
        frmComTool.resize(1173, 741)
        self.gridLayout_3 = QtWidgets.QGridLayout(frmComTool)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.widgeMain = QtWidgets.QWidget(frmComTool)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widgeMain.sizePolicy().hasHeightForWidth())
        self.widgeMain.setSizePolicy(sizePolicy)
        self.widgeMain.setObjectName("widgeMain")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widgeMain)
        self.horizontalLayout.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.txtMain = QTextEdit()
        self.txtMain.setObjectName("txtMain")
        self.horizontalLayout.addWidget(self.txtMain)
        self.widgetRight = QtWidgets.QWidget(self.widgeMain)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(self.widgetRight.sizePolicy().hasHeightForWidth())
        self.widgetRight.setSizePolicy(sizePolicy)
        self.widgetRight.setMinimumSize(QtCore.QSize(200, 0))
        self.widgetRight.setMaximumSize(QtCore.QSize(300, 16777215))
        self.widgetRight.setObjectName("widgetRight")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widgetRight)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.widgetRight)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.TabPosition.South)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_5.setContentsMargins(6, 6, 6, 6)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.ckAutoSend = QtWidgets.QCheckBox(self.tab)
        self.ckAutoSend.setObjectName("ckAutoSend")
        self.gridLayout.addWidget(self.ckAutoSend, 0, 0, 1, 1)
        self.btnSend = QtWidgets.QPushButton(self.tab)
        self.btnSend.setMinimumSize(QtCore.QSize(80, 0))
        self.btnSend.setMaximumSize(QtCore.QSize(80, 16777215))
        self.btnSend.setObjectName("btnSend")
        self.gridLayout.addWidget(self.btnSend, 4, 1, 1, 1)
        self.ckAutoSave = QtWidgets.QCheckBox(self.tab)
        self.ckAutoSave.setObjectName("ckAutoSave")
        self.gridLayout.addWidget(self.ckAutoSave, 1, 0, 1, 1)
        self.cboxData = QtWidgets.QComboBox(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cboxData.sizePolicy().hasHeightForWidth())
        self.cboxData.setSizePolicy(sizePolicy)
        self.cboxData.setEditable(True)
        self.cboxData.setDuplicatesEnabled(False)
        self.cboxData.setObjectName("cboxData")
        self.gridLayout.addWidget(self.cboxData, 4, 0, 1, 1)
        self.cboxSaveInterval = QtWidgets.QComboBox(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cboxSaveInterval.sizePolicy().hasHeightForWidth())
        self.cboxSaveInterval.setSizePolicy(sizePolicy)
        self.cboxSaveInterval.setObjectName("cboxSaveInterval")
        self.gridLayout.addWidget(self.cboxSaveInterval, 1, 1, 1, 1)
        self.btnSave = QtWidgets.QPushButton(self.tab)
        self.btnSave.setObjectName("btnSave")
        self.gridLayout.addWidget(self.btnSave, 2, 1, 1, 1)
        self.cboxSendInterval = QtWidgets.QComboBox(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cboxSendInterval.sizePolicy().hasHeightForWidth())
        self.cboxSendInterval.setSizePolicy(sizePolicy)
        self.cboxSendInterval.setObjectName("cboxSendInterval")
        self.gridLayout.addWidget(self.cboxSendInterval, 0, 1, 1, 1)
        self.btnStopShow = QtWidgets.QPushButton(self.tab)
        self.btnStopShow.setObjectName("btnStopShow")
        self.gridLayout.addWidget(self.btnStopShow, 2, 0, 1, 1)
        self.btnData = QtWidgets.QPushButton(self.tab)
        self.btnData.setObjectName("btnData")
        self.gridLayout.addWidget(self.btnData, 3, 0, 1, 1)
        self.btnClear = QtWidgets.QPushButton(self.tab)
        self.btnClear.setObjectName("btnClear")
        self.gridLayout.addWidget(self.btnClear, 3, 1, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout, 19, 0, 1, 3)
        self.cboxPortName = QtWidgets.QComboBox(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cboxPortName.sizePolicy().hasHeightForWidth())
        self.cboxPortName.setSizePolicy(sizePolicy)
        self.cboxPortName.setEditable(True)
        self.cboxPortName.setObjectName("cboxPortName")
        self.gridLayout_5.addWidget(self.cboxPortName, 0, 2, 1, 1)
        self.btnOpen = QtWidgets.QPushButton(self.tab)
        self.btnOpen.setObjectName("btnOpen")
        self.gridLayout_5.addWidget(self.btnOpen, 15, 2, 1, 1)
        self.labParity = QtWidgets.QLabel(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labParity.sizePolicy().hasHeightForWidth())
        self.labParity.setSizePolicy(sizePolicy)
        self.labParity.setObjectName("labParity")
        self.gridLayout_5.addWidget(self.labParity, 3, 0, 1, 1)
        self.ckAutoClear = QtWidgets.QCheckBox(self.tab)
        self.ckAutoClear.setObjectName("ckAutoClear")
        self.gridLayout_5.addWidget(self.ckAutoClear, 8, 2, 1, 1)
        self.labDataBit = QtWidgets.QLabel(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labDataBit.sizePolicy().hasHeightForWidth())
        self.labDataBit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.labDataBit.setFont(font)
        self.labDataBit.setObjectName("labDataBit")
        self.gridLayout_5.addWidget(self.labDataBit, 2, 0, 1, 1)
        self.btnReceiveCount = QtWidgets.QPushButton(self.tab)
        self.btnReceiveCount.setObjectName("btnReceiveCount")
        self.gridLayout_5.addWidget(self.btnReceiveCount, 12, 0, 1, 3)
        self.cboxStopBit = QtWidgets.QComboBox(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cboxStopBit.sizePolicy().hasHeightForWidth())
        self.cboxStopBit.setSizePolicy(sizePolicy)
        self.cboxStopBit.setObjectName("cboxStopBit")
        self.gridLayout_5.addWidget(self.cboxStopBit, 4, 2, 1, 1)
        self.ckHexReceive = QtWidgets.QCheckBox(self.tab)
        self.ckHexReceive.setObjectName("ckHexReceive")
        self.gridLayout_5.addWidget(self.ckHexReceive, 7, 2, 1, 1)
        self.labPortName = QtWidgets.QLabel(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labPortName.sizePolicy().hasHeightForWidth())
        self.labPortName.setSizePolicy(sizePolicy)
        self.labPortName.setObjectName("labPortName")
        self.gridLayout_5.addWidget(self.labPortName, 0, 0, 1, 1)
        self.cboxBaudRate = QtWidgets.QComboBox(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cboxBaudRate.sizePolicy().hasHeightForWidth())
        self.cboxBaudRate.setSizePolicy(sizePolicy)
        self.cboxBaudRate.setEditable(True)
        self.cboxBaudRate.setObjectName("cboxBaudRate")
        self.gridLayout_5.addWidget(self.cboxBaudRate, 1, 2, 1, 1)
        self.labStopBit = QtWidgets.QLabel(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labStopBit.sizePolicy().hasHeightForWidth())
        self.labStopBit.setSizePolicy(sizePolicy)
        self.labStopBit.setObjectName("labStopBit")
        self.gridLayout_5.addWidget(self.labStopBit, 4, 0, 1, 1)
        self.btnSendCount = QtWidgets.QPushButton(self.tab)
        self.btnSendCount.setObjectName("btnSendCount")
        self.gridLayout_5.addWidget(self.btnSendCount, 11, 0, 1, 3)
        self.cboxLogTime = QtWidgets.QCheckBox(self.tab)
        self.cboxLogTime.setObjectName("cboxLogTime")
        self.gridLayout_5.addWidget(self.cboxLogTime, 9, 0, 1, 1)
        self.ckDebug = QtWidgets.QCheckBox(self.tab)
        self.ckDebug.setObjectName("ckDebug")
        self.gridLayout_5.addWidget(self.ckDebug, 8, 0, 1, 1)
        self.ckHexSend = QtWidgets.QCheckBox(self.tab)
        self.ckHexSend.setObjectName("ckHexSend")
        self.gridLayout_5.addWidget(self.ckHexSend, 7, 0, 1, 1)
        self.cboxParity = QtWidgets.QComboBox(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cboxParity.sizePolicy().hasHeightForWidth())
        self.cboxParity.setSizePolicy(sizePolicy)
        self.cboxParity.setObjectName("cboxParity")
        self.gridLayout_5.addWidget(self.cboxParity, 3, 2, 1, 1)
        self.btnScan = QtWidgets.QPushButton(self.tab)
        self.btnScan.setObjectName("btnScan")
        self.gridLayout_5.addWidget(self.btnScan, 15, 0, 1, 1)
        self.cboxDataBit = QtWidgets.QComboBox(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cboxDataBit.sizePolicy().hasHeightForWidth())
        self.cboxDataBit.setSizePolicy(sizePolicy)
        self.cboxDataBit.setObjectName("cboxDataBit")
        self.gridLayout_5.addWidget(self.cboxDataBit, 2, 2, 1, 1)
        self.labBaudRate = QtWidgets.QLabel(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labBaudRate.sizePolicy().hasHeightForWidth())
        self.labBaudRate.setSizePolicy(sizePolicy)
        self.labBaudRate.setMaximumSize(QtCore.QSize(50, 16777215))
        self.labBaudRate.setObjectName("labBaudRate")
        self.gridLayout_5.addWidget(self.labBaudRate, 1, 0, 1, 1)
        self.cboxWrap = QtWidgets.QCheckBox(self.tab)
        self.cboxWrap.setObjectName("cboxWrap")
        self.gridLayout_5.addWidget(self.cboxWrap, 9, 2, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_2.setContentsMargins(6, 6, 6, 6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.labServerIP = QtWidgets.QLabel(self.tab_2)
        self.labServerIP.setObjectName("labServerIP")
        self.gridLayout_2.addWidget(self.labServerIP, 3, 0, 1, 1)
        self.scan = QtWidgets.QPushButton(self.tab_2)
        self.scan.setObjectName("scan")
        self.gridLayout_2.addWidget(self.scan, 9, 0, 1, 2)
        self.labSleepTime = QtWidgets.QLabel(self.tab_2)
        self.labSleepTime.setObjectName("labSleepTime")
        self.gridLayout_2.addWidget(self.labSleepTime, 6, 0, 1, 1)
        self.txtListenPort = QtWidgets.QLineEdit(self.tab_2)
        self.txtListenPort.setObjectName("txtListenPort")
        self.gridLayout_2.addWidget(self.txtListenPort, 5, 1, 1, 1)
        self.labServerPort = QtWidgets.QLabel(self.tab_2)
        self.labServerPort.setObjectName("labServerPort")
        self.gridLayout_2.addWidget(self.labServerPort, 4, 0, 1, 1)
        self.txtServerPort = QtWidgets.QLineEdit(self.tab_2)
        self.txtServerPort.setText("")
        self.txtServerPort.setObjectName("txtServerPort")
        self.gridLayout_2.addWidget(self.txtServerPort, 4, 1, 1, 1)
        self.txtServerIP = QtWidgets.QLineEdit(self.tab_2)
        self.txtServerIP.setText("")
        self.txtServerIP.setObjectName("txtServerIP")
        self.gridLayout_2.addWidget(self.txtServerIP, 3, 1, 1, 1)
        self.labListenPort = QtWidgets.QLabel(self.tab_2)
        self.labListenPort.setObjectName("labListenPort")
        self.gridLayout_2.addWidget(self.labListenPort, 5, 0, 1, 1)
        self.ckAutoConnect = QtWidgets.QCheckBox(self.tab_2)
        self.ckAutoConnect.setObjectName("ckAutoConnect")
        self.gridLayout_2.addWidget(self.ckAutoConnect, 10, 1, 1, 1)
        self.cboxSleepTime = QtWidgets.QComboBox(self.tab_2)
        self.cboxSleepTime.setObjectName("cboxSleepTime")
        self.gridLayout_2.addWidget(self.cboxSleepTime, 6, 1, 1, 1)
        self.labMode = QtWidgets.QLabel(self.tab_2)
        self.labMode.setObjectName("labMode")
        self.gridLayout_2.addWidget(self.labMode, 2, 0, 1, 1)
        self.cboxMode = QtWidgets.QComboBox(self.tab_2)
        self.cboxMode.setObjectName("cboxMode")
        self.cboxMode.addItem("")
        self.cboxMode.addItem("")
        self.cboxMode.addItem("")
        self.cboxMode.addItem("")
        self.gridLayout_2.addWidget(self.cboxMode, 2, 1, 1, 1)
        self.lineEditLocal = QtWidgets.QLineEdit(self.tab_2)
        self.lineEditLocal.setReadOnly(True)
        self.lineEditLocal.setObjectName("lineEditLocal")
        self.gridLayout_2.addWidget(self.lineEditLocal, 7, 0, 1, 2)
        self.btnStart = QtWidgets.QPushButton(self.tab_2)
        self.btnStart.setObjectName("btnStart")
        self.gridLayout_2.addWidget(self.btnStart, 10, 0, 1, 1)
        self.lineEditRemote = QtWidgets.QLineEdit(self.tab_2)
        self.lineEditRemote.setReadOnly(True)
        self.lineEditRemote.setObjectName("lineEditRemote")
        self.gridLayout_2.addWidget(self.lineEditRemote, 8, 0, 1, 2)
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.horizontalLayout.addWidget(self.widgetRight)
        self.horizontalLayout.setStretch(0, 6)
        self.horizontalLayout.setStretch(1, 2)
        self.gridLayout_3.addWidget(self.widgeMain, 0, 0, 1, 1)

        self.retranslateUi(frmComTool)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(frmComTool)

    def retranslateUi(self, frmComTool):
        _translate = QtCore.QCoreApplication.translate
        self.ckAutoSend.setText(_translate("frmComTool", "自动发送"))
        self.btnSend.setText(_translate("frmComTool", "发送"))
        self.ckAutoSave.setText(_translate("frmComTool", "自动保存"))
        self.btnSave.setText(_translate("frmComTool", "保存数据"))
        self.btnStopShow.setText(_translate("frmComTool", "停止显示"))
        self.btnData.setText(_translate("frmComTool", "管理数据"))
        self.btnClear.setText(_translate("frmComTool", "清空数据"))
        self.btnOpen.setText(_translate("frmComTool", "打开串口"))
        self.labParity.setText(_translate("frmComTool", "校验位"))
        self.ckAutoClear.setText(_translate("frmComTool", "自动清空"))
        self.labDataBit.setText(_translate("frmComTool", "数据位"))
        self.btnReceiveCount.setText(_translate("frmComTool", "接收 : 0 字节"))
        self.ckHexReceive.setText(_translate("frmComTool", "Hex接收"))
        self.labPortName.setText(_translate("frmComTool", "串口号"))
        self.labStopBit.setText(_translate("frmComTool", "停止位"))
        self.btnSendCount.setText(_translate("frmComTool", "发送 : 0 字节"))
        self.cboxLogTime.setText(_translate("frmComTool", "添加时间"))
        self.ckDebug.setText(_translate("frmComTool", "模拟设备"))
        self.ckHexSend.setText(_translate("frmComTool", "Hex发送"))
        self.btnScan.setText(_translate("frmComTool", "扫描串口"))
        self.labBaudRate.setText(_translate("frmComTool", "波特率"))
        self.cboxWrap.setText(_translate("frmComTool", "自动换行"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("frmComTool", "串口"))
        self.labServerIP.setText(_translate("frmComTool", "远程地址"))
        self.scan.setText(_translate("frmComTool", "扫描UDP服务端"))
        self.labSleepTime.setText(_translate("frmComTool", "延时时间"))
        self.labServerPort.setText(_translate("frmComTool", "远程端口"))
        self.labListenPort.setText(_translate("frmComTool", "监听端口"))
        self.ckAutoConnect.setText(_translate("frmComTool", "自动重连"))
        self.labMode.setText(_translate("frmComTool", "转换模式"))
        self.cboxMode.setItemText(0, _translate("frmComTool", "Tcp_Client"))
        self.cboxMode.setItemText(1, _translate("frmComTool", "Tcp_Server"))
        self.cboxMode.setItemText(2, _translate("frmComTool", "Udp_Client"))
        self.cboxMode.setItemText(3, _translate("frmComTool", "Udp_Server"))
        self.btnStart.setText(_translate("frmComTool", "启动"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("frmComTool", "网络"))
