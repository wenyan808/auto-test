#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211122
# @Author : 
    用例标题
        获取止盈止损历史委托（全仓）
    前置条件
        
    步骤/文本
        调用接口：/linear-swap-api/v1/swap_cross_tpsl_hisorders
    预期结果
        A)接口返回的json格式、字段名、字段值正确
    优先级
        0
    用例别名
        TestLinearApiSchema_105
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
class TestLinearApiSchema_105:

    @allure.step('前置条件')
    def setup(self):
        print('''  ''')

    @allure.title('获取止盈止损历史委托（全仓）')
    @allure.step('测试执行')
    def test_execute(self, contract_code, symbol):
        with allure.step('调用接口：/linear-swap-api/v1/swap_cross_tpsl_hisorders'):
            r = linear_api.linear_cross_tpsl_hisorders(contract_code=contract_code,
                                                       status='0',
                                                       create_date='7',
                                                       page_size='',
                                                       page_index='',
                                                       sort_by='')
            pprint(r)
            schema = {'data': {'current_page': int,
                               'orders': [{'canceled_at': int,
                                           'contract_code': contract_code,
                                           'created_at': int,
                                           'direction': str,
                                           'fail_code': Or(str, None),
                                           'fail_reason': Or(str, None),
                                           'margin_account': 'USDT',
                                           'margin_mode': 'cross',
                                           'order_id': int,
                                           'order_id_str': str,
                                           'order_price': float,
                                           'order_price_type': str,
                                           'order_source': str,
                                           'order_type': int,
                                           'relation_order_id': str,
                                           'relation_tpsl_order_id': str,
                                           'source_order_id': Or(int, None, str),
                                           'status': int,
                                           'symbol': str,
                                           'tpsl_order_type': str,
                                           'trigger_price': float,
                                           'trigger_type': str,
                                           'triggered_price': Or(str, None),
                                           'update_time': int,
                                           'contract_type': 'swap',
                                           'business_type': 'swap',
                                           'pair': contract_code,
                                           'volume': float}, ],
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
