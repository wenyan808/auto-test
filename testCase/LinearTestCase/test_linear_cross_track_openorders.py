#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/8/7
# @Author  : zhangranghan



from common.LinearServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema,And,Or,Regex,SchemaError

from pprint import pprint
import pytest,allure,random,time




@allure.epic('正向永续')
@allure.feature('获取跟踪委托当前委托(全仓)')
class TestLinearCrossTrackOpenorders:

    def test_linear_cross_track_openorders(self,contract_code,symbol):
        t.linear_cross_track_order(contract_code=contract_code,
                                 direction='buy',
                                 offset='open',
                                 lever_rate='5',
                                 volume='1',
                                 callback_rate='0.01',
                                 active_price='50000',
                                 order_price_type='formula_price')
        time.sleep(1)
        r = t.linear_cross_track_openorders(contract_code=contract_code,
                                      page_index='',
                                      page_size='')
        pprint(r)
        schema = {'data': {'current_page': int,
                          'orders': [{'active_price': float,
                                      'callback_rate': float,
                                      'contract_code': contract_code,
                                      'created_at': int,
                                      'direction': str,
                                      'is_active': int,
                                      'lever_rate': int,
                                      'margin_account': 'USDT',
                                      'margin_mode': 'cross',
                                      'offset': str,
                                      'order_id': int,
                                      'order_id_str': str,
                                      'order_price_type': str,
                                      'order_source': str,
                                      'order_type': int,
                                      'status': int,
                                      'symbol': symbol,
                                      'volume': float}],
                          'total_page': int,
                          'total_size': int},
                 'status': 'ok',
                 'ts': int}

        Schema(schema).validate(r)

if __name__ == '__main__':
    pytest.main()
