import ctypes
import json
import queue
import re
import sys
import threading
import traceback
import urllib
from datetime import datetime
from time import sleep

from PyQt6 import QtWidgets
from PyQt6.QtCore import QTimer, QObject
from PyQt6.QtWidgets import QWidget, QFileDialog
from numpy import unicode_


from module.ota.httpSimpleServer import httpServerBaseOnSocket
from module.ota.otaWidget import Ui_OtaWidget
from sdk_src.utils import utils

hostFilePath = "C:/Windows/System32/drivers/etc/hosts"
ServerHost = "factory-app.govee.com"
ServerIp = "192.168.137.1"
otaFilePath = "./ota.bin"
serverPort = 80

win = None    # 主线程类
setValue = 0  # 进度条值
bq = queue.Queue(maxsize=5)
# lock = threading.Lock()
lock = threading.RLock()


def goveeDev_ota_process_threading(socket, fileData: bytes, fileSize: int):
    print("start ok")
    win.ui.pte_serderInfo.append("{}升级中...".format(threading.currentThread().name))
    PerPackSize = 1432
    packSendedSize = 0
    packSendedIndex = 0
    while True:
        try:
            start = packSendedIndex * PerPackSize
            stop = (packSendedIndex + 1) * PerPackSize
            if stop > fileSize:
                stop = fileSize
            # print("{} {}".format(start, stop))
            data = fileData[start: stop]
        except:
            win.ui.pte_serderInfo.append("out of data")
            break
        if data:
            sleep(0.2)
            packSendedSize += PerPackSize
            global setValue
            setValue = int(packSendedSize / fileSize * 100)
            try:
                bq.put(setValue, True, timeout=1)
            except queue.Full:
                win.ui.pte_serderInfo.append("queue put timeout")
            try:
                socket.send(data)
                packSendedIndex += 1
            except:
                win.ui.pte_serderInfo.append("{}升级中断！！！".format(threading.currentThread().name))
                if socket is not None:
                    socket.close()
                return
        else:
            print("all sended")
            break

    if socket is not None:
        socket.close()
    else:
        print("socket is None")
    win.ui.pte_serderInfo.append("{}升级成功！！！".format(threading.currentThread().name))


def goveeDev_httpServer_recvPost_handle(new_socket, request):
    # new_socket.recvfrom(1024) 返回元组，但第二项不知为什么为一串零
    body = utils.bytes2string(new_socket.recvfrom(1024)[0])

    if 'Content-Length' in request:  # 有主体内容
        if 'wifiVersionSoft' in body:  # OTA查询请求
            win.ui.pte_clientInfo.append("govee设备查询升级...")

            if utils.fileIsExists(otaFilePath):
                not_need_update = False
            else:
                not_need_update = True

            if not_need_update:
                reply = '{"data":{"dst":{"deviceDst":[],"timezoneID":"","sync":0}},"checkVersion":{"sku":"",' \
                        '"versionHard":"",' \
                        '"versionSoft":"","needUpdate":false,"downloadUrl":"","md5":"","size":0,"time":27789835},' \
                        '"message":"success","status":200}'
                win.ui.pte_serderInfo.append("不可升级")
            else:
                dist = {"data": {"dst": {"deviceDst": [], "timezoneID": "", "sync": 0}},
                        "checkVersion": {"sku": "", "versionHard": "", "versionSoft": "", "needUpdate": "true",
                                         "downloadUrl": "", "md5": "", "size": 0, "time": 27789835},
                        "message": "success", "status": 200}
                # print(json.dumps(dist))
                dist['checkVersion']['versionSoft'] = 'V1.00.99'
                dist['checkVersion']['downloadUrl'] = "http://" + ServerHost + '/ota.bin'
                dist['checkVersion']['md5'] = str(utils.fileMd5("./ota.bin")[8:24])
                dist['checkVersion']['size'] = utils.fileSize("./ota.bin")
                reply = json.dumps(dist, sort_keys=True, indent=2)
                # 美化打印
                # print(reply.encode('utf-8').decode('unicode_escape'))

                win.ui.pte_serderInfo.append("可升级")

            try:
                new_socket.send(govee_httpServerResponse(reply))
            except:
                print("unKnow error")

    elif "gateway" in request:
        win.ui.pte_clientInfo.append("请求网关信息")

    elif 'Connection: close' in request:  # 关闭链接请求
        win.ui.pte_clientInfo.append("请求关闭连接")
        win.ui.pte_serderInfo.append("关闭连接 ok")

    try:
        new_socket.close()
    except:
        print("close socket {}".format(new_socket))


def govee_httpServerResponse(context: str):
    buf = 'HTTP/1.1 200 OK\r\n'  # 版本
    buf += 'Server: haha\r\n'
    buf += 'Connection: keep-alive\r\n'
    GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
    buf += 'Date: {}\r\n'.format(datetime.utcnow().strftime(GMT_FORMAT))
    buf += 'Content-Type: application/json; charset=utf-8\r\n'
    buf += 'Vary: Vary: Origin\r\n'
    buf += 'Access-Control-Allow-Origin: *\r\n'
    buf += 'X-RTime: 301ms\r\n'
    buf += 'X-traceId: 871e2580-5b29-11ed-b65a-fdfea871e272\r\n'
    buf += 'Content-Length: {}\r\n'.format(len(context))
    buf += '\r\n'
    buf += context
    return utils.string2bytes(buf)


