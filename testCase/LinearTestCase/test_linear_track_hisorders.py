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
@allure.feature('获取跟踪委托历史委托')
class TestLinearTrackHisorders:

    def test_linear_track_hisorders(self,contract_code,symbol):

        r = t.linear_track_hisorders(contract_code=contract_code,
                                     status='0',
                                     trade_type='0',
                                     create_date='7',
                                     page_size='',
                                     page_index='',
                                     sort_by='')

        pprint(r)
        schema = {'data': {'current_page': int,
                          'orders': [{'active_price': float,
                                      'callback_rate': float,
                                      'canceled_at': int,
                                      'contract_code': contract_code,
                                      'created_at': int,
                                      'direction': str,
                                      'fail_code': Or(None,str),
                                      'fail_reason': Or(None,str),
                                      'formula_price': Or(None,str,int,float),
                                      'is_active': int,
                                      'lever_rate': int,
                                      'margin_account': contract_code,
                                      'margin_mode': 'isolated',
                                      'market_limit_price': Or(None,int,float,str),
                                      'offset': str,
                                      'order_id': int,
                                      'order_id_str': str,
                                      'order_price_type': str,
                                      'order_source': str,
                                      'order_type': int,
                                      'real_volume': Or(int,float),
                                      'relation_order_id': str,
                                      'status': int,
                                      'symbol': symbol,
                                      'triggered_price': Or(None,int,str,float),
                                      'update_time': int,
                                      'volume': float},],
                          'total_page': int,
                          'total_size': int},
                 'status': 'ok',
                 'ts': int}

        Schema(schema).validate(r)

if __name__ == '__main__':
    pytest.main()
