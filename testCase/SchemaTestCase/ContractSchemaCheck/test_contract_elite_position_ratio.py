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
@allure.feature('精英账户多空持仓对比-持仓量')
class TestContractElitePositionRatio:


    def test_contract_elite_position_ratio(self,symbol):

        r = t.contract_elite_position_ratio(symbol=symbol,
                                            period='5min')
        pprint(r)
        assert r['status'] == 'ok'



if __name__ == '__main__':
    pytest.main()