#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/9/7
# @Author  : zhangranghan

import os
from report.root import root


#此功能仅在本地有用，集成jenkins后废弃
"""用于清理allure报告历史原数据"""

def clear_allure_results():
    ALLURE_RESULTS = root + '/allure'
    var = True
    for i in os.listdir(ALLURE_RESULTS):
        new_path = os.path.join(ALLURE_RESULTS, i)
        if os.path.isfile(new_path):
            os.remove(new_path)
            # print("删除{}成功！".format(new_path))
            var = False
    if var:
        print("没有数据可清理！")


if __name__ == "__main__":
    clear_allure_results()