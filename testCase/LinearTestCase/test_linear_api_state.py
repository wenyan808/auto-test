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
@allure.feature('查询系统状态')
class TestLinearApiState:


    def test_linear_api_state(self,contract_code,symbol):
        r = t.linear_api_state(contract_code=contract_code)
        pprint(r)
        schema = {
            'data': [
                {
                    'cancel': int,
                    'close': int,
                    'contract_code': contract_code,
                    'margin_account': str,
                    'margin_mode': 'isolated',
                    'master_transfer_sub': int,
                    'master_transfer_sub_inner_in': int,
                    'master_transfer_sub_inner_out': int,
                    'open':int,
                    'sub_transfer_master': int,
                    'sub_transfer_master_inner_in': int,
                    'sub_transfer_master_inner_out': int,
                    'symbol': symbol,
                    'transfer_in': int,
                    'transfer_inner_in': int,
                    'transfer_inner_out': int,
                    'transfer_out': int
                }
            ],
            'status': 'ok',
            'ts': int
        }

        Schema(schema).validate(r)



if __name__ == '__main__':
    pytest.main()
