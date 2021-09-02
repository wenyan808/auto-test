#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/8/20
# @Author  : zhangranghan


from common.SwapServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema, And, Or, Regex, SchemaError

from pprint import pprint
import pytest, allure, random, time


@allure.epic('反向永续')
@allure.feature('平台持仓量的查询')
class TestSwapHidOpenInterest:

    def test_swap_his_open_interest(self, contract_code):
        r = t.swap_his_open_interest(contract_code=contract_code, period='60min', size='20', amount_type='1')
        schema = {
            "status": "ok",
            "data":
                {
                    "symbol": str,
                    "contract_code": contract_code,
                    "tick": [
                        {
                            "volume": Or(int, float, None),
                            "amount_type": int,
                            "ts": int
                        }
                    ]
                },
            "ts": int
        }
        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
