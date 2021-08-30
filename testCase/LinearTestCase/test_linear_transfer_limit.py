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
@allure.feature('获取用户的合约划转限制')
class TestLinearTransferLimit:

    def test_linear_transfer_limit(self,contract_code,symbol):
        r = t.linear_transfer_limit(contract_code=contract_code)
        pprint(r)
        schema = {
                    'data': [
                        {
                            'contract_code': contract_code,
                            'margin_account': str,
                            'margin_mode': 'isolated',
                            'net_transfer_in_max_daily': float,
                            'net_transfer_out_max_daily': float,
                            'symbol': symbol,
                            'transfer_in_max_daily': float,
                            'transfer_in_max_each': float,
                            'transfer_in_min_each': float,
                            'transfer_out_max_daily': float,
                            'transfer_out_max_each': float,
                            'transfer_out_min_each': float
                        }
                    ],
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

if __name__ == '__main__':
    pytest.main()
