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
@allure.feature('获取合约的资金费率')
class TestLinearFundingRate:


    def test_linear_funding_rate1(self,contract_code,symbol):
        r = t.linear_funding_rate(contract_code=contract_code)
        pprint(r)
        schema = {
                    'data': {
                        'contract_code': contract_code,
                        'estimated_rate': str,
                        'fee_asset': 'USDT',
                        'funding_rate': str,
                        'funding_time': str,
                        'next_funding_time': str,
                        'symbol': symbol
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
