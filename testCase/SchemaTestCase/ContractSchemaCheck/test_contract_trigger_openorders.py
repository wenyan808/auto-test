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
@allure.feature('获取计划委托当前委托')
class TestContractTriggerOpenorders:


    def test_contract_trigger_openorders(self,symbol):


        r = t.contract_trigger_openorders(symbol=symbol,
                                          contract_code='',
                                          page_index='',
                                          page_size='')
        pprint(r)
        assert r['status'] == 'ok'

if __name__ == '__main__':
    pytest.main()