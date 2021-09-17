#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/1 3:06 PM
# @Author  : zhangranghan

from common.ContractServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema,And,Or,Regex,SchemaError
from pprint import pprint
import pytest,allure,random,time



@allure.epic('反向交割')
@allure.feature('获取最高限价和最低限价')
class TestContractPriceLimit:


    def test_contract_price_limit(self,symbol):

        r = t.contract_price_limit(symbol=symbol,
                                   contract_code='',
                                   contract_type='this_week')
        pprint(r)
        assert r['status'] == 'ok'



if __name__ == '__main__':
    pytest.main()