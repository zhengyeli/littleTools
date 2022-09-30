class utils:
    def bytes2hex(self, bytes):
        return bytes.hex()

    def hex2bytes(self, hex):
        return bytes.fromhex(hex)

    def hex2int(self, hex):
        return int(hex, 16)

    def int2hex(self, int):
        return hex(int)

    def int2bytes(self, int):
        return str(int).encode()

    def bytes2int(self, bytes):
        return int.from_bytes(bytes)

    def string2bytes(self, string):
        return bytes(string, "utf-8")

    def bytes2string(self, bytes):
        return str(bytes, encoding="utf-8")

    def intlist2bytes(self, list):
        byteArray = bytearray(list)
        hex_string = bytearray.hex(byteArray)
        return bytes.fromhex(hex_string)

    def string2intlist(self, string):
        hex = bytes.fromhex(string)
        send_hex = [0] * len(hex)
        for i in range(0, len(hex)):
            send_hex[i] = hex[i]
        return send_hex