#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2019/11/1 12:44 PM
# @Author  : zhangranghan


from common.ContractServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema,And,Or,Regex,SchemaError
from pprint import pprint
import pytest,allure,random,time



@allure.epic('反向交割')
@allure.feature('合约下单')
class TestContractOrder:


    @allure.severity('blocker')
    @allure.story('合约下单')
    def test_contract_order(self,symbol):
        """
        用例描述：XXXXXXXX
        """
        r = t.contract_order(symbol=symbol,
                           contract_type='quarter',
                           contract_code='',
                           client_order_id='',
                           price='50000',
                           volume='1',
                           direction='buy',
                           offset='open',
                           lever_rate='5',
                           order_price_type='limit')
        pprint(r)
        assert r['status'] == 'ok'
        assert 'order_id' in r['data']
        assert 'order_id_str' in r['data']
        assert 'ts' in r





if __name__ == '__main__':
    pytest.main()


