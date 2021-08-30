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
@allure.feature('获取平台持仓量（全逐通用）')
class TestLinearHisOpenInterest:

    def test_linear_his_open_interest(self,contract_code,symbol):
        r = t.linear_his_open_interest(contract_code=contract_code,period='60min',size='48',amount_type='1')
        pprint(r)
        schema = {
            'data':
                {
                    'symbol': symbol,
                    'contract_code': contract_code,
                    'tick': [
                        {'volume': float,
                        'amount_type' : int,
                         'value' : float,
                         'ts' : int
                         }
                    ]
                },

            'status': 'ok',
            'ts': int
        }
        Schema(schema).validate(r)



if __name__ == '__main__':
    pytest.main()
