#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211122
# @Author : 
    用例标题
        获取用户的合约账户信息（全仓）
    前置条件
        
    步骤/文本
        调用接口：/linear-swap-api/v1/swap_cross_account_info
    预期结果
        A)接口返回的json格式、字段名、字段值正确
    优先级
        0
    用例别名
        TestLinearApiSchema_073
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
class TestLinearApiSchema_073:

    @allure.step('前置条件')
    def setup(self):
        print('''  ''')

    @allure.title('获取用户的合约账户信息（全仓）')
    @allure.step('测试执行')
    def test_execute(self, contract_code, symbol):
        with allure.step('调用接口：/linear-swap-api/v1/swap_cross_account_info'):
            trade_partition = linear_api.get_trade_partition(contract_code)
            r = linear_api.linear_cross_account_info(margin_account=trade_partition)
            pprint(r)
            schema1 = {'data': [{'contract_detail': [{'symbol': str,
                                                      'contract_code': str,
                                                      'contract_type': 'swap',
                                                      'pair': str,
                                                      'business_type': 'swap',
                                                      'margin_position': Or(float, int),
                                                      'margin_frozen': Or(int, float, None),
                                                      'margin_available': float,
                                                      'profit_unreal': Or(float, int),
                                                      'liquidation_price': Or(None, float),
                                                      'lever_rate': int,
                                                      'adjust_factor': float,
                                                      'trade_partition': trade_partition}, ],
                                 'futures_contract_detail': [{'symbol': str,
                                                              'contract_code': str,
                                                              'contract_type': Or('next_quarter', 'this_week',
                                                                                  'next_week', 'quarter'),
                                                              'pair': str,
                                                              'business_type': 'futures',
                                                              'margin_position': Or(float, int),
                                                              'margin_frozen': Or(int, float, None),
                                                              'margin_available': float,
                                                              'profit_unreal': Or(float, int),
                                                              'liquidation_price': Or(None, float),
                                                              'lever_rate': int,
                                                              'adjust_factor': float,
                                                              'trade_partition': trade_partition}, ],
                                 'margin_mode': 'cross',
                                 'margin_account': trade_partition,
                                 'margin_asset': trade_partition,
                                 'margin_balance': float,
                                 'margin_static': float,
                                 'margin_position': Or(float, int),
                                 'margin_frozen': Or(int, float, None),
                                 'profit_real': float,
                                 'profit_unreal': Or(int, float),
                                 'withdraw_available': float,
                                 'risk_rate': float,
                                 'position_mode': Or('single_side', 'dual_side')}],
                       'status': 'ok',
                       'ts': int}

            Schema(schema1).validate(r)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
