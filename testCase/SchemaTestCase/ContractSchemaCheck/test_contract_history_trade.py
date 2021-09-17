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
@allure.feature('批量获取最近的交易记录')
class TestContractHistoryTrade:


    def test_contract_history_trade(self,symbol_period):

        r = t.contract_history_trade(symbol=symbol_period,
                                     size='1')
        pprint(r)
        assert r['status'] == 'ok'



if __name__ == '__main__':
    pytest.main()