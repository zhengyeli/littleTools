import base64
import datetime
import json
import os
import re
import chardet


LOG_FILE_PATH = "module/iotLogAnalyzer"
LOG_FILE_NAME = "in_log.txt"
DECODE_FILE_NAME = "out_log.txt"

# 来源解释
cmd_from = {
    "u": "安卓(app4.2及以上) 读取或操作",
    "v": "苹果(app4.2及以上) 读取或操作",
    "x": "安卓status查询消息（app4.2及以上）",
    "y": "苹果status查询消息（app4.2及以上）",
    "f": "alexa",
    "g": "google",
    "h": "ifttt",
    "i": "昼夜节律,联动（未来这俩种也会区分开）",
    "1": "govee定时开关",
    "o": "开放api",
    "s": "siri",
    "e": "测服自动化压测",
    "c": "govee home云端特殊控制（H5151）",
    "no": "其它(可能旧app（包括查询消息）响应，旧版本设备的本地与蓝牙控制，和上线后的status消息)",
    "old": "部分旧设备旧固件上报(写死的transaction)",
    "Govee": "部分旧设备旧固件上报(Govee开头的transaction)",
    "oldA": "[~]物理断电上电控制次数（如果有旧版本，就还包括旧设备的'[~]设备本地控制...+ iot重连上报消息'）",
    "a": "[~]设备本地控制（蓝牙或物理）+ 设备网络不稳定iot重连后也会上报该消息（未来新通用固件计划把这部分过滤掉）",
    "k": "ios小组件",
    "j": "联动",
}

# stc 来源解释
stc_from = [
    "MQTT_SOURCE_FROM_EVENTS",
    "MQTT_SOURCE_FROM_MQTT_CONNECT",
    "MQTT_SOURCE_FROM_MQTT_RECONNECT",
    "MQTT_SOURCE_FROM_MASTER_MCU",
    "MQTT_SOURCE_FROM_MASTER_MCU_BUTTON",
    "MQTT_SOURCE_FROM_LOCAL_TIMER",
    "MQTT_SOURCE_FROM_BLE",
    "MQTT_SOURCE_FROM_IOT",
    "MQTT_SOURCE_FROM_UNKNOWN",
    "MQTT_SOURCE_FROM_TEST",
    "MQTT_SOURCE_FROM_ANDROID",
    "MQTT_SOURCE_FROM_IPHONE",
    "MQTT_SOURCE_FROM_AUTO_TEST",
    "MQTT_SOURCE_FROM_ALEXA",
    "MQTT_SOURCE_FROM_GOOGLE",
    "MQTT_SOURCE_FROM_IFTTT",
    "MQTT_SOURCE_FROM_SIRI",
    "MQTT_SOURCE_FROM_OPENAPI",
    "MQTT_SOURCE_FROM_SERVER_TIMER",
    "MQTT_SOURCE_FROM_SERVER_READ",
]


