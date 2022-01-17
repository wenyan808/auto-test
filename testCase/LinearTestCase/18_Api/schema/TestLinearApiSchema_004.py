#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211122
# @Author : 
    用例标题
        获取当前可用合约总持仓量（全逐通用）
    前置条件
        
    步骤/文本
        调用接口：/linear-swap-api/v1/swap_open_interest
    预期结果
        A)接口返回的json格式、字段名、字段值正确
    优先级
        0
    用例别名
        TestLinearApiSchema_004
"""

from common.LinearServiceAPI import t as linear_api

from pprint import pprint
from schema import Schema,Or
import pytest, allure, random, time


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('api')  # 这里填功能
@allure.story('schema校验')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : 张广南', 'Case owner : 张让翰')
@pytest.mark.stable
class TestLinearApiSchema_004:

    @allure.step('前置条件')
    def setup(self):
        print('''  ''')

    @allure.title('获取当前可用合约总持仓量（全逐通用）')
    @allure.step('测试执行')
    def test_execute(self, contract_code,symbol):
        with allure.step('调用接口：/linear-swap-api/v1/swap_open_interest'):
            trade_partition = linear_api.get_trade_partition(contract_code)
            r = linear_api.linear_open_interest(contract_code=contract_code)
            pprint(r)
            schema = {
                'data': [
                    {
                        'symbol': symbol,
                        'contract_code': contract_code,
                        'contract_type': 'swap',
                        'business_type': 'swap',
                        'pair': contract_code,
                        'amount': float,
                        'volume': float,
                        'value': float,
                        'trade_amount': Or(int, float),
                        'trade_volume': Or(int, float),
                        'trade_turnover': Or(int, float),
                        'trade_partition': trade_partition
                    }
                ],
                'status': 'ok',
                'ts': int
            }
            Schema(schema).validate(r)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
