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
@allure.feature('跟踪委托全部撤单')
class TestLinearTrackCancelall:

    def test_linear_track_cancelall(self,contract_code):
        t.linear_track_order(contract_code=contract_code,
                                 direction='buy',
                                 offset='open',
                                 lever_rate='5',
                                 volume='1',
                                 callback_rate='0.01',
                                 active_price='50000',
                                 order_price_type='formula_price')
        time.sleep(1)
        r = t.linear_track_cancelall(contract_code=contract_code)
        pprint(r)
        schema = {'data': {'errors': list,
                           'successes': str},
                         'status': 'ok',
                         'ts': int}

        Schema(schema).validate(r)

if __name__ == '__main__':
    pytest.main()
