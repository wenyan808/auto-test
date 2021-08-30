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
@allure.feature('精英账户多空持仓对比-账户数')
class TestLinearEliteAccountRatio:


    def test_linear_elite_account_ratio1(self,contract_code,symbol):
        r = t.linear_elite_account_ratio(contract_code=contract_code,
                                         period='60min')
        pprint(r)
        schema = {
                    'data': {
                        'contract_code': contract_code,
                        'list': [
                            {
                                'buy_ratio': float,
                                'locked_ratio': float,
                                'sell_ratio': float,
                                'ts': int
                            }
                        ],
                        'symbol': symbol
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)




if __name__ == '__main__':
    pytest.main()
