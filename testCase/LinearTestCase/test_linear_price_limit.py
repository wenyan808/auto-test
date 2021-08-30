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
@allure.feature('获取合约最高限价和最低限价')
class TestLinearPriceLimit:

    def test_linear_price_limit(self,contract_code,symbol):
        r = t.linear_price_limit(contract_code=contract_code)
        pprint(r)
        schema = {
                    'data': [
                        {
                            'high_limit': Or(float,None),
                            'contract_code': contract_code,
                            'low_limit': Or(float,None),
                            'symbol': symbol
                        }
                    ],
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
