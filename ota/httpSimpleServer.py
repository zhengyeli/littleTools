# api 1
import os
import socket
import sys
import threading
import time
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler, CGIHTTPRequestHandler


class httpServerBaseOnSocket(threading.Thread):

    def __init__(self):
        super().__init__()

        # 接收
        self.httpSocket = None
        self.recvPostMethodHandler = None
        self.recvPutMethodHandler = None
        self.recvHeadMethodHandler = None
        self.recvGetMethodHandler = None

        # 发送
        self.sendPostMethodHandler = None
        self.sendPutMethodHandler = None
        self.sendHeadMethodHandler = None
        self.sendGetMethodHandler = None

        self.NeedClose = False
        self.NeedPause = False
        self.serverPort = 80
        self.serverIp = "127.0.0.1"

    def methodRegister(self, recvPost=None, recvPut=None, recvHead=None, recvGet=None):
        self.recvPostMethodHandler = recvPost
        self.recvPutMethodHandler = recvPut
        self.recvHeadMethodHandler = recvHead
        self.recvGetMethodHandler = recvGet

    def configSet(self, ip: str, port: int):
        self.serverIp = ip
        self.serverPort = port

    def service_client(self, new_socket):
        # 为这个客户端返回数据
        # 1.接收浏览器发过来的请求，即http请求

        request = new_socket.recv(1024).decode('utf-8')
        # print(request)
        request_header_lines = request.splitlines()
        print("head :" + request_header_lines[0])

        if "POST" in request_header_lines[0]:
            self.postReceiveHandle(new_socket, request)
        elif "GET" in request_header_lines[0]:
            self.getReceiveHandle(new_socket, request)
        elif "HEAD" in request_header_lines[0]:
            self.headReceiveHandle(new_socket, request)
        elif "PUT" in request_header_lines[0]:
            self.putReceiveHandle(new_socket, request)

    def headReceiveHandle(self, new_socket, header):
        if self.recvHeadMethodHandler is not None:
            self.recvHeadMethodHandler(new_socket, header)

    def putReceiveHandle(self, new_socket, header):
        if self.recvPutMethodHandler is not None:
            self.recvPutMethodHandler(new_socket, header)

    def postReceiveHandle(self, new_socket, header):
        if self.recvPostMethodHandler is not None:
            self.recvPostMethodHandler(new_socket, header)

    def getReceiveHandle(self, new_socket, request):
        if self.recvGetMethodHandler is not None:
            self.recvGetMethodHandler(new_socket, request)

    def close(self):
        self.NeedClose = True

    def stop(self):
        self.NeedPause = True

    def open(self):
        self.NeedClose = False

    def reStart(self):
        self.NeedPause = False

    def run(self):
        self.httpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.httpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.httpSocket.bind((self.serverIp, self.serverPort))
        self.httpSocket.listen(self.serverPort)
        self.httpSocket.settimeout(1)
        print(self.httpSocket.getsockname())
        while True:
            # 4.等待新客户端的链接
            try:
                new_socket, client_addr = self.httpSocket.accept()
                print('接收来自{}:{}的请求'.format(client_addr[0], client_addr[1]))
                # 5.为这个客户端服务
                self.service_client(new_socket)
            except:
                if self.NeedClose:
                    self.httpSocket.close()
                    print("thread exit")
                    return

                while self.NeedPause:
                    time.sleep(0.1)

    def httpServerStart(self, httpServerIp="127.0.0.1", port=80):
        httpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        httpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        httpSocket.bind((httpServerIp, port))
        httpSocket.listen(port)
        httpSocket.settimeout(1)
        print(httpSocket.getsockname())
        while True:
            # 4.等待新客户端的链接
            try:
                new_socket, client_addr = httpSocket.accept()
                print('接收来自{}:{}的请求'.format(client_addr[0], client_addr[1]))
                # 5.为这个客户端服务
                self.service_client(new_socket)
            except:
                if self.NeedClose:
                    print("thread exit")
                    return


# api 2
def httpServerFileExplorer(port=80,
                           bind='127.0.0.1',
                           server_class=ThreadingHTTPServer,
                           handler_class=SimpleHTTPRequestHandler,
                           cgi=True,
                           directory=os.getcwd()):
    """http服务器文件浏览器 Run an HTTP server on port 8000 (or the port argument).

        Args:
            server_class (_type_, optional): Class of server. Defaults to DualStackServer.
            handler_class (_type_, optional): Class of handler. Defaults to SimpleHTTPRequestHandler.
            port (int, optional): Specify alternate port. Defaults to 8000.
            bind (str, optional): Specify alternate bind address. Defaults to '127.0.0.1'.
            cgi (bool, optional): Run as CGI Server. Defaults to False.
            directory (_type_, optional): Specify alternative directory. Defaults to os.getcwd().
        """
    if cgi:
        handler_class = partial(CGIHTTPRequestHandler, directory=directory)
    else:
        handler_class = partial(SimpleHTTPRequestHandler, directory=directory)

    with server_class((bind, port), handler_class) as httpd:
        print(
            f"Serving HTTP on {bind} port {port} "
            f"(http://{bind}:{port}/) ..."
        )
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            sys.exit(0)
