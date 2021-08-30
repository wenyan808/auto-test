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
@allure.feature('获取计划委托当前委托(全仓)')
class TestLinearCrossTriggerOpenorders:


    def test_linear_cross_trigger_openorders(self,contract_code,symbol):
        a = t.linear_cross_trigger_order(contract_code=contract_code,
                                   trigger_type='le',
                                   trigger_price='10000',
                                   order_price='10000',
                                   order_price_type='limit',
                                   volume='1',
                                   direction='buy',
                                   offset='open',
                                   lever_rate='5')
        time.sleep(1)


        r = t.linear_cross_trigger_openorders(contract_code=contract_code,
                                       page_index='',
                                       page_size='')
        pprint(r)
        schema = {
                    'data': {
                        'current_page': int,
                        'orders': [
                            {
                                'contract_code': contract_code,
                                'created_at': int,
                                'direction': str,
                                'lever_rate': int,
                                'margin_account': str,
                                'margin_mode': 'cross',
                                'offset': str,
                                'order_id': int,
                                'order_id_str': str,
                                'order_price': float,
                                'order_price_type': str,
                                'order_source': str,
                                'order_type': int,
                                'status': int,
                                'symbol': symbol,
                                'trigger_price': float,
                                'trigger_type': str,
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