# get 请求回复
def httpServer_recvGet_handle(new_socket, request):
    request_header_lines = request.splitlines()
    ret = re.match(r'[^/]+(/[^ ]*)', request_header_lines[0])
    print(request_header_lines[0])

    if ret:
        path = ret.group(1)  # 取出请求中的路径名
        path_name = urllib.parse.unquote(path)  # 浏览器请求的路径中带有中文，会被自动编码，需要先解码成中文，才能找到后台中对应的html文件
        if path_name == '/':
            httpServer_recvGet_fileResponse(new_socket, "./index.html")
        elif path_name == "/ota.bin":
            # Govee Ota 文件请求
            win.ui.pte_clientInfo.append("govee设备请求升级...")
            goveeDev_httpServer_recvGet_handle(new_socket, request)
        else:
            httpServer_recvGet_fileResponse(new_socket, path_name)

    else:
        print("match no file")


# 返回 对应文件
def httpServer_recvGet_fileResponse(socket, filePath):
    # 返回http格式的数据给浏览器
    file_name = './' + filePath
    print("处理请求：{}".format(file_name))
    try:
        f = open(file_name, 'rb+')
    except FileNotFoundError:
        response = "HTTP/1.1 404 NOT FOUND\r\n"
        response += "\r\n"
        response += "------file not found------"
        win.ui.pte_serderInfo.append("没有找到文件 ：" + file_name)
        socket.send(response.encode("utf-8"))
    else:
        win.ui.pte_serderInfo.append("找到文件 ：" + file_name)
        packSendSize = 1483
        try:
            data = f.read(packSendSize)
            if data:
                sleep(0.02)
                try:
                    socket.send(data)
                except:
                    win.ui.pte_serderInfo.append("发送中断！")
                    f.close()
                    socket.close()
                    return
            else:
                win.ui.pte_serderInfo.append("文件已读取完...")
                f.close()
                socket.close()
                return
        except:
            win.ui.pte_serderInfo.append("unknow error ...")

        f.close()
    socket.close()


def goveeDev_httpServer_recvGet_handle(new_socket, request):
    request_header_lines = request.splitlines()
    ret = re.match(r'[^/]+(/[^ ]*)', request_header_lines[0])

    path_name = "/"

    if ret:
        path = ret.group(1)  # 取出请求中的路径名
        path_name = urllib.parse.unquote(path)  # 浏览器请求的路径中带有中文，会被自动编码，需要先解码成中文，才能找到后台中对应的html文件
    else:
        print("request default file")

    if path_name == "/":  # 用户请求/时，返回index.html页面
        path_name = "/ota.bin"

    # 2.返回http格式的数据给浏览器
    file_name = '.' + path_name
    print("处理请求：{}".format(file_name))
    try:
        f = open(file_name, 'rb+')
    except FileNotFoundError:
        response = "HTTP/1.1 404 NOT FOUND\r\n"
        response += "\r\n"
        response += "------file not found------"
        win.ui.pte_serderInfo.append("没有找到ota文件 ：" + file_name)
        new_socket.send(response.encode("utf-8"))
    else:
        win.ui.pte_serderInfo.append("准备升级")
        # 准备发给浏览器的数据 -- header
        response = 'HTTP/1.1 206 Partial Content\r\n' \
                   'x-amz-id-2: pq+rGR3RE2fW0OqFmokwOBEurVLFckv8l9QLjwk1CkCcSWYHJBWEZnXDtOfBbOHcPomH6OdWDyk=\r\n' \
                   'x-amz-request-id: MXNDA8RED8NQC2G3\r\n' \
                   'Date: Thu, 03 Nov 2022 11:32:27 GMT\r\n' \
                   'Last-Modified: Thu, 22 Sep 2022 06:14:27 GMT\r\n' \
                   'ETag: "bf66b46ad03d7c23b48f7b6817063a3c"\r\n' \
                   'x-amz-version-id: ACDrL3bmSfGJOfv5iH14xwH6A76QLt0h\r\nAccept-Ranges: bytes\r\n' \
                   'Content-Range: bytes 0-{0}/{1}\r\n' \
                   'Content-Type: application/octet-stream\r\n' \
                   'Server: AmazonS3\r\n' \
                   'Content-Length: {2}\r\n\r\n'
        fileSize = utils.fileSize("./ota.bin")
        response = response.format(fileSize - 1, fileSize, fileSize)
        # new_socket.send(response)
        # response += "\r\n"
        new_socket.send(response.encode("utf-8"))
        fileData = f.read()
        f.close()
        t = threading.Thread(target=goveeDev_ota_process_threading, args=(new_socket, fileData, fileSize))
        t.setDaemon(True)
        t.start()
        print("start threading")


