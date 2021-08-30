#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/8/7
# @Author  : zhangranghan



from common.LinearServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema,And,Or,Regex,SchemaError

from pprint import pprint
import pytest,allure,random,time



@allure.epic('正向永续')
@allure.feature('获取预估结算价（全逐通用）')
class TestLinearEstimatedSettlementPrice:


    def test_linear_estimated_settlement_price(self,contract_code,symbol):
        r = t.linear_estimated_settlement_price(contract_code=contract_code)
        pprint(r)
        schema = {'data': [{'contract_code': contract_code,
                               'estimated_settlement_price': Or(float,int,None),
                               'settlement_type': 'settlement'}],
                     'status': 'ok',
                     'ts': int}

        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()



