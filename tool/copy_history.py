#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/9/7
# @Author  : zhangranghan


import os
import shutil
from report.root import root
from config.root import path

#此功能仅在本地有用，集成jenkins后废弃
def copy_history():

    ALLURE_REPORT = root + '/html'
    ALLURE_RESULTS = root + '/allure'
    start_path = os.path.join(ALLURE_REPORT, 'history')
    end_path = os.path.join(ALLURE_RESULTS, 'history')
    if os.path.exists(end_path):
        shutil.rmtree(end_path)
        # print("复制上一运行结果成功！")
    try:
        shutil.copytree(start_path, end_path)
    except FileNotFoundError:
        print("allure没有历史数据可复制！")

    #在allure中复制可自定义的类别json文件
    os.system('cp {}/categories.json {}/categories.json'.format(path, ALLURE_RESULTS))

if __name__ == "__main__":
    copy_history()