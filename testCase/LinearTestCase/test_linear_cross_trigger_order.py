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
@allure.feature('合约计划委托下单(全仓)')
class TestLinearCrossTriggerOrder:


    def test_linear_cross_trigger_order(self,contract_code):
        r = t.linear_cross_trigger_order(contract_code=contract_code,
                                   trigger_type='le',
                                   trigger_price='10000',
                                   order_price='10000',
                                   order_price_type='limit',
                                   volume='1',
                                   direction='buy',
                                   offset='open',
                                   lever_rate='5')
        pprint(r)
        schema = {
                    'data': {
                        'order_id': int,
                        'order_id_str': str
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
