#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211122
# @Author : 
    用例标题
        获取用户API指标禁用信息（全逐通用）
    前置条件
        
    步骤/文本
        调用接口：/linear-swap-api/v1/swap_api_trading_status
    预期结果
        A)接口返回的json格式、字段名、字段值正确
    优先级
        0
    用例别名
        TestLinearApiSchema_042
"""

from pprint import pprint

import allure
import pytest
from schema import Schema, Or

from common.LinearServiceAPI import t as linear_api


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('api')  # 这里填功能
@allure.story('schema校验')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : 张广南', 'Case owner : 张让翰')
@pytest.mark.stable
class TestLinearApiSchema_042:

    @allure.step('前置条件')
    def setup(self):
        print('''  ''')

    @allure.title('获取用户API指标禁用信息（全逐通用）')
    @allure.step('测试执行')
    def test_execute(self, contract_code, symbol):
        with allure.step('调用接口：/linear-swap-api/v1/swap_api_trading_status'):
            r = linear_api.linear_api_trading_status()
            pprint(r)
            schema = {
                'data': {
                    'COR': {
                        'cancel_ratio': Or(float, int),
                        'cancel_ratio_threshold': Or(float, int),
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
                    'disable_reason': Or(str, None),
                    'is_disable': int,
                    'order_price_types': Or(str, None),
                    'recovery_time': int
                },
                'status': 'ok',
                'ts': int
            }

            Schema(schema).validate(r)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
