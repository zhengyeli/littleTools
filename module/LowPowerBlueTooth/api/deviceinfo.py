from PyQt6.QtBluetooth import QBluetoothDeviceInfo


class DeviceInfo(QBluetoothDeviceInfo):

    def __init__(self, info, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.m_device = info

    def getDevice(self):
        return self.m_device

    def getName(self):
        return self.m_device.name()

    def getAddress(self):
        return self.m_device.address()

    def setDevice(self, device):
        self.m_device = device