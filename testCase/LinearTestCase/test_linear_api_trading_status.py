#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/8/7
# @Author  : zhangranghan



from common.LinearServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema,And,Or,Regex,SchemaError

from pprint import pprint
import pytest,allure,random,time




@allure.epic('正向永续')
@allure.feature('获取用户API指标禁用信息')
class TestLinearApiTradingStatus:


    def test_linear_api_trading_status(self):
        r = t.linear_api_trading_status()
        pprint(r)
        schema = {
            'data': {
                'COR': {
                    'cancel_ratio': Or(float,int),
                    'cancel_ratio_threshold': Or(float,int),
                    'invalid_cancel_orders': int,
                    'is_active': int,
                    'is_trigger': int,
                    'orders': int,
                    'orders_threshold': int
                },
                'TDN': {
                    'disables': int,
                    'disables_threshold': int,
                    'is_active': int,
                    'is_trigger': int
                },
                'disable_interval': int,
                'disable_reason': Or(str,None),
                'is_disable': int,
                'order_price_types': Or(str,None),
                'recovery_time': int
            },
            'status': 'ok',
            'ts': int
        }

        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
