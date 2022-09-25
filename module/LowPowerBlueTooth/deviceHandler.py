from PyQt6.QtBluetooth import QBluetoothUuid, QLowEnergyService, QLowEnergyController, QLowEnergyDescriptor, \
    QBluetoothDeviceInfo
from PyQt6.QtCore import QTimer, pyqtSignal, QByteArray

from module.LowPowerBlueTooth.BluetoothBaseClass import BluetoothBaseClass

class DeviceHandler(BluetoothBaseClass):
    emit_bleMessageChange = pyqtSignal(bytes)

    def __init__(self, bthBaseClass):
        super().__init__(bthBaseClass)
        self.getChar = None
        self.setChar = None
        self.m_currentDevice = QBluetoothDeviceInfo()
        self.bthBaseClass = bthBaseClass
        self.m_serviceList = []
        self.m_service = QLowEnergyService()
        self.m_control = QLowEnergyController()
        self.m_notificationDesc = QLowEnergyDescriptor()

    def setAddressType(self, type):
        pass

    def serviceScanDone(self):
        self.bthBaseClass.setInfo("Service scan done.")
        uuids = self.m_control.services()
        if self.m_service is not None:
            self.m_service.clear()
            self.m_service = None

        for uuid in uuids:
            service = self.m_control.createServiceObject(QBluetoothUuid(uuid))
            self.m_serviceList.append(service)
            self.bthBaseClass.setInfo("Service scan done.")

        if len(self.m_serviceList) == 0:
            self.bthBaseClass.setInfo("Service not found")
            return

    def setDevice(self, device):
        self.m_currentDevice = device

        if self.m_control is not None:
            self.m_control.disconnectFromDevice()
            self.m_control.clear()
            self.m_control = None

        if self.m_currentDevice:
            self.m_control = QLowEnergyController.createCentral(self.m_currentDevice.getDevice())
            self.m_control.setRemoteAddressType(QLowEnergyController.RemoteAddressType.PublicAddress)
            self.m_control.serviceDiscovered.connect(self.serviceDiscovered)
            self.m_control.discoveryFinished.connect(self.serviceScanDone)
            self.m_control.errorOccurred.connect(lambda: self.bthBaseClass.setError("Cannot connect to remote device."))
            self.m_control.connected.connect(lambda: self.bthBaseClass.setError("Cannot connect to remote device."), self.m_control.discoverServices())
            self.m_control.disconnected.connect(lambda: self.bthBaseClass.setError("LowEnergy controller disconnected."))
            self.m_control.connectToDevice()

    def serviceDiscovered(self, gatt):
        self.bthBaseClass.setInfo("serviceDiscovered:" + gatt.toString())

    def selectService(self, uuid):
        for service in self.m_serviceList:
            if service.serviceUuid() == uuid:
                service.descriptorWritten.connect(self.confirmedDescriptorWrite)
                service.descriptorRead.connect(self.descriptorRead)
                service.stateChanged.connect(self.serviceStateChanged)
                service.characteristicChanged.connect(self.updateInfoFromDev)
                service.characteristicRead.connect(self.characteristicRead)
                service.characteristicWritten.connect(self.characteristicWrittenFun)
                service.discoverDetails()
                self.m_service = service
                return service

    def confirmedDescriptorWrite(self, LowEnergyDescriptor, value):
        if LowEnergyDescriptor.isValid() and LowEnergyDescriptor == self.m_notificationDesc and value == "0000":
            self.m_control.disconnectFromDevice()
            self.sender().clear()

    def descriptorRead(self, d, value):
        self.bthBaseClass.setInfo("descriptorRead " + d.name())

    def serviceStateChanged(self, newState):
        if newState == QLowEnergyService.ServiceState.RemoteServiceDiscovering:
            self.bthBaseClass.setInfo("QLowEnergyService.ServiceState.RemoteServiceDiscovering")
        elif newState == QLowEnergyService.ServiceState.RemoteServiceDiscovered:
            self.bthBaseClass.setInfo("QLowEnergyService.ServiceState.RemoteServiceDiscovered")
            self.searchCharacteristic()
        elif newState == QLowEnergyService.ServiceState.RemoteService:
            self.bthBaseClass.setInfo("QLowEnergyService.ServiceState.RemoteService")
            QTimer.singleShot(self.serviceScanDone)
        else:
            self.bthBaseClass.setInfo(str(newState, encoding="utf-8"))

    def updateInfoFromDev(self, c, value):
        self.emit_bleMessageChange(bytes(value, "utf-8"))

    def characteristicRead(self, c, value):
        self.bthBaseClass.setInfo("characteristicRead " + value)

    def characteristicWrittenFun(self, c, value):
        self.bthBaseClass.setInfo("characteristicWrittenFun " + value)

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
            self.bthBaseClass.setError("getChar not found.")

        if self.setChar.isValid() is False:
            self.bthBaseClass.setError("setChar not found.")

        self.m_notificationDesc = self.getChar.descriptor(QBluetoothUuid.DescriptorType.ClientCharacteristicConfiguration)

        if self.m_notificationDesc.isValid():
            self.m_service.writeCharacteristic(self.m_notificationDesc, QByteArray(bytes("0100", "utf-8")))
        else:
            self.bthBaseClass.setError("m_notificationDesc is null.")




