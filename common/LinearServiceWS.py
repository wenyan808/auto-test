#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/9/11
# @Author  : zhangranghan

from common.util import sub,api_key_sub
from config.conf import WSURL,ACCESS_KEY,SECRET_KEY
import uuid




class WebsocketSevice:

    def __init__(self,url,access_key,secret_key):
        self.__url = url
        self.__access_key = access_key
        self.__secret_key = secret_key


    def linear_sub_kline(self,contract_code,period):
        subs = {
                "sub": "market.{}.kline.{}".format(contract_code,period),
                "id": "id1"
            }
        path = '/linear-swap-ws'
        url = self.__url + path
        return sub(url,subs)



    def linear_req_kline(self,contract_code,period,From,to):
        subs = {
                "req": "market.{}.kline.{}".format(contract_code,period),
                "id": "id1",
                "from" : "{}".format(From),
                "to" : "{}".format(to)
            }
        path = '/linear-swap-ws'
        url = self.__url + path
        return sub(url,subs)


    def linear_sub_depth(self,contract_code,type):
        subs = {
                "sub": "market.{}.depth.{}".format(contract_code,type),
                "id": "id1"
            }
        path = '/linear-swap-ws'
        url = self.__url + path
        return sub(url,subs)


    def linear_sub_depth_high_freq(self,data_type,contract_code,size,):
        subs = {
                "data_type":"{}".format(data_type),
                "sub": "market.{}.depth.size_{}.high_freq".format(contract_code,size),
                "id": "id1"
            }
        path = '/linear-swap-ws'
        url = self.__url + path
        return sub(url,subs)


    def linear_sub_detail(self,contract_code):
        subs = {
                "sub": "market.{}.detail".format(contract_code),
                "id": "id1"
            }
        path = '/linear-swap-ws'
        url = self.__url + path
        return sub(url,subs)




    #有问题size参数
    def linear_req_trade_detail(self,contract_code):
        subs = {
                "req": "market.{}.trade.detail".format(contract_code),
                "id": "id1"
            }
        path = '/linear-swap-ws'
        url = self.__url + path
        return sub(url,subs)


    def linear_sub_trade_detail(self,contract_code):
        subs = {
                "sub": "market.{}.trade.detail".format(contract_code),
                "id": "id1"
            }
        path = '/linear-swap-ws'
        url = self.__url + path
        return sub(url,subs)


    def linear_sub_basis(self,contract_code,period,basis_price_type):
        subs = {
            "sub": "market.{}.basis.{}.{}".format(contract_code,period,basis_price_type),
            "id":"id1"
        }
        path = '/linear-swap-ws'
        url = self.__url + path
        return sub(url,subs)



    def linear_req_basis(self,contract_code,period,basis_price_type,From,to):
        subs = {
            "req": "market.{}.basis.{}.{}".format(contract_code,period,basis_price_type),
            "id":"id1",
            "from": "{}".format(From),
            "to": "{}".format(to)
        }
        path = '/linear-swap-ws'
        url = self.__url + path
        return sub(url,subs)


    def linear_sub_premium_index(self,contract_code,period):
        subs = {
            "sub": "market.{}.premium_index.{}".format(contract_code,period),
            "id":"id1"
        }
        path = '/linear-swap-ws'
        url = self.__url + path
        return sub(url,subs)

    def linear_req_premium_index(self, contract_code, period,From,to):
        subs = {
            "req": "market.{}.premium_index.{}".format(contract_code, period),
            "id": "id1",
            "from": "{}".format(From),
            "to": "{}".format(to)
        }
        path = '/linear-swap-ws'
        url = self.__url + path
        return sub(url, subs)


    def linear_sub_estimated_rate(self,contract_code,period):
        subs = {
            "req": "market.{}.estimated_rate.{}".format(contract_code, period),
            "id": "id1"
        }
        path = '/linear-swap-ws'
        url = self.__url + path
        return sub(url, subs)



    def linear_req_estimated_rate(self, contract_code, period,From,to):
        subs = {
            "req": "market.{}.estimated_rate.{}".format(contract_code, period),
            "id": "id1",
            "from": "{}".format(From),
            "to": "{}".format(to)
        }
        path = '/linear-swap-ws'
        url = self.__url + path
        return sub(url, subs)



    def linear_sub_account(self,contract_code):
        subs = {
                "op": "sub",
                "cid": '11433084',
                "topic": "accounts.{}".format(contract_code)
        }
        path = '/linear-swap-notification'
        url = self.__url + path
        return api_key_sub(url,self.__access_key,self.__secret_key,subs)


t = WebsocketSevice(WSURL,ACCESS_KEY,SECRET_KEY)