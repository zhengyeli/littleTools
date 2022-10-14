import re
import typing
from datetime import time
from distutils.util import strtobool

from PyQt6 import QtSerialPort, QtWidgets
from PyQt6.QtCore import QSettings, QTimer, QIODevice, pyqtSignal, Qt, QByteArray, QDateTime, QFile, QTextStream, \
    QEvent, QObject
from PyQt6.QtGui import QTextCursor, QColor, QFont, QKeyEvent
from PyQt6.QtNetwork import QTcpSocket, QUdpSocket, QHostAddress, QNetworkInterface, QAbstractSocket, QTcpServer, \
    QNetworkDatagram
from PyQt6.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox, QCheckBox, QFileDialog
from PySide6.QtWidgets import QAbstractSlider

from module.SerialPort.AppConfig import AppConfig
from module.SerialPort.Ui_frmComTool import Ui_frmComTool
from module.test import test_wave
from module.utils import utils

rxBufSize = 512

hotkey = [
    "govee",
    "dev_info",
    "ifconfig",
    "reboot",
    "log print 0",
    "log print 1",
    "log print 2",
    "log print 3",
    "log print 4",
    "log enable mcu",
    "log disable mcu",
    "log enable ble",
    "log disable ble",
    "log enable scan",
    "log disable scan",
]

test_wave_enable = True


