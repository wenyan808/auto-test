#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211122
# @Author : 
    用例标题
        组合查询合约历史委托（逐仓）
    前置条件
        
    步骤/文本
        调用接口：linear-swap-api/v1/swap_hisorders_exact
    预期结果
        A)接口返回的json格式、字段名、字段值正确
    优先级
        0
    用例别名
        TestLinearApiSchema_053
"""
import time
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
class TestLinearApiSchema_053:

    @allure.step('前置条件')
    def setup(self):
        print('''  ''')

    @allure.title('组合查询合约历史委托（逐仓）')
    @allure.step('测试执行')
    def test_execute(self, contract_code, symbol):
        with allure.step('调用接口：linear-swap-api/v1/swap_hisorders_exact'):
            r = linear_api.linear_hisorders_exact(contract_code=contract_code,
                                         trade_type='0',
                                         type='1',
                                         status='0',
                                         order_price_type='limit',
                                         start_time='',
                                         end_time='',
                                         from_id='',
                                         size='',
                                         direct='')
            pprint(r)
            schema = {'data': {'next_id': Or(int, None),
                               'orders': [{'contract_code': contract_code,
                                           'create_date': int,
                                           'direction': str,
                                           'fee': float,
                                           'fee_asset': 'USDT',
                                           'is_tpsl': int,
                                           'lever_rate': int,
                                           'liquidation_type': str,
                                           'margin_account': contract_code,
                                           'margin_frozen': float,
                                           'margin_mode': 'isolated',
                                           'offset': str,
                                           'order_id': int,
                                           'order_id_str': str,
                                           'order_price_type': str,
                                           'order_source': str,
                                           'order_type': int,
                                           'price': float,
                                           'profit': float,
                                           'query_id': int,
                                           'real_profit': Or(int, float),
                                           'status': int,
                                           'symbol': symbol,
                                           'trade_avg_price': Or(int, float),
                                           'trade_turnover': float,
                                           'trade_volume': float,
                                           'volume': float}, ],
                               'remain_size': int},
                      'status': 'ok',
                      'ts': int}
            Schema(schema).validate(r)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
