#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/1
# @Author  : zhangranghan


from common.ContractServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema,And,Or,Regex,SchemaError
from pprint import pprint
import pytest,allure,random,time



@allure.epic('反向交割')
@allure.feature('跟踪委托订单下单')
class TestContractTrackOrder:


    def test_contract_track_order(self,symbol):

        r = t.contract_track_order(symbol=symbol,contract_type='quarter',direction='buy',offset='open',lever_rate='5',volume='1',callback_rate='0.1',active_price='50000',order_price_type='formula_price')
        pprint(r)
        assert r['status'] == 'ok'



if __name__ == '__main__':
    pytest.main()
