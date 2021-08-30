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
@allure.feature('撤销全部合约单(全仓)')
class TestLinearCrossCancelall:


    def test_linear_cross_cancelall(self,contract_code):
        t.linear_cross_order(contract_code=contract_code,
                       client_order_id='',
                       price='50000',
                       volume='1',
                       direction='buy',
                       offset='open',
                       lever_rate='5',
                       order_price_type='limit')
        time.sleep(1)

        r = t.linear_cross_cancelall(contract_code=contract_code)
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
