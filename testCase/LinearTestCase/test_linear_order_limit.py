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
@allure.feature('获取用户的合约下单量限制')
class TestLinearOrderLimit:



    def test_linear_order_info(self,contract_code,symbol):
        r = t.linear_order_limit(contract_code=contract_code,order_price_type='limit')
        pprint(r)
        schema = {
                    'data': {
                        'list': [
                            {
                                'close_limit': Or(float,None),
                                'contract_code': contract_code,
                                'open_limit': Or(float,None),
                                'symbol': symbol
                            }
                        ],
                        'order_price_type': str
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
