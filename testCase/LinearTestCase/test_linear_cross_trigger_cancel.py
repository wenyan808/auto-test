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
@allure.feature('合约计划委托撤单(全仓)')
class TestLinearCrossTriggerCancel:


    def test_linear_cross_trigger_cancel(self,contract_code):
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
        order_id = a['data']['order_id']


        r = t.linear_cross_trigger_cancel(contract_code=contract_code,
                                    order_id=order_id)
        pprint(r)
        schema = {
                    'data': {
                        'errors': [

                        ],
                        'successes': str
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
