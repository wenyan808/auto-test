#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/8/1
# @Author  : zhangranghan


import pandas as pd
import os


name_list = []

def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            yield f


def main(module):
    base =  '../testCase/{}TestCase'.format(module)
    for i in findAllFile(base):
        if 'test_' in i and '.pyc' not in i:
            name_list.append(i)
            print(i)



    with pd.ExcelWriter('./tool/{}TestData.xlsx'.format(module)) as writer:
        for i in range(len(name_list)):
            data_sheet = pd.DataFrame({name_list[i][5:][:-3]:[]})
            data_sheet.to_excel(writer,sheet_name=name_list[i][5:][:-3],index=False)

if __name__ == '__main__':
    """
    输入模块名创建excel 交割：Contract 永续：Swap 期权：Option 正向：Linear
    创建后先确认testFile目录中是否已存在相同文件再移动，防止已有测试数据被覆盖
    """
    main('Swap')

