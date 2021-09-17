#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/2
# @Author  : zhangranghan

from common.ContractServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema,And,Or,Regex,SchemaError
from pprint import pprint
import pytest,allure,random,time



@allure.epic('反向交割')
@allure.feature('查询用户品种实际可用杠杆倍数')
class TestContractAvailableLevelRate:


    def test_contract_available_level_rate(self,symbol):

        r = t.contract_available_level_rate(symbol=symbol)
        pprint(r)
        assert r['status'] == 'ok'



if __name__ == '__main__':
    pytest.main()
