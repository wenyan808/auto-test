#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/10/11
# @Author  : YuHuiQing

from common.util import sub, api_key_sub
from config.conf import WSURL, ACCESS_KEY, SECRET_KEY
import uuid


class WebsocketSevice:

    def __init__(self, url, access_key, secret_key):
        self.__url = url
        self.default_ws_path = url + '/ws'
        self.__access_key = access_key
        self.__secret_key = secret_key

    # 【通用】订阅 KLine 数据
    def contract_sub_kline(self, contract_code, period):
        subs = {
            "sub": "market.{}.kline.{}".format(contract_code, period),
            "id": "id1"
        }
        path = '/ws'
        url = self.__url + path
        return sub(url, subs)

    def contract_req_kline(self, contract_code, period, From, to):
        subs = {
            "req": "market.{}.kline.{}".format(contract_code, period),
            "from": int(From),
            "to": int(to)
        }
        return sub(self.default_ws_path, subs)

    # 【通用】订阅 Market Depth 数据
    def contract_sub_depth(self, contract_code, type):
        subs = {
            "sub": "market.{}.depth.{}".format(contract_code, type),
            "id": "id5"
        }
        path = '/ws'
        url = self.__url + path
        return sub(url, subs)

    # 【通用】买一卖一逐笔行情推送 BBO
    def contract_sub_bbo(self, contract_code):
        subs = {
            "sub": "market.{}.bbo".format(contract_code),
            "id": "id8"
        }
        path = '/ws'
        url = self.__url + path
        return sub(url, subs)


t = WebsocketSevice(WSURL, ACCESS_KEY, SECRET_KEY)
