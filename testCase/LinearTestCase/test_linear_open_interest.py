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
@allure.feature('获取当前可用合约总持仓量')
class TestLinearOpenInterset:


    def test_linear_open_interest(self,contract_code,symbol):
        r = t.linear_open_interest(contract_code=contract_code)
        pprint(r)
        schema = {
            'data': [
                {
                    'symbol': symbol,
                    'contract_code': contract_code,
                    'trade_amount': float,
                    'trade_turnover': float,
                    'trade_volume': int,
                    'volume': float,
                    'value': float,
                    'amount': float
                    }
                ],
            'status': 'ok',
            'ts': int
        }
        Schema(schema).validate(r)



if __name__ == '__main__':
    pytest.main()
