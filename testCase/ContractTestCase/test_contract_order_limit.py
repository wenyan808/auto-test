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
@allure.feature('获取用户当前的下单量限制')
class TestContractOrderLimit:


    def test_contract_order_limit(self,symbol):


        r = t.contract_order_limit(symbol=symbol,
                                   order_price_type='limit')
        pprint(r)
        assert r['status'] == 'ok'

if __name__ == '__main__':
    pytest.main()