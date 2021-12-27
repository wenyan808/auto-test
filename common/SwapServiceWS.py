#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/10/09
# @Author  : HuiQing Yu

from common.util import sub, api_key_sub
from config.conf import WSURL, ACCESS_KEY, SECRET_KEY
from config.conf import USERINFO

class WebsocketSevice:

    def __init__(self, url, access_key, secret_key):
        self.__url = url
        self.__access_key = access_key
        self.__secret_key = secret_key

    #WS市场行情
    def swap_sub(self,subs=None,keyword=None):
        path = '/swap-ws'
        url = self.__url + path
        return sub(url=url, subs=subs,keyword=keyword)

    # WS鉴权订阅，请求
    def swap_sub_auth(self, subs):
        path = '/swap-notification'
        url = self.__url + path
        return api_key_sub(url, self.__access_key, self.__secret_key, subs)

    # 订阅(sub) 指数与基差数据
    def swap_sub_index(self,subs,keyword):
        path = '/ws_index'
        url = self.__url + path
        return sub(url, subs,keyword)


t = WebsocketSevice(WSURL,ACCESS_KEY,SECRET_KEY)
userList = eval(USERINFO)
user01 = WebsocketSevice(WSURL, userList[0]['ACCESS_KEY'], userList[0]['SECRET_KEY'])
user02 = WebsocketSevice(WSURL, userList[1]['ACCESS_KEY'], userList[1]['SECRET_KEY'])
user03 = WebsocketSevice(WSURL, userList[2]['ACCESS_KEY'], userList[2]['SECRET_KEY'])