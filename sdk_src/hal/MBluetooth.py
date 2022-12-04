import asyncio
import threading
from enum import Enum
from time import sleep

from bleak import BleakScanner, BleakGATTCharacteristic, BLEDevice
from bleak import BleakClient

from sdk_src.ui.MObject import MObject
from sdk_src.utils import utils

address = None
MODEL_NBR_UUID = "00010203-0405-0607-0809-0a0b0c0d1910"


async def example():
    global address
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)
        if d.name == "Govee_H6061_3C08":
            address = d.address

    if address is not None:
        async with BleakClient(address) as client:
            for service in client.services:
                print("[Service] {}".format(service))

                for char in service.characteristics:
                    if "read" in char.properties:
                        try:
                            value = await client.read_gatt_char(char.uuid)
                            print("  [Characteristic] {} {}, Value: {}".format(char, ",".join(char.properties), value))
                        except Exception as e:
                            print("  [Characteristic] {} {}, Error: {}".format(char, ",".join(char.properties), e))

                    else:
                        print("  [Characteristic] {} {}".format(char, ",".join(char.properties)))

                for descriptor in char.descriptors:
                    try:
                        value = await client.read_gatt_descriptor(descriptor.handle)
                        print("    [Descriptor] {}, Value: {}".format(descriptor, value))
                    except Exception as e:
                        print("    [Descriptor] {}, Error: {}".format(descriptor, e))


def notification_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
    """Simple notification handler which prints the data received."""
    print("{}: {}".format(characteristic.description, ' '.join(hex(x) for x in data)))


async def writeCharacteristic(client: BleakClient, characteristic):
    while True:
        if "write-without-response" in characteristic.properties:
            try:
                Hex = "33 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 33"
                Hex = Hex.replace(' ', '')
                value = await client.write_gatt_char(characteristic.uuid, bytes.fromhex(Hex))
                print("  [Characteristic] {} {}, Value: {}".format(characteristic, ",".join(characteristic.properties),
                                                                   value))
            except Exception as e:
                print("  [Characteristic] {} {}, Error: {}".format(characteristic, ",".join(characteristic.properties),
                                                                   e))
        sleep(1)


async def main():
    global address
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)
        if d.name == "Govee_H6061_3C08":
            address = d.address

    if address is not None:
        async with BleakClient(address) as client:
            for service in client.services:
                print("[Service] {}".format(service))
                if service.uuid == "00010203-0405-0607-0809-0a0b0c0d1910":
                    for char in service.characteristics:
                        if char.uuid == "00010203-0405-0607-0809-0a0b0c0d2b10":
                            await client.start_notify(char, notification_handler)
                        elif char.uuid == "00010203-0405-0607-0809-0a0b0c0d2b11":
                            await writeCharacteristic(client, char)


# asyncio.run(main())
print("here")


class event(Enum):
    ScanDone = 0
    ScanError = 1
    ScanSuccess = 2

    ConnectError = 3
    ConnectSuccess = 4
    Disconnected = 5

    ServiceUuid_DiscoveryDone = 6
    ServiceUuid_Subscribe_Success = 7
    ServiceUuid_Subscribe_Error = 8

    CharacteristicUuid_DiscoveryDone = 9
    CharacteristicUuid_Subscribe_Success = 10
    CharacteristicUuid_Subscribe_Error = 11

    FoundDevice = 12
    Notify = 13
    NoDevice = 14


def callback_try(callback, *args, **kwargs):
    if callback is not None:
        try:
            callback(*args, **kwargs)
        except Exception as e:
            print(e)
    else:
        print("callback is None")


class DeviceFinder(BleakScanner):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.signal_devices_found = MObject()
        self.signal_devices_found_error = MObject()
        self.signal_devices_no_found = MObject()
        self.devices = None

    async def scan(self):
        try:
            self.devices = await self.discover()
            if self.devices is not None:
                callback_try(self.signal_devices_found.callback, self.devices)
            else:
                callback_try(self.signal_devices_no_found.callback, None)
        except Exception as e:
            callback_try(self.signal_devices_found_error.callback, e)


class MLowPowerBlueTooth:
    def __init__(self):
        self.deviceFinder = DeviceFinder()

        self.deviceHandler = None
        self.signal_device_connect_ok = MObject()
        self.signal_device_connect_failed = MObject()

        self.signal_services_found = MObject()

        self.signal_characteristic_found = MObject()

        self.signal_properties_found = MObject()

        self.signal_descriptor_found = MObject()

        self.signal_notify = MObject()

        self.client = None

    async def connectToDevice(self, name=None):
        if self.deviceFinder.devices is None:
            await self.deviceFinder.scan()
        Address = None
        if name is not None:
            for d in self.deviceFinder.devices:
                if d.name == name:
                    Address = d.address
                    break
        if Address is None:
            callback_try(self.signal_device_connect_failed.callback)
        else:
            async with BleakClient(Address) as self.client:
                callback_try(self.signal_device_connect_ok.callback)
                for service in self.client.services:
                    callback_try(self.signal_services_found.callback, service.uuid)

    async def connectToService(self, serviceUuid=""):
        if serviceUuid != "":
            for service in self.client.services:
                if service.uuid == serviceUuid:
                    for char in service.characteristics:
                        callback_try(self.signal_characteristic_found.callback, char)
                        if "read" in char.properties:
                            callback_try(self.signal_properties_found.callback, char.properties)
                            try:
                                value = await self.client.read_gatt_char(char.uuid)
                                print("  [Characteristic] {} {}, Value: {}".format(char, ",".join(char.properties),
                                                                                   value))
                            except Exception as e:
                                print("  [Characteristic] {} {}, Error: {}".format(char, ",".join(char.properties), e))
                        elif "notify" in char.properties:
                            await self.client.start_notify(char, self.notify)
                        else:
                            print("  [Characteristic] {} {}".format(char, ",".join(char.properties)))

                        for descriptor in char.descriptors:
                            callback_try(self.signal_descriptor_found.callback, descriptor)
                            try:
                                value = await self.client.read_gatt_descriptor(descriptor.handle)
                                print("    [Descriptor] {}, Value: {}".format(descriptor, value))
                            except Exception as e:
                                print("    [Descriptor] {}, Error: {}".format(descriptor, e))
                        break

    def notify(self, byte: bytearray):
        callback_try(self.signal_notify.callback, byte)

    async def write(self, characteristicUuID: str, byte):
        try:
            await self.client.write_gatt_char(characteristicUuID, byte)
        except Exception as e:
            print(e)


async def loop():
    b = MLowPowerBlueTooth()
    await b.connectToDevice("Govee_H6061_3C08")
    Hex = "33 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 33"
    Hex = Hex.replace(' ', '')
    await b.write("00010203-0405-0607-0809-0a0b0c0d2b11", bytes.fromhex(Hex))


if __name__ == "__main__":
    asyncio.run(loop())
    print(123)
