#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211122
# @Author : 
    用例标题
        查询母账户下的单个子账户资产信息（全仓）
    前置条件
        
    步骤/文本
        调用接口：/linear-swap-api/v1/swap_cross_sub_account_info
    预期结果
        A)接口返回的json格式、字段名、字段值正确
    优先级
        0
    用例别名
        TestLinearApiSchema_077
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
class TestLinearApiSchema_077:

    @allure.step('前置条件')
    def setup(self):
        print('''  ''')

    @allure.title('查询母账户下的单个子账户资产信息（全仓）')
    @allure.step('测试执行')
    def test_execute(self, contract_code, symbol):
        with allure.step('调用接口：/linear-swap-api/v1/swap_cross_sub_account_info'):
            r = linear_api.linear_sub_account_list(contract_code=contract_code)
            subuid = r['data'][0]['sub_uid']

            r = linear_api.linear_cross_sub_account_info(margin_account='USDT', sub_uid=subuid)
            pprint(r)
            schema = {'data': [{'contract_detail': [{'symbol': str,
                                                     'contract_code': str,
                                                     'contract_type': 'swap',
                                                     'pair': str,
                                                     'business_type': 'swap',
                                                     'margin_position': Or(int, float),
                                                     'margin_frozen': Or(int, float),
                                                     'margin_available': Or(int, float),
                                                     'profit_unreal': Or(int, float),
                                                     'liquidation_price': Or(float, int, str, None),
                                                     'lever_rate': int,
                                                     'adjust_factor': float,
                                                     'trade_partition': 'USDT'}],
                                'futures_contract_detail': [{'symbol': str,
                                                             'contract_code': str,
                                                             'contract_type': Or('next_quarter', 'this_week',
                                                                                 'next_week', 'quarter'),
                                                             'pair': str,
                                                             'business_type': 'futures',
                                                             'margin_position': Or(int, float),
                                                             'margin_frozen': Or(int, float),
                                                             'margin_available': Or(int, float),
                                                             'profit_unreal': Or(int, float),
                                                             'liquidation_price': Or(float, int, str, None),
                                                             'lever_rate': int,
                                                             'adjust_factor': float,
                                                             'trade_partition': 'USDT'}],
                                'margin_account': 'USDT',
                                'margin_asset': 'USDT',
                                'margin_balance': Or(int, float),
                                'margin_frozen': Or(int, float),
                                'margin_mode': 'cross',
                                'margin_position': Or(int, float),
                                'margin_static': Or(int, float),
                                'profit_real': Or(int, float),
                                'profit_unreal': Or(int, float),
                                'risk_rate': Or(int, None, float),
                                'withdraw_available': Or(int, None, float)}],
                      'status': 'ok',
                      'ts': int}
            Schema(schema).validate(r)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
