#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/10/19
# @Author  : HuiQing Yu

from common.util import api_http_post
from config.conf import MQ_INFO


class mqComm:
    info = eval(MQ_INFO)

    # 个人初始化
    def UserProductTriggerInitChannel(self, userId,symbol):
        params = {
            "vhost": "/",
            "name": "UserProductTriggerInitChannel",
            "properties": {
                "delivery_mode": 2,
                "headers": {}
            },
            "routing_key": "",
            "delivery_mode": "2",
            "payload": "{\"" + symbol + "\":{\"" + userId + "\":\"DEL_USER_PRODUCT_APO\"}}",
            "headers": {},
            "props": {},
            "payload_encoding": "string"
        }
        headers = {
            'authorization': self.info['contract']['auth']
        }
        path = '/api/exchanges/%2F/UserProductTriggerInitChannel/publish'
        url = self.info['contract']['uri']+path
        result = api_http_post(url, params=params, add_to_headers=headers)
        return result

    # 品种初始化
    def productTradeStatus(self,symbol):
        path = '/api/exchanges/%2F/SM%3AproductTradeStatus/publish'
        params = {
            "vhost": "/",
            "name": "SM:productTradeStatus",
            "properties": {
                "delivery_mode": 2,
                "headers": {}
            },
            "routing_key": "",
            "delivery_mode": "2",
            "payload": "{\""+symbol+"\":{\""+symbol+"\":1}}",
            "headers": {},
            "props": {},
            "payload_encoding": "string"
        }
        headers = {
            'authorization': self.info['contract']['auth']
        }
        url = self.info['contract']['uri'] + path
        result = api_http_post(url, params=params, add_to_headers=headers)
        return result
        pass


mqComm = mqComm()