class Mqtt_Utils:
    log_dict = {}
    log_json = []
    out_file_dir = None
    in_file_dir = None
    allLine = None

    def __init__(self):

        if os.path.exists(LOG_FILE_PATH) is False:
            os.makedirs(LOG_FILE_PATH)
        try:
            file = open(LOG_FILE_PATH + '/' + LOG_FILE_NAME, 'rb')
            # print(chardet.detect(file.read())['encoding'])
            # 尝试获取文本的编码格式
            encodingType = chardet.detect(file.read())['encoding']
            file.close()
            self.in_file = open(LOG_FILE_PATH + '/' + LOG_FILE_NAME, mode='r', encoding=encodingType)
            self.out_file = open(LOG_FILE_PATH + '/' + DECODE_FILE_NAME, mode='w', encoding='utf-8')
        except FileNotFoundError:
            print("create input file " + LOG_FILE_PATH + '/' + LOG_FILE_NAME)
            self.in_file = open(LOG_FILE_PATH + '/' + LOG_FILE_NAME, mode='w+', encoding='utf-8')

        try:
            self.allLine = self.in_file.readlines()
        except UnicodeDecodeError:
            self.__del__()
            self.in_file = open(LOG_FILE_PATH + '/' + LOG_FILE_NAME, mode='r', encoding='ansi')
            self.out_file = open(LOG_FILE_PATH + '/' + DECODE_FILE_NAME, mode='w', encoding='utf-8')

    def in_file_input(self, file_dir):
        self.__del__()
        file = open(file_dir, 'rb')
        # print(chardet.detect(file.read())['encoding'])
        # 尝试获取文本的编码格式
        encodingType = chardet.detect(file.read())['encoding']
        file.close()
        try:
            self.in_file = open(file_dir, mode='r', encoding=encodingType)
            last_index = file_dir.rindex('/')
            out_file_dir = file_dir[:last_index] + '/out.txt'
            self.out_file = open(out_file_dir, mode='w', encoding='utf-8')

            self.in_file_dir = file_dir
            self.out_file_dir = out_file_dir

            self.allLine = self.in_file.readlines()
        except FileNotFoundError:
            print("create input file " + LOG_FILE_NAME)
            self.in_file = open(file_dir, mode='w+', encoding='utf-8')

    def __del__(self):
        try:
            self.in_file.close()
            self.out_file.close()
        except Exception as err_info:
            print(err_info)

    # 输出到文件
    def output_to_file(self, data):
        self.out_file.write(data)
        self.out_file.write("\n")

    # hex 输出
    @staticmethod
    def format_hex(data):
        output_str = ""
        for byte_data in data:
            output_str += ("{:02x} ".format(byte_data))
        return output_str

    #
    def insert_str(self, source_str, insert_str, pos):
        return source_str[:pos] + insert_str + source_str[pos:]

    # mac 地址预处理
    def format_mac(self, in_str):
        # 处理mac地址格式，后面好做解析
        mac_addr = re.search(r'([a-f0-9]{2}:){7}[a-f0-9]{2}', in_str, re.I)
        if None != mac_addr:
            new_str = self.insert_str(in_str, '\"', mac_addr.span()[0])
            new_str = self.insert_str(new_str, '\"', mac_addr.span()[1] + 1)
            return new_str
        else:
            return in_str

    #
    def split_log(self, f_line, f_head, f_tail):
        s_head = f_line.find(f_head)
        s_tail = f_line.find(f_tail)
        if (s_head == -1) or (s_tail == -1):
            return -1
        else:
            s_head = re.split(f_head, f_line)
            s_tail = re.split(f_tail, s_head[1])
            return s_tail[0]

    def remove_log(self, in_str, range_red, range_green):
        range_r = in_str.find(range_red)
        range_g = in_str.find(range_green)
        if (range_r != -1) and (range_g != -1):
            return in_str[:range_r] + in_str[range_g:]
        else:
            return None

    def renew_log(self, str_info):
        list1 = []
        str_info = str_info.replace('{', ' ')
        str_info = str_info.replace('}', ' ')
        str_info = str_info.split('\",')
        for l in str_info:
            b = []
            a = l.strip().split('\":')
            for i in a:
                b.append(i.strip("\""))
            list1.append(b)

        for d in list1:
            self.log_dict[d[0]] = d[1]


