from PyQt6.QtCore import QObject


class BluetoothBaseClass(QObject):

    def __init__(self, pbaseInfoShow):
        super().__init__()
        self.m_info = None
        self.m_error = None
        self.baseInfoShow = pbaseInfoShow

    def error(self):
        return self.m_error

    def info(self):
        return self.m_info

    def setError(self, errString):
        if self.baseInfoShow is not None:
            self.baseInfoShow.append("ERR|" + errString)
            print("ERR|" + errString)

    def setInfo(self, infoString):
        if self.baseInfoShow is not None:
            self.baseInfoShow.append("INO|" + infoString)
            print("INO|" + infoString)

    def clear(self):
        if self.baseInfoShow is not None:
            self.baseInfoShow.clear()

    def itself(self):
        if self.baseInfoShow is not None:
            return self.baseInfoShow
