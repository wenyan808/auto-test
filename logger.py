#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/8/19
# @Author  : zhangranghan


import os,sys
import logging
from time import strftime
from logging.handlers import TimedRotatingFileHandler


class Logger(object):
    def __init__(self, logger_name='log'):
        self.logger = logging.getLogger(logger_name)
        logging.root.setLevel(logging.NOTSET)
        timestamp = strftime('%Y%m%d')
        self.log_file_name = 'log_%s.log' % timestamp  # 日志文件的名称
        self.backup_count = 30  # 最多存放日志的数量
        # 日志输出级别
        self.console_output_level = 'DEBUG'
        self.file_output_level = 'INFO'
        # 日志输出格式
        # self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    def get_logger(self):
        """在logger中添加日志句柄并返回，如果logger已有句柄，则直接返回"""
        if not self.logger.handlers:  # 避免重复日志
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(self.formatter)
            console_handler.setLevel(self.console_output_level)
            self.logger.addHandler(console_handler)

            PROJECT_NAME = 'Autotest'
            project_path = os.path.abspath(os.path.dirname(__file__))
            # root_path = project_path[:project_path.find("{}".format(PROJECT_NAME)) + len("{}".format(PROJECT_NAME))]
            log_path = project_path + "/log"

            # 每天重新创建一个日志文件，最多保留backup_count份
            file_handler = TimedRotatingFileHandler(filename=os.path.join(log_path, self.log_file_name), when='D',
                                                    interval=1, backupCount=self.backup_count, delay=True,
                                                    encoding='utf-8')
            file_handler.setFormatter(self.formatter)
            file_handler.setLevel(self.file_output_level)
            self.logger.addHandler(file_handler)
        return self.logger


logger = Logger().get_logger()



