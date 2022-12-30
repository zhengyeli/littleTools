import re

import numpy
import numpy as np
from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout

from sdk_src.utils import utils

DistanceFilterMaxIndex = 8
calculacy = 0.5

BlockFilter_Max = 8
BlockFilter_MaxTimes = 8


class test_wave:
    def __init__(self, plot):
        self.lastState = "null"
        self.DistanceFilter = [0] * DistanceFilterMaxIndex

        self.BlockFilter_Is_Generator = False
        self.BlockFilter = [0] * BlockFilter_Max
        self.BlockFilter_Max_Average = [0] * BlockFilter_Max
        self.BlockFilter_Min_Average = [0] * BlockFilter_Max
        self.BlockFilter_CurIndex = 0
        self.BlockFilter_CurTimes = 0
        self.BlockFilter_Max = 0
        self.BlockFilter_Min = 0

        self.lastDistance = 3
        self.newDistance = 3
        self.dataReadyFlag = False
        # 静止持续次数
        self.occRxCount = 0
        self.occMaxTimes = 10

        # 距离变化次数
        self.serialInterval = 100
        self.disNotChangeCount = 0
        self.disChangeCount = 0
        self.unmannedTime = 5000 # 毫秒 无人时间
        self.mannedTime = 1000 # 毫秒 有人时间


        self.DistanceFilter_index = 0

        # self.mqtt = govee_mqtt_client()

        self.Myplot = plot

        self.widget = QWidget()
        self.widget.setMinimumWidth(800)
        self.widget.setMinimumHeight(600)
        self.layout = QGridLayout(self.widget)
        self.label = QLabel()
        font = QtGui.QFont()
        font.setPointSize(100)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label1 = QLabel()
        self.label1.setFont(font)
        self.label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label, 0, 0)
        self.layout.addWidget(self.label1, 1, 0)
        self.widget.setLayout(self.layout)
        # self.widget.show()

    def split_log(self, f_line, f_head, f_tail):
        s_head = f_line.find(f_head)
        s_tail = f_line.find(f_tail)
        if (s_head == -1) or (s_tail == -1):
            return -1
        else:
            s_head = re.split(f_head, f_line)
            s_tail = re.split(f_tail, s_head[1])
            return s_tail[0]

    def upStream_or_downStream(self, filter):
        event = " "
        if self.lastState > self.DistanceFilter[0]:
            event = "farAway"
            for i in range(0, DistanceFilterMaxIndex - 5):
                if self.DistanceFilter[i + 1] > self.DistanceFilter[i] + calculacy:
                    continue
                else:
                    event = " "
                    break
        else:
            event = "getClose"
            for i in range(0, DistanceFilterMaxIndex - 5):
                if self.DistanceFilter[i + 1] + calculacy < self.DistanceFilter[i]:
                    continue
                else:
                    event = " "
                    break

        return event

    def getClose_or_farAway_select(self, dis):
        if self.DistanceFilter_index == DistanceFilterMaxIndex:
            self.DistanceFilter_index = 0
            self.newDistance = numpy.mean(self.DistanceFilter)
            if self.newDistance - self.lastDistance > calculacy:
                self.event_triger("farAway")
            elif self.lastDistance - self.newDistance > calculacy:
                self.event_triger("getClose")
            self.lastDistance = self.newDistance
            # event = self.upStream_or_downStream(self.DistanceFilter)

        else:
            self.DistanceFilter[self.DistanceFilter_index] = dis
            self.DistanceFilter_index += 1

    # 单个区域干扰源过滤生成器
    def blockArea_filter_generator(self, dis):
        if self.BlockFilter_Is_Generator is False:
            if self.BlockFilter_CurIndex < BlockFilter_Max:
                # 存一组数据，一组8个数据
                self.BlockFilter[self.BlockFilter_CurIndex] = dis
                self.BlockFilter_CurIndex += 1
            else:
                if self.BlockFilter_CurIndex == BlockFilter_Max:
                    # 处理一组数据
                    self.BlockFilter_CurIndex = 0
                    self.BlockFilter_Max_Average[self.BlockFilter_CurTimes] = max(self.BlockFilter)
                    self.BlockFilter_Min_Average[self.BlockFilter_CurTimes] = max(self.BlockFilter)
                    self.BlockFilter_CurTimes += 1

            if self.BlockFilter_CurTimes == BlockFilter_MaxTimes:
                # 收集8组数据，提取最大值与最小值
                self.BlockFilter_Min = min(self.BlockFilter_Min_Average)
                self.BlockFilter_Max = max(self.BlockFilter_Max_Average)
                print(self.BlockFilter_Max, self.BlockFilter_Min)
                self.BlockFilter_CurTimes = 0
                self.BlockFilter_Is_Generator = True

    def xijiewei_dis_handle(self, dis):
        if self.lastDistance != dis:
            self.lastDistance = dis
            self.disChangeCount += 1
            if self.disChangeCount * self.serialInterval > self.mannedTime:
                self.disChangeCount = 0
                if self.lastState != "move":
                    self.lastState = "move"
                    print(self.lastState)
        else:
            self.disNotChangeCount += 1
            if self.disNotChangeCount * self.serialInterval > self.unmannedTime:
                self.disNotChangeCount = 0
                if self.lastState != "null":
                    self.lastState = "null"
                    print(self.lastState)

    # 硒杰微
    def xijiewei_serial_data_handle(self, string):
        disString = self.split_log(string, "dis=", '\n')
        dis = float(disString)
        if dis == -1:
            return
        self.blockArea_filter_generator(dis)

        if self.BlockFilter_Is_Generator:
            self.getClose_or_farAway_select(dis)
            if dis > self.BlockFilter_Max or dis < self.BlockFilter_Min:
                self.Myplot.update_point_plot(dis)

    def split_string(self, f_line, f_head, f_tail):
        s_head = f_line.find(f_head)
        s_tail = f_line.find(f_tail)
        if (s_head == -1) or (s_tail == -1):
            return -1
        else:
            s_head = re.split(f_head, f_line)
            s_tail = re.split(f_tail, s_head[1])
            return s_tail[0]

    # 隔空
    def gekong_serial_data_handle(self, string):
        string_lists = re.split("\r\n", string)
        for strings in string_lists:
            print(strings)
            string_list = re.split(",", strings)
            if 'BSS' in string_list[0]:
                if len(string_list) > 2:
                    if int(string_list[1]) == 1:
                        self.label.setText("有人")
                        self.label.setStyleSheet("QLabel{background-color:rgb(0,255,0);}")
                    else:
                        self.label.setText("无人")
                        self.label.setStyleSheet("QLabel{background-color:rgb(255,0,0);}")

            elif 'RPO' in string_list[0]:
                if len(string_list) > 4:
                    if float(string_list[3]) > 0.00001:
                        self.label1.setText(string_list[3])

                        self.Myplot.update_plot(float(string_list[3]))

    # 典微
    def dianwei_serial_data_handle(self, string):
        string_lists = self.split_string(string, "f4 f3 f2 f1 0b 00 02 aa", "55 00 f8 f7 f6 f5")
        hex_lists = utils.string2intlist(string_lists)
        if len(hex_lists) != 7:
            return

        if hex_lists[0] > 0:
            self.label.setText("有人")
            self.label.setStyleSheet("QLabel{background-color:rgb(0,255,0);}")
            move_dis = hex_lists[2] * 100 + hex_lists[1]
            print("动作距离：" + str(move_dis))

            stop_dis = hex_lists[5] * 256 + hex_lists[4]
            print("静止距离：" + str(stop_dis))
            self.label1.setText(str(move_dis) + '\n' + str(stop_dis))
        else:
            self.label.setText("无人")
            self.label.setStyleSheet("QLabel{background-color:rgb(255,0,0);}")

        # self.Myplot.update_plot(float(hex_lists[3]))

    def serial_data_handle(self, string):
        data_from = 3
        if data_from == 1:  # 隔空
            self.gekong_serial_data_handle(string)
        elif data_from == 2:  # 典微
            self.dianwei_serial_data_handle(string)
        elif data_from == 3:  # 杰微
            self.xijiewei_serial_data_handle(string)

    def event_triger(self, event):

        mqtt_json = " "
        # print("cur state is " + event)

        if event == "on":
            mqtt_json = "{\
                        \"msg\": {\
                            \"accountTopic\": \"GA/5a508ccad2bd3f27d35efa8cb467ef40\",\
                            \"cmd\": \"ptReal\",\
                            \"cmdVersion\": 0,\
                            \"data\": {\
                              \"command\": [\
                                \"MwEBAAAAAAAAAAAAAAAAAAAAADM=\"\
                              ]\
                            },\
                            \"transaction\": \"u_1664331120625\",\
                            \"type\": 1\
                          }\
                        }"

        elif event == "off":
            mqtt_json = "{\
                        \"msg\": {\
                            \"accountTopic\": \"GA/5a508ccad2bd3f27d35efa8cb467ef40\",\
                            \"cmd\": \"ptReal\",\
                            \"cmdVersion\": 0,\
                            \"data\": {\
                              \"command\": [\
                                \"MwEAAAAAAAAAAAAAAAAAAAAAADI=\"\
                              ]\
                            },\
                            \"transaction\": \"u_1664331120625\",\
                            \"type\": 1\
                          }\
                        }"
        elif event == "max":
            mqtt_json = "{\
                        \"msg\": {\
                            \"accountTopic\": \"GA/5a508ccad2bd3f27d35efa8cb467ef40\",\
                            \"cmd\": \"ptReal\",\
                            \"cmdVersion\": 0,\
                            \"data\": {\
                              \"command\": [\
                                \"MwUBCQAAAAAAAAAAAAAAAAAAAD4=\"\
                              ]\
                            },\
                            \"transaction\": \"u_1664331120625\",\
                            \"type\": 1\
                          }\
                        }"
        elif event == "min":
            mqtt_json = "{\
                        \"msg\": {\
                            \"accountTopic\": \"GA/5a508ccad2bd3f27d35efa8cb467ef40\",\
                            \"cmd\": \"ptReal\",\
                            \"cmdVersion\": 0,\
                            \"data\": {\
                              \"command\": [\
                                \"MwUBAQAAAAAAAAAAAAAAAAAAADY=\"\
                              ]\
                            },\
                            \"transaction\": \"u_1664331120625\",\
                            \"type\": 1\
                          }\
                        }"

        elif event == "getClose":
            mqtt_json = "{\
                        \"msg\": {\
                            \"accountTopic\": \"GA/5a508ccad2bd3f27d35efa8cb467ef40\",\
                            \"cmd\": \"ptReal\",\
                            \"cmdVersion\": 0,\
                            \"data\": {\
                              \"command\": [\
                                \"MxsBZAAA/wAAAAAAAAAAAAAAALI=\"\
                              ]\
                            },\
                            \"transaction\": \"u_1664331120625\",\
                            \"type\": 1\
                          }\
                        }"
        elif event == "farAway":
            mqtt_json = "{\
                        \"msg\": {\
                            \"accountTopic\": \"GA/5a508ccad2bd3f27d35efa8cb467ef40\",\
                            \"cmd\": \"ptReal\",\
                            \"cmdVersion\": 0,\
                            \"data\": {\
                              \"command\": [\
                                \"MxsAZAAA/wAAAAAAAAAAAAAAALM=\"\
                              ]\
                            },\
                            \"transaction\": \"u_1664331120625\",\
                            \"type\": 1\
                          }\
                        }"
        else:
            pass
        if mqtt_json != " ":
            pass
            # self.mqtt.send(mqtt_json)
