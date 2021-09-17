#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/9
# @Author  : zhangranghan


from common.ContractServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema,And,Or,Regex,SchemaError
from pprint import pprint
import pytest,allure,random,time



@allure.epic('反向交割')
@allure.feature('计划委托撤单')
class TestContractTriggerCancel:

    def test_contract_trigger_cancel(self,symbol):

        order_json = t.contract_trigger_order(symbol=symbol,
                                     contract_type='quarter',
                                     contract_code='',
                                     trigger_type='le',
                                     trigger_price='50000',
                                     order_price='50000',
                                     order_price_type='',
                                     volume='1',
                                     direction='buy',
                                     offset='open',
                                     lever_rate='5')
        time.sleep(1)
        order_id = order_json['data']['order_id']


        r = t.contract_trigger_cancel(symbol='BTC',
                                      order_id=order_id)
        pprint(r)
        assert r['status'] == 'ok'


if __name__ == '__main__':
    pytest.main()
