import ctypes
import hashlib
import os
import shutil


class utils:
    @staticmethod
    def bytes2hexString(bytesData):
        return bytes.hex(bytesData, ' ')

    @staticmethod
    def stringHex2bytes(stringHex):
        return bytes.fromhex(stringHex)

    @staticmethod
    def hex2int(Hex: str):
        return int(Hex, 16)

    @staticmethod
    def int2hex(int):
        return hex(int)

    @staticmethod
    def int2bytes(inter: int, length=1):
        return inter.to_bytes(length, 'big')

    @staticmethod
    def bytes2int(byte):
        return int.from_bytes(byte, 'big')

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
    def bytearray2hexString(byteArray: bytearray):
        """底下byteArray是原始数据，该函数只是为了输出看起来更加清晰"""
        hexString = ' '.join(hex(x) for x in byteArray)
        return hexString

    @staticmethod
    def string2intlist(string):
        hex = bytes.fromhex(string)
        send_hex = [0] * len(hex)
        for i in range(0, len(hex)):
            send_hex[i] = hex[i]
        return send_hex

    @staticmethod
    def intlist2hexString(intList):
        string = bytes(intList).hex()
        return string

    @staticmethod
    def fileMd5(filePath):
        with open(filePath, 'rb') as fd:
            md5obj = hashlib.md5()
            md5obj.update(fd.read())
            return md5obj.hexdigest()

    @staticmethod
    def fileSize(filePath):
        return os.path.getsize(filePath)

    @staticmethod
    def mycopyfile(srcfile, dstpath):  # 复制函数
        if not os.path.isfile(srcfile):
            print("%s not exist!" % (srcfile))
        else:
            fpath, fname = os.path.split(srcfile)  # 分离文件名和路径
            if not os.path.exists(dstpath):
                os.makedirs(dstpath)  # 创建路径
            shutil.copy(srcfile, dstpath + fname)  # 复制文件
            print("copy %s -> %s" % (srcfile, dstpath + fname))

    @staticmethod
    def fileIsExists(srcfileName):  # 复制并重命名函数
        return os.path.exists(srcfileName)

    @staticmethod
    def mycopyfileChangeName(srcfileName, dstpathName):  # 复制并重命名函数
        if not os.path.isfile(srcfileName):
            print("%s not exist!" % (srcfileName))
        else:
            fpath, fname = os.path.split(srcfileName)  # 分离文件名和路径
            dfpath, dfname = os.path.split(dstpathName)  # 分离文件名和路径
            if not os.path.exists(dfpath):
                os.makedirs(dfpath)  # 创建路径
            shutil.copy(srcfileName, dfname)  # 复制文件
            print("copy %s -> %s" % (srcfileName, dfname))
            # shutil.move(srcfileName, dstpathName)

    @staticmethod
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
