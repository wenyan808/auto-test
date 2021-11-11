#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/10 7:45 下午
# @Author  : yuhuiqing
import time

def retryUtil(func, *args):
    tryTimes = 1
    while True:
        func_info = func(args[0])
        if args[1] in func_info:
            break
        else:
            # 超过5次，跳过循环
            if tryTimes > 5:
                break
            else:
                tryTimes = tryTimes + 1
                time.sleep(1)
                print('未返回预期数据，等待1秒，第', tryTimes, '次重试………………')
    return func_info