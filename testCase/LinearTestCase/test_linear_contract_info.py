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
@allure.feature('获取合约信息')
class TestLinearContractInfo:


    def test_linear_contract_info1(self,contract_code,symbol):
        r = t.linear_contract_info(contract_code=contract_code)
        pprint(r)
        schema = {
                    'data': [
                        {
                            'contract_code': contract_code,
                            'contract_size': Or(float,int),
                            'contract_status': int,
                            'create_date': str,
                            'delivery_time': str,
                            'price_tick': Or(float,int),
                            'settlement_date': str,
                            'support_margin_mode': Or('cross','isolated','all'),
                            'symbol': symbol
                        }
                    ],
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
