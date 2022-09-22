from datetime import time
from distutils.util import strtobool

from PyQt6 import QtSerialPort, QtWidgets
from PyQt6.QtCore import QSettings, QTimer, QIODevice, pyqtSignal, Qt, QByteArray, QDateTime, QFile, QTextStream
from PyQt6.QtGui import QTextCursor, QColor, QFont
from PyQt6.QtNetwork import QTcpSocket, QUdpSocket, QHostAddress
from PyQt6.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox, QCheckBox, QFileDialog
from PySide6.QtWidgets import QAbstractSlider

from module.SerialPort.AppConfig import AppConfig
from module.SerialPort.Ui_frmComTool import Ui_frmComTool

rxBufSize = 512
isinputText = True

netMode = ["Tcp_client", "Tcp_Server", "Udp_Client", "Udp_Server"]

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


class FrmComTool(Ui_frmComTool):
    btn_list = None
    # 信号 . 发送到外面控件
    emit_open_com_successful = pyqtSignal()

    def __init__(self, ui):
        self.isinputText = True
        self.currentCount = None
        self.ui = ui
        self.com = QSerialPort()
        self.comOk = False
        self.receiveCount = 0
        self.sendCount = 0
        self.isShow = True

        self.timerSend = None
        self.timerSave = None
        self.timerConnect = None

        self.udpOk = False
        self.udpsocket = None
        self.tcpOk = False
        self.tcpsocket = None

        self.AppConfig = AppConfig()
        self.AppConfig.readConfig()

        self.comTool_form_init()
        self.comTool_config_init()
        # self.module_init()
        # self.ui = Ui_frmComTool

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
            # AppData::readSendData()

    def comTool_btnClear_clicked(self):
        self.ui.txtMain.clear()
        self.ui.txtMain.setFontWeight(QFont.Weight.Bold)
        self.ui.txtMain.insertPlainText("#")
        self.ui.txtMain.setFontWeight(QFont.Weight.Normal)

    def comTool_btnSendData(self):
        str = self.ui.cboxData.currentText()
        if str.isEmpty():
            self.ui.cboxData.setFocus()
            return

        self.comTool_sendData(str)

        if self.ui.ckAutoClear.isChecked():
            self.ui.cboxData.setCurrentIndex(-1)
            self.ui.cboxData.setFocus()

    def comTool_sendData(self, string):
        if self.comOk == False or self.com.isOpen() is False:
            return
        # 短信猫调试
        if string.startsWith("AT"):
            string += "\r"

        if self.ui.ckHexSend.isChecked():
            buffer = string
        else:
            buffer = string

        self.com.write(buffer)
        # append(0, buffer)
        self.sendCount = self.sendCount + buffer.size()
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

    def comTool_form_init(self):
        # 连接按键
        self.button_init()

        self.ui.btnStopShow.clicked.connect(self.comTool_btnStopShow_clicked)
        self.ui.btnSave.clicked.connect(self.comTool_saveData)
        self.ui.btnReceiveCount.clicked.connect(self.comTool_btnReceiveCount_clicked)
        self.ui.btnSendCount.clicked.connect(self.comTool_btnSendCount_clicked)
        self.ui.btnData.clicked.connect(self.comTool_btnData_clicked)
        self.ui.btnClear.clicked.connect(self.comTool_btnClear_clicked)
        self.ui.txtMain.setLineWrapMode(QtWidgets.QTextEdit.LineWrapMode.WidgetWidth)
        self.ui.btnScan.clicked.connect(self.comTool_AvailableCom_Scan)

        # 添加显示参数
        Intervals = ["1", "10", "20", "50", "100", "200", "300", "500", "1000", "1500", "2000", "3000", "5000", "10000"]
        Datas = ["AA BB CC"]
        self.ui.cboxSendInterval.addItems(Intervals)
        self.ui.cboxData.addItems(Datas)

        self.timerSend = QTimer()
        self.timerSend.setInterval(100)
        self.timerSend.timeout.connect(self.comTool_btnSendData)

        self.timerSave = QTimer()
        self.timerSave.setInterval(100)
        self.timerSave.timeout.connect(self.comTool_saveData)

        self.tcpOk = False
        self.tcpsocket = QTcpSocket()
        self.tcpsocket.abort()
        self.tcpsocket.readyRead.connect(self.comTool_Data_readFromCom)

        self.udpOk = False
        self.udpsocket = QUdpSocket()
        self.udpsocket.abort()
        self.udpsocket.readyRead.connect(self.comTool_Data_readFromCom)

        self.timerConnect = QTimer()
        self.timerConnect.timeout.connect(self.comTool_Data_readFromCom)

        self.com.readyRead.connect(lambda: self.comTool_Data_readFromCom())

        self.ui.txtMain.installEventFilter(self.ui.txtMain)

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
        print(123)
        comList = []
        info = QSerialPortInfo.availablePorts()
        for i in info:
            comList.append(i.portName())

        if len(comList) > 0:
            return

        self.ui.cboxPortName.addItems(comList)

    def comTool_Data_readFromCom(self):
        # self.com = QSerialPort()
        if self.com.bytesAvailable() == 0:
            return
        # data = QByteArray()
        QBA_data = self.com.readAll()
        Str_data = str(QBA_data, encoding='utf-8')

        if len(Str_data) == 0:
            return

        if "\b \b" in Str_data:  # backspace
            # 获取当前文本光标
            cursor = self.ui.txtMain.textCursor()
            # 将光标移动到文本结尾
            cursor.movePosition(QTextCursor.PreviousCharacter)
            # 判断当前是否选中了文本，如果选中了文本则取消选中的文本，再删除前一个字符
            if cursor.hasSelection():
                cursor.clearSelection()
            # 删除前一个字符
            while Str_data.indexOf("\b \b") != -1:
                # cursor.movePosition(QTextCursor::End)
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
        # buffer = QString::fromLocal8Bit(data)

        # 启用调试则模拟调试数据
        if self.ui.ckDebug.isChecked():
            '''count = AppData::Keys.count()
            for i in range(0, count):
                if (buffer.startsWith(AppData::Keys.at(i))):
                    sendData(AppData::Values.at(i))
                    break'''
        self.comTool_Show_Append(1, buffer)
        self.receiveCount = self.receiveCount + len(Str_data)
        self.ui.btnReceiveCount.setText("接收 : {} 字节".format(self.receiveCount))

        # 启用网络转发则调用网络发送数据
        if self.tcpOk:
            self.tcpsocket.write(Str_data)
            self.comTool_Show_Append(4, buffer)

    # data是字符串类型
    def comTool_Show_Append(self, type, data):
        self.currentCount = 0
        maxCount = 10000

        if self.currentCount >= maxCount:
            self.saveData()
            self.ui.txtMain.clear()
            self.currentCount = 0

        if self.isShow is False:
            return

        # 过滤回车换行符
        strData = data

        strData = strData.replace('\r', '')

        # 不同类型不同颜色显示
        if type == 0:
            strType = "串口发送"
        elif type == 1:
            strType = "串口接收"
            strData = strData.replace("\n", "<br />")  # html's \r
        elif type == 2:
            strType = "处理延时"
        elif type == 3:
            strType = "正在校验"
        elif type == 4:
            strType = "网络发送"
        elif type == 5:
            strType = "网络接收"
            # strData = strData.replace("\r", "")
        elif type == 6:
            strType = "提示信息"

        # strData = "时间[{0}] [{1}] {2} <br />".format(time, strType, strData)

        # 文本替换
        strData.replace("ERR", "<font color=red>ERR</font>")
        strData.replace("WARN", "<font color=yellow>WARN</font>")
        strData.replace("INF", "<font color=yellow>INF</font>")
        strData.replace("success", "<font color=green>success</font>")

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

    def button_init(self):
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

        # 连接串口界面按键
        self.ui.btnOpen.clicked.connect(self.ComOpen_Button_Clicked)

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
                # self.emit_open_com_successful()
                # 清空缓冲区
                self.com.flush()
                self.ComOpen_changeEnable(False)
                self.ui.btnOpen.setText("关闭串口")

        else:
            self.com.close()
            self.com.deleteLater()

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
        self.ui.btnSend.setEnabled(b)
        self.ui.ckAutoSend.setEnabled(b)
        self.ui.ckAutoSave.setEnabled(b)

    def Hotkey_Button_Clicked(self):
        data = self.ui.tabWidget.sender().text()
        data = data + '\n'
        # data.append(0x0d)
        # convert string to byte
        res = bytes(data, 'utf-8')

        if self.comOk:
            self.com.write(res)

        if self.udpOk:
            self.udpsocket.writeDatagram(res, QHostAddress(self.AppConfig.ServerIP), self.AppConfig.ServerPort)

        if self.tcpOk:
            self.tcpsocket.write(res)

    def module_init(self):
        pass

    def module_serialports_init(self):
        pass
