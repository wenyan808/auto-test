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
@allure.feature('合约闪电平仓下单(全仓)')
class TestLinearCrossLightningClosePosition:



    def test_linear_cross_lightning_close_position(self,contract_code):
        a = t.linear_cross_order(contract_code=contract_code,
                       client_order_id='',
                       price='',
                       volume='1',
                       direction='buy',
                       offset='open',
                       lever_rate='5',
                       order_price_type='opponent')
        time.sleep(1)

        r = t.linear_cross_lightning_close_position(contract_code=contract_code,
                                              volume='1',
                                              direction='sell',
                                              client_order_id='',
                                              order_price_type='lightning')
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