class Mqtt_Prase:
    utils = Mqtt_Utils()
    allLine = utils.allLine
    sku = "H7160"

    def __init__(self):
        self.log_json = None
        self.log_dev_json = None

    def prase_custom_file_set(self, file_dir):
        self.utils.in_file_input(file_dir)
        self.allLine = self.utils.allLine

    def prase_general_info(self, i_head, i_info):
        self.utils.output_to_file(str(i_head) + str(i_info))

    def prase_status_info(self, i_info):
        if "onOff" in i_info:
            self.utils.output_to_file("onoff:" + str(i_info["onOff"]))

        if "sta" in i_info:
            stc_info = i_info["sta"]
            if "stc" in stc_info:
                stc_info_dict = stc_info["stc"]
                self.utils.output_to_file("stc:" + stc_info_dict)

    def prase_timestamp_info(self, timestamp):
        self.utils.output_to_file('UTC:' + str(timestamp))
        # 当地的时间戳
        self.utils.output_to_file('Now:' + str(datetime.datetime.fromtimestamp(timestamp / 1000)))

    def prase_BLE_decode(self, info):
        for i in info:
            base64_data = base64.b64decode(i)
            self.prase_general_info("", self.utils.format_hex(base64_data))
            if base64_data[1] == 0x10:
                if "717" in self.sku:
                    temper = base64_data[3] << 8 | base64_data[4]
                    self.utils.output_to_file('temper:' + str(temper) + "F")
                else:
                    humi = base64_data[3] << 16 | base64_data[4] << 8 | base64_data[5]
                    self.utils.output_to_file("ht: " + str(humi))

    def prase_json_info(self):
        if self.log_json is None:
            print("self.log_json is NONE")
            return
        try:
            self.log_dev_json = json.loads(str(self.log_json))
        except:
            return

        if self.log_dev_json == -1:
            return

        if 'warn' in self.log_dev_json:
            self.prase_general_info("warn:", self.log_dev_json['warn'])

        if 'type' in self.log_dev_json:
            self.prase_general_info("type:", self.log_dev_json['type'])

        if 'op' in self.log_dev_json:
            self.prase_BLE_decode(self.log_dev_json['op']['command'])

        if 'state' in self.log_dev_json:
            self.prase_status_info(self.log_dev_json['state'])

        if 'timestamp' in self.log_dev_json:
            self.prase_timestamp_info(self.log_dev_json['timestamp'])

    def prase_data_line_split_handle(self, file_line):
        if -1 != file_line.find("bizType"):
            self.log_json = self.utils.split_log(file_line, "\"message\":\"", "\",\"@timestamp")
            new_string = self.utils.format_mac(file_line)
            new_string = self.utils.remove_log(new_string, "\"message\":\"", "\"@timestamp")
            if new_string is not None:
                self.utils.renew_log(new_string)

    def prase_data_from_split_handle(self, file_line):
        if -1 != file_line.find("bizType"):
            data_from = self.utils.split_log(file_line, "\"from\":\"", "\",\"transaction")
            if data_from != -1:
                self.prase_general_info("from:\"" + data_from + "\":", cmd_from[data_from])

    def prase_data_cmd_split_handle(self, file_line):
        if -1 != file_line.find("bizType"):
            data_cmd = self.utils.split_log(file_line, "\"cmd\":\"", "\",\"from")
            if data_cmd != -1:
                self.utils.output_to_file("cmd:\"" + data_cmd + "\"")

    def prase_data_stc_split_handle(self, file_line):
        if -1 != file_line.find("bizType"):
            data_from = self.utils.split_log(file_line, "\"from\":\"", "\",\"transaction")
            if data_from != -1:
                self.prase_general_info("from:\"" + data_from + "\":", cmd_from['x'])

    def prase_data_sku_split_handle(self, file_line):
        if -1 != file_line.find("bizType"):
            sku = self.utils.split_log(file_line, "\"sku\":\"", "\",\"cmd")
            if sku != -1:
                self.sku = sku

    def run_prase(self):
        for file_line in self.allLine:
            if -1 != file_line.find("bizType"):
                Mqtt_Prase.prase_data_sku_split_handle(self, file_line)
                Mqtt_Prase.prase_data_from_split_handle(self, file_line)  # from
                Mqtt_Prase.prase_data_cmd_split_handle(self, file_line)  # cmd
                Mqtt_Prase.prase_data_line_split_handle(self, file_line)  # 截取message数据
                Mqtt_Prase.prase_json_info(self)  # 解析message数据
                self.utils.output_to_file("\n")
            else:
                pass
                # self.utils.out_file.write('Server time:' + file_line)
