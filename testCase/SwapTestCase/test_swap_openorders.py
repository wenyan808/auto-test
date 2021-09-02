#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/10/13
# @Author  : zhangranghan


from common.SwapServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema, And, Or, Regex, SchemaError

from pprint import pprint
import pytest, allure, random, time


@allure.epic('反向永续')
@allure.feature('获取合约当前未成交委托')
class TestSwapOpenorders:

    def test_swap_openorders(self, contract_code):
        t.swap_order(contract_code=contract_code,
                     client_order_id='',
                     price='50000',
                     volume='1',
                     direction='buy',
                     offset='open',
                     lever_rate='5',
                     order_price_type='limit')
        time.sleep(1)

        r = t.swap_openorders(contract_code=contract_code,
                              page_size='',
                              page_index='')
        schema = {
            'data': {
                'current_page': 1,
                'orders': [{
                    'canceled_at': Or(int, None),
                    'client_order_id': Or(str, None),
                    'contract_code': 'BTC-USD',
                    'created_at': int,
                    'direction': str,
                    'fee': 0,
                    'fee_asset': 'BTC',
                    'is_tpsl': int,
                    'lever_rate': Or(float, int),
                    'liquidation_type': Or(int, None),
                    'margin_frozen': Or(float, int),
                    'offset': str,
                    'order_id': int,
                    'order_id_str': str,
                    'order_price_type': str,
                    'order_source': str,
                    'order_type': int,
                    'price': Or(float, int),
                    'profit': Or(float, int),
                    'real_profit': Or(float, int),
                    'status': int,
                    'symbol': 'BTC',
                    'trade_avg_price': Or(float, int,None),
                    'trade_turnover': Or(float, int),
                    'trade_volume': Or(float, int),
                    'update_time': int,
                    'volume': Or(float, int)
                }],
                'total_page': int,
                'total_size': int
            },
            'status': 'ok',
            'ts': int
        }
        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
