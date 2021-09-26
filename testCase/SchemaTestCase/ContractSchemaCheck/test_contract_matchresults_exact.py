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
@allure.feature('组合查询历史成交记录')
class TestContractMatchresultsExact:



    def test_contract_matchresults_exact(self,symbol):

        r = t.contract_matchresults_exact(symbol=symbol,
                                    trade_type='0')
        pprint(r)
        assert r['status'] == 'ok'



if __name__ == '__main__':
    pytest.main()
