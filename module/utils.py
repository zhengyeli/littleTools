class utils:
    @staticmethod
    def bytes2hex(bytesData):
        return bytes.hex(bytesData, ' ')

    @staticmethod
    def hex2bytes(hex):
        return bytes.fromhex(hex)

    @staticmethod
    def hex2int(hex):
        return int(hex, 16)

    @staticmethod
    def int2hex(int):
        return hex(int)

    @staticmethod
    def int2bytes(int):
        return str(int).encode()

    @staticmethod
    def bytes2int(bytes):
        return int.from_bytes(bytes)

    @staticmethod
    def string2bytes(string):
        return bytes(string, "utf-8")

    @staticmethod
    def bytes2string(bytes):
        return str(bytes, encoding="utf-8")

    @staticmethod
    def intlist2bytes(list):
        byteArray = bytearray(list)
        hex_string = bytearray.hex(byteArray)
        return bytes.fromhex(hex_string)

    @staticmethod
    def string2intlist(string):
        hex = bytes.fromhex(string)
        send_hex = [0] * len(hex)
        for i in range(0, len(hex)):
            send_hex[i] = hex[i]
        return send_hex