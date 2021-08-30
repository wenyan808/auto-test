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
@allure.feature('对仓位设置止盈止损订单（逐仓）')
class TestLinearTpslOrder:



    def test_linear_tpsl_order(self,contract_code):
        t.linear_order(contract_code=contract_code,
                           client_order_id='',
                           price='',
                           volume='1',
                           direction='buy',
                           offset='open',
                           lever_rate='5',
                           order_price_type='opponent')

        r = t.linear_tpsl_order(contract_code=contract_code,
                                direction='sell',
                                volume='1',
                                tp_trigger_price='60000',
                                tp_order_price='60000',
                                tp_order_price_type='limit',
                                sl_order_price='20000',
                                sl_order_price_type='limit',
                                sl_trigger_price='20000')
        pprint(r)
        schema = {'data': {'sl_order': {'order_id': int,
                            'order_id_str': str},
                          'tp_order': {'order_id': int,
                                       'order_id_str': str}},
                         'status': 'ok',
                         'ts': int}

        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
