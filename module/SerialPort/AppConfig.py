from PyQt6.QtCore import QSettings

boolDict = {
    "true": True,
    "false": False,
    "True": True,
    "False": False,
    True: True,
    False: False,
}


class AppConfig:

    def __init__(self):
        self.ConfigFile = "setting.ini"  # 配置文件路径
        self.SendFileName = "send.txt"  # 发送配置文件名
        self.DeviceFileName = "device.txt"  # 模拟设备数据文件名

        self.FirstConfig = "True"  # 第一次使用Config

        self.PortName = ""  # 串口号
        self.BaudRate = "115200"  # 波特率
        self.DataBit = "8"  # 数据位
        self.Parity = "无"  # 校验位
        self.StopBit = "1"  # 停止位

        self.HexSend = False  # 16进制发送
        self.HexReceive = False  # 16进制接收
        self.Debug = False  # 模拟设备
        self.AutoClear = False  # 自动清空

        self.AutoSend = False  # 自动发送
        self.SendInterval = "1000"  # 自动发送间隔
        self.AutoSave = False  # 自动保存
        self.SaveInterval = "1000"  # 自动保存间隔

        self.Mode = "Tcp_Client"  # 转换模式
        self.ServerIP = "192.168.1.101"  # 服务器IP
        self.ServerPort = "80"  # 服务器端口
        self.ListenPort = "80"  # 监听端口
        self.SleepTime = "1000"  # 延时时间
        self.AutoConnect = False  # 自动重连

    # 读写配置参数
    def readConfig(self):  # 读取配置参数

        serialConfigSet = QSettings(self.ConfigFile, QSettings.Format.IniFormat)
        serialConfigSet.beginGroup("FirstConfig")
        self.FirstConfig = serialConfigSet.value("FirstConfig")
        serialConfigSet.endGroup()
        if self.FirstConfig == "True":
           pass
        else:
            print("config have not saved before")
            self.FirstConfig = "True"
            self.writeConfig()
            return

        serialConfigSet.beginGroup("ComConfig")
        self.PortName = serialConfigSet.value("PortName", self.PortName)
        self.BaudRate = serialConfigSet.value("BaudRate", self.BaudRate)
        self.DataBit = serialConfigSet.value("DataBit", self.DataBit)
        self.Parity = serialConfigSet.value("Parity", self.Parity)
        self.StopBit = serialConfigSet.value("StopBit", self.StopBit)

        self.HexSend = boolDict[serialConfigSet.value("HexSend", self.HexSend)]
        self.HexReceive = boolDict[serialConfigSet.value("HexReceive", self.HexReceive)]
        self.Debug = boolDict[serialConfigSet.value("Debug", self.Debug)]
        self.AutoClear = boolDict[serialConfigSet.value("AutoClear", self.AutoClear)]

        self.AutoSend = boolDict[serialConfigSet.value("AutoSend", self.AutoSend)]
        self.SendInterval = serialConfigSet.value("SendInterval", self.SendInterval)
        self.AutoSave = boolDict[serialConfigSet.value("AutoSave", self.AutoSave)]
        self.SaveInterval = serialConfigSet.value("SaveInterval", self.SaveInterval)
        serialConfigSet.endGroup()

        serialConfigSet.beginGroup("NetConfig")
        self.Mode = serialConfigSet.value("Mode", self.Mode)
        self.ServerIP = serialConfigSet.value("ServerIP", self.ServerIP)
        self.ServerPort = serialConfigSet.value("ServerPort", self.ServerPort)
        self.ListenPort = serialConfigSet.value("ListenPort", self.ListenPort)
        self.SleepTime = serialConfigSet.value("SleepTime", self.SleepTime)
        self.AutoConnect = boolDict[serialConfigSet.value("AutoConnect", self.AutoConnect)]
        serialConfigSet.endGroup()

    def writeConfig(self):  # 写入配置参数
        serialConfigSet = QSettings(self.ConfigFile, QSettings.Format.IniFormat)

        serialConfigSet.beginGroup("FirstConfig")
        serialConfigSet.setValue("FirstConfig", self.FirstConfig)
        serialConfigSet.endGroup()

        serialConfigSet.beginGroup("ComConfig")
        serialConfigSet.setValue("PortName", self.PortName)
        serialConfigSet.setValue("BaudRate", self.BaudRate)
        serialConfigSet.setValue("DataBit", self.DataBit)
        serialConfigSet.setValue("Parity", self.Parity)
        serialConfigSet.setValue("StopBit", self.StopBit)

        serialConfigSet.setValue("HexSend", self.HexSend)
        serialConfigSet.setValue("HexReceive", self.HexReceive)
        serialConfigSet.setValue("Debug", self.Debug)
        serialConfigSet.setValue("AutoClear", self.AutoClear)

        serialConfigSet.setValue("AutoSend", self.AutoSend)
        serialConfigSet.setValue("SendInterval", self.SendInterval)
        serialConfigSet.setValue("AutoSave", self.AutoSave)
        serialConfigSet.setValue("SaveInterval", self.SaveInterval)
        serialConfigSet.endGroup()

        serialConfigSet.beginGroup("NetConfig")
        serialConfigSet.setValue("Mode", self.Mode)
        serialConfigSet.setValue("ServerIP", self.ServerIP)
        serialConfigSet.setValue("ServerPort", self.ServerPort)
        serialConfigSet.setValue("ListenPort", self.ListenPort)
        serialConfigSet.setValue("SleepTime", self.SleepTime)
        serialConfigSet.setValue("AutoConnect", self.AutoConnect)
        serialConfigSet.endGroup()
