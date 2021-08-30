#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/10/13
# @Author  : zhangranghan



from common.SwapServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema,And,Or,Regex,SchemaError

from pprint import pprint
import pytest,allure,random,time


@allure.epic('反向永续')
@allure.feature('查询用户财务记录')
class TestSwapFinancialRecord:


    def test_swap_financial_record(self,contract_code):

        r = t.swap_financial_record(contract_code=contract_code,type='0',create_date='90',page_index='',page_size='')
        pprint(r)
        assert r['status'] == 'ok'



if __name__ == '__main__':
    pytest.main()