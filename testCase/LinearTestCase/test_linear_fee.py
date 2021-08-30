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
@allure.feature('获取用户的合约手续费费率')
class TestLinearFee:


    def test_linear_fee1(self,contract_code,symbol):
        r = t.linear_fee(contract_code=contract_code)
        pprint(r)
        schema = {
                    'data': [
                        {
                            'close_maker_fee': str,
                            'close_taker_fee': str,
                            'contract_code': contract_code,
                            'fee_asset': 'USDT',
                            'open_maker_fee': str,
                            'open_taker_fee': str,
                            'symbol': symbol
                        }
                    ],
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
