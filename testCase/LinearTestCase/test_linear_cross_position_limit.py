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
@allure.feature('获取用户的合约持仓量限制（全仓）')
class TestLinearCrossPositionLimit:


    def test_linear_cross_position_limit(self,contract_code,symbol):
        r = t.linear_cross_position_limit(contract_code=contract_code)
        pprint(r)
        schema = {
                    'data': [
                        {
                            'buy_limit': Or(float,None),
                            'contract_code': contract_code,
                            'margin_mode': 'cross',
                            'sell_limit': Or(float,None),
                            'symbol': symbol
                        }
                    ],
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)



if __name__ == '__main__':
    pytest.main()
