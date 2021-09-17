#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2019/9/12 3:06 PM
# @Author  : zhangranghan

from common.ContractServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema,And,Or,Regex,SchemaError
from pprint import pprint
import pytest,allure,random,time



@allure.epic('反向交割')
@allure.feature('获取指数信息')
class TestContractIndex:



    def test_contract_index(self,symbol):

        r = t.contract_index(symbol=symbol)
        pprint(r)
        assert r['status'] == 'ok'




if __name__ == '__main__':
    pytest.main()