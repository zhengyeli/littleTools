import ctypes
import json
import re
import sys
import traceback
import urllib
from datetime import datetime
from time import sleep

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QWidget, QFileDialog
from numpy import unicode_

from module.ota.httpSimpleServer import httpServerBaseOnSocket
from module.ota.otaWidget import Ui_OtaWidget
from sdk_src.utils import utils

hostFilePath = "C:/Windows/System32/drivers/etc/hosts"
ServerHost = "factory-app.govee.com"
ServerIp = "192.168.137.1"
serverPort = 80

otaFilePath = "./ota.bin"

win = None


def goveeDev_httpServer_recvPost_handle(new_socket, request):
    # new_socket.recvfrom(1024) 返回元组，但第二项不知为什么为一串零
    body = utils.bytes2string(new_socket.recvfrom(1024)[0])

    if 'Content-Length' in request:  # 有主体内容
        if 'wifiVersionSoft' in body:  # OTA查询请求
            win.ui.pte_clientInfo.appendPlainText("govee设备查询升级...")

            if utils.fileIsExists(otaFilePath):
                not_need_update = False
            else:
                not_need_update = True

            if not_need_update:
                reply = '{"data":{"dst":{"deviceDst":[],"timezoneID":"","sync":0}},"checkVersion":{"sku":"",' \
                        '"versionHard":"",' \
                        '"versionSoft":"","needUpdate":false,"downloadUrl":"","md5":"","size":0,"time":27789835},' \
                        '"message":"success","status":200}'
                win.ui.pte_serderInfo.appendPlainText("不可升级")
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

                win.ui.pte_serderInfo.appendPlainText("可升级")

            try:
                new_socket.send(govee_httpServerResponse(reply))
            except:
                print("unKnow error")

    elif "gateway" in request:
        win.ui.pte_clientInfo.appendPlainText("请求网关信息")

    elif 'Connection: close' in request:  # 关闭链接请求
        win.ui.pte_clientInfo.appendPlainText("请求关闭连接")
        win.ui.pte_serderInfo.appendPlainText("关闭连接 ok")

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


def goveeDev_httpServer_recvGet_handle(new_socket, request):
    request_header_lines = request.splitlines()
    ret = re.match(r'[^/]+(/[^ ]*)', request_header_lines[0])
    path_name = "/"

    if ret:
        path = ret.group(1)  # 取出请求中的路径名
        path_name = urllib.parse.unquote(path)  # 浏览器请求的路径中带有中文，会被自动编码，需要先解码成中文，才能找到后台中对应的html文件

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
        win.ui.pte_serderInfo.appendPlainText("没有找到ota文件 ：" + file_name)
        new_socket.send(response.encode("utf-8"))
    else:
        win.ui.pte_serderInfo.appendPlainText("准备升级")
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
        PerPackSize = 1432
        packSendedSize = 0
        response = response.format(fileSize - 1, fileSize, fileSize)
        # new_socket.send(response)
        # response += "\r\n"
        new_socket.send(response.encode("utf-8"))
        win.ui.pte_serderInfo.appendPlainText("升级中...")
        while True:
            try:
                data = f.read(PerPackSize)
            except:
                continue
            if data:
                sleep(0.2)
                packSendedSize += PerPackSize
                win.ui.progressBar.setValue(int(packSendedSize / fileSize * 100))
                # data += '\r\n'.encode("utf-8")
                try:
                    new_socket.send(data)
                except:
                    win.ui.pte_serderInfo.appendPlainText("升级中断！！！")
                    f.close()
                    return
            else:
                break
        win.ui.pte_serderInfo.appendPlainText("升级ok~")
        print(f'文件发送成功！')
        f.close()
        new_socket.close()
        # new_socket.send()
    # 关闭套接字
    # new_socket.close()


class otaWindow():
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
        global handler
        handler = self.ui.progressBar

        # 创建服务器
        self.httpServer = httpServerBaseOnSocket()
        # 注册回调
        self.httpServer.methodRegister(goveeDev_httpServer_recvPost_handle, None, None, goveeDev_httpServer_recvGet_handle)
        # 关闭主线程 同时关闭 子线程
        self.httpServer.__setattr__("daemon", True)
        # 创建线程 线程可以共享一个全局变量
        # self.httpServerProcess = threading.Thread(target=self.httpServer.httpServerStart, args=(ServerIp, serverPort))

        # 进程无法共享一个全局变量，需要其他手段进行进程间通信 self.httpServerProcess = multiprocessing.Process(
        # target=httpServer.httpServerStart, args=(ServerIp, serverPort))
        self.init()
        global win
        win = self

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
            self.httpServer.stop()
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
                    self.ui.pte_serderInfo.appendPlainText("需要获取管理权限！！！")
                    # ide下无法生效，处于非ide下时需要手动退出
                    # try:
                    #     exit(0)
                    # except:
                    #     sys.exit()
            self.httpServer.configSet(ServerIp, serverPort)
            try:
                self.httpServer.start()
            except RuntimeError:
                print(str(traceback.format_exc()))
                try:
                    self.httpServer.reStart()
                except:
                    self.ui.pte_serderInfo.appendPlainText("无效的ip")

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
            except:
                print("stop error?")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Window = QtWidgets.QWidget()
    win = otaWindow(Window)
    Window.show()
    sys.exit(app.exec())
