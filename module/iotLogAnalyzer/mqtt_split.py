import re
import datetime
import base64
import json

from PyQt6.QtCore import QFile, QTextStream

LOG_FILE_NAME = "in_log.txt"
DECODE_FILE_NAME = "out_log.txt"


class Mqtt_Utils:
    log_dict = {}
    log_json = []

    def __init__(self):
        try:
            self.in_file = open(LOG_FILE_NAME, mode='r', encoding='utf-8')
            self.out_file = open(DECODE_FILE_NAME, mode='w', encoding='utf-8')
        except FileNotFoundError:
            print("create input file " + LOG_FILE_NAME)
            self.in_file = open(LOG_FILE_NAME, mode='w+', encoding='utf-8')

    def in_file_input(self, file_dir):
        self.__del__()

        try:
            self.in_file = open(file_dir, mode='r', encoding='utf-8')
            last_index = file_dir.rindex('/')
            out_file_dir = file_dir[:last_index] + '/out.txt'
            self.out_file = open(out_file_dir, mode='w', encoding='utf-8')

            self.in_file_dir = file_dir
            self.out_file_dir = out_file_dir
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

    def prase_custom_file_set(self, file_dir):
        self.utils.in_file_input(file_dir)

    def prase_general_info(self, i_head, i_info):
        self.utils.output_to_file(str(i_head) + str(i_info))

    def prase_status_info(self, i_info):
        if "onOff" in i_info:
            self.utils.output_to_file("onoff:" + str(i_info["onOff"]))

    def prase_timestamp_info(self, timestamp):
        self.utils.output_to_file('UTC:  ' + str(timestamp))
        # 当地的时间戳
        self.utils.output_to_file('Now:  ' + str(datetime.datetime.fromtimestamp(timestamp / 1000)))

    def prase_BLE_decode(self, info):
        for i in info:
            base64_data = base64.b64decode(i)
            self.prase_general_info("", self.utils.format_hex(base64_data))

    def prase_json_info(self):
        try:
            self.log_dev_json = json.loads(str(self.log_json))
        except:
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
            self.utils.renew_log(new_string)

    def run_prase(self):
        file_all_lines = Mqtt_Prase.utils.in_file.readlines()
        for file_line in file_all_lines:
            Mqtt_Prase.prase_data_line_split_handle(self, file_line)
            Mqtt_Prase.prase_json_info(self)