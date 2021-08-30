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
@allure.feature('获取计划委托历史委托(全仓)')
class TestLinearCrossTriggerHisorders:


    def test_linear_cross_trigger_hisorders(self,contract_code,symbol):
        r = t.linear_cross_trigger_hisorders(contract_code=contract_code,
                                       trade_type='1',
                                       status='0',
                                       create_date='7',
                                       page_index='',
                                       page_size='')
        pprint(r)
        schema = {
                    'data': {
                        'current_page': int,
                        'orders': [
                            {
                                'canceled_at': Or(int,None),
                                'contract_code': contract_code,
                                'created_at': int,
                                'direction': 'buy',
                                'fail_code': Or(int,None),
                                'fail_reason': Or(str,None),
                                'lever_rate': int,
                                'margin_account': str,
                                'margin_mode': 'cross',
                                'offset': str,
                                'order_id': int,
                                'order_id_str': str,
                                'order_insert_at': int,
                                'order_price': float,
                                'order_price_type': str,
                                'order_source': str,
                                'order_type': int,
                                'relation_order_id': str,
                                'status': int,
                                'symbol': symbol,
                                'trigger_price': float,
                                'trigger_type': Or('ge','le'),
                                'triggered_at': Or(int,None),
                                'triggered_price': Or(int,float,None),
                                'update_time': int,
                                'volume': float
                            }
                        ],
                        'total_page': int,
                        'total_size': int
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)



if __name__ == '__main__':
    pytest.main()
