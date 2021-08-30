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
@allure.feature('止盈止损订单全部撤单（逐仓）')
class TestLinearTpslCancelall:

    def test_linear_tpsl_cancelall(self,contract_code):
        t.linear_order(contract_code=contract_code,
                           client_order_id='',
                           price='',
                           volume='1',
                           direction='buy',
                           offset='open',
                           lever_rate='5',
                           order_price_type='opponent')

        t.linear_tpsl_order(contract_code=contract_code,
                                direction='sell',
                                volume='1',
                                tp_trigger_price='60000',
                                tp_order_price='60000',
                                tp_order_price_type='limit',
                                sl_order_price='20000',
                                sl_order_price_type='limit',
                                sl_trigger_price='20000')
        time.sleep(1)

        r = t.linear_tpsl_cancelall(contract_code=contract_code)
        pprint(r)
        schema = {'data': {'errors': list,
                           'successes': str},
                             'status': 'ok',
                             'ts': int}

        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
