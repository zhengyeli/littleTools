from PyQt6.QtBluetooth import QBluetoothDeviceDiscoveryAgent, QBluetoothDeviceInfo
from PyQt6.QtCore import pyqtSignal

from module.LowPowerBlueTooth.api.deviceHandler import DeviceHandler
from module.LowPowerBlueTooth.api.deviceinfo import DeviceInfo


class DeviceFinder(DeviceHandler):
    signal_devicefound = pyqtSignal(QBluetoothDeviceInfo)

    def __init__(self, bthBaseWidget):
        super().__init__(bthBaseWidget)

        self.m_deviceHandler = super()
        self.m_deviceDiscoveryAgent = QBluetoothDeviceDiscoveryAgent()
        self.m_deviceDiscoveryAgent.setLowEnergyDiscoveryTimeout(0)
        self.m_deviceDiscoveryAgent.deviceDiscovered.connect(self.addDevice)
        self.m_deviceDiscoveryAgent.errorOccurred.connect(self.scanError)
        self.m_deviceDiscoveryAgent.finished.connect(self.scanFinished)

    def addDevice(self, device):
        if device.coreConfigurations() == QBluetoothDeviceInfo.CoreConfiguration.LowEnergyCoreConfiguration:
            self.setInfo(device.name())
            self.signal_devicefound.emit(device)

    def scanError(self, error):
        if error == QBluetoothDeviceDiscoveryAgent.Error.PoweredOffError:
            self.setInfo("The Bluetooth adaptor is powered off.")
        elif error == QBluetoothDeviceDiscoveryAgent.Error.InputOutputError:
            self.setInfo("Writing or reading from the device resulted in an error.")
        else:
            self.setInfo("An unknown error has occurred.")

    def scanFinished(self):
        if len(self.m_deviceDiscoveryAgent.discoveredDevices()) == 0:
            self.setInfo("Low Energy device Scan finish...")
        else:
            self.setInfo("Low Energy device Scan finish...")

    def startSearch(self):
        self.m_deviceHandler.setDevice(None)

        self.setInfo("Scanning for devices...")
        self.m_deviceDiscoveryAgent.start(QBluetoothDeviceDiscoveryAgent.DiscoveryMethod.LowEnergyMethod)

    def stopSearch(self):
        self.setInfo("Stop scan")
        self.m_deviceDiscoveryAgent.stop()

    def connectToService(self, name):
        self.m_deviceDiscoveryAgent.stop()
        print(len(self.m_deviceDiscoveryAgent.discoveredDevices()))
        for device in self.m_deviceDiscoveryAgent.discoveredDevices():
            if device.name() == name:
                self.m_deviceHandler.setDevice(device)
                self.setInfo("connect to " + name)
                break

    def scanning(self):
        return self.m_deviceDiscoveryAgent.isActive()


