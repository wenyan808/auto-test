#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/8/1
# @Author  : zhangranghan


import inspect
import requests
from pprint import pprint
import json
from pathlib import Path,PurePath
import pandas as pd
from testFile.__init__ import root

# 已废弃从Excel读取数据的方法
# #根据传入的接口名组装文件路径
# def file_path(api_name):
#     file_name = api_name.split('_',1)[0].capitalize()+'TestData.xlsx'
#     path = root + '/' + file_name
#     return path
#
# #读取测试数据
# def data(api_name):
#     df = pd.read_excel(file_path(api_name),sheet_name=api_name,keep_default_na=False) #使用keep_default_na=False将读取空单元格设置为''而不是nan
#     nrows,ncols = df.shape
#     test_data = []
#     for i in range(1,ncols):
#         nrows_list = []
#         for j in range(nrows):
#             value = df.iloc[j,i]
#             nrows_list.append(value)
#             print(nrows_list)
#         if len(nrows_list) > 1:
#             nrows_tuple = tuple(nrows_list)
#             test_data.append(nrows_tuple)
#         else:
#             test_data.append(nrows_list[0])
#     return test_data
#
# #读取参数名
# def param(api_name):
#     df = pd.read_excel(file_path(api_name),sheet_name=api_name)
#     nrows,ncols = df.shape
#     func_param_list = []
#     for i in range(nrows):
#         func_param_list.append(df.iloc[i,0])
#     func_param = ''
#     for i in range(len(func_param_list)):
#         func_param = func_param +','+ func_param_list[i]
#     return func_param[1:]
#
# #读取第一行数据
# def description(api_name):
#     df = pd.read_excel(file_path(api_name),sheet_name=api_name,header=None)
#     nrows,ncols = df.shape
#     description_list = []
#     for i in range(1,ncols):
#         description_list.append(df.iloc[0,i])
#     return description_list



def case_data():
    caller_frame = inspect.stack()[1]
    file_name = caller_frame.filename.split('_',1)[1][:-3]
    # file_name = caller_frame.filename
    # print(file_name)
    # name = PurePath(file_name).stem
    # print(name)
    response = requests.get('http://10.151.110.63:8000/api_case/get_api_test_data_by_case_id/?case_id=5')
    r = response.json()[0]['request']['symbol']
    return [r]



#("test_input,expected",[ ("3+5", 8),("2+4", 6),("6 * 9", 42),])


