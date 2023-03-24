from time import sleep

from PyQt6.QtBluetooth import QBluetoothUuid, QLowEnergyService, QLowEnergyController
from PyQt6.QtCore import QTimer, pyqtSignal

from module.LowPowerBlueTooth.api.BluetoothBaseClass import BluetoothBaseClass


class DeviceHandler(BluetoothBaseClass):
    emit_bleMessageChange = pyqtSignal(bytes)
    emit_bleConnectSuccessful = pyqtSignal(bool)

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
            del self.m_service
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
            del self.m_control
            self.m_control = None

        if self.m_currentDevice is not None:
            self.m_control = QLowEnergyController.createCentral(self.m_currentDevice)
            self.m_control.setRemoteAddressType(QLowEnergyController.RemoteAddressType.PublicAddress)
            self.m_control.serviceDiscovered.connect(self.serviceDiscovered)
            self.m_control.discoveryFinished.connect(self.serviceScanDone)
            self.m_control.errorOccurred.connect(lambda: self.setInfo("Cannot connect to remote device."))
            self.m_control.connected.connect(self.connectSuccessful)
            self.m_control.disconnected.connect(lambda: self.setInfo("LowEnergy controller disconnected."))
            self.m_control.connectToDevice()

    def connectSuccessful(self):
        self.emit_bleConnectSuccessful.emit(True)
        self.setInfo("Connect successful.")
        self.m_control.discoverServices()

    def serviceDiscovered(self, gatt):
        self.setInfo("serviceDiscovered:" + gatt.toString())

    def confirmedDescriptorWrite(self, descriptor, value):
        self.setInfo("descriptor change:" + str(value))

    def descriptorRead(self, d, value):
        self.setInfo("descriptorRead " + str(value))

    def serviceStateChanged(self, newState):
        if newState == QLowEnergyService.ServiceState.RemoteServiceDiscovering:
            self.setInfo("QLowEnergyService.ServiceState.RemoteServiceDiscovering")
        elif newState == QLowEnergyService.ServiceState.RemoteServiceDiscovered:
            self.setInfo("QLowEnergyService.ServiceState.RemoteServiceDiscovered")
            self.searchCharacteristic()
            # 终于是发现问题：不能在服务发现完成的槽函数中直接进行发现特性。
        elif newState == QLowEnergyService.ServiceState.RemoteService:
            self.setInfo("QLowEnergyService.ServiceState.RemoteService")
            QTimer.singleShot(0, self.serviceScanDone)
        else:
            self.setInfo(str(newState))

    def updateInfoFromDev(self, c, value):
        self.emit_bleMessageChange.emit(bytes(value))

    def characteristicRead(self, c, value):
        self.setInfo("characteristicRead " + str(value))

    def characteristicWrittenFun(self, c, value):
        self.setInfo("characteristicWrittenFun " + str(value))

    def characteristicWrite(self, byte_value):
        if self.m_service is not None:
            if self.setChar is not None:
                self.m_service.writeCharacteristic(self.setChar, byte_value,
                                                   QLowEnergyService.WriteMode.WriteWithoutResponse)
            else:
                self.setError("write characteristic not valid")
        else:
            self.setError("service is not valid")

    def searchCharacteristic(self):
        chars = self.m_service.characteristics()
        for char in chars:
            d = char.descriptor(QBluetoothUuid(QBluetoothUuid.DescriptorType.ClientCharacteristicConfiguration))

            if d.isValid() is False:
                continue

            self.m_service.writeDescriptor(d, bytes.fromhex("0100"))

        self.setChar = self.m_service.characteristic(QBluetoothUuid("00010203-0405-0607-0809-0a0b0c0d2b11"))
        self.getChar = self.m_service.characteristic(QBluetoothUuid("00010203-0405-0607-0809-0a0b0c0d2b10"))

        if self.getChar.isValid() is False:
            self.setError("getChar not found.")

        if self.setChar.isValid() is False:
            self.setError("setChar not found.")

        # self.m_notificationDesc = self.setChar.descriptor(QBluetoothUuid(
        #     QBluetoothUuid.DescriptorType.ClientCharacteristicConfiguration
        # ))
        #
        # if self.m_notificationDesc.isValid():
        #     # QLowEnergyService.writeDescriptor()
        #     self.m_service.writeDescriptor(self.m_notificationDesc, bytes.fromhex("0100"))
        # else:
        #     self.setError("m_notificationDesc is null.")
        # self.m_service.readDescriptor(self.m_notificationDesc)

    def disconnectDevice(self):
        if self.m_control:
            self.m_control.disconnectFromDevice()
            del self.m_control
            self.m_control = None
            del self.getChar
            del self.setChar
            self.getChar = None
            self.setChar = None

    def disconnectService(self):
        if self.m_notificationDesc:
            self.m_service.writeDescriptor(self.m_notificationDesc, bytes.fromhex("0000"))

    def continueConnectService(self):
        if self.m_notificationDesc:
            self.m_service.writeDescriptor(self.m_notificationDesc, bytes.fromhex("0100"))
