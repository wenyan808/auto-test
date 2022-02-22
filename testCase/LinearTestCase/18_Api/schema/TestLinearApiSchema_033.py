#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211122
# @Author : 
    用例标题
        查询用户结算记录（全仓）
    前置条件
        
    步骤/文本
        调用接口：/linear-swap-api/v1/swap_cross_user_settlement_records
    预期结果
        A)接口返回的json格式、字段名、字段值正确
    优先级
        0
    用例别名
        TestLinearApiSchema_033
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
class TestLinearApiSchema_033:

    @allure.step('前置条件')
    def setup(self):
        print('''  ''')

    @allure.title('查询用户结算记录（全仓）')
    @allure.step('测试执行')
    def test_execute(self, contract_code, symbol):
        with allure.step('调用接口：/linear-swap-api/v1/swap_cross_user_settlement_records'):
            #contract_code = 'BTC-USDT'
            trade_partition = linear_api.get_trade_partition(contract_code)
            r = linear_api.linear_cross_user_settlement_records(margin_account=trade_partition,
                                                                start_time='',
                                                                end_time='',
                                                                page_size='',
                                                                page_index='')
            pprint(r)
            schema = {'data': {'current_page': int,
                               'settlement_records': [{'clawback': float,
                                                       'contract_detail': [{'contract_code': str,
                                                                            'fee': float,
                                                                            'fee_asset': trade_partition,
                                                                            'offset_profitloss': float,
                                                                            'pair': str,
                                                                            'positions': [{'symbol': str,
                                                                                           'contract_code': str,
                                                                                           'pair': str,
                                                                                           'direction': str,
                                                                                           'volume': float,
                                                                                           'cost_hold': float,
                                                                                           'cost_hold_pre': float,
                                                                                           'cost_open': float,
                                                                                           'settlement_price': float,
                                                                                           'settlement_profit_unreal': float,
                                                                                           'settlement_type': Or('settlement', 'delivery')}],
                                                                            'symbol': str,
                                                                            'trade_partition': trade_partition}, ],
                                                       'fee': float,
                                                       'fee_asset': trade_partition,
                                                       'funding_fee': float,
                                                       'margin_account': trade_partition,
                                                       'margin_balance': Or(float, None),
                                                       'margin_balance_init': Or(float, None),
                                                       'margin_mode': 'cross',
                                                       'offset_profitloss': float,
                                                       'settlement_profit_real': float,
                                                       'settlement_time': int}],
                               'total_page': int,
                               'total_size': int},
                      'status': 'ok',
                      'ts': int}

            Schema(schema).validate(r)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
