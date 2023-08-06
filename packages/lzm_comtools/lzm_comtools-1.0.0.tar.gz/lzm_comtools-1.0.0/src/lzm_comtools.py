# encoding: utf-8
from asyncore import read
import imp
import sys
from tabnanny import check
import serial
import time
import datetime
import logging

name = "lzm_comtools"
add = "v1.0"

print(name, add)

class lzm_comtools:
    def __init__(self, port, baud):

        # 信息
        self.get_data_flag = True
        self.real_time_data = ''

        # 串口
        self.port = port
        self.baud = int(baud)
        self.open_com = None

        # 日志
        logging.basicConfig(filename="./log/lzm_log.log", format="[%(asctime)s %(message)s]", filemode="w")
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.DEBUG)

    def get_real_time_data(self):
        return self.real_time_data

    def clear_real_time_data(self):
        self.real_time_data = ''

    def set_get_data_flag(self, flag):
        self.get_data_flag = flag

    def open(self):
        try:
            self.open_com = serial.Serial(self.port, self.baud)
        except Exception as e:
            self.log.error("Open com fail:{}/{}".format(self.port, self.baud))
            self.log.error("Exception:{}".format(e))

    def close(self):
        if self.open_com is not None and self.open_com.isOpen:
            self.open_com.close()
            self.log.info("close")

    def send_data(self, data):
        if self.open_com is None:
            self.open()
        
        success_bytes = self.open_com.write(data.encode('UTF-8'))
        self.log.info("[send_data][{}]".format(data.encode('UTF-8')))
        print("[{}]".format(datetime.datetime.now()), "[send_data][start]")
        print(data)
        print("[{}]".format(datetime.datetime.now()), "[send_data][stop]")
        return success_bytes

    def recv_data(self, over_time_s=60):
        return self.recv_key_word("", over_time_s)

    # 定制 辅助
    def recv_key_word(self, data_list, over_time_s = 10):
        """等待指定数据"""
        all_data = ''
        check_data = ''
        max_len = 0
        check_flag = True # 是否检查特定字符串
        checked_flag = False # 是否存在字符串

        if self.open_com is None:
            self.open()

        if len(data_list) == 0:
            check_flag = False
        else:
            max_len = max([len(i) for i in data_list])
        # print("max_len is [{}]".format(max_len))

        start_time = time.time()
        while True:
            end_time = time.time()
            if (end_time - start_time) < over_time_s and self.get_data_flag\
                and ((check_flag == True and checked_flag == False) or check_flag == False):

                data = self.open_com.read(self.open_com.inWaiting())

                if len(data) != 0:
                    # str_data = bytes.decode(data)
                    str_data = data.decode("UTF-8")
                    str_b_data = str(data)
                    self.log.info("[recv_data][{}]".format(str_b_data))
                    all_data = all_data + str_b_data
                    self.read_time_data = all_data

                    # 检查是否存在指定字符串
                    check_data += str_b_data
                    if( any( kw in check_data for kw in data_list ) ):
                        checked_flag = True
                    else:
                        # 只保留需要检索的size即可
                        check_data = check_data[0-max_len:]

                    # log
                    print("[{}]".format(datetime.datetime.now()), "[recv_data][start]")
                    print(str_data)
                    print("[{}]".format(datetime.datetime.now()), "[recv_data][stop]")
            else:
                self.set_get_data_flag(True)
                break
        return all_data



    # 定制 API
    ## 发送 AT 指令
    def send_qat(self, data):
        if data[-1] != '\r':
            data = data + '\r'
        self.send_data(data)

    ## 发送 AT 并等待响应后再发送 AT
    def send_qat_interactive(self, at_and_ret_list):
        at_cnt = len(at_and_ret_list)
        print("len is", at_cnt)
        for index in range(at_cnt):
            self.send_qat(at_and_ret_list[index][0])
            
            self.recv_key_word(at_and_ret_list[index][1], at_and_ret_list[index][2])

    ## 接收指定数据保存到指定文件 指定格式 指定开始字符，指定结束字符
    def recv_key_word_data_to_file(self, file, at_key_word_list, over_time_s):

        if len(at_key_word_list) < 3:
            print(len(at_key_word_list))
            return

        # if not os.path.isfile(file):
        suffix = file.split(".")[1]
        print(suffix)
        # .hex
        if suffix == "hex":
            fd = open(file, "wb")
        # .txt
        elif suffix == "txt":
            fd = open(file, "w")
        else:
            return

        self.send_qat(at_key_word_list[0])

        stop_flag = False
        start_time = time.time()
        state = 0
        max_len = 0
        check_str_data = ""
        str_data = ""
        all_bytes_data = b""
        while True:
            end_time = time.time()
            if (end_time - start_time) < over_time_s and self.get_data_flag and stop_flag == False:

                if state == 0:
                    data = self.open_com.read()
                    check_str_data += bytes.decode(data)
                    if( any( kw in check_str_data for kw in at_key_word_list[1] ) ):
                        state = 1
                        check_str_data = ""
                        data = b""
                        max_len = max([len(i) for i in at_key_word_list[2]])
                elif state == 1:
                    str_data = ""
                    data = self.open_com.read(self.open_com.inWaiting())
                    # data = self.open_com.read()
                    all_bytes_data += data
                    try:
                        # str_data = bytes.decode(data)
                        str_data = data.decode("UTF-8")
                    except:
                        str_data = "hex"
                        # print("hex")
                    check_str_data += str_data
                    if( any( kw in check_str_data for kw in at_key_word_list[2] ) ):
                        state = 2

                    if suffix == "hex":
                        fd.write(data)
                    elif suffix == "txt":
                        fd.write(str_data)

                    check_str_data = check_str_data[0-max_len:]
                
                else:
                    self.set_get_data_flag(True)
                    break

            else:
                self.set_get_data_flag(True)
                break