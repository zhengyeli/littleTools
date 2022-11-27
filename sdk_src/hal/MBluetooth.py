import asyncio
import threading
from time import sleep

from bleak import BleakScanner, BleakGATTCharacteristic
from bleak import BleakClient

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
                print("  [Characteristic] {} {}, Value: {}".format(characteristic, ",".join(characteristic.properties), value))
            except Exception as e:
                print("  [Characteristic] {} {}, Error: {}".format(characteristic, ",".join(characteristic.properties), e))
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

asyncio.run(main())
print("here")

