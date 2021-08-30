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
@allure.feature('合约计划委托全部撤单')
class TestLinearTriggerCancelall:


    def test_linear_trigger_cancelall(self,contract_code):
        t.linear_trigger_order(contract_code=contract_code,
                                   trigger_type='le',
                                   trigger_price='10000',
                                   order_price='10000',
                                   order_price_type='limit',
                                   volume='1',
                                   direction='buy',
                                   offset='open',
                                   lever_rate='5')
        time.sleep(1)

        r = t.linear_trigger_cancelall(contract_code=contract_code)
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
