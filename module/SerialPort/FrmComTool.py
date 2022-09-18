from distutils.util import strtobool

from PyQt6 import QtSerialPort
from PyQt6.QtCore import QSettings, QTimer, QIODevice, pyqtSignal
from PyQt6.QtNetwork import QTcpSocket, QUdpSocket
from PyQt6.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox, QCheckBox

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
        self.ui = ui
        self.serial = None
        self.com = None
        self.comOk = False
        self.receiveCount = 0
        self.sendCount = 0
        self.isShow = True

        self.timerRead = None
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
        # self.ui = Ui_frmComTool(self.ui)

    def comTool_form_init(self):
        # 连接按键
        self.button_init()

        # 添加显示参数
        Intervals = ["1", "10", "20", "50", "100", "200", "300", "500", "1000", "1500", "2000", "3000", "5000", "10000"]
        Datas = ["AA BB CC"]
        self.ui.cboxSendInterval.addItems(Intervals)
        self.ui.cboxData.addItems(Datas)

        self.timerRead = QTimer()
        self.timerRead.setInterval(100)
        self.timerRead.timeout.connect(self.comTool_Data_readFromCom)

        self.timerSend = QTimer()
        self.timerSend.setInterval(100)
        self.timerSend.timeout.connect(self.comTool_Data_readFromCom)

        self.timerSave = QTimer()
        self.timerSave.setInterval(100)
        self.timerSave.timeout.connect(self.comTool_Data_readFromCom)

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
        self.AppConfig.ServerIP = self.ui.txtServerIP
        self.AppConfig.ServerPort = self.ui.txtServerPort
        self.AppConfig.ListenPort = self.ui.txtListenPort
        self.AppConfig.SleepTime = self.ui.cboxSleepTime.currentText()
        if self.ui.ckAutoConnect.isChecked():
            self.AppConfig.AutoConnect = 1
        else:
            self.AppConfig.AutoConnect = 0

        self.AppConfig.writeConfig()

    def comTool_Data_readFromCom(self):
        if self.com.bytesAvailable() <= 0:
            return
        data = self.com.readAll()
        if data.len <= 0:
            return
        print(data)

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
            self.com = QSerialPort()

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
                self.timerRead.start()

        elif self.ui.btnOpen.text() == "扫描":
            comList = []
            info = QSerialPortInfo.availablePorts()
            for i in info:
                comList.append(i.portName())

            if info.isEmpty():
                self.ui.btnOpen.setText("扫描")

            self.ui.cboxPortName.addItems(comList)
        else:
            self.timerRead.stop()
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
        # data.append(0x0d)
        if self.com is not None:
            self.com.write(data)

        if self.udpOk:
            self.udpsocket.writeDatagram(data.data(), QHostAddress(ServerIP), ServerPort)

        if self.tcpOk:
            self.tcpsocket.write(data)

    def module_init(self):
        pass

    def module_serialports_init(self):
        pass
