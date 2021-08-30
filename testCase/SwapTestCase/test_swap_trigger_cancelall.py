#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/10/13
# @Author  : zhangranghan



from common.SwapServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema,And,Or,Regex,SchemaError

from pprint import pprint
import pytest,allure,random,time

@allure.epic('反向永续')
@allure.feature('合约计划委托全部撤单')
class TestSwapTriggerOrderCancelall:



    def test_swap_trigger_cancelall(self,contract_code):
        t.swap_trigger_order(contract_code=contract_code,
                             trigger_type='le',
                             trigger_price='20000',
                             order_price='20000',
                             order_price_type='limit',
                             volume='1',
                             direction='buy',
                             offset='open',
                             lever_rate='5')
        time.sleep(1)

        r = t.swap_trigger_cancelall(contract_code=contract_code)
        pprint(r)
        assert r['status'] == 'ok'

if __name__ == '__main__':
    pytest.main()