class otaWindow(QObject):
    def __init__(self, widget):
        super().__init__()

        self.widget = widget
        self.fileData = None
        self.ui = Ui_OtaWidget()

        if widget is None:
            self.widget = QWidget()
            self.widget.show()

        self.ui.setupUi(self.widget)
        self.httpServerProcess = None

        if utils.is_admin():
            self.widget.setWindowTitle(self.widget.windowTitle() + "(管理者)")

        # 创建服务器
        self.httpServer = httpServerBaseOnSocket()
        # 注册回调
        self.httpServer.methodRegister(goveeDev_httpServer_recvPost_handle, None, None, httpServer_recvGet_handle)
        # 关闭主线程 同时关闭 子线程
        self.httpServer.setDaemon(True)
        # 创建线程 线程可以共享一个全局变量
        # self.httpServerProcess = threading.Thread(target=self.httpServer.httpServerStart, args=(ServerIp, serverPort))

        # 进程无法共享一个全局变量，需要其他手段进行进程间通信 self.httpServerProcess = multiprocessing.Process(
        # target=httpServer.httpServerStart, args=(ServerIp, serverPort))
        self.init()
        global win, setValue
        win = self

        setValue = 0
        self.t = QTimer()
        self.t.timeout.connect(self.fun)

    def fun(self):
        try:
            value = bq.get(True, timeout=0)
            self.ui.progressBar.setValue(value)
        except queue.Empty:
            return

    def __del__(self):
        try:
            if self.fileData is not None:
                dnsfile = open(hostFilePath, mode='w', encoding='utf-8')
                dnsfile.write(self.fileData)
                dnsfile.close()
                self.fileData = None
        except:
            pass
        try:
            self.httpServer.close()
            self.t.stop()
        except:
            print("kill error?")

    def init(self):
        self.ui.progressBar.setRange(0, 100)
        self.ui.progressBar.setValue(0)
        self.ui.let_serverIp.setText(ServerIp)
        self.ui.let_dns.setText(ServerHost)
        self.ui.pbt_dnsSet.clicked.connect(lambda: self.dnsConfigSet())
        self.ui.pbt_otaFileLoad.clicked.connect(self.loadOtaFile)

    def loadOtaFile(self):
        widget = QWidget()
        dirInfo = QFileDialog.getOpenFileName(widget, "load file", "")
        dir = dirInfo[0]

        utils.mycopyfileChangeName(dir, otaFilePath)
        self.ui.let_otaFile.setText(dir)

    def dnsConfigSet(self):
        dns = self.ui.let_dns.text()
        text = self.ui.pbt_dnsSet.text()
        Ip = self.ui.let_serverIp.text()
        global ServerIp
        global ServerHost
        ServerHost = dns

        if Ip is not None and len(Ip) > 0:
            ServerIp = Ip
        else:
            pass

        if text == "生效":
            # 尝试打开host文件读取
            try:
                dnsfile = open(hostFilePath, mode='r', encoding='utf-8')
                self.fileData = dnsfile.read()
                dnsfile.close()
            except FileNotFoundError:
                print(hostFilePath + " not found")

            if self.fileData is not None:
                # 尝试修改host文件
                if utils.is_admin():
                    try:
                        dnsfile = open(hostFilePath, mode='w', encoding='utf-8')
                        dnsfile.write(self.fileData + '\n' + ServerIp + ' ' + dns)
                        dnsfile.close()
                        self.ui.pbt_dnsSet.setText("失效")
                    except:
                        pass
                else:
                    if sys.version_info[0] == 3:
                        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
                    else:  # in python2.x
                        ctypes.windll.shell32.ShellExecuteW(None, u"runas", unicode_(sys.executable),
                                                            unicode_(__file__), None, 1)
                    self.ui.pte_serderInfo.append("需要获取管理权限！！！")

            self.httpServer.configSet(ServerIp, serverPort)
            try:
                self.httpServer.start()
            except RuntimeError:
                print(str(traceback.format_exc()))
                try:
                    self.httpServer.reStart()
                except:
                    self.ui.pte_serderInfo.append("无效的ip")

            self.t.start(100)
            self.ui.pbt_dnsSet.setText("失效")

        elif text == "失效":
            if self.fileData is not None:
                try:
                    dnsfile = open(hostFilePath, mode='w', encoding='utf-8')
                    dnsfile.write(self.fileData)
                    dnsfile.close()
                    self.fileData = None
                except:
                    pass

            self.ui.pbt_dnsSet.setText("生效")
            try:
                # 需要关闭线程 fixme
                self.httpServer.stop()
                self.t.stop()
            except:
                print("stop error?")


# 调试使用
def function():
    global setValue
    while True:
        setValue += 1
        if setValue > 99:
            setValue = 1
        try:
            bq.put(setValue, True, timeout=1)
        except queue.Full:
            print("timeout")

        if True:
            print(threading.currentThread().name)
            win.ui.pte_serderInfo.append(threading.currentThread().name)
        else:
            print(threading.currentThread().name + " {}".format("False"))
        sleep(0.01)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Window = QtWidgets.QWidget()
    win = otaWindow(Window)
    Window.show()
    sys.exit(app.exec())
