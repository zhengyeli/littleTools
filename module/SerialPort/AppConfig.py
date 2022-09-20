import PyQt6
from PyQt6.QtCore import QSettings, QFile

dict = {
    "true": True,
    "false": False,
}

class AppConfig:

    def __init__(self):
      self.ConfigFile = "setting.ini"          #配置文件路径
      self.SendFileName = "send.txt"        #发送配置文件名
      self.DeviceFileName = "device.txt"      #模拟设备数据文件名

      self.FirstConfig = "True"     #第一次使用Config

      self.PortName = ""            #串口号
      self.BaudRate = "115200"                #波特率
      self.DataBit = "8"                 #数据位
      self.Parity = "无"              #校验位
      self.StopBit = "1"              #停止位

      self.HexSend = False                #16进制发送
      self.HexReceive = False             #16进制接收
      self.Debug = False                  #模拟设备
      self.AutoClear = False              #自动清空

      self.AutoSend = False               #自动发送
      self.SendInterval = "1000"            #自动发送间隔
      self.AutoSave = False               #自动保存
      self.SaveInterval = "1000"              #自动保存间隔

      self.Mode = "Tcp_Client"                #转换模式
      self.ServerIP = "192.168.1.101"            #服务器IP
      self.ServerPort = "80"              #服务器端口
      self.ListenPort = "80"              #监听端口
      self.SleepTime = "1000"               #延时时间
      self.AutoConnect = False            #自动重连

    # 读写配置参数
    def readConfig(self):           # 读取配置参数

        set = QSettings(self.ConfigFile, QSettings.Format.IniFormat)
        set.beginGroup("FirstConfig")
        self.FirstConfig = set.value("FirstConfig")
        set.endGroup()
        if self.FirstConfig == "True":
            print("Config had been saved")
        else:
            print("config have not saved before")
            self.FirstConfig = "True"
            self.writeConfig()
            return

        set.beginGroup("ComConfig")
        self.PortName = set.value("PortName", self.PortName)
        self.BaudRate = set.value("BaudRate", self.BaudRate)
        self.DataBit = set.value("DataBit", self.DataBit)
        self.Parity = set.value("Parity", self.Parity)
        self.StopBit = set.value("StopBit", self.StopBit)

        self.HexSend = dict[set.value("HexSend", self.HexSend)]
        self.HexReceive = dict[set.value("HexReceive", self.HexReceive)]
        self.Debug = dict[set.value("Debug", self.Debug)]
        self.AutoClear = dict[set.value("AutoClear", self.AutoClear)]

        self.AutoSend = dict[set.value("AutoSend", self.AutoSend)]
        self.SendInterval = set.value("SendInterval", self.SendInterval)
        self.AutoSave = dict[set.value("AutoSave", self.AutoSave)]
        self.SaveInterval = set.value("SaveInterval", self.SaveInterval)
        set.endGroup()

        set.beginGroup("NetConfig")
        self.Mode = set.value("Mode", self.Mode)
        self.ServerIP = set.value("ServerIP", self.ServerIP)
        self.ServerPort = set.value("ServerPort", self.ServerPort)
        self.ListenPort = set.value("ListenPort", self.ListenPort)
        self.SleepTime = set.value("SleepTime", self.SleepTime)
        self.AutoConnect = dict[set.value("AutoConnect", self.AutoConnect)]
        set.endGroup()
        
    def writeConfig(self):          # 写入配置参数
        set = QSettings(self.ConfigFile, QSettings.Format.IniFormat)

        set.beginGroup("FirstConfig")
        set.setValue("FirstConfig", self.FirstConfig)
        set.endGroup()

        set.beginGroup("ComConfig")
        set.setValue("PortName", self.PortName)
        set.setValue("BaudRate", self.BaudRate)
        set.setValue("DataBit", self.DataBit)
        set.setValue("Parity", self.Parity)
        set.setValue("StopBit", self.StopBit)

        set.setValue("HexSend", self.HexSend)
        set.setValue("HexReceive", self.HexReceive)
        set.setValue("Debug", self.Debug)
        set.setValue("AutoClear", self.AutoClear)

        set.setValue("AutoSend", self.AutoSend)
        set.setValue("SendInterval", self.SendInterval)
        set.setValue("AutoSave", self.AutoSave)
        set.setValue("SaveInterval", self.SaveInterval)
        set.endGroup()

        set.beginGroup("NetConfig")
        set.setValue("Mode", self.Mode)
        set.setValue("ServerIP", self.ServerIP)
        set.setValue("ServerPort", self.ServerPort)
        set.setValue("ListenPort", self.ListenPort)
        set.setValue("SleepTime", self.SleepTime)
        set.setValue("AutoConnect", self.AutoConnect)
        set.endGroup()