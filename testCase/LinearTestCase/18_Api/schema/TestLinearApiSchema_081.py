#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211122
# @Author : 
    用例标题
        获取用户资产和持仓信息（全仓）
    前置条件
        
    步骤/文本
        调用接口：/linear-swap-api/v1/swap_cross_account_position_info
    预期结果
        A)接口返回的json格式、字段名、字段值正确
    优先级
        0
    用例别名
        TestLinearApiSchema_081
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
class TestLinearApiSchema_081:

    @allure.step('前置条件')
    def setup(self):
        print('''  ''')

    @allure.title('获取用户资产和持仓信息（全仓）')
    @allure.step('测试执行')
    def test_execute(self, contract_code, symbol):
        with allure.step('调用接口：/linear-swap-api/v1/swap_cross_account_position_info'):
            r = linear_api.linear_cross_account_position_info(margin_account='USDT')
            pprint(r)
            schema1 = {'data': {'contract_detail': [{'symbol': str,
                                                     'contract_code': str,
                                                     'contract_type': Or('swap'),
                                                     'pair': str,
                                                     'business_type': 'swap',
                                                     'margin_position': Or(int, float),
                                                     'margin_frozen': Or(int, float),
                                                     'margin_available': float,
                                                     'profit_unreal': Or(int, float),
                                                     'liquidation_price': Or(None, float),
                                                     'lever_rate': int,
                                                     'adjust_factor': float,
                                                     'trade_partition': 'USDT'}, ],
                                'futures_contract_detail': [{'symbol': str,
                                                             'contract_code': str,
                                                             'contract_type': Or('swap', 'next_quarter', 'this_week',
                                                                   'next_week', 'quarter'),
                                                             'pair': str,
                                                             'business_type': 'futures',
                                                             'margin_position': Or(int, float),
                                                             'margin_frozen': Or(int, float),
                                                             'margin_available': float,
                                                             'profit_unreal': Or(int, float),
                                                             'liquidation_price': Or(None, float),
                                                             'lever_rate': int,
                                                             'adjust_factor': float,
                                                             'trade_partition': 'USDT'}, ],
                                'margin_account': 'USDT',
                                'margin_asset': 'USDT',
                                'margin_balance': Or(float, int),
                                'margin_frozen': Or(float, int),
                                'margin_mode': 'cross',
                                'margin_position': Or(float, int),
                                'margin_static': Or(float, int),
                                'positions': [{'symbol': str,
                                               'contract_code': str,
                                               'contract_type': Or('swap', 'next_quarter', 'this_week',
                                                                   'next_week', 'quarter'),
                                               'pair': str,
                                               'business_type': Or('swap', 'futures'),
                                               'margin_mode': 'cross',
                                               'margin_account': 'USDT',
                                               'volume': float,
                                               'available': Or(float, int),
                                               'frozen': float,
                                               'cost_open': Or(float, int),
                                               'cost_hold': Or(float, int),
                                               'profit_unreal': Or(float, int),
                                               'profit_rate': Or(float, int),
                                               'profit': Or(float, int),
                                               'margin_asset': 'USDT',
                                               'position_margin': Or(float, int),
                                               'lever_rate': int,
                                               'direction': str,
                                               'last_price': Or(float, int),
                                               'trade_partition': 'USDT'}, ],
                                'profit_real': float,
                                'profit_unreal': float,
                                'risk_rate': float,
                                'withdraw_available': float},
                       'status': 'ok',
                       'ts': int}

            Schema(schema1).validate(r)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