class FrmComTool(QObject, Ui_frmComTool):
    btn_list = None
    # 信号 . 发送到外面控件
    emit_open_com_successful = pyqtSignal()

    def __init__(self, ui, handle):
        super().__init__()
        self.mainPtr = handle
        self.plot = self.mainPtr.plot
        if test_wave_enable:
            self.test = test_wave(self.plot)

        self.udpEventTuple = None
        self.m_udpSocketlist = None
        self.isinputText = True
        self.currentCount = None
        self.ui = Ui_frmComTool()  # 方便知道ui里的成员
        self.ui = ui
        self.com = QSerialPort()
        self.comOk = False
        self.receiveCount = 0
        self.sendCount = 0
        self.isShow = True

        self.timerSend = QTimer()
        self.timerSave = QTimer()
        self.timerConnect = QTimer()

        self.udpOk = False
        self.udpsocket = QUdpSocket()
        self.udplocalsocket = QUdpSocket()
        self.tcpOk = False
        self.tcpsocket = QTcpSocket()
        self.tcpServer = QTcpServer()
        self.tcpClientList = []

        self.AppConfig = AppConfig()
        self.AppConfig.readConfig()
        self.comTool_config_init()

        self.ui.txtMain.installEventFilter(self)
        self.comTool_form_and_signal_init()
        self.networkTool_module_init()

    def eventFilter(self, obj, event):
        if obj == self.ui.txtMain:  # 判断是不是我的事件
            if event.type() == QEvent.Type.MouseButtonPress:  # 如果label触发了鼠标点击的事件
                return True  # 表示停止处理该事件，此时目标对象和后面安装的事件过滤器就无法获得该事件
            elif event.type() == QEvent.Type.KeyPress:
                keyEvent = event
                self.ui.txtMain.verticalScrollBar().setSliderPosition(self.ui.txtMain.verticalScrollBar().maximum())

                cursor = self.ui.txtMain.textCursor()
                cursor.movePosition(QTextCursor.MoveOperation.End)
                self.ui.txtMain.setTextCursor(cursor)

                if self.comOk:
                    if keyEvent.key() == 16777217:  # tab
                        pass
                        # self.comTool_sendData(keyEvent.text())
                    else:
                        self.comTool_sendData(keyEvent.text())

                if self.udpOk:
                    pass
                    data = keyEvent.text()
                    bytes_data = bytes(data, "utf-8")
                    if self.ui.cboxMode.currentText() == "Udp_Server":
                        if self.udpEventTuple is None:
                            print("self.udpEventTuple is None")
                            return
                        senderIp = self.udpEventTuple.senderAddress()
                        senderPor = self.udpEventTuple.senderPort()
                        count = self.udpsocket.writeDatagram(bytes_data, senderIp, senderPor)
                    else:
                        count = self.udpsocket.writeDatagram(bytes_data, QHostAddress(self.AppConfig.ServerIP), int(self.AppConfig.ServerPort))

                    if count > 0:
                        self.ui.txtMain.insertPlainText(data)

                if self.tcpOk:
                    data = keyEvent.text()
                    self.ui.lineEditLocal.setText("local:" + self.tcpsocket.localAddress().toString() + ":" + str(self.tcpsocket.localPort()))
                    count = self.tcpsocket.write(bytes(data, "utf-8"))
                    if count > 0:
                        self.ui.txtMain.insertPlainText(data)
            return True  # 表示停止处理该事件，此时目标对象和后面安装的事件过滤器就无法获得该事件
        else:
            return super().eventFilter(obj, event)  # 返回默认的事件过滤器

    def comTool_form_and_signal_init(self):

        self.ComOpen_changeEnable(True)
        self.ui.txtMain.setFontWeight(QFont.Weight.Bold)

        # 连接按键
        self.hotkey_button_init()

        self.ui.btnStopShow.clicked.connect(self.comTool_btnStopShow_clicked)
        self.ui.btnSave.clicked.connect(self.comTool_saveData)
        self.ui.btnReceiveCount.clicked.connect(self.comTool_btnReceiveCount_clicked)
        self.ui.btnSendCount.clicked.connect(self.comTool_btnSendCount_clicked)
        self.ui.btnData.clicked.connect(self.comTool_btnData_clicked)
        self.ui.btnClear.clicked.connect(self.comTool_btnClear_clicked)
        self.ui.txtMain.setLineWrapMode(QtWidgets.QTextEdit.LineWrapMode.WidgetWidth)
        self.ui.btnScan.clicked.connect(self.comTool_AvailableCom_Scan)
        self.ui.btnSend.clicked.connect(self.comTool_btnSendData)
        self.ui.btnOpen.clicked.connect(self.ComOpen_Button_Clicked)
        self.com.readyRead.connect(self.comTool_Data_readFromCom)

        # self.ui.txtMain.installEventFilter(self.ui.txtMain)

    def comTool_config_init(self):
        comList = []
        info = QSerialPortInfo.availablePorts()
        for i in info:
            comList.append(i.portName())
        self.ui.cboxPortName.addItems(comList)
        self.ui.cboxPortName.setCurrentIndex(self.ui.cboxPortName.findText(self.AppConfig.PortName))
        self.ui.cboxPortName.currentIndexChanged.connect(self.comTool_config_save)

        baudList = ["50", "75", "100", "134", "150", "200", "300", "600", "1200", "1800", "2400", "4800", "9600",
                    "14400", "19200", "38400", "56000", "57600", "76800", "115200", "128000", "256000"]
        self.ui.cboxBaudRate.addItems(baudList)
        self.ui.cboxBaudRate.setCurrentIndex(self.ui.cboxBaudRate.findText(self.AppConfig.BaudRate))
        self.ui.cboxBaudRate.currentIndexChanged.connect(self.comTool_config_save)

        dataBitsList = ["5", "6", "7", "8"]
        self.ui.cboxDataBit.addItems(dataBitsList)
        self.ui.cboxDataBit.setCurrentIndex(self.ui.cboxDataBit.findText(self.AppConfig.DataBit))
        self.ui.cboxDataBit.currentIndexChanged.connect(self.comTool_config_save)

        parityList = ["无", "奇", "偶"]
        self.ui.cboxParity.addItems(parityList)
        self.ui.cboxParity.setCurrentIndex(self.ui.cboxParity.findText(self.AppConfig.Parity))
        self.ui.cboxParity.currentIndexChanged.connect(self.comTool_config_save)

        stopBitsList = ["1", "1.5", "2"]
        self.ui.cboxStopBit.addItems(stopBitsList)
        self.ui.cboxStopBit.setCurrentIndex(self.ui.cboxStopBit.findText(self.AppConfig.StopBit))
        self.ui.cboxStopBit.currentIndexChanged.connect(self.comTool_config_save)

        self.ui.ckHexSend.setChecked(self.AppConfig.HexSend)
        self.ui.ckHexSend.clicked.connect(self.comTool_config_save)

        self.ui.ckHexReceive.setChecked(self.AppConfig.HexReceive)
        self.ui.ckHexReceive.clicked.connect(self.comTool_config_save)

        self.ui.ckDebug.setChecked(self.AppConfig.Debug)
        self.ui.ckDebug.clicked.connect(self.comTool_config_save)

        self.ui.ckAutoClear.setChecked(self.AppConfig.AutoClear)
        self.ui.ckAutoClear.clicked.connect(self.comTool_config_save)

        self.ui.ckAutoSend.setChecked(self.AppConfig.AutoSend)
        self.ui.ckAutoSend.clicked.connect(self.comTool_config_save)

        self.ui.ckAutoSave.setChecked(self.AppConfig.AutoSave)
        self.ui.ckAutoSave.clicked.connect(self.comTool_config_save)

        sendInterval = ["100", "300", "500"]
        saveInterval = []

        for i in range(1000, 10000, 1000):
            sendInterval.append(str(i))
            saveInterval.append(str(i))

        self.ui.cboxSendInterval.addItems(sendInterval)
        self.ui.cboxSaveInterval.addItems(saveInterval)

        self.ui.cboxSendInterval.setCurrentIndex(self.ui.cboxSendInterval.findText(self.AppConfig.SendInterval))
        self.ui.cboxSendInterval.currentIndexChanged.connect(self.comTool_config_save)

        self.ui.cboxSaveInterval.setCurrentIndex(self.ui.cboxSaveInterval.findText(self.AppConfig.SaveInterval))
        self.ui.cboxSaveInterval.currentIndexChanged.connect(self.comTool_config_save)

        self.timerSend.setInterval(int(self.AppConfig.SendInterval))
        self.timerSave.setInterval(int(self.AppConfig.SaveInterval))

        if self.AppConfig.AutoSend:
            self.timerSend.start()

        if self.AppConfig.AutoSave:
            self.timerSave.start()

        # 串口转网络部分
        self.ui.cboxMode.setCurrentIndex(self.ui.cboxMode.findText(self.AppConfig.Mode))
        self.ui.cboxMode.currentIndexChanged.connect(self.comTool_config_save)

        self.ui.txtServerIP.setText(self.AppConfig.ServerIP)
        self.ui.txtServerIP.textChanged.connect(self.comTool_config_save)

        self.ui.txtServerPort.setText(self.AppConfig.ServerPort)
        self.ui.txtServerPort.textChanged.connect(self.comTool_config_save)

        self.ui.txtListenPort.setText(self.AppConfig.ListenPort)
        self.ui.txtListenPort.textChanged.connect(self.comTool_config_save)

        values = ["0", "10", "50"]

        for i in range(100, 1001, 100):
            values.append(str(i))

        self.ui.cboxSleepTime.addItems(values)

        self.ui.cboxSleepTime.setCurrentIndex(self.ui.cboxSleepTime.findText(self.AppConfig.SleepTime))
        self.ui.cboxSleepTime.currentIndexChanged.connect(self.comTool_config_save)

        self.ui.ckAutoConnect.setChecked(self.AppConfig.AutoConnect)
        self.ui.ckAutoConnect.clicked.connect(self.comTool_config_save)

        # 添加显示参数
        Intervals = ["1", "10", "20", "50", "100", "200", "300", "500", "1000", "1500", "2000", "3000", "5000", "10000"]
        Datas = ["AA BB CC"]
        self.ui.cboxSendInterval.addItems(Intervals)
        self.ui.cboxData.addItems(Datas)

        self.timerSend.setInterval(100)
        self.timerSend.timeout.connect(self.comTool_btnSendData)

        self.timerSave.setInterval(100)
        self.timerSave.timeout.connect(self.comTool_saveData)

    def comTool_btnStopShow_clicked(self):
        if self.ui.btnStopShow.text() == "停止显示":
            self.isShow = False
            self.ui.btnStopShow.setText("开始显示")
        else:
            self.isShow = True
            self.ui.btnStopShow.setText("停止显示")

    def comTool_btnSendCount_clicked(self):
        self.ui.btnSendCount.setText("发送 : 0 字节")

    def comTool_btnReceiveCount_clicked(self):
        self.ui.btnReceiveCount.setText("接受 : 0 字节")

    def comTool_btnData_clicked(self):
        qwidget = QWidget()
        dir = QFileDialog.getOpenFileName(qwidget, "select file", "", None)
        # fileName = "{0}/{1}".format("./", "send.txt")
        file = QFile(dir[0])

        if file.exists() is False:
            return

        if self.ui.btnData.text() == "管理数据":
            self.ui.txtMain.setReadOnly(False)
            self.ui.txtMain.clear()
            file.open(QFile.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text)
            inputStream = QTextStream(file)
            self.ui.txtMain.setText(inputStream.readAll())
            file.close()
            self.ui.btnData.setText("保存数据")
        else:
            self.ui.txtMain.setReadOnly(True)
            file.open(QFile.OpenModeFlag.WriteOnly | QIODevice.OpenModeFlag.Text)
            out = QTextStream(file)
            out << self.ui.txtMain.toPlainText()
            file.close()
            self.ui.btnData.setText("管理数据")
            # AppData.readSendData()

    def comTool_btnClear_clicked(self):
        self.ui.txtMain.clear()
        self.ui.txtMain.insertPlainText("#")

    def comTool_btnSendData(self):
        string = self.ui.cboxData.currentText()
        if len(string) == 0:
            self.ui.cboxData.setFocus()
            return

        self.comTool_sendData(string)

        if self.ui.ckAutoClear.isChecked():
            self.ui.cboxData.setCurrentIndex(-1)
            self.ui.cboxData.setFocus()

    def comTool_sendData(self, string):
        if self.comOk == False or self.com.isOpen() is False:
            return

        # 短信猫调试
        if "AT" in string:
            string += "\n"

        # convert string to byte
        res = bytes(string, 'utf-8')

        if self.ui.ckHexSend.isChecked():
            buffer = res
        else:
            buffer = res

        self.com.write(res)

        # append(0, buffer)
        self.sendCount = self.sendCount + len(buffer)
        self.ui.btnSendCount.setText("发送 : {} 字节".format(self.sendCount))

    def comTool_saveData(self):
        tempData = self.ui.txtMain.toPlainText()
        if len(tempData) == 0:
            return

        now = QDateTime.currentDateTime()
        name = now.toString("yyyy-MM-dd-HH-mm-ss")

        if self.ui.cboxPortName.currentText() is None:
            fileName = "{0}/{1} {2}.txt".format("./", "comX", name)
        else:
            fileName = "{0}{1} {2}.txt".format("./", self.ui.cboxPortName.currentText(), name)

        file = QFile(fileName)
        file.open(QFile.OpenModeFlag.ReadWrite | QIODevice.OpenModeFlag.ReadWrite)
        out = QTextStream(file)
        out << tempData
        file.close()
        # on_btnClear_clicked()

    def comTool_config_save(self):
        self.AppConfig.PortName = self.ui.cboxPortName.currentText()
        self.AppConfig.BaudRate = self.ui.cboxBaudRate.currentText()
        self.AppConfig.DataBit = self.ui.cboxDataBit.currentText()
        self.AppConfig.Parity = self.ui.cboxParity.currentText()
        self.AppConfig.StopBit = self.ui.cboxStopBit.currentText()

        self.AppConfig.HexSend = self.ui.ckHexSend.isChecked()
        self.AppConfig.HexReceive = self.ui.ckHexReceive.isChecked()
        self.AppConfig.Debug = self.ui.ckDebug.isChecked()
        self.AppConfig.AutoClear = self.ui.ckAutoClear.isChecked()

        self.AppConfig.AutoSend = self.ui.ckAutoSend.isChecked()
        self.AppConfig.AutoSave = self.ui.ckAutoSave.isChecked()

        sendInterval = self.ui.cboxSendInterval.currentText()
        if sendInterval != self.AppConfig.SendInterval:
            self.AppConfig.SendInterval = sendInterval
            self.timerSend.setInterval(int(self.AppConfig.SendInterval))

        saveInterval = self.ui.cboxSaveInterval.currentText()
        if saveInterval != self.AppConfig.SaveInterval:
            self.AppConfig.SaveInterval = saveInterval
            self.timerSave.setInterval(int(self.AppConfig.SaveInterval))

        self.AppConfig.Mode = self.ui.cboxMode.currentText()
        self.AppConfig.ServerIP = self.ui.txtServerIP.text()
        self.AppConfig.ServerPort = self.ui.txtServerPort.text()
        self.AppConfig.ListenPort = self.ui.txtListenPort.text()
        self.AppConfig.SleepTime = self.ui.cboxSleepTime.currentText()
        self.AppConfig.AutoConnect = self.ui.ckAutoConnect.isChecked()

        self.AppConfig.writeConfig()

    def comTool_AvailableCom_Scan(self):
        comList = []
        info = QSerialPortInfo.availablePorts()
        for i in info:
            comList.append(i.portName())

        if len(comList) == 0:
            return
        self.ui.cboxPortName.addItems(comList)

    def comTool_Data_readFromCom(self):
        # self.com = QSerialPort()
        if self.com.bytesAvailable() == 0:
            return
        # data = QByteArray()
        QBA_data = self.com.readAll()

        if self.AppConfig.HexReceive:
            Str_data = utils.bytes2hex(bytes(QBA_data))
        else:
            try:
                Str_data = str(QBA_data, encoding='utf-8')
            except:
                self.ui.txtMain.append("转字符串失败")

        if len(Str_data) == 0:
            return

        if test_wave_enable:
            if self.AppConfig.HexReceive:
                pass
            else:
                self.test.serial_data_handle(Str_data)


        if "\b \b" in Str_data:  # backspace
            # 获取当前文本光标
            cursor = self.ui.txtMain.textCursor()
            # 将光标移动到文本结尾
            cursor.movePosition(QTextCursor.MoveOperation.PreviousCharacter)
            # 判断当前是否选中了文本，如果选中了文本则取消选中的文本，再删除前一个字符
            if cursor.hasSelection():
                cursor.clearSelection()
            # 删除前一个字符
            while Str_data.indexOf("\b \b") != -1:
                # cursor.movePosition(QTextCursor.End)
                cursor.deletePreviousChar()
                self.ui.txtMain.setTextCursor(cursor)
                Str_data.remove(Str_data.indexOf("\b \b"), Str_data.indexOf("\b \b") + 3)
                self.ui.txtMain.verticalScrollBar().triggerAction(QAbstractSlider.SliderToMaximum)
                data = Str_data.replace("\b \b", "")

        if self.isShow:
            if self.ui.ckHexReceive.isChecked():
                buffer = Str_data
            else:
                buffer = Str_data
        else:
            return
        # buffer = QString.fromLocal8Bit(data)

        # 启用调试则模拟调试数据
        if self.ui.ckDebug.isChecked():
            '''count = AppData.Keys.count()
            for i in range(0, count):
                if (buffer.startsWith(AppData.Keys.at(i))):
                    sendData(AppData.Values.at(i))
                    break'''
        self.comTool_Show_Append(1, buffer)
        self.receiveCount = self.receiveCount + len(Str_data)
        self.ui.btnReceiveCount.setText("接收 : {} 字节".format(self.receiveCount))

        # 启用网络转发则调用网络发送数据
        self.networkTool_SendStringToNetwork(Str_data)

    # data是字符串类型
    def comTool_Show_Append(self, msg_from, data):
        if len(data) > 0:
            if data.find("\n") > 0:
                pass
            else:
                if msg_from != 1:  # 串口来源
                    data += "\n"

        self.currentCount = 0
        maxCount = 1000

        if self.currentCount >= maxCount:
            self.comTool_saveData()
            self.ui.txtMain.clear()
            self.currentCount = 0

        if self.isShow is False:
            return

        # 过滤回车换行符
        strData = data

        strData = strData.replace('\r', '')
        strData = strData.replace("\n", "<br />")  # html's \r
        # 不同类型不同颜色显示
        if msg_from == 0:
            strType = "串口发送"
        elif msg_from == 1:
            strType = "串口接收"
            # strData = strData.replace("\n", "<br />")  # html's \r
        elif msg_from == 2:
            strType = "处理延时"
        elif msg_from == 3:
            strType = "正在校验"
        elif msg_from == 4:
            strType = "网络发送"
        elif msg_from == 5:
            strType = "网络接收"
            # strData = strData.replace("\r", "")
        elif msg_from == 6:
            strType = "提示信息"

        # strData = "时间[{0}] [{1}] {2} <br />".format(time, strType, strData)

        # 文本替换
        strData = strData.replace("ERR", "<font color=red>ERR</font>")
        strData = strData.replace("WARN", "<font color=yellow>WARN</font>")
        strData = strData.replace("INF", "<font color=yellow>INF</font>")
        strData = strData.replace("success", "<font color=green>success</font>")

        # 进度条在尾部，实时显示打印
        if self.ui.txtMain.verticalScrollBar().value() == self.ui.txtMain.verticalScrollBar().maximum():
            self.isinputText = True
        else:
            self.isinputText = False

        # 记录滑条的位置
        curBarPosition = self.ui.txtMain.verticalScrollBar().value()
        # 光标的处理
        cursor = self.ui.txtMain.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.deletePreviousChar()
        self.ui.txtMain.setTextCursor(cursor)

        # insertHtml 支持html格式颜色文字
        self.ui.txtMain.insertHtml(strData)
        self.ui.txtMain.insertPlainText("#")

        if self.isinputText:
            self.ui.txtMain.verticalScrollBar().setSliderPosition(self.ui.txtMain.verticalScrollBar().maximum())
            self.ui.txtMain.update()
        else:
            self.ui.txtMain.verticalScrollBar().setSliderPosition(curBarPosition)

        self.currentCount += 1

    def hotkey_button_init(self):
        # init hot key
        w = QWidget(self.ui.tabWidget)
        self.ui.tabWidget.addTab(w, "hotkey")
        verticalLayout = QVBoxLayout(w)
        for i in hotkey:
            btn = QPushButton(w)
            btn.setText(i)
            btn.clicked.connect(lambda: self.Hotkey_Button_Clicked())
            verticalLayout.addWidget(btn)
        w.setLayout(verticalLayout)

    def ComOpen_Button_Clicked(self):
        if self.ui.btnOpen.text() == "打开串口":

            self.com.setPortName(self.AppConfig.PortName)
            self.com.setReadBufferSize(65535)

            dataBit = int(self.AppConfig.DataBit)
            if dataBit == 5:
                self.com.setDataBits(QSerialPort.DataBits.Data5)
            elif dataBit == 6:
                self.com.setDataBits(QSerialPort.DataBits.Data6)
            elif dataBit == 7:
                self.com.setDataBits(QSerialPort.DataBits.Data7)
            elif dataBit == 8:
                self.com.setDataBits(QSerialPort.DataBits.Data8)
            else:
                self.com.setDataBits(QSerialPort.DataBits.Data8)

            self.com.setBaudRate(int(self.AppConfig.BaudRate))

            Parity = self.AppConfig.Parity
            if Parity == "无":
                self.com.setParity(QSerialPort.Parity.NoParity)
            elif Parity == "奇":
                self.com.setParity(QSerialPort.Parity.OddParity)
            elif Parity == "偶":
                self.com.setParity(QSerialPort.Parity.EvenParity)
            else:
                self.com.setParity(QSerialPort.Parity.NoParity)

            StopBit = int(self.AppConfig.StopBit)
            if StopBit == 1:
                self.com.setStopBits(QSerialPort.StopBits.OneStop)
            elif StopBit == 1.5:
                self.com.setStopBits(QSerialPort.StopBits.OneAndHalfStop)
            elif StopBit == 2:
                self.com.setStopBits(QSerialPort.StopBits.TwoStop)
            else:
                self.com.setStopBits(QSerialPort.StopBits.OneStop)

            self.com.setFlowControl(QSerialPort.FlowControl.NoFlowControl)
            self.comOk = self.com.open(QIODevice.OpenModeFlag.ReadWrite)

            if self.comOk:
                # 改变tab名字信号
                self.emit_open_com_successful.emit()
                # 清空缓冲区
                self.com.flush()
                self.ComOpen_changeEnable(False)
                self.ui.btnOpen.setText("关闭串口")

        else:
            self.com.close()
            # self.com.deleteLater()

            self.ComOpen_changeEnable(True)
            self.ui.btnOpen.setText("打开串口")
            # on_btnClear_clicked()
            self.comOk = False

    def ComOpen_changeEnable(self, b):
        self.ui.cboxBaudRate.setEnabled(b)
        self.ui.cboxDataBit.setEnabled(b)
        self.ui.cboxParity.setEnabled(b)
        self.ui.cboxPortName.setEnabled(b)
        self.ui.cboxStopBit.setEnabled(b)
        self.ui.btnSend.setEnabled(bool(1-b))
        self.ui.ckAutoSend.setEnabled(bool(1-b))
        self.ui.ckAutoSave.setEnabled(bool(1-b))

    def networkTool_module_init(self):
        self.networkTool_form_enable(True)

        self.tcpOk = False
        self.tcpsocket.abort()
        self.tcpsocket.readyRead.connect(self.networkTool_TcpData_Read)
        self.tcpsocket.connected.connect(lambda: print("connected"))
        self.tcpsocket.disconnected.connect(lambda: print("disconnected"))
        self.tcpsocket.errorOccurred.connect(self.networkTool_NetworkData_ReadError)

        self.tcpServer.newConnection.connect(self.networkTool_TcpServer_clintCnt)

        self.udpOk = False
        self.udpsocket.abort()
        self.udpsocket.readyRead.connect(self.networkTool_UdpData_Read)
        self.udpsocket.errorOccurred.connect(self.networkTool_NetworkData_ReadError)

        self.timerConnect.timeout.connect(self.networkTool_Client_AutoConnect)
        self.ui.btnStart.clicked.connect(self.networkTool_btn_network_start)

    def networkTool_TcpServer_clintCnt(self):
        self.tcpOk = True
        self.tcpsocket.close()
        self.tcpsocket = self.tcpServer.nextPendingConnection()
        self.tcpsocket.readyRead.connect(self.networkTool_TcpData_Read)

    def networkTool_SendStringToNetwork(self, string):
        bytes_data = bytes(string, "utf-8")
        if self.tcpOk:
            self.tcpsocket.write(bytes_data)

        # 启用网络转发则调用网络发送数据
        if self.udpOk:
            self.udpsocket.writeDatagram(bytes_data, QHostAddress(self.AppConfig.ServerIP),\
                                         int(self.AppConfig.ServerPort))
        self.comTool_Show_Append(4, string)

    def networkTool_form_enable(self, b):
        self.ui.cboxMode.setEnabled(b)
        self.ui.txtServerIP.setEnabled(b)
        self.ui.txtServerPort.setEnabled(b)
        self.ui.txtListenPort.setEnabled(b)

    def networkTool_btn_network_start(self):
        mode = self.ui.cboxMode.currentText()
        if self.ui.btnStart.text() == "启动":
            if self.AppConfig.ServerIP == "" or self.AppConfig.ServerPort == "0":
                self.comTool_Show_Append(6, "IP地址和远程端口不能为空")
                return

            if mode == "Tcp_Client":
                self.tcpsocket.connectToHost(self.AppConfig.ServerIP, int(self.AppConfig.ServerPort))
                if self.tcpsocket.waitForConnected(1000):
                    self.ui.btnStart.setText("停止")
                    self.comTool_Show_Append(6, "连接tcp服务器成功")
                    self.tcpOk = True
                else:
                    self.tcpOk = False
                    self.comTool_Show_Append(6, "连接tcp服务器fail")
            elif mode == "Tcp_Server":
                ok = self.tcpServer.listen(QHostAddress(self.AppConfig.ServerIP), int(self.AppConfig.ListenPort))
                if ok:
                    self.ui.btnStart.setText("停止")
                    self.comTool_Show_Append(6, "bind成功")
                else:
                    self.tcpOk = False
                    self.comTool_Show_Append(6, "连接tcp服务器fail")
            elif mode == "Udp_Client":
                data = "govee"
                if self.udpsocket.writeDatagram(bytes(data, 'utf-8'), QHostAddress(self.AppConfig.ServerIP), int(self.AppConfig.ServerPort)) > 0:
                    self.comTool_Show_Append(6, "连接udp服务器成功")
                    self.ui.btnStart.setText("停止")
                    self.udpOk = True
                    self.udplocalsocket.bind(self.udpsocket.localAddress(), int(self.AppConfig.ListenPort), QUdpSocket.BindFlag.DefaultForPlatform)
                    self.udplocalsocket.readyRead.connect(self.networkTool_AllLocalIp_UdpData_Read)
                    self.udplocalsocket.errorOccurred.connect(self.networkTool_NetworkData_ReadError)
                else:
                    self.udpOk = False
                    self.comTool_Show_Append(6, "连接 失败")
            elif mode == "Udp_Server":
                if self.udpsocket.bind(QHostAddress.SpecialAddress.AnyIPv4, \
                                       int(self.AppConfig.ListenPort), QUdpSocket.BindFlag.DefaultForPlatform):
                    self.ui.btnStart.setText("停止")
                    self.comTool_Show_Append(6, "bind udp 成功")
                    self.udpOk = True
                else:
                    self.udpOk = False
                    self.comTool_Show_Append(6, "bind udp服务器fail")
        else:
            if mode == "Tcp_Client":
                self.tcpsocket.disconnectFromHost()
                if self.tcpsocket.state() == QAbstractSocket.SocketState.UnconnectedState or \
                        self.tcpsocket.waitForDisconnected(100):
                    self.ui.btnStart.setText("启动")
                    self.tcpOk = False
                    self.comTool_Show_Append(6, "断开Tcp服务器成功")
            elif mode == "Tcp_Server":
                self.tcpOk = False
                self.tcpServer.close()
                self.tcpsocket.close()
                self.ui.btnStart.setText("启动")
                self.comTool_Show_Append(6, "断开绑定")
            elif mode == "Udp_Client":
                self.udpOk = False
                self.udpsocket.close()
                self.udplocalsocket.close()
                self.ui.btnStart.setText("启动")
                if self.udpEventTuple is not None:
                    self.udpEventTuple.clear()
                self.udpEventTuple = None
                self.comTool_Show_Append(6, "断开udp服务器成功")
            elif mode == "Udp_Server":
                self.udpOk = False
                self.udpsocket.close()
                self.ui.btnStart.setText("启动")
                self.comTool_Show_Append(6, "断开")

        if self.ui.btnStart.text() == "启动":
            self.networkTool_form_enable(True)
        else:
            self.networkTool_form_enable(False)

    def networkTool_Btn_UdpBroadfast_Scan(self):
        mode = self.ui.cboxMode.currentText()
        if mode == "Udp_Client":
            data = "where are you?"
            if self.m_udpSocketlist.isEmpty():
                self.m_udpSocketlist = QNetworkInterface.allInterfaces()
                for QNetworkInter in self.m_udpSocketlist:
                    for entry in QNetworkInter:
                        broadcastAddress = entry.broadcast()
                        if broadcastAddress != QHostAddress.SpecialAddress.Null and \
                                entry.ip() != QHostAddress.SpecialAddress.LocalHost and \
                                entry.ip().protocol() == QAbstractSocket.NetworkLayerProtocol.IPv4Protocol:
                            sock = QUdpSocket()
                            if sock.bind(entry.ip(), self.AppConfig.ServerPort):
                                print("bind ok" + entry.ip())
                                sock.readyRead.connect(self.networkTool_TcpData_Read())
                                # convert string to byte
                                res = bytes(data, 'utf-8')
                                sock.writeDatagram(res, QHostAddress.SpecialAddress.Broadcast, self.AppConfig.ServerPort)
                                self.m_udpSocketlist.append(sock)
            else:
                for sock in self.m_udpSocketlist:
                    if sock.state() == QAbstractSocket.SocketState.BoundState:
                        sock.writeDatagram(data, QHostAddress.SpecialAddress.Broadcast, self.AppConfig.ServerPort)
        else:
            self.comTool_Show_Append(4, "only work at udp client mode")

    def networkTool_NetworkData_ReadError(self):
        self.ui.btnStart.setText("启动")
        self.networkTool_form_enable(True)
        if self.sender() == self.tcpsocket:
            self.comTool_Show_Append(6, "Tcp,{}".format(self.tcpsocket.errorString()))
            self.tcpsocket.disconnectFromHost()
            self.tcpOk = False
        elif self.sender() == self.udplocalsocket:
            self.comTool_Show_Append(6, "Udp,{}".format(self.udplocalsocket.errorString()))
            self.udplocalsocket.disconnectFromHost()
            self.udpOk = False
        elif self.sender() == self.udpsocket:
            self.comTool_Show_Append(6, "Udp,{}".format(self.udpsocket.errorString()))
            self.udpsocket.disconnectFromHost()
            self.udpOk = False

    def networkTool_TcpData_Read(self):
        if self.tcpsocket.bytesAvailable() > 0:
            if self.ui.cboxMode == "Tcp_Server":
                self.ui.lineEditRemote.setText("remote:" + self.tcpsocket.peerAddress().toString() + ":" + str(self.tcpsocket.peerPort()))
            else:
                self.ui.lineEditRemote.setText("remote:" + self.ui.txtServerIP.text() + ":" + self.ui.txtServerPort.text())
            data = self.tcpsocket.readAll()
            data = str(data, "utf-8")
            if self.ui.ckHexReceive.isChecked():
                buffer = data
            else:
                buffer = data

            self.comTool_Show_Append(5, buffer)

            # 将收到的网络数据转发给串口
            if self.comOk:
                self.comTool_sendData(buffer)
                self.comTool_Show_Append(0, buffer)

    def networkTool_UdpData_Read(self):
        if self.udpsocket.hasPendingDatagrams():
            self.udpEventTuple = self.udpsocket.receiveDatagram(512)
        else:
            return
        udpDataBytes = self.udpEventTuple.data().data()

        destIp = self.udpEventTuple.senderAddress()
        destPort = self.udpEventTuple.senderPort()
        self.ui.lineEditRemote.setText("remote:" + destIp.toString() + ":" + str(destPort))
        senderIp = self.udpEventTuple.destinationAddress()
        senderPort = self.udpEventTuple.destinationPort()
        self.ui.lineEditLocal.setText("local:" + senderIp.toString() + ":" + str(senderPort))

        data = str(udpDataBytes, encoding='utf-8')
        if self.ui.ckHexReceive.isChecked():
            buffer = data
        else:
            buffer = data
        if self.udpOk:
            self.comTool_Show_Append(5, data)

        # 将收到的网络数据转发给串口
        if self.comOk:
            self.com.write(udpDataBytes)
            self.comTool_Show_Append(0, buffer)

        # for sock in self.m_udpSocketlist:
        #     if sock.bytesAvailable() > 0:
        #         addr = QHostAddress()
        #         port = int()
        #         sock.readDatagram(data, rxBufSize, addr, port)
        #         if self.ui.ckHexReceive.isChecked():
        #             buffer = data
        #         else:
        #             buffer = data
        #         if "Server" in data:
        #             self.m_ipServerlist << addr.toString()
        #             self.comTool_Show_Append(5, buffer)

    def networkTool_AllLocalIp_UdpData_Read(self):
        if self.udplocalsocket.hasPendingDatagrams():
            self.udpEventTuple = self.udplocalsocket.receiveDatagram(512)
        else:
            return
        udpDataBytes = self.udpEventTuple.data().data()

        destIp = self.udpEventTuple.senderAddress()
        destPort = self.udpEventTuple.senderPort()
        self.ui.lineEditRemote.setText("remote:" + destIp.toString() + ":" + str(destPort))
        senderIp = self.udpEventTuple.destinationAddress()
        senderPort = self.udpEventTuple.destinationPort()
        self.ui.lineEditLocal.setText("local:" + senderIp.toString() + ":" + str(senderPort))

        data = str(udpDataBytes, encoding='utf-8')
        if self.ui.ckHexReceive.isChecked():
            buffer = data
        else:
            buffer = data
        if self.udpOk:
            self.comTool_Show_Append(5, data)

        # 将收到的网络数据转发给串口
        if self.comOk:
            self.com.write(udpDataBytes)
            self.comTool_Show_Append(0, buffer)

        # for sock in self.m_udpSocketlist:
        #     if sock.bytesAvailable() > 0:
        #         addr = QHostAddress()
        #         port = int()
        #         sock.readDatagram(data, rxBufSize, addr, port)
        #         if self.ui.ckHexReceive.isChecked():
        #             buffer = data
        #         else:
        #             buffer = data
        #         if "Server" in data:
        #             self.m_ipServerlist << addr.toString()
        #             self.comTool_Show_Append(5, buffer)

    def networkTool_Client_AutoConnect(self):
        if self.tcpOk and self.AppConfig.AutoConnect and self.ui.btnStart.text() == "启动":
            if self.AppConfig.ServerIP != "" and self.AppConfig.ServerPort != "0":
                self.tcpsocket.connectToHost(self.AppConfig.ServerIP, int(self.AppConfig.ServerPort))
                if self.tcpsocket.waitForConnected(100):
                    self.ui.btnStart.setText("停止")
                    self.comTool_Show_Append(6, "连接服务器成功")
                    self.tcpOk = True

    def Hotkey_Button_Clicked(self):
        string = self.ui.tabWidget.sender().text()
        print(string)
        print(type(string))
        data = bytes(string + '\n', "utf-8")
        # data.append(0x0d)

        if self.comOk:
            self.com.write(data)

        if self.udpOk:
            if self.ui.cboxMode.currentText() == "Udp_Client":
                print(123)
                if self.udpEventTuple is not None:
                    print(self.udpEventTuple.senderAddress().toString())
                    destIp = self.udpEventTuple.senderAddress()
                    destPort = self.udpEventTuple.senderPort()
                    self.udpsocket.writeDatagram(data, destIp, destPort)

        if self.tcpOk:
            self.tcpsocket.write(data)

    def module_fromMain_init(self, plot):
        self.plot = plot

    def module_serialports_init(self):
        pass
