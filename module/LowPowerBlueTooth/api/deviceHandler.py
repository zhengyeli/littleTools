from PyQt6.QtBluetooth import QBluetoothUuid, QLowEnergyService, QLowEnergyController, QLowEnergyDescriptor, \
    QBluetoothDeviceInfo
from PyQt6.QtCore import QTimer, pyqtSignal, QByteArray

from module.LowPowerBlueTooth.api.BluetoothBaseClass import BluetoothBaseClass


class DeviceHandler(BluetoothBaseClass):
    emit_bleMessageChange = pyqtSignal(bytes)

    def __init__(self, bthBaseWidget):
        super().__init__(bthBaseWidget)
        self.getChar = None
        self.setChar = None
        self.m_currentDevice = None
        self.m_service = None
        self.m_control = None
        self.m_notificationDesc = None

    def setAddressType(self, type):
        pass

    def serviceScanDone(self):
        self.setInfo("Service scan done.")
        uuids = self.m_control.services()
        if self.m_service is not None:
            self.m_service.clear()
            self.m_service = None

        for uuid in uuids:
            if uuid.toString() == "{00010203-0405-0607-0809-0a0b0c0d1910}":
                self.m_service = self.m_control.createServiceObject(QBluetoothUuid(uuid))
                self.setInfo("select Service uuid" + uuid.toString())
                break

        if self.m_service is not None:
            self.m_service.descriptorWritten.connect(self.confirmedDescriptorWrite)
            self.m_service.descriptorRead.connect(self.descriptorRead)
            self.m_service.stateChanged.connect(self.serviceStateChanged)
            self.m_service.characteristicChanged.connect(self.updateInfoFromDev)
            self.m_service.characteristicRead.connect(self.characteristicRead)
            self.m_service.characteristicWritten.connect(self.characteristicWrittenFun)
            self.m_service.discoverDetails()

    def setDevice(self, device):
        self.m_currentDevice = device

        if self.m_control is not None:
            self.m_control.disconnectFromDevice()
            self.m_control.clear()
            self.m_control = None

        if self.m_currentDevice is not None:
            self.m_control = QLowEnergyController.createCentral(self.m_currentDevice)
            self.m_control.setRemoteAddressType(QLowEnergyController.RemoteAddressType.PublicAddress)
            self.m_control.serviceDiscovered.connect(self.serviceDiscovered)
            self.m_control.discoveryFinished.connect(self.serviceScanDone)
            self.m_control.errorOccurred.connect(lambda: self.setError("Cannot connect to remote device."))
            self.m_control.connected.connect(self.connectSuccessful)
            self.m_control.disconnected.connect(lambda: self.setError("LowEnergy controller disconnected."))
            self.m_control.connectToDevice()

    def connectSuccessful(self):
        self.setInfo("Connect successful.")
        self.m_control.discoverServices()

    def serviceDiscovered(self, gatt):
        self.setInfo("serviceDiscovered:" + gatt.toString())

    def confirmedDescriptorWrite(self, LowEnergyDescriptor, value):
        pass
        # if LowEnergyDescriptor.isValid() and LowEnergyDescriptor == self.m_notificationDesc and value == "0000":
        #     self.m_control.disconnectFromDevice()
        #     self.sender().clear()

    def descriptorRead(self, d, value):
        self.setInfo("descriptorRead ")

    def serviceStateChanged(self, newState):
        print(newState)
        if newState == QLowEnergyService.ServiceState.RemoteServiceDiscovering:
            self.setInfo("QLowEnergyService.ServiceState.RemoteServiceDiscovering")
        elif newState == QLowEnergyService.ServiceState.RemoteServiceDiscovered:
            self.setInfo("QLowEnergyService.ServiceState.RemoteServiceDiscovered")
            self.searchCharacteristic()
        elif newState == QLowEnergyService.ServiceState.RemoteService:
            self.setInfo("QLowEnergyService.ServiceState.RemoteService")
            QTimer.singleShot(self.serviceScanDone)
        else:
            pass
            # self.setInfo(str(newState, encoding="utf-8"))

    def updateInfoFromDev(self, c, value):
        self.emit_bleMessageChange(bytes(value, "utf-8"))

    def characteristicRead(self, c, value):
        self.setInfo("characteristicRead " + value)

    def characteristicWrittenFun(self, c, value):
        self.setInfo("characteristicWrittenFun " + value)

    def characteristicWrite(self, service, character, value):
        service.writeCharacteristic(character, value, QLowEnergyService.WriteMode.WriteWithoutResponse)

    def searchCharacteristic(self):
        print(self.m_service == self.sender())
        service = self.sender()
        chars = service.characteristics()
        for char in chars:
            pass

        self.setChar = service.characteristic(QBluetoothUuid("00010203-0405-0607-0809-0a0b0c0d2b11"))
        self.getChar = service.characteristic(QBluetoothUuid("00010203-0405-0607-0809-0a0b0c0d2b10"))

        if self.getChar.isValid() is False:
            self.setError("getChar not found.")

        if self.setChar.isValid() is False:
            self.setError("setChar not found.")

        self.m_notificationDesc = self.getChar.descriptor(QBluetoothUuid.DescriptorType.ClientCharacteristicConfiguration)

        if self.m_notificationDesc.isValid():
            self.m_service.writeCharacteristic(self.m_notificationDesc, QByteArray(bytes("0100", "utf-8")))
        else:
            self.setError("m_notificationDesc is null.")

    def disconnectDevice(self):
        if self.m_control:
            self.m_control.disconnectFromDevice()
            self.m_control.clear()
            self.m_control = None

    def disconnectService(self):
        if self.m_notificationDesc:
            self.m_service.writeDescriptor(self.m_notificationDesc, QByteArray("0000"))

    def continueConnectService(self):
        if self.m_notificationDesc:
            self.m_service.writeDescriptor(self.m_notificationDesc, QByteArray("0100"))





