#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/10 7:45 下午
# @Author  : yuhuiqing
import time

def retryUtil(func, *args):
    tryTimes = 1
    flag = True

    while True:
        func_info = func(args[0])
        if isinstance(args[1], str):
            flag = args[1] in func_info
        elif isinstance(args[1],list) and len(args[1]) == 2:
            flag = args[1][1] in func_info[args[1][0]] and func_info[args[1][0]][args[1][1]] is not None
        elif isinstance(args[1],list) and len(args[1]) == 3:
            flag = args[1][2] in func_info[args[1][0]][args[1][1]] and func_info[args[1][0]][args[1][1]][args[1][2]] is not None

        if flag:
            break
        else:
            # 超过5次，跳过循环
            if tryTimes >= 5:
                break
            else:
                print('未返回预期数据，等待1秒，第', tryTimes, '次重试………………')
                tryTimes = tryTimes + 1
                time.sleep(1)
    return func_info
