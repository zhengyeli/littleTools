import re

import numpy

from module.Mqtt.pahoMqttClient import govee_mqtt_client
from module.photograph.graphDraw import BasicArrayPlot, dynamicArrayPlot

DistanceFilterMaxIndex = 8
calculacy = 0.5
class test_wave:
    def __init__(self, plot):
        self.lastState = "null"
        self.DistanceFilter = [0] * DistanceFilterMaxIndex
        self.lastDistance = 3
        self.newDistance = 3
        self.dataReadyFlag = False
        # 静止持续次数
        self.occRxCount = 0
        self.occMaxTimes = 10

        self.DistanceFilter_index = 0

        # self.mqtt = govee_mqtt_client()

        self.Myplot = plot

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

    def serial_data_handle(self, string):
        dis = self.split_log(string, "dis=", '\n')
        if 'occ' in string:
            self.occRxCount += 1
            if self.occRxCount > self.occMaxTimes:
                if self.lastState != 'occ':
                    self.lastState = 'occ'
                    self.event_triger("min")
                elif self.lastState == 'null':
                    self.lastState = 'occ'
                    self.event_triger("on")
                else:
                    pass
            else:
                pass

        elif 'mov' in string:
            if self.lastState == 'occ':
                self.lastState = 'mov'
                self.event_triger("max")
            elif self.lastState == 'null':
                self.lastState = 'mov'
                self.event_triger("on")
            else:
                pass

            self.getClose_or_farAway_select(float(dis))

        elif 'null' in string:
            if self.lastState != 'null':
                self.lastState = 'null'
                self.event_triger("off")

        self.Myplot.update_plot(float(dis))

    def event_triger(self, event):

        mqtt_json = " "
        print("cur state is " + event)

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
