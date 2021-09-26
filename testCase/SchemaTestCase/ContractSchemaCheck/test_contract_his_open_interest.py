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
@allure.feature('平台持仓量查询')
class TestContractHisOpenInterest:


    def test_contract_his_open_interest(self,symbol):

        r = t.contract_his_open_interest(symbol=symbol,
                                         contract_type='this_week',
                                         period='60min',
                                         amount_type='1',
                                         size='20')
        pprint(r)
        assert r['status'] == 'ok'



if __name__ == '__main__':
    pytest.main()
