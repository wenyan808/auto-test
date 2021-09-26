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
@allure.feature('组合查询用户财务记录')
class TestSwapFinancialRecordExact:


    def test_swap_financial_record_exact(self,contract_code):

        r = t.swap_financial_record_exact(contract_code=contract_code,type='5',start_time='',end_time='',from_id='',size='',direct='')
        assert r['status'] == 'ok'


if __name__ == '__main__':
    pytest.main()