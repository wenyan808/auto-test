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

    # 【WS通用请求】
    def contract_sub(self, subs):
        path = '/ws'
        url = self.__url + path
        return sub(url, subs)

    # 【WS鉴权请求】
    def contract_sub_auth(self, subs):
        path = '/ws'
        url = self.__url + path
        return api_key_sub(url, self.__access_key, self.__secret_key, subs)

    # 【指数与基差接口】订阅(sub)指数K线数据
    def contract_sub_index(self, symbol, period):
        subs = {
            "sub": "market.{}.index.{}".format(symbol, period),
            "id": "id1"
        }
        path = '/ws_index'
        url = self.__url + path
        return sub(url, subs)

    # 【通用】订阅 KLine 数据
    def contract_sub_kline(self, contract_code=None, period=None):
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
            "from": From,
            "to": to
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

    def contract_req_kline(self, contract_code, period, From, to):
        subs = {
            "req": "market.{}.kline.{}".format(contract_code, period),
            "from": From,
            "to": to
        }
        path = '/ws'
        url = self.__url + path
        return sub(url, subs)

    # 【通用】订阅 Market Depth 数据
    def contract_sub_depth(self, contract_code, type):
        subs = {
            "sub": "market.{}.depth.{}".format(contract_code, type),
            "id": "id5"
        }
        path = '/ws'
        url = self.__url + path
        print(url)
        requestInfo = '\n请求信息：url=' + url + ',参数=' + str(subs)
        print('\033[1;32;49m%s\033[0m' % requestInfo)
        return sub(url, subs)

    def contract_sub_depth_high_freq(self, data_type, contract_code, size, ):
        subs = {
            "data_type": "{}".format(data_type),
            "sub": "market.{}.depth.size_{}.high_freq".format(contract_code, size),
            "id": "id1"
        }
        path = '/ws'
        url = self.__url + path
        return sub(url, subs)

    # 【通用】订阅 Market detail 数据
    def contract_sub_detail(self, symbol):
        subs = {
            "sub": "market.{}.detail".format(symbol),
            "id": "id1"
        }
        path = '/ws'
        url = self.__url + path
        return sub(url, subs)

    # 有问题size参数
    def contract_req_trade_detail(self, contract_code):
        subs = {
            "req": "market.{}.trade.detail".format(contract_code),
            "id": "id1"
        }
        path = '/ws'
        url = self.__url + path
        return sub(url, subs)

    def contract_sub_trade_detail(self, symbol):
        subs = {
            "sub": "market.{}.trade.detail".format(symbol),
            "id": "id1"
        }
        path = '/ws'
        url = self.__url + path
        return sub(url, subs)

    def contract_sub_basis(self, contract_code, period, basis_price_type):
        subs = {
            "sub": "market.{}.basis.{}.{}".format(contract_code, period, basis_price_type),
            "id": "id1"
        }
        path = '/ws'
        url = self.__url + path
        return sub(url, subs)

    def contract_req_basis(self, contract_code, period, basis_price_type, From, to):
        subs = {
            "req": "market.{}.basis.{}.{}".format(contract_code, period, basis_price_type),
            "id": "id1",
            "from": "{}".format(From),
            "to": "{}".format(to)
        }
        path = '/ws'
        url = self.__url + path
        return sub(url, subs)

    def contract_sub_premium_index(self, contract_code, period):
        subs = {
            "sub": "market.{}.premium_index.{}".format(contract_code, period),
            "id": "id1"
        }
        path = '/ws'
        url = self.__url + path
        return sub(url, subs)

    def contract_req_premium_index(self, contract_code, period, From, to):
        subs = {
            "req": "market.{}.premium_index.{}".format(contract_code, period),
            "id": "id1",
            "from": "{}".format(From),
            "to": "{}".format(to)
        }
        path = '/ws'
        url = self.__url + path
        return sub(url, subs)

    def contract_sub_estimated_rate(self, contract_code, period):
        subs = {
            "req": "market.{}.estimated_rate.{}".format(contract_code, period),
            "id": "id1"
        }
        path = '/ws'
        url = self.__url + path
        return sub(url, subs)

    def contract_req_estimated_rate(self, contract_code, period, From, to):
        subs = {
            "req": "market.{}.estimated_rate.{}".format(contract_code, period),
            "id": "id1",
            "from": "{}".format(From),
            "to": "{}".format(to)
        }
        path = '/ws'
        url = self.__url + path
        return sub(url, subs)

    def contract_sub_account(self, contract_code):
        subs = {
            "op": "sub",
            "cid": '11433084',
            "topic": "accounts.{}".format(contract_code)
        }
        path = '/ws-notification'
        url = self.__url
        return api_key_sub(url, self.__access_key, self.__secret_key, subs, path)

    # 订阅订单成交数据
    def contract_notification(self, subs):
        path = '/notification'
        url = self.__url
        print(url)
        return api_key_sub(url, self.__access_key, self.__secret_key, subs, path)

    # WS订阅成交(req)
    def contract_req_tradedetail(self, contract_code=None):
        subs = {
            "req": "market.{}.trade.detail".format(contract_code),
            "id": "id1",
            "size": 1
        }
        path = '/ws'
        url = self.__url + path
        return sub(url, subs)

    # WS订阅成交(sub)
    def contract_sub_tradedetail(self, contract_code=None):
        subs = {
            "sub": "market.{}.trade.detail".format(contract_code),
            "id": "id1",
        }
        path = '/ws'
        url = self.__url + path
        return sub(url, subs)


t = WebsocketSevice(WSURL, ACCESS_KEY, SECRET_KEY)
