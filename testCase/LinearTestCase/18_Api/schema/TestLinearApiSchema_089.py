#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211122
# @Author : 
    用例标题
        获取用户的合约订单明细信息（全仓）
    前置条件
        
    步骤/文本
        调用接口：/linear-swap-api/v1/swap_cross_order_detail
    预期结果
        A)接口返回的json格式、字段名、字段值正确
    优先级
        0
    用例别名
        TestLinearApiSchema_089
"""
import random
import time
from pprint import pprint

import allure
import pytest
from schema import Schema, Or
from common.LinearServiceAPI import t as linear_api
from tool.atp import ATP


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('api')  # 这里填功能
@allure.story('schema校验')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : 张广南', 'Case owner : 张让翰')
@pytest.mark.stable
class TestLinearApiSchema_089:

    @allure.step('前置条件')
    def setup(self):
        pass

    @allure.title('获取用户的合约订单明细信息（全仓）')
    @allure.step('测试执行')
    def test_execute(self, contract_code, symbol):
        with allure.step('调用接口：/linear-swap-api/v1/swap_cross_order_detail'):
            lastprice = ATP.get_current_price()

            sell_order = linear_api.linear_cross_order(contract_code=contract_code,
                                                       price=lastprice,
                                                       volume='1',
                                                       direction='sell',
                                                       offset='open',
                                                       order_price_type="limit")
            pprint(sell_order)

            buy_order = linear_api.linear_cross_order(contract_code=contract_code,
                                                      price=lastprice,
                                                      volume='1',
                                                      direction='buy',
                                                      offset='open',
                                                      order_price_type="limit")
            pprint(buy_order)

            time.sleep(1)
            order_id = buy_order['data']['order_id']
            created_at = buy_order['ts']
            trade_partition = linear_api.get_trade_partition(contract_code)
            r = linear_api.linear_cross_order_detail(contract_code=contract_code,
                                                     order_id=order_id,
                                                     created_at=created_at,
                                                     order_type='1',
                                                     page_index='1',
                                                     page_size='20')
            pprint(r)
            schema = {
                'data': {
                    'adjust_value': Or(int, float),
                    'canceled_at': int,
                    'client_order_id': Or(str, None),
                    'contract_code': contract_code,
                    'created_at': int,
                    'current_page': int,
                    'direction': str,
                    'fee': Or(int, float),
                    'fee_asset': trade_partition,
                    'final_interest': int,
                    'instrument_price': Or(int, float),
                    'is_tpsl': Or(0, 1),
                    'lever_rate': int,
                    'liquidation_type': str,
                    'margin_account': str,
                    'margin_asset': trade_partition,
                    'margin_frozen': Or(float, int),
                    'margin_mode': 'cross',
                    'offset': str,
                    'order_id': int,
                    'order_id_str': str,
                    'order_price_type': str,
                    'order_source': str,
                    'order_type': str,
                    'price': Or(int, float),
                    'profit': float,
                    'real_profit': Or(int, float),
                    'status': int,
                    'symbol': symbol,
                    'total_page': int,
                    'total_size': int,
                    'trade_avg_price': Or(int, float, None),
                    'trade_turnover': float,
                    'trade_volume': float,
                    'contract_type': 'swap',
                    'business_type': 'swap',
                    'pair': str,
                    'trade_partition': trade_partition,
                    'trades': [
                        {'created_at': int,
                         'fee_asset': trade_partition,
                         'id': str,
                         'profit': float,
                         'real_profit': float,
                         'role': str,
                         'trade_fee': float,
                         'trade_id': int,
                         'trade_price': float,
                         'trade_turnover': float,
                         'trade_volume': float}
                    ],
                    'volume': float
                },
                'status': 'ok',
                'ts': int
            }

            assert r['data']['trades'][0]
            Schema(schema).validate(r)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        print(ATP.cancel_all_order())
        #print(ATP.close_all_position())



if __name__ == '__main__':
    pytest.main()
