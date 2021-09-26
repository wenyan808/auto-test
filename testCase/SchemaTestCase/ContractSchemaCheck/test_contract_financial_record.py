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
@allure.feature('查询用户财务记录')
class TestContractFinancialRecord:


    def test_contract_financial_record(self,symbol):

        r = t.contract_financial_record(symbol=symbol,
                                        type='',
                                        create_date='',
                                        page_index='',
                                        page_size='')
        pprint(r)
        assert r['status'] == 'ok'



if __name__ == '__main__':
    pytest.main()
