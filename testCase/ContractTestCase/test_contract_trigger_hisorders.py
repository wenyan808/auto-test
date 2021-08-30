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
@allure.feature('获取计划委托历史委托')
class TestContractTriggerHisorders:


    def test_contract_trigger_hisorders(self,symbol):


        r = t.contract_trigger_hisorders(symbol=symbol,
                                         contract_code='',
                                         trade_type='0',
                                         status='0',
                                         create_date='90',
                                         page_index='',
                                         page_size='')
        pprint(r)
        assert r['status'] == 'ok'

if __name__ == '__main__':
    pytest.main()