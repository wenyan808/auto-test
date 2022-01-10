#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/9/11
# @Author  : zhangranghan

from common.util import sub, api_key_sub
from config.conf import WSURL, ACCESS_KEY, SECRET_KEY


class WebsocketSevice:

    def __init__(self, url, access_key, secret_key):
        self.__url = url
        self.__access_key = access_key
        self.__secret_key = secret_key

    # 【通用】普通订阅
    def linear_sub(self, subs):
        path = '/linear-swap-ws'
        url = self.__url + path
        return sub(url, subs)

    # 订阅(sub)指数K线数据
    def linear_sub_index(self, contract_code, period):
        subs = {
            "sub": "market.{}.index.{}".format(contract_code, period),
            "id": "id1"
        }
        path = '/ws_index'
        url = self.__url + path
        print(url)
        return sub(url, subs)

    # 【通用】鉴权订阅
    def linear_sub_auth(self, subs):
        path = '/linear-swap-ws'
        url = self.__url + path
        return api_key_sub(url, self.__access_key, self.__secret_key, subs)

    # 【通用】订阅 KLine 数据
    def linear_sub_kline(self, contract_code, period):
        subs = {
            "sub": "market.{}.kline.{}".format(contract_code, period),
            "id": "id1"
        }
        path = '/linear-swap-ws'
        url = self.__url + path
        keyword = 'tick'
        return sub(url, subs, keyword)

    # 通用】买一卖一逐笔行情推送
    def linear_sub_bbo(self, contract_code):
        subs = {
            "sub": "market.{}.bbo".format(contract_code),
            "id": "id8"
        }
        path = '/linear-swap-ws'
        url = self.__url + path
        keyword = 'tick'
        return sub(url, subs, keyword)

    def linear_req_kline(self, contract_code, period, from_, to):
        subs = {
            "req": "market.{}.kline.{}".format(contract_code, period),
            "from": int(from_),
            "to": int(to)
        }
        path = '/linear-swap-ws'
        url = self.__url + path
        return sub(url, subs)

    # 【通用】订阅 Market Depth 数据
    def linear_sub_depth(self, contract_code, type):
        subs = {
            "sub": "market.{}.depth.{}".format(contract_code, type),
            "id": "id5"
        }
        path = '/linear-swap-ws'
        url = self.__url + path
        keyword = 'tick'
        return sub(url, subs, keyword)

    def linear_sub_depth_web(self, contract_code, type):
        subs = {
            "sub": "market.{}.depth.{}.sync".format(contract_code, type),
            "id": "id6"
        }
        path = '/linear-swap-ws'
        url = self.__url + path
        keyword = 'tick'
        return sub(url, subs, keyword)

    def linear_sub_depth_high_freq(self, contract_code, size, data_type="incremental"):
        subs = {
            "data_type": data_type,
            "sub": "market.{}.depth.size_{}.high_freq".format(contract_code, size),
            "id": "id1"
        }
        path = '/linear-swap-ws'
        url = self.__url + path
        return sub(url, subs)

    # 【通用】订阅 Market detail 数据
    def linear_sub_detail(self, contract_code):
        subs = {
            "sub": "market.{}.detail".format(contract_code),
            "id": "id1"
        }
        path = '/linear-swap-ws'
        url = self.__url + path
        return sub(url, subs)

    # 有问题size参数
    def linear_req_trade_detail(self, contract_code):
        subs = {
            "req": "market.{}.trade.detail".format(contract_code),
            "id": "id1"
        }
        path = '/linear-swap-ws'
        url = self.__url + path
        return sub(url, subs)

    def linear_sub_trade_detail(self, contract_code):
        subs = {
            "sub": "market.{}.trade.detail".format(contract_code),
            "id": "id1"
        }
        path = '/linear-swap-ws'
        url = self.__url + path
        return sub(url, subs)

    # 订阅聚合行情
    def linear_sub_detail_merged(self, contract_code):
        subs = {
            "zip": 0,
            "sub": f"market.{contract_code}.detail",
            "id": "id7"
        }
        path = '/linear-swap-ws'
        url = self.__url + path
        return sub(url, subs)

    # 订阅深度图
    def linear_sub_depth_chart(self, contract_code, percent):
        subs = {"sub": f"market.{contract_code}.depth.{percent}",
                "id": "id8"}
        path = '/linear-swap-ws'
        url = self.__url + path
        return sub(url, subs)

    # 订阅基差数据

    def linear_sub_basis(self, contract_code, period, basis_price_type="open"):
        subs = {
            "sub": "market.{}.basis.{}.{}".format(contract_code, period, basis_price_type),
            "id": "id1"
        }
        path = '/ws_index'
        url = self.__url + path
        return sub(url, subs)

    def linear_req_basis(self, contract_code, period, basis_price_type, From, to):
        subs = {
            "req": "market.{}.basis.{}.{}".format(contract_code, period, basis_price_type),
            "id": "id1",
            "from": "{}".format(From),
            "to": "{}".format(to)
        }
        path = '/ws_index'
        url = self.__url + path
        return sub(url, subs)

    def linear_sub_premium_index(self, contract_code, period):
        subs = {
            "sub": "market.{}.premium_index.{}".format(contract_code, period),
            "id": "id1"
        }
        path = '/linear-swap-ws'
        url = self.__url + path
        return sub(url, subs)

    def linear_req_premium_index(self, contract_code, period, From, to):
        subs = {
            "req": "market.{}.premium_index.{}".format(contract_code, period),
            "id": "id1",
            "from": "{}".format(From),
            "to": "{}".format(to)
        }
        path = '/linear-swap-ws'
        url = self.__url + path
        return sub(url, subs)

    def linear_sub_estimated_rate(self, contract_code, period):
        subs = {
            "req": "market.{}.estimated_rate.{}".format(contract_code, period),
            "id": "id1"
        }
        path = '/linear-swap-ws'
        url = self.__url + path
        return sub(url, subs)

    def linear_req_estimated_rate(self, contract_code, period, From, to):
        subs = {
            "req": "market.{}.estimated_rate.{}".format(contract_code, period),
            "id": "id1",
            "from": "{}".format(From),
            "to": "{}".format(to)
        }
        path = '/linear-swap-ws'
        url = self.__url + path
        return sub(url, subs)

    def linear_sub_account(self, contract_code):
        subs = {
            "op": "sub",
            "cid": '11538447',
            "topic": "accounts.{}".format(contract_code)
        }
        path = '/linear-swap-notification'
        url = self.__url
        return api_key_sub(url, self.__access_key, self.__secret_key, subs, path)

    def linear_notification(self, sub):
        path = '/linear-swap-notification'
        url = self.__url
        return api_key_sub(url, self.__access_key, self.__secret_key, sub, path)


t = WebsocketSevice(WSURL, ACCESS_KEY, SECRET_KEY)
