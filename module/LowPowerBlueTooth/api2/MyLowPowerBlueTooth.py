import binascii

from PyQt6.uic.properties import QtWidgets
from PyQt6.QtBluetooth import QBluetoothDeviceDiscoveryAgent, QLowEnergyController, QLowEnergyService, QBluetoothUuid
from PyQt6.QtCore import QByteArray, QTimer
from PyQt6.QtWidgets import QApplication


class MyLowPowerBluetooth:
    def __init__(self):
        self.character = None
        self.getChar = None
        self.setChar = None
        self.bleController = None
        self.service = None
        self.ScanDevices()

    def ScanDevices(self):
        self.bleDeviceDiscoveryAgent = QBluetoothDeviceDiscoveryAgent()
        self.bleDeviceDiscoveryAgent.setLowEnergyDiscoveryTimeout(0)
        self.bleDeviceDiscoveryAgent.errorOccurred.connect(self.scanError)
        self.bleDeviceDiscoveryAgent.deviceDiscovered.connect(self.deviceDiscovered)
        self.bleDeviceDiscoveryAgent.start()

    def scanError(self, error):
        if error == QBluetoothDeviceDiscoveryAgent.Error.PoweredOffError:
            print("The Bluetooth adaptor is powered off.")
        elif error == QBluetoothDeviceDiscoveryAgent.Error.InputOutputError:
            print("Writing or reading from the device resulted in an error.")
        else:
            print("An unknown error has occurred.")

    def deviceDiscovered(self, deviceiInfo):
        print(deviceiInfo.name())
        if deviceiInfo.name() == "ihoment_H7171_A883":
            self.bleDeviceDiscoveryAgent.stop()
            self.bleController = QLowEnergyController.createCentral(deviceiInfo)
            self.bleController.connected.connect(self.deviceConnected)
            self.bleController.discoveryFinished.connect(self.discoveryFinished)
            self.bleController.connectToDevice()

    def deviceConnected(self):
        self.bleController.discoverServices()

    def discoveryFinished(self):
        if self.service is not None:
            del self.service
            self.service = None

        serviceUuids = self.bleController.services()
        for serviceUuid in serviceUuids:
            if serviceUuid.toString() == "{00010203-0405-0607-0809-0a0b0c0d1910}":
                self.character = serviceUuid
                self.service = self.bleController.createServiceObject(serviceUuid)
                break

        if self.service is not None:
            self.service.stateChanged.connect(self.serviceStateChanged)
            self.service.characteristicChanged.connect(self.updateInfoFromDev)
            self.service.discoverDetails()

    def updateInfoFromDev(self, c, value):
        print(value)

    def characteristicWrite(self, service, character, value):
        print(value)
        service.writeCharacteristic(character, value, QLowEnergyService.WriteMode.WriteWithoutResponse)

    def serviceStateChanged(self, state):
        print(state)
        if state == QLowEnergyService.ServiceState.RemoteServiceDiscovered:
            chars = self.service.characteristics()
            for char in chars:
                print(char)

            self.setChar = self.service.characteristic(QBluetoothUuid("00010203-0405-0607-0809-0a0b0c0d2b11"))
            self.getChar = self.service.characteristic(QBluetoothUuid("00010203-0405-0607-0809-0a0b0c0d2b10"))

            if self.getChar.isValid() is False:
                print("getChar not found.")

            if self.setChar.isValid() is False:
                print("setChar not found.")

            m_notificationDesc = self.getChar.descriptor(
                QBluetoothUuid(QBluetoothUuid.DescriptorType.ClientCharacteristicConfiguration))

            if m_notificationDesc.isValid():
                self.service.writeDescriptor(m_notificationDesc, QByteArray(bytes("0100", "utf-8")))
            else:
                print("m_notificationDesc is null.")


            hex = "33 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 32"
            hex = hex.replace(' ', '')

            self.characteristicWrite(self.service, self.setChar, bytes.fromhex(hex))
        elif state == QLowEnergyService.ServiceState.RemoteService:
            QTimer.singleShot(0, self.discoveryFinished)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ble = MyLowPowerBluetooth()
    sys.exit(app.exec())
    # int_array = [170, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 171]
    # byte_array = bytearray(int_array)
    # print(bytearray.hex(byte_array))
    # print(bytes.fromhex(bytearray.hex(byte_array)))








