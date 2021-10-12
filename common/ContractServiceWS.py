#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/10/11
# @Author  : YuHuiQing

from common.util import sub,api_key_sub
from config.conf import WSURL,ACCESS_KEY,SECRET_KEY
import uuid




class WebsocketSevice:

    def __init__(self,url,access_key,secret_key):
        self.__url = url
        self.__access_key = access_key
        self.__secret_key = secret_key

    #【WS通用请求】
    def contract_sub(self,subs):
        path = '/ws'
        url = self.__url + path
        return sub(url,subs)

    # 【WS鉴权请求】
    def contract_sub_auth(self, subs):
        path = '/ws'
        url = self.__url + path
        return api_key_sub(url,self.__access_key,self.__secret_key,subs)

    # 【通用】订阅 KLine 数据
    def contract_sub_kline(self,contract_code,period):
        subs = {
                "sub": "market.{}.kline.{}".format(contract_code,period),
                "id": "id1"
            }
        path = '/ws'
        url = self.__url + path
        return sub(url,subs)

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




t = WebsocketSevice(WSURL,ACCESS_KEY,SECRET_KEY)