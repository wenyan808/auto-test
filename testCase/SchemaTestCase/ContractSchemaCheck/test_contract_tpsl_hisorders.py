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
@allure.feature('查询止盈止损订单历史委托接口')
class TestContractTpslHisorders:


    def test_contract_tpsl_hisorders(self,symbol):

        r = t.contract_tpsl_hisorders(symbol=symbol,status='0',create_date='7')
        pprint(r)
        assert r['status'] == 'ok'



if __name__ == '__main__':
    pytest.main